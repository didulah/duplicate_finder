"""
duplicate_detector.py
----------------------
Core detection engine. user-specified table එකේ, user-specified columns
(match_columns) අනුව duplicate records සොයාගන්නවා.

Logic: GROUP BY match_columns HAVING COUNT(*) > 1
ඊට පස්සේ, ඒ group එකේ full record details ටික fetch කරනවා.
"""

from db_connector import DatabaseConnector


class DuplicateDetector:
    def __init__(self, db: DatabaseConnector, table: str, match_columns: list,
                 primary_key: str, keep_strategy: str = "keep_first"):
        self.db = db
        self.table = table
        self.match_columns = match_columns
        self.primary_key = primary_key
        self.keep_strategy = keep_strategy

    def find_duplicate_groups(self) -> list:
        """
        Step 1: match_columns අනුව duplicate value combinations සොයාගන්නවා.
        Returns: [{"email": "a@x.com", "count": 3}, ...] වගේ list එකක්
        """
        columns_str = ", ".join(self.match_columns)

        query = f"""
            SELECT {columns_str}, COUNT(*) AS dup_count
            FROM {self.table}
            GROUP BY {columns_str}
            HAVING COUNT(*) > 1
            ORDER BY dup_count DESC
        """

        results = self.db.execute_query(query)
        return results

    def get_full_duplicate_records(self, duplicate_groups: list) -> list:
        """
        Step 2: හම්බුන duplicate groups වල, සම්පූර්ණ record details
        (primary_key එකත් සමඟ) fetch කරනවා. "keep" කරන record එකයි
        "delete candidate" record(s) එකයි වෙන් කරලා label කරනවා.
        """
        all_groups = []

        for group in duplicate_groups:
            where_clauses = []
            params = []

            for col in self.match_columns:
                where_clauses.append(f"{col} = %s")
                params.append(group[col])

            where_str = " AND ".join(where_clauses)

            # keep_strategy අනුව order එක තීරණය කරනවා
            order_direction = "ASC" if self.keep_strategy == "keep_first" else "DESC"

            query = f"""
                SELECT * FROM {self.table}
                WHERE {where_str}
                ORDER BY {self.primary_key} {order_direction}
            """

            records = self.db.execute_query(query, tuple(params))

            if not records:
                continue

            labeled_records = []
            for idx, record in enumerate(records):
                labeled_records.append({
                    "record": record,
                    "action": "KEEP" if idx == 0 else "DELETE_CANDIDATE"
                })

            all_groups.append({
                "match_values": {col: group[col] for col in self.match_columns},
                "duplicate_count": group["dup_count"],
                "records": labeled_records
            })

        return all_groups

    def run(self) -> list:
        """Full detection process එක run කරනවා. Main entry point එක."""
        print(f"[INFO] '{self.table}' table එකේ, {self.match_columns} columns අනුව scan කරමින්...")

        duplicate_groups = self.find_duplicate_groups()

        if not duplicate_groups:
            print("[INFO] Duplicates කිසිවක් හම්බුනේ නෑ. Database එක clean!")
            return []

        print(f"[INFO] Duplicate groups {len(duplicate_groups)}ක් හම්බුනා. Full details fetch කරමින්...")
        full_results = self.get_full_duplicate_records(duplicate_groups)

        return full_results
