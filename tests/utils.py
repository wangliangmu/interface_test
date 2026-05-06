import re
import json
import jsonpath_ng
from datetime import datetime, timezone, timedelta


def resolve_template(text: str, context: dict) -> str:
    if not isinstance(text, str):
        return text
    
    def replacer(match):
        var_name = match.group(1)
        if var_name.startswith("$date"):
            beijing_time = datetime.now(timezone.utc) + timedelta(hours=8)
            return beijing_time.strftime("%m%d_%H%M")
        if var_name in context:
            return str(context[var_name])
        return match.group(0)
    
    return re.sub(r'\{\{(\S+?)\}\}', replacer, text)


def resolve_dict(d, context: dict):
    if isinstance(d, dict):
        result = {}
        for k, v in d.items():
            if isinstance(v, str):
                match = re.search(r'\{\{(\w+)\}\}', v)
                if match:
                    var_name = match.group(1)
                    result[k] = context.get(var_name, v)
                else:
                    result[k] = resolve_template(v, context)
            else:
                result[k] = resolve_dict(v, context)
        return result
    elif isinstance(d, list):
        return [resolve_dict(v, context) for v in d]
    elif isinstance(d, str):
        return resolve_template(d, context)
    return d


def extract_json_path(data, path: str):
    expr = jsonpath_ng.parse(path)
    matches = expr.find(data)
    if matches:
        return matches[0].value
    return None
