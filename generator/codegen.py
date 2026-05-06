import json
import re
import unicodedata
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
REPORTS_DIR = DATA_DIR / "reports"
TESTS_DIR = Path(__file__).resolve().parent.parent / "tests"
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"


def slugify(text):
    text = unicodedata.normalize("NFKD", text)
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "_", text).strip("_")
    return text.lower()


def to_class_name(text):
    slug = slugify(text)
    return "".join(word.capitalize() for word in slug.split("_") if word)


def to_py_repr(obj):
    s = json.dumps(obj, ensure_ascii=False, indent=4)
    s = s.replace("true", "True").replace("false", "False").replace("null", "None")
    return s


def make_func_name(step, index):
    if step["type"] == "wait":
        return f"wait_{index + 1}"
    path = step.get("path", "")
    method = step.get("method", "get").lower()
    parts = [p for p in path.split("/") if p and not p.startswith("{")]
    if parts:
        name = "_".join(parts[-2:]) if len(parts) >= 2 else parts[-1]
    else:
        name = f"step_{index + 1}"
    name = re.sub(r"[^a-zA-Z0-9_]", "", name)
    return f"{method}_{name}"[:50]


def process_step(step, index):
    if step["type"] == "http":
        func_name = make_func_name(step, index)

        headers = {}
        for h in step.get("headers", []):
            name = h["name"]
            value = h.get("sample_value") or h.get("value", "")
            headers[name] = value

        body = step.get("body")
        body_py = to_py_repr(body) if body else None

        return {
            "type": "http",
            "index": index,
            "func_name": func_name,
            "name": step.get("name", ""),
            "method": step.get("method", "GET"),
            "path": step.get("path", ""),
            "headers": headers if headers else None,
            "headers_py": to_py_repr(headers) if headers else None,
            "body": body,
            "body_py": body_py,
            "extracts": step.get("extracts", []),
            "assertions": generate_assertions(step),
        }
    elif step["type"] == "wait":
        return {
            "type": "wait",
            "index": index,
            "func_name": f"wait_{index + 1}",
            "duration": step.get("duration", 1000),
        }
    else:
        return {
            "type": "skip",
            "index": index,
            "func_name": f"step_{index + 1}",
        }


def generate_assertions(step):
    assertions = []
    raw_assertions = step.get("assertions", [])
    for a in raw_assertions:
        if isinstance(a, dict):
            target = a.get("target", "")
            expression = a.get("expression", "")
            expected = a.get("expected", a.get("value", ""))
            operator = a.get("operator", "eq")

            if target in ("responseCode", "statusCode"):
                assertions.append(
                    f'assert response.status_code == {expected}, f"Expected status {expected}, got {{response.status_code}}"'
                )
            elif expression:
                if operator == "eq":
                    assertions.append(
                        f'actual = extract_json_path(response.json(), "{expression}")\n'
                        f'        assert actual == {repr(expected)}, f"Assertion failed: {expression} == {repr(expected)}, got {{actual}}"'
                    )
                elif operator == "neq":
                    assertions.append(
                        f'actual = extract_json_path(response.json(), "{expression}")\n'
                        f'        assert actual != {repr(expected)}, f"Assertion failed: {expression} != {repr(expected)}, got {{actual}}"'
                    )
                elif operator == "gt":
                    assertions.append(
                        f'actual = extract_json_path(response.json(), "{expression}")\n'
                        f'        assert actual > {repr(expected)}, f"Assertion failed: {expression} > {repr(expected)}, got {{actual}}"'
                    )
                elif operator == "contains":
                    assertions.append(
                        f'actual = extract_json_path(response.json(), "{expression}")\n'
                        f'        assert {repr(expected)} in str(actual), f"Assertion failed: {expression} contains {repr(expected)}, got {{actual}}"'
                    )
                elif operator in ("not_null", "exists"):
                    assertions.append(
                        f'actual = extract_json_path(response.json(), "{expression}")\n'
                        f'        assert actual is not None, f"Assertion failed: {expression} should not be null"'
                    )
                else:
                    assertions.append(
                        f'actual = extract_json_path(response.json(), "{expression}")\n'
                        f'        # TODO: implement {operator} assertion for {expression}'
                    )
    return assertions


def generate_tests(data_path=None):
    if data_path is None:
        data_path = REPORTS_DIR / "project_data.json"

    with open(data_path, "r", encoding="utf-8") as f:
        project_data = json.load(f)

    TESTS_DIR.mkdir(parents=True, exist_ok=True)

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        keep_trailing_newline=True,
        lstrip_blocks=True,
        trim_blocks=True,
    )
    template = env.get_template("test_scenario.py.j2")

    base_url = project_data.get("base_url", "")
    common_headers = project_data.get("common_headers", [])
    common_headers_py = to_py_repr(common_headers)
    scenarios = project_data.get("scenarios", [])

    generated_files = []
    seen_names = set()

    for scenario in scenarios:
        steps = scenario.get("steps", [])
        if not steps:
            continue

        http_steps = [s for s in steps if s["type"] == "http"]
        if not http_steps:
            continue

        name = scenario["name"]
        folder_name = scenario.get("folder_name", "")

        base_slug = slugify(name)
        if base_slug in seen_names:
            base_slug = f"{base_slug}_{scenario['id']}"
        seen_names.add(base_slug)

        file_name = f"test_{base_slug}.py"
        class_name = to_class_name(name)
        if not class_name:
            class_name = f"TestScenario{scenario['id']}"

        processed_steps = []
        for i, step in enumerate(steps):
            processed = process_step(step, i)
            if processed["type"] != "skip":
                processed_steps.append(processed)

        content = template.render(
            base_url=base_url,
            common_headers_py=common_headers_py,
            class_name=class_name,
            steps=processed_steps,
        )

        output_path = TESTS_DIR / file_name
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        generated_files.append({
            "file": file_name,
            "scenario": name,
            "folder": folder_name,
            "steps": len(http_steps),
        })

    conftest_path = TESTS_DIR / "conftest.py"
    with open(conftest_path, "w", encoding="utf-8") as f:
        f.write("import pytest\nimport requests\n\n")

    print(f"Generated {len(generated_files)} test files in {TESTS_DIR}")
    for gf in generated_files:
        print(f"  {gf['file']}: {gf['scenario']} ({gf['steps']} HTTP steps)")

    return generated_files


if __name__ == "__main__":
    generate_tests()
