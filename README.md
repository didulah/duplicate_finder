# Duplicate Finder & Cleaner

A CLI tool that automatically finds duplicate records in a MySQL / PostgreSQL table, lets you **safely** review them, and cleans them up.

## Features

- Supports both MySQL and PostgreSQL
- Duplicate detection based on one or multiple columns (composite match)
- **Dry-run by default** — without the `--confirm` flag, no record is ever deleted
- Automatic JSON backup before deleting
- CSV / JSON report export
- Readable summary table printed to the terminal

## Installation

```bash
pip install -r requirements.txt
```

## Setup

1. Copy `config.example.yaml` to `config.yaml`:
   ```bash
   cp config.example.yaml config.yaml
   ```
2. Fill in your database credentials, table name, and match columns in `config.yaml`.

## Usage

**Step 1 — Dry run (preview only, nothing is deleted):**
```bash
python main.py --config config.yaml
```
This generates a duplicate records report (CSV/JSON) and shows a summary in the terminal. A backup is taken, but nothing is deleted.

**Step 2 — Review the report, and if it looks correct, run the actual delete:**
```bash
python main.py --config config.yaml --confirm
```

## Project Structure

```
duplicate_finder/
├── main.py                 # CLI entry point
├── db_connector.py         # MySQL/PostgreSQL connection handler
├── duplicate_detector.py   # Core detection logic (GROUP BY / HAVING)
├── report_generator.py     # CSV/JSON report export
├── safe_action.py          # Backup + safe delete logic
├── config.example.yaml     # Config template
├── requirements.txt
├── reports/                # Generated reports are saved here
└── backups/                # Backups are saved here before deletion
```

## Safety Notes

- **Always dry-run first.** Run without `--confirm` and check the report.
- Backup files are saved in the `backups/` folder — if anything goes wrong after a delete, you can restore data from these files (via manual INSERT).
- Never push `config.yaml` (the file with real credentials) to GitHub — it's already excluded in `.gitignore`.

## License

Commercial license — see the LICENSE file for terms.
