# Duplicate Finder & Cleaner

Database (MySQL / PostgreSQL) table එකක duplicate records automatic ලෙස සොයාගෙන, **safely** review කරලා, clean කරන CLI tool එකක්.

## Features

- MySQL සහ PostgreSQL දෙකටම support
- එකක් හෝ ගණනාවක් columns (composite match) අනුව duplicate detection
- **Dry-run by default** — `--confirm` flag නොදුන්නොත් කිසිම record එකක් delete වෙන්නෙ නෑ
- Delete කරන්න කලින් automatic JSON backup
- CSV / JSON report export
- Terminal එකේ readable summary table එක

## Installation

```bash
pip install -r requirements.txt
```

## Setup

1. `config.example.yaml` file එක `config.yaml` විදිහට copy කරන්න:
   ```bash
   cp config.example.yaml config.yaml
   ```
2. `config.yaml` එකේ ඔයාගේ database credentials, table name, සහ match columns දාන්න.

## Usage

**Step 1 — Dry run (preview විතරයි, කිසිවක් delete වෙන්නෙ නෑ):**
```bash
python main.py --config config.yaml
```
මේකෙන් duplicate records report එකක් (CSV/JSON) generate කරලා, terminal එකේ summary එක පෙන්නනවා. Backup එකක් ගන්නවා, delete කරන්නෙ නෑ.

**Step 2 — Report එක review කරලා, ඔයාට හරි කියලා හිතුනොත්, actual delete කරන්න:**
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
├── reports/                # Generated reports save වෙන තැන
└── backups/                # Delete කරන්න කලින් backups save වෙන තැන
```

## Safety Notes

- **Always dry-run first.** `--confirm` නැතුව run කරලා report එක check කරන්න.
- Backup file එක `backups/` folder එකේ save වෙනවා — delete එකකින් පස්සේ මොකක් හරි වැරදුනොත් මේකෙන් data restore කරන්න පුළුවන් (manual INSERT කරලා).
- `config.yaml` (real credentials තියෙන file එක) කවදාවත් GitHub වලට push කරන්න එපා — `.gitignore` එකේ දැනටමත් exclude කරලා තියෙනවා.

## License

Commercial license — see LICENSE file for terms (marketplace එකේ publish කරද්දී මේ file එක add කරන්න).
