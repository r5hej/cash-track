import sqlite3
import pathlib


sqlite3_connection: sqlite3.Connection = None
_db_path = "test_db.db"


def _init_db_if_not_yet() -> None:
    global sqlite3_connection
    if sqlite3_connection is not None:
        return

    sqlite3_connection = sqlite3.connect(_db_path)

def disconnect() -> None:
    pass

# Delete old db
f = pathlib.Path(_db_path)
f.unlink(missing_ok=True)

# Make a fresh
conn = sqlite3.connect(_db_path)
with conn:
    conn.execute('CREATE TABLE accounts (name TEXT NOT NULL, username TEXT NOT NULL UNIQUE)')
    conn.execute('CREATE TABLE groups (name TEXT NOT NULL)')
    conn.execute('CREATE TABLE accounts_and_groups (account_id INTEGER, group_id INTEGER, PRIMARY KEY (account_id, group_id), FOREIGN KEY (account_id) REFERENCES accounts (rowid), FOREIGN KEY (group_id) REFERENCES groups (rowid))')
    conn.execute('CREATE TABLE payments (payee_id INTEGER NOT NULL, group_id INTEGER NOT NULL, distribution TEXT NOT NULL, message TEXT, FOREIGN KEY (payee_id) REFERENCES accounts (rowid), FOREIGN KEY (group_id) REFERENCES groups (rowid))')