import sys
import argparse
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")


def cmd_login(args):
    from scraper.login import _do_login
    _do_login(headless=not args.show_browser)
    print("Login successful!")


def cmd_scrape(args):
    from scraper.extractor import fetch_all_data
    fetch_all_data()


def cmd_generate(args):
    from generator.codegen import generate_tests
    data_path = args.data if args.data else None
    generate_tests(data_path=data_path)


def cmd_all(args):
    from scraper.extractor import fetch_all_data
    from generator.codegen import generate_tests
    print("=== Step 1: Scraping data from Apifox ===")
    fetch_all_data()
    print("\n=== Step 2: Generating test cases ===")
    generate_tests()


def main():
    parser = argparse.ArgumentParser(description="Apifox Test Case Generator")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    login_parser = subparsers.add_parser("login", help="Login to Apifox and save auth state")
    login_parser.add_argument("--show-browser", action="store_true", help="Show browser window")

    scrape_parser = subparsers.add_parser("scrape", help="Scrape test data from Apifox")
    scrape_parser.add_argument("--data", help="Path to existing project data JSON (skip scraping)")

    generate_parser = subparsers.add_parser("generate", help="Generate test cases from scraped data")
    generate_parser.add_argument("--data", help="Path to project data JSON file")

    all_parser = subparsers.add_parser("all", help="Run full pipeline: scrape + generate")

    args = parser.parse_args()

    if args.command == "login":
        cmd_login(args)
    elif args.command == "scrape":
        cmd_scrape(args)
    elif args.command == "generate":
        cmd_generate(args)
    elif args.command == "all":
        cmd_all(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
