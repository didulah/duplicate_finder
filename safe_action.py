"""
safe_action.py
---------------
Delete කරන්න කලින් automatic backup එකක් ගන්නවා (data loss risk අඩු කරන්න).
User confirm කරාට පස්සේ විතරයි actual DELETE query run වෙන්නෙ.
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
        Delete කරන්න යන records ටික, JSON file එකකට backup කරනවා.
        මොකක් හරි වැරැද්දක් උනොත්, මේ file එකෙන් data restore කරන්න පුළුවන්.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"backup_{self.table}_{timestamp}.json"
        backup_path = os.path.join(self.backup_dir, backup_filename)

        with open(backup_path, "w", encoding="utf-8") as f:
            json.dump(records_to_delete, f, indent=2, default=str, ensure_ascii=False)

        print(f"[OK] Backup එක save විය: {backup_path} ({len(records_to_delete)} records)")
        return backup_path

    def collect_delete_candidates(self, duplicate_groups: list) -> list:
        """duplicate_groups ලිස්ට් එකෙන්, "DELETE_CANDIDATE" ලෙස label කරපු records ටික විතරක් අයින් කරගන්නවා."""
        delete_candidates = []
        for group in duplicate_groups:
            for item in group["records"]:
                if item["action"] == "DELETE_CANDIDATE":
                    delete_candidates.append(item["record"])
        return delete_candidates

    def execute_delete(self, duplicate_groups: list, confirm: bool = False) -> int:
        """
        Full safe-delete workflow එක:
        1. Delete candidates collect කරනවා
        2. Backup ගන්නවා (auto_backup=True නම්)
        3. User confirm කරලා තියෙනවා නම් විතරක් actual DELETE run කරනවා
        """
        delete_candidates = self.collect_delete_candidates(duplicate_groups)

        if not delete_candidates:
            print("[INFO] Delete කරන්න records නෑ.")
            return 0

        if self.auto_backup:
            self.backup_records(delete_candidates)

        if not confirm:
            print(f"[SKIPPED] {len(delete_candidates)} records delete කරන්න තිබුණා, "
                  f"but --confirm flag එක දීලා නෑ. Dry-run විදිහට ඉවරයි.")
            return 0

        deleted_count = 0
        for record in delete_candidates:
            pk_value = record[self.primary_key]
            query = f"DELETE FROM {self.table} WHERE {self.primary_key} = %s"
            self.db.execute_write(query, (pk_value,))
            deleted_count += 1

        print(f"[OK] Records {deleted_count}ක් සාර්ථකව delete කරන ලදී.")
        return deleted_count
