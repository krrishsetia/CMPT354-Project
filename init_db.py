from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'db' / 'project_demo.db'
SCHEMA_PATH = BASE_DIR / 'db' / 'schema_sqlite.sql'
SEED_PATH = BASE_DIR / 'db' / 'seed_sqlite.sql'

DB_PATH.parent.mkdir(parents=True, exist_ok=True)
conn = sqlite3.connect(DB_PATH)
with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
    conn.executescript(f.read())
with open(SEED_PATH, 'r', encoding='utf-8') as f:
    conn.executescript(f.read())
conn.commit()
conn.close()
print(f'Initialized SQLite demo DB at {DB_PATH}')
