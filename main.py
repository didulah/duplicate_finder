"""
main.py
--------
Duplicate Finder & Cleaner - CLI Entry Point

Usage:
    python main.py --config config.yaml                  # Scan + report only (safe, nothing is deleted)
    python main.py --config config.yaml --confirm         # Scan + report + actual DELETE (with backup)

Author: didulah (github.com/didulah)
"""

import argparse
import sys
import yaml

from db_connector import DatabaseConnector
from duplicate_detector import DuplicateDetector
from report_generator import ReportGenerator
from safe_action import SafeActionHandler


def load_config(config_path: str) -> dict:
    """Loads the config.yaml file and returns it as a dict."""
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"[ERROR] Config file not found: {config_path}")
        print("        Copy config.example.yaml to config.yaml and fill in your DB details.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"[ERROR] config.yaml has an invalid format: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Duplicate Finder & Cleaner - finds duplicate database records and safely cleans them up."
    )
    parser.add_argument(
        "--config", default="config.yaml",
        help="Config file path (default: config.yaml)"
    )
    parser.add_argument(
        "--confirm", action="store_true",
        help="Pass this flag to actually run the DELETE operation. "
             "Without it, the tool runs as a dry-run (preview + report only)."
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
            print("\n[TIP] To confirm the delete, run: python main.py --config config.yaml --confirm")

    finally:
        db.close()


if __name__ == "__main__":
    main()
