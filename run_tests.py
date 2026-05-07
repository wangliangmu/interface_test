#!/usr/bin/env python3
"""
接口测试统一入口文件
功能：
1. 自动运行项目内所有测试用例
2. 生成日志文件
3. 生成 HTML 测试报告
4. 支持并行执行
5. 支持按标记筛选测试
6. 支持失败重试
"""

import os
import sys
import argparse
import subprocess
import logging
from datetime import datetime
from pathlib import Path


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class TestRunner:
    def __init__(self):
        self.project_root = Path(__file__).parent.absolute()
        self.tests_dir = self.project_root / "tests"
        self.reports_dir = self.project_root / "reports"
        self.logs_dir = self.project_root / "logs"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._log_file_path = None

    def setup_directories(self):
        self.reports_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)

    def build_pytest_args(self, args) -> list:
        pytest_args = ["-v", "--tb=short"]

        if args.test_path:
            pytest_args.append(args.test_path)
        else:
            pytest_args.append(str(self.tests_dir))

        if args.parallel:
            workers = args.workers if args.workers else "auto"
            pytest_args.extend(["-n", workers, "--dist=loadscope"])
            logger.info(f"并行执行模式: {workers} 个 worker")

        if args.marker:
            pytest_args.extend(["-m", args.marker])

        if args.rerun:
            pytest_args.extend(["--reruns", str(args.rerun)])

        if args.html_report:
            detail_file = self.reports_dir / f"api_test_detail_{self.timestamp}.html"
            pytest_args.extend(["--html", str(detail_file), "--self-contained-html"])
            logger.info(f"详细报告: {detail_file}")

        if args.junit:
            junit_file = self.reports_dir / f"junit_{self.timestamp}.xml"
            pytest_args.extend(["--junitxml", str(junit_file)])

        if args.log_file:
            log_file = self.logs_dir / f"api_test_{self.timestamp}.log"
            self._log_file_path = str(log_file)
            pytest_args.extend([
                "--log-file", self._log_file_path,
                "--log-file-level", "DEBUG",
                "--log-file-format", "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
                "--log-file-date-format", "%Y-%m-%d %H:%M:%S"
            ])
            logger.info(f"日志文件: {log_file}")

        if args.quiet:
            pytest_args.append("-q")
        elif args.verbose:
            pytest_args.append("-vv")

        if args.collect_only:
            pytest_args.append("--collect-only")

        if args.failfast:
            pytest_args.append("-x")

        if args.coverage:
            pytest_args.extend(["--cov=.", "--cov-report=html", "--cov-report=term"])

        return pytest_args

    def run(self, args) -> int:
        self.setup_directories()

        if not self.tests_dir.exists():
            logger.error(f"测试目录不存在: {self.tests_dir}")
            return 1

        pytest_args = self.build_pytest_args(args)
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.project_root)

        logger.info("=" * 80)
        logger.info("开始执行接口测试")
        logger.info(f"项目根目录: {self.project_root}")
        logger.info(f"测试目录: {self.tests_dir}")
        logger.info("=" * 80)

        cmd = [sys.executable, "-m", "pytest"] + pytest_args
        start_time = datetime.now()

        try:
            result = subprocess.run(cmd, cwd=self.project_root, env=env, capture_output=False)
            exit_code = result.returncode
        except KeyboardInterrupt:
            logger.warning("测试被用户中断")
            exit_code = 130
        except Exception as e:
            logger.error(f"执行测试时出错: {e}")
            exit_code = 1

        duration = (datetime.now() - start_time).total_seconds()

        logger.info("=" * 80)
        logger.info("测试执行完成")
        logger.info(f"耗时: {duration:.2f} 秒")

        if exit_code == 0:
            logger.info("结果: 全部通过 ✓")
        elif exit_code == 1:
            logger.error("结果: 存在失败用例 ✗")
        elif exit_code == 5:
            logger.warning("结果: 未收集到任何测试")
        else:
            logger.error(f"结果: 未知退出码 {exit_code}")

        summary_files = sorted(self.reports_dir.glob("api_test_summary_*.html"), key=lambda p: p.stat().st_mtime, reverse=True)
        if summary_files:
            logger.info(f"汇总报告: {summary_files[0]}")

        detail_files = sorted(self.reports_dir.glob("api_test_detail_*.html"), key=lambda p: p.stat().st_mtime, reverse=True)
        if detail_files:
            logger.info(f"详细报告: {detail_files[0]}")

        if self._log_file_path and os.path.isfile(self._log_file_path):
            self._add_utf8_bom(self._log_file_path)

        logger.info("=" * 80)
        return exit_code

    @staticmethod
    def _add_utf8_bom(file_path):
        try:
            with open(file_path, "rb") as f:
                content = f.read()
            if not content.startswith(b"\xef\xbb\xbf"):
                with open(file_path, "wb") as f:
                    f.write(b"\xef\xbb\xbf" + content)
        except Exception:
            pass


def main():
    parser = argparse.ArgumentParser(description="接口测试统一入口")
    parser.add_argument("test_path", nargs="?", help="指定测试路径")
    parser.add_argument("-m", "--marker", help="按标记筛选测试")
    parser.add_argument("-p", "--parallel", action="store_true", help="启用并行执行")
    parser.add_argument("-w", "--workers", help="并行 worker 数量")
    parser.add_argument("--rerun", type=int, help="失败重试次数")
    parser.add_argument("-x", "--failfast", action="store_true", help="遇到失败即停止")
    parser.add_argument("--html", dest="html_report", action="store_true", help="生成详细 HTML 报告")
    parser.add_argument("--junit", action="store_true", help="生成 JUnit XML 报告")
    parser.add_argument("--coverage", action="store_true", help="生成覆盖率报告")
    parser.add_argument("-l", "--log", dest="log_file", action="store_true", help="生成日志文件")
    parser.add_argument("-v", "--verbose", action="store_true", help="详细输出")
    parser.add_argument("-q", "--quiet", action="store_true", help="安静模式")
    parser.add_argument("--collect-only", action="store_true", help="只收集测试不执行")

    args = parser.parse_args()
    runner = TestRunner()
    sys.exit(runner.run(args))


if __name__ == "__main__":
    main()
