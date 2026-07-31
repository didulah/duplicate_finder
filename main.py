"""
main.py
--------
Duplicate Finder & Cleaner - CLI Entry Point

Usage:
    python main.py --config config.yaml                 # Scan + report විතරක් (safe, delete වෙන්නෙ නෑ)
    python main.py --config config.yaml --confirm        # Scan + report + actual DELETE (backup සමඟ)

Author: [ඔයාගේ නම / GitHub username එක මෙතන දාන්න]
"""

import argparse
import sys
import yaml

from db_connector import DatabaseConnector
from duplicate_detector import DuplicateDetector
from report_generator import ReportGenerator
from safe_action import SafeActionHandler


def load_config(config_path: str) -> dict:
    """config.yaml file එක load කරලා dict එකක් ලෙස return කරනවා."""
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"[ERROR] Config file එක හම්බුනේ නෑ: {config_path}")
        print("        config.example.yaml, config.yaml විදිහට copy කරලා, ඔයාගේ DB details දාන්න.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"[ERROR] config.yaml file එකේ format එක වැරදියි: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Duplicate Finder & Cleaner - Database duplicate records සොයාගෙන, safely clean කරන tool එක."
    )
    parser.add_argument(
        "--config", default="config.yaml",
        help="Config file path (default: config.yaml)"
    )
    parser.add_argument(
        "--confirm", action="store_true",
        help="මේ flag එක දුන්නොත් විතරයි actual DELETE operation එක run වෙන්නෙ. "
             "නැත්නම් dry-run (preview + report විතරක්) ලෙස ක්‍රියා කරනවා."
    )
    args = parser.parse_args()

    # --- Step 1: Load Configuration ---
    config = load_config(args.config)

    db_config = config["database"]
    scan_config = config["scan"]
    output_config = config.get("output", {"format": "csv", "directory": "./reports"})
    safety_config = config.get("safety", {"auto_backup_before_delete": True, "backup_directory": "./backups"})

    # --- Step 2: Connect to Database ---
    db = DatabaseConnector(db_config)
    db.connect()

    try:
        # --- Step 3: Run Duplicate Detection ---
        detector = DuplicateDetector(
            db=db,
            table=scan_config["table"],
            match_columns=scan_config["match_columns"],
            primary_key=scan_config["primary_key"],
            keep_strategy=scan_config.get("keep_strategy", "keep_first"),
        )
        duplicate_groups = detector.run()

        if not duplicate_groups:
            return

        # --- Step 4: Generate Report ---
        reporter = ReportGenerator(
            output_dir=output_config.get("directory", "./reports"),
            output_format=output_config.get("format", "csv"),
        )
        reporter.print_summary(duplicate_groups)
        reporter.export(duplicate_groups)

        # --- Step 5: Safe Delete (only if --confirm flag used) ---
        action_handler = SafeActionHandler(
            db=db,
            table=scan_config["table"],
            primary_key=scan_config["primary_key"],
            backup_dir=safety_config.get("backup_directory", "./backups"),
            auto_backup=safety_config.get("auto_backup_before_delete", True),
        )
        action_handler.execute_delete(duplicate_groups, confirm=args.confirm)

        if not args.confirm:
            print("\n[TIP] Delete confirm කරන්න: python main.py --config config.yaml --confirm")

    finally:
        db.close()


if __name__ == "__main__":
    main()
