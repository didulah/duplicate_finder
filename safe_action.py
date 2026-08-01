"""
safe_action.py
---------------
Takes an automatic backup before deleting (to reduce data loss risk).
The actual DELETE query only runs after the user has confirmed.
"""

import json
import os
from datetime import datetime
from db_connector import DatabaseConnector


class SafeActionHandler:
    def __init__(self, db: DatabaseConnector, table: str, primary_key: str,
                 backup_dir: str = "./backups", auto_backup: bool = True):
        self.db = db
        self.table = table
        self.primary_key = primary_key
        self.backup_dir = backup_dir
        self.auto_backup = auto_backup
        os.makedirs(self.backup_dir, exist_ok=True)

    def backup_records(self, records_to_delete: list) -> str:
        """
        Backs up the records that are about to be deleted into a JSON file.
        If anything goes wrong, this file can be used to restore the data.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"backup_{self.table}_{timestamp}.json"
        backup_path = os.path.join(self.backup_dir, backup_filename)

        with open(backup_path, "w", encoding="utf-8") as f:
            json.dump(records_to_delete, f, indent=2, default=str, ensure_ascii=False)

        print(f"[OK] Backup saved: {backup_path} ({len(records_to_delete)} records)")
        return backup_path

    def collect_delete_candidates(self, duplicate_groups: list) -> list:
        """Pulls out only the records labeled "DELETE_CANDIDATE" from duplicate_groups."""
        delete_candidates = []
        for group in duplicate_groups:
            for item in group["records"]:
                if item["action"] == "DELETE_CANDIDATE":
                    delete_candidates.append(item["record"])
        return delete_candidates

    def execute_delete(self, duplicate_groups: list, confirm: bool = False) -> int:
        """
        Full safe-delete workflow:
        1. Collect delete candidates
        2. Take a backup (if auto_backup=True)
        3. Only run the actual DELETE if the user has confirmed
        """
        delete_candidates = self.collect_delete_candidates(duplicate_groups)

        if not delete_candidates:
            print("[INFO] No records to delete.")
            return 0

        if self.auto_backup:
            self.backup_records(delete_candidates)

        if not confirm:
            print(f"[SKIPPED] {len(delete_candidates)} record(s) were eligible for deletion, "
                  f"but the --confirm flag was not provided. Dry-run complete.")
            return 0

        deleted_count = 0
        for record in delete_candidates:
            pk_value = record[self.primary_key]
            query = f"DELETE FROM {self.table} WHERE {self.primary_key} = %s"
            self.db.execute_write(query, (pk_value,))
            deleted_count += 1

        print(f"[OK] Successfully deleted {deleted_count} record(s).")
        return deleted_count
