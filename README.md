# CMPT 354 Project - Checkpoint Frontend Demo

This branch adds a minimal but working GUI so the team can take a checkpoint screenshot and show a meaningful query early in the semester.

## What was added

- `app.py` - lightweight Python web server for the checkpoint demo
- `main.py` - simple entry point that runs the demo server
- `db/schema_sqlite.sql` - SQLite schema used by the demo platform
- `db/seed_sqlite.sql` - sample data for the demo platform
- `init_db.py` - optional one-shot database initialization script
- `static/style.css` - styling for the GUI
- `docs/CHECKPOINT_SCREENSHOT_DESCRIPTION.md` - short write-up for the screenshot section
- `legacy/sqlserver_connection_test.py` - preserved version of the old DB connection test without hard-coded credentials
- updated `SQL Dump/SQLQuery1.sql` - cleaner SQL Server dump with sample tuples

## Folder structure

```text
CMPT354-Project-main/
├── app.py
├── main.py
├── README.md
├── db/
│   ├── schema_sqlite.sql
│   ├── seed_sqlite.sql
│   └── project_demo.db   # auto-created after first run
├── docs/
│   └── CHECKPOINT_SCREENSHOT_DESCRIPTION.md
├── legacy/
│   └── sqlserver_connection_test.py
├── SQL Dump/
│   └── SQLQuery1.sql
├── static/
│   └── style.css
├── ER Diagram.drawio
└── Untitled Diagram.drawio
```

## How to run

### 1) Initialize the demo database (optional)

From the project root:

```bash
python init_db.py
```

You can skip this because `python main.py` also auto-creates the SQLite DB if it does not exist.

### 2) Start the app

```bash
python main.py
```

### 3) Open the GUI

In a browser, go to:

```text
http://127.0.0.1:8000/
```

### 4) Take the checkpoint screenshot

Use this route for a ready-made meaningful query:

```text
http://127.0.0.1:8000/search?robot_id=1&part_category=All
```

That page shows:
- selected robot
- team name
- manager
- sub-assemblies
- parts
- part subtype details

## Notes for teammates

- The GUI is intentionally simple because the checkpoint only requires a rudimentary frontend.
- The demo backend uses SQLite so anyone on the team can run it immediately.
- The final project can still move to SQL Server later; the included SQL dump is kept separately in `SQL Dump/`.
- Before final submission, the ER diagram should be updated so it matches the cleaned schema names exactly.
