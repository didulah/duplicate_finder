"""
duplicate_detector.py
----------------------
Core detection engine. Finds duplicate records in the user-specified table,
based on the user-specified columns (match_columns).

Logic: GROUP BY match_columns HAVING COUNT(*) > 1
Then fetches the full record details for each of those groups.
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
        Step 1: Finds duplicate value combinations based on match_columns.
        Returns: a list like [{"email": "a@x.com", "count": 3}, ...]
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
        Step 2: For each duplicate group found, fetches the full record details
        (including the primary_key). Labels which record to "keep" and which
        record(s) are "delete candidates".
        """
        all_groups = []

        for group in duplicate_groups:
            where_clauses = []
            params = []

            for col in self.match_columns:
                where_clauses.append(f"{col} = %s")
                params.append(group[col])

            where_str = " AND ".join(where_clauses)

            # Decide sort order based on keep_strategy
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
        """Runs the full detection process. Main entry point."""
        print(f"[INFO] Scanning table '{self.table}' on columns {self.match_columns}...")

        duplicate_groups = self.find_duplicate_groups()

        if not duplicate_groups:
            print("[INFO] No duplicates found. Database is clean!")
            return []

        print(f"[INFO] Found {len(duplicate_groups)} duplicate group(s). Fetching full details...")
        full_results = self.get_full_duplicate_records(duplicate_groups)

        return full_results
