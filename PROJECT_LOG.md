# Project Log - Duplicate Finder & Cleaner

මේ file එකේ, project එකේ progress එක session එකෙන් session එකට track කරනවා.
අලුත් entry එකක් top එකට add කරන්න (newest first), පරණ entries ඉවත් කරන්නෙ නෑ.

---

## Template (අලුත් entry එකකට copy කරගන්න)

```
## [YYYY-MM-DD] - කෙටි title එකක්

**කරපු දේවල්:**
-

**තීරණ ගත් දේවල්:**
-

**Blockers / Issues:**
-

**ඊළඟ steps:**
-
```

---

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