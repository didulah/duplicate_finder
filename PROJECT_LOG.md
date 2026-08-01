# Project Log - Duplicate Finder & Cleaner
මේ file එකේ, project එකේ progress එක session එකෙන් session එකට track කරනවා.
අලුත් entry එකක් top එකට add කරන්න (newest first), පරණ entries ඉවත් කරන්නෙ නෑ.
---
## Template (අලුත් entry එකකට copy කරගන්න)
```
## [YYYY-MM-DD] - කෙටි title එකක්
**කරපු දේවල්:**
**තීරණ ගත් දේවල්:**
**Blockers / Issues:**
**ඊළඟ steps:**

## [2026-08-01] - MySQL Testing + Repo Audit

**කරපු දේවල්:**
- MySQL 8.0 container එකේ install කරලා, dupfinder_test DB එකක් + customers table (8 records, email duplicates 3ක්) හදලා full end-to-end test කළා
- Dry-run test ✅ (3 delete candidates identify කළා, කිසිවක් delete වුණේ නෑ)
- --confirm test ✅ (records 3 correct ලෙස delete වුණා, keep_first strategy verify වුණා)
- Re-run test ✅ (duplicates නැති බව confirm වුණා)
- Backup JSON content verify කළා (restorable format)
- Repo audit කළා - LICENSE සහ config.example.yaml push වෙලා නොතිබූ බව හඳුනාගත්තා

**තීරණ ගත් දේවල්:**
- LICENSE type: Custom "Regular License" (CodeCanyon-style) - source code access ඇතුව, resell/redistribute බෑ
- Anonymity සඳහා LICENSE සහ main.py වල real name නොදා GitHub username (didulah) විතරක් use කළා

**Blockers / Issues:**
- කිසිවක් නෑ

**ඊළඟ steps:**
- [ ] LICENSE, config.example.yaml, main.py (fixed) push කරන්න
- [ ] Gumroad/CodeCanyon listing description ලියන්න
- [ ] v2 features plan කරන්න (fuzzy matching, multi-table support, simple GUI)

## 2026-07-31 - MySQL Testing Complete

**කරපු දේවල්:**
- MySQL 8.0 එකෙන් full end-to-end test කළා (dry-run → confirm → re-run → backup verify)
- customers table එකේ email duplicates 3ක් correct ව detect + delete වුණා
- Backup JSON restore-ready බව confirm කළා

**තීරණ ගත් දේවල්:**
- MySQL සහ PostgreSQL දෙකෙන්ම logic එකම (driver එක විතරයි වෙනස) - db_connector.py design එක validate වුණා

**Blockers / Issues:**
- `config.example.yaml` file එක repo එකට push වෙලා තිබුණේ නෑ - fix කළා

**ඊළඟ steps:**
- [x] GitHub repo එකට push කරන්න
- [x] MySQL එකෙනුත් end-to-end test කරන්න
- [ ] `LICENSE` file එක ලියන්න
- [ ] Gumroad/CodeCanyon listing description එක ලියන්න
- [ ] Fuzzy matching (v2 feature) plan කරන්න

## 2026-07-31 - MVP Build + PostgreSQL Test

**කරපු දේවල්:**
- Architecture design (CLI → DB Connector → Duplicate Detector → Report Generator → Safe Action)
- Core files 5ම build කළා: `main.py`, `db_connector.py`, `duplicate_detector.py`, `report_generator.py`, `safe_action.py`
- `config.example.yaml`, `requirements.txt`, `README.md`, `.gitignore` හදුවා
- Container එකේ temporary PostgreSQL database එකක් හදලා, dummy duplicate data (customers table, 8 records, intentional email duplicates) දාලා end-to-end test කළා

**තීරණ ගත් දේවල්:**
- Tech stack: Python (MySQL + PostgreSQL දෙකටම support)
- Safety-first design: `--confirm` flag නැතුව delete වෙන්නෙ නෑ (dry-run default), delete කරන්න කලින් auto-backup
- Duplicate detection logic: `GROUP BY match_columns HAVING COUNT(*) > 1`, `keep_first`/`keep_latest` strategy
- GitHub repo folder structure එක plan කළා (src/tests/examples/reports/backups + .gitignore)

**Blockers / Issues:**
- Real production database එකක් තවම නෑ (temporary test DB එකෙන් විතරයි verify කළේ)
- MySQL driver එකෙන් test කරලා නෑ (PostgreSQL එකෙන් විතරයි)

**ඊළඟ steps:**
- [ ] GitHub repo එකට push කරන්න
- [ ] MySQL එකෙනුත් end-to-end test කරන්න
- [ ] `LICENSE` file එක ලියන්න
- [ ] Gumroad/CodeCanyon listing description එක ලියන්න
- [ ] Fuzzy matching (v2 feature) plan කරන්න