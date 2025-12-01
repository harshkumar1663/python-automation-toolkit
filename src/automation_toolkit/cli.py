"""
Command-line interface for the Automation Toolkit.

Usage examples:
- Organize files in Downloads:
    python -m automation_toolkit.cli organize ~/Downloads
- Analyze a log file:
    python -m automation_toolkit.cli analyze-log app.log
- Clean a CSV:
    python -m automation_toolkit.cli clean-csv data/raw.csv data/clean.csv

Author: Harsh Kumar
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from .csv_cleaner import CSVCleaner, CSVCleanerConfig
from .file_organizer import FileOrganizer
from .log_analyzer import LogAnalyzer

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s - %(message)s",
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Python Automation Toolkit by Harsh Kumar",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # File organizer command
    organize_parser = subparsers.add_parser("organize", help="Organize files in a directory.")
    organize_parser.add_argument("directory", type=str, help="Directory to organize.")

    # Log analyzer command
    log_parser = subparsers.add_parser("analyze-log", help="Analyze a log file.")
    log_parser.add_argument("log_file", type=str, help="Path to the log file.")

    # CSV cleaner command
    csv_parser = subparsers.add_parser("clean-csv", help="Clean a CSV file.")
    csv_parser.add_argument("input_csv", type=str, help="Input CSV path.")
    csv_parser.add_argument("output_csv", type=str, help="Output CSV path.")
    csv_parser.add_argument("--fillna", type=str, default=None, help="Value to fill missing fields (optional).")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "organize":
        organizer = FileOrganizer(args.directory)
        organizer.organize()

    elif args.command == "analyze-log":
        analyzer = LogAnalyzer(args.log_file)
        stats = analyzer.analyze()

        print(f"Log file: {Path(args.log_file).name}")
        print(f"Total lines: {stats.total_lines}")
        for level, count in stats.level_counts.items():
            print(f"{level}: {count}")
        print(f"ERROR lines: {stats.error_lines}")

    elif args.command == "clean-csv":
        config = CSVCleanerConfig(fillna_value=args.fillna)
        cleaner = CSVCleaner(args.input_csv, args.output_csv, config)
        cleaner.clean()
        print(f"Cleaned CSV written to: {args.output_csv}")


if __name__ == "__main__":
    main()
