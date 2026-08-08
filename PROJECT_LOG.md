# Project Log - Duplicate Finder & Cleaner
This file tracks project progress from session to session.
Add new entries to the top (newest first); do not remove old entries.
---
## Template (copy this for a new entry)
```
## [YYYY-MM-DD] - Short title
**What was done:**
**Decisions made:**
**Blockers / Issues:**
**Next steps:**
```
## [2026-08-08] - MySQL End-to-End Testing Complete

**What was done:**
- MySQL Community Server 8.0.46 installed on Windows using port 3400 (default ports 3306/3307 were blocked by Hyper-V/WSL2 dynamic port exclusion ranges)
- Forgotten root password reset using the `--init-file` / skip-grant-tables method (mysqld run manually with an ALTER USER init file, then service restarted normally)
- VS Code SQLTools connection (`local_mysql`) configured and verified against `localhost:3400`
- Test database `duplicate_finder_test` created with a `customers` table: 4 unique records + 3 duplicate records (matching on `email`)
- Missing Python dependencies installed: `pyyaml`, `mysql-connector-python==9.1.0`, `tabulate`
- `config.yaml` created pointing to the MySQL test database
- Ran full dry-run -> review -> `--confirm` workflow via `python main.py` / `python main.py --confirm`

**Decisions made:**
- `psycopg2-binary` install was skipped for now (fails to build on Python 3.14.3 due to missing `pg_config`); not needed for MySQL testing, to be revisited before PostgreSQL retesting
- Local Python environment confirmed as Python 3.14.3

**Blockers / Issues:**
- None blocking. Minor non-blocking UX issue found: after `--confirm` successfully deletes records, the final CLI message reads "No duplicates found. Database is clean!" instead of an explicit "N records deleted" confirmation. Flagged as a future improvement, not a launch blocker.

**Next steps:**
- Confirm cleaned English-only source files, `config.example.yaml`, and `LICENSE` are pushed to the GitHub repo (unconfirmed since last session)
- Fix `psycopg2-binary` install for Python 3.14.3 (or document a supported Python version) before retesting PostgreSQL
- Set up PayPal account for Gumroad payouts
- Publish Gumroad product listing
- Submit CodeCanyon / Envato Author application

### Test Results Detail
| Check | Result |
|---|---|
| MySQL connection | Success (port 3400) |
| Dry-run duplicate detection | 2 groups found, 3 records eligible for deletion |
| CSV report + JSON backup | Both generated automatically before delete |
| `--confirm` delete | Success — row count 7 -> 4, 0 duplicate groups remaining (verified via SQL query) |

## [2026-08-01] - MySQL Testing + Repo Audit

**What was done:**
- Installed MySQL 8.0 in a container, created a dupfinder_test DB + customers table (8 records, 3 email duplicates) and ran a full end-to-end test
- Dry-run test passed (identified 3 delete candidates, nothing was deleted)
- --confirm test passed (3 records deleted correctly, keep_first strategy verified)
- Re-run test passed (confirmed no duplicates remain)
- Verified backup JSON content (restorable format)
- Audited the repo - found that LICENSE and config.example.yaml had not been pushed

**Decisions made:**
- LICENSE type: Custom "Regular License" (CodeCanyon-style) - includes source code access, no resell/redistribute
- For anonymity, used the GitHub username (didulah) instead of a real name in LICENSE and main.py

**Blockers / Issues:**
- None

**Next steps:**
- [ ] Push LICENSE, config.example.yaml, main.py (fixed)
- [ ] Write Gumroad/CodeCanyon listing description
- [ ] Plan v2 features (fuzzy matching, multi-table support, simple GUI)

## 2026-07-31 - MySQL Testing Complete

**What was done:**
- Ran a full end-to-end test with MySQL 8.0 (dry-run -> confirm -> re-run -> backup verify)
- Correctly detected + deleted 3 email duplicates in the customers table
- Confirmed the backup JSON is restore-ready

**Decisions made:**
- The logic is identical for MySQL and PostgreSQL (only the driver differs) - validated the db_connector.py design

**Blockers / Issues:**
- The `config.example.yaml` file had not been pushed to the repo - fixed

**Next steps:**
- [x] Push to GitHub repo
- [x] End-to-end test with MySQL as well
- [ ] Write the `LICENSE` file
- [ ] Write the Gumroad/CodeCanyon listing description
- [ ] Plan fuzzy matching (v2 feature)

## 2026-07-31 - MVP Build + PostgreSQL Test

**What was done:**
- Architecture design (CLI -> DB Connector -> Duplicate Detector -> Report Generator -> Safe Action)
- Built all 5 core files: `main.py`, `db_connector.py`, `duplicate_detector.py`, `report_generator.py`, `safe_action.py`
- Created `config.example.yaml`, `requirements.txt`, `README.md`, `.gitignore`
- Set up a temporary PostgreSQL database in a container with dummy duplicate data (customers table, 8 records, intentional email duplicates) and ran an end-to-end test

**Decisions made:**
- Tech stack: Python (supporting both MySQL and PostgreSQL)
- Safety-first design: no delete without the `--confirm` flag (dry-run by default), auto-backup before deleting
- Duplicate detection logic: `GROUP BY match_columns HAVING COUNT(*) > 1`, `keep_first`/`keep_latest` strategy
- Planned the GitHub repo folder structure (src/tests/examples/reports/backups + .gitignore)

**Blockers / Issues:**
- No real production database yet (only verified against a temporary test DB)
- Not yet tested with the MySQL driver (only PostgreSQL so far)

**Next steps:**
- [ ] Push to GitHub repo
- [ ] End-to-end test with MySQL as well
- [ ] Write the `LICENSE` file
- [ ] Write the Gumroad/CodeCanyon listing description
- [ ] Plan fuzzy matching (v2 feature)
