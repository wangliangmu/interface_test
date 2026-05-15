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
import time
import pytz


# 配置日志
def beijing_time(*args):
    """获取北京时间"""
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.now(tz).timetuple()

logging.Formatter.converter = beijing_time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def get_beijing_now():
    """获取当前北京时间的 datetime 对象"""
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.now(tz)


class TestRunner:
    """测试运行器"""

    def __init__(self):
        self.project_root = Path(__file__).parent.absolute()
        self.tests_dir = self.project_root / "tests"
        self.reports_dir = self.project_root / "reports"
        self.logs_dir = self.project_root / "logs"
        self.timestamp = get_beijing_now().strftime("%Y%m%d_%H%M%S")
        self._log_file_path = None

    def setup_directories(self):
        """创建必要的目录"""
        self.reports_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        logger.info("目录初始化完成")

    def build_pytest_args(self, args) -> list:
        """构建 pytest 参数"""
        pytest_args = [
            "-v",
            "--tb=short",
        ]

        # 测试路径
        if args.test_path:
            pytest_args.append(args.test_path)
        else:
            pytest_args.append(str(self.tests_dir))

        # 并行执行
        if args.parallel:
            workers = args.workers if args.workers else "4"
            pytest_args.extend(["-n", workers, "--dist=loadscope"])
            logger.info(f"并行执行模式: {workers} 个 worker")

        # 按标记筛选
        if args.marker:
            pytest_args.extend(["-m", args.marker])
            logger.info(f"筛选标记: {args.marker}")

        # 失败重试
        if args.rerun:
            pytest_args.extend(["--reruns", str(args.rerun)])
            logger.info(f"失败重试次数: {args.rerun}")

        # 生成 HTML 详细报告（pytest-html，每个测试步骤的详细结果）
        if args.html_report:
            detail_file = self.reports_dir / f"api_test_detail_{self.timestamp}.html"
            pytest_args.extend(["--html", str(detail_file), "--self-contained-html"])
            logger.info(f"详细报告: {detail_file}")

        # 生成 JUnit XML 报告（CI 集成用）
        if args.junit:
            junit_file = self.reports_dir / f"junit_{self.timestamp}.xml"
            pytest_args.extend(["--junitxml", str(junit_file)])
            logger.info(f"JUnit XML 报告: {junit_file}")

        # 日志文件配置
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

        # 控制台日志级别
        if args.quiet:
            pytest_args.append("-q")
        elif args.verbose:
            pytest_args.append("-vv")

        # 只收集测试不执行
        if args.collect_only:
            pytest_args.append("--collect-only")

        # 失败即停止
        if args.failfast:
            pytest_args.append("-x")

        # 覆盖率报告
        if args.coverage:
            pytest_args.extend(["--cov=.", "--cov-report=html", "--cov-report=term"])
            logger.info("启用覆盖率统计")

        return pytest_args

    def run(self, args) -> int:
        """运行测试"""
        self.setup_directories()

        # 检查测试目录是否存在
        if not self.tests_dir.exists():
            logger.error(f"测试目录不存在: {self.tests_dir}")
            return 1

        # 构建 pytest 命令
        pytest_args = self.build_pytest_args(args)

        # 添加环境变量
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.project_root)
        
        # 根据选择的环境设置 API_BASE_URL
        env_configs = {
            "prod": "https://metahuman-prod.wair.ac.cn",
            "staging": "https://metahuman-staging.wair.ac.cn",
            "dev": "https://metahuman-demo.wair.ac.cn",
        }
        api_base_url = env_configs.get(args.env, env_configs["prod"])
        env["API_BASE_URL"] = api_base_url
        logger.info(f"测试环境: {args.env} ({api_base_url})")

        logger.info("=" * 80)
        logger.info("开始执行接口测试")
        logger.info(f"项目根目录: {self.project_root}")
        logger.info(f"测试目录: {self.tests_dir}")
        logger.info(f"pytest 参数: {' '.join(pytest_args)}")
        logger.info("=" * 80)

        # 执行 pytest
        cmd = [sys.executable, "-m", "pytest"] + pytest_args
        logger.info(f"执行命令: {' '.join(cmd)}")

        start_time = get_beijing_now()
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                env=env,
                capture_output=False
            )
            exit_code = result.returncode
        except KeyboardInterrupt:
            logger.warning("测试被用户中断")
            exit_code = 130
        except Exception as e:
            logger.error(f"执行测试时出错: {e}")
            exit_code = 1

        end_time = get_beijing_now()
        duration = (end_time - start_time).total_seconds()

        # 输出汇总信息
        logger.info("=" * 80)
        logger.info("测试执行完成")
        logger.info(f"耗时: {duration:.2f} 秒")

        if exit_code == 0:
            logger.info("结果: 全部通过 ✓")
        elif exit_code == 1:
            logger.error("结果: 存在失败用例 ✗")
        elif exit_code == 2:
            logger.error("结果: 测试执行被中断")
        elif exit_code == 3:
            logger.error("结果: 内部错误")
        elif exit_code == 4:
            logger.error("结果: pytest 使用错误")
        elif exit_code == 5:
            logger.warning("结果: 未收集到任何测试")
        else:
            logger.error(f"结果: 未知退出码 {exit_code}")

        # 输出报告路径
        summary_files = sorted(self.reports_dir.glob("api_test_summary_*.html"), key=lambda p: p.stat().st_mtime, reverse=True)
        if summary_files:
            logger.info(f"汇总报告: {summary_files[0]}")

        detail_files = sorted(self.reports_dir.glob("api_test_detail_*.html"), key=lambda p: p.stat().st_mtime, reverse=True)
        if detail_files:
            logger.info(f"详细报告: {detail_files[0]}")

        # 给日志文件添加 UTF-8 BOM（解决 Windows 记事本乱码）
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
    """主函数"""
    parser = argparse.ArgumentParser(
        description="接口测试统一入口",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 运行所有测试（默认配置，prod环境）
  python run_tests.py

  # 指定运行环境（dev/staging/prod）
  python run_tests.py --env dev

  # 并行执行所有测试
  python run_tests.py -p

  # 只运行冒烟测试
  python run_tests.py -m smoke

  # 运行指定测试文件
  python run_tests.py tests/test_登录.py

  # 生成 HTML 报告和日志文件
  python run_tests.py --html --log

  # 失败重试 2 次
  python run_tests.py --rerun 2

  # 只收集测试不执行
  python run_tests.py --collect-only

  # 详细输出模式
  python run_tests.py -vv

  # 完整示例：在dev环境运行AI测试，并行执行，生成报告
  python run_tests.py --env dev -m ai -p --html --log
        """
    )

    # 环境选择
    parser.add_argument(
        "-e", "--env",
        choices=["dev", "staging", "prod"],
        default="prod",
        help="指定测试环境（dev/staging/prod），默认 prod"
    )

    # 测试选择
    parser.add_argument(
        "test_path",
        nargs="?",
        help="指定测试路径（文件或目录），默认运行 tests/ 目录下所有测试"
    )

    parser.add_argument(
        "-m", "--marker",
        help="按标记筛选测试（如: smoke, clone, ai, dialog, login, risk）"
    )

    # 执行模式
    parser.add_argument(
        "-p", "--parallel",
        action="store_true",
        help="启用并行执行（默认使用 auto 自动检测 CPU 核心数）"
    )

    parser.add_argument(
        "-w", "--workers",
        help="指定并行 worker 数量（如: 4, auto）"
    )

    parser.add_argument(
        "--rerun",
        type=int,
        metavar="N",
        help="失败用例重试 N 次"
    )

    parser.add_argument(
        "-x", "--failfast",
        action="store_true",
        help="遇到第一个失败即停止"
    )

    # 报告生成
    parser.add_argument(
        "--html",
        dest="html_report",
        action="store_true",
        help="生成 HTML 测试报告"
    )

    parser.add_argument(
        "--junit",
        action="store_true",
        help="生成 JUnit XML 报告（CI 集成用）"
    )

    parser.add_argument(
        "--coverage",
        action="store_true",
        help="生成代码覆盖率报告"
    )

    # 日志配置
    parser.add_argument(
        "-l", "--log",
        dest="log_file",
        action="store_true",
        help="生成详细的日志文件"
    )

    # 输出控制
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="详细输出模式（-vv）"
    )

    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="安静模式，减少输出"
    )

    parser.add_argument(
        "--collect-only",
        action="store_true",
        help="只收集测试用例，不执行"
    )

    # 版本信息
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )

    args = parser.parse_args()

    # 创建运行器并执行
    runner = TestRunner()
    exit_code = runner.run(args)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
