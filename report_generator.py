"""
report_generator.py
--------------------
Duplicate detection results, CSV හෝ JSON report එකක් ලෙස save කරනවා.
Terminal එකේ readable summary එකක් print කරන්නත් function එකක් තියෙනවා.
"""

import csv
import json
import os
from datetime import datetime
from tabulate import tabulate


class ReportGenerator:
    def __init__(self, output_dir: str = "./reports", output_format: str = "csv"):
        self.output_dir = output_dir
        self.output_format = output_format.lower()
        os.makedirs(self.output_dir, exist_ok=True)

    def print_summary(self, duplicate_groups: list):
        """Terminal එකේ, table format එකකින් duplicate summary එක පෙන්නනවා."""
        if not duplicate_groups:
            return

        table_rows = []
        for group in duplicate_groups:
            match_str = ", ".join(f"{k}={v}" for k, v in group["match_values"].items())
            table_rows.append([
                match_str,
                group["duplicate_count"],
                sum(1 for r in group["records"] if r["action"] == "DELETE_CANDIDATE")
            ])

        headers = ["Match Value(s)", "Total Records", "Delete Candidates"]
        print("\n" + tabulate(table_rows, headers=headers, tablefmt="grid"))

        total_deletable = sum(row[2] for row in table_rows)
        print(f"\n[SUMMARY] Duplicate Groups: {len(duplicate_groups)} | "
              f"Delete කරන්න පුළුවන් records: {total_deletable}")

    def export(self, duplicate_groups: list) -> str:
        """Report එක file එකකට (CSV/JSON) export කරලා, file path එක return කරනවා."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"duplicate_report_{timestamp}.{self.output_format}"
        filepath = os.path.join(self.output_dir, filename)

        flat_rows = []
        for group in duplicate_groups:
            for item in group["records"]:
                row = dict(item["record"])
                row["_action"] = item["action"]
                flat_rows.append(row)

        if self.output_format == "csv":
            self._export_csv(flat_rows, filepath)
        elif self.output_format == "json":
            self._export_json(duplicate_groups, filepath)
        else:
            raise ValueError(f"Unsupported output format: {self.output_format}")

        print(f"[OK] Report එක save විය: {filepath}")
        return filepath

    def _export_csv(self, flat_rows: list, filepath: str):
        if not flat_rows:
            return
        fieldnames = list(flat_rows[0].keys())
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(flat_rows)

    def _export_json(self, duplicate_groups: list, filepath: str):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(duplicate_groups, f, indent=2, default=str, ensure_ascii=False)
