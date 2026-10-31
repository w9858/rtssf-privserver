"""SQLite document storage. Each game request is one atomic transaction.

The original JSON files are immutable seeds, never live save files. SQLite owns
locking across threads/processes; no in-memory save cache is used.
"""
import json
import sqlite3
from contextlib import closing, contextmanager
from pathlib import Path


class Store:
    def __init__(self, database, seed_dir):
        self.database = str(Path(database).resolve())
        Path(self.database).parent.mkdir(parents=True, exist_ok=True)
        with closing(self.connect()) as connection, connection:
            connection.execute("PRAGMA journal_mode=WAL")
            connection.execute("BEGIN IMMEDIATE")
            connection.execute("CREATE TABLE IF NOT EXISTS documents (name TEXT PRIMARY KEY, value TEXT NOT NULL)")
            connection.execute("CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
            version = connection.execute("PRAGMA user_version").fetchone()[0]
            if version not in (0, 1):
                raise RuntimeError(f"Unsupported save schema {version}; refusing to modify it")
            seeds = sorted(Path(seed_dir).glob('*.json'))
            if not seeds: raise ValueError('Seed directory must contain JSON documents')
            for path in seeds:
                value = json.loads(path.read_text(encoding='utf-8'))
                connection.execute('INSERT OR IGNORE INTO documents VALUES (?, ?)',
                                   (path.stem, json.dumps(value, ensure_ascii=False)))
            connection.execute('PRAGMA user_version=1')

    def connect(self):
        connection = sqlite3.connect(self.database, timeout=10, isolation_level=None)
        connection.execute('PRAGMA busy_timeout=10000')
        connection.execute('PRAGMA synchronous=FULL')
        return connection

    @contextmanager
    def transaction(self):
        connection = self.connect()
        try:
            connection.execute('BEGIN IMMEDIATE')
            yield connection
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()

    def backup(self, destination):
        destination = Path(destination).resolve()
        if str(destination) == self.database or destination.exists():
            raise ValueError('Backup destination must be a new file')
        destination.parent.mkdir(parents=True, exist_ok=True)
        try:
            destination.open('xb').close()
        except FileExistsError as error:
            raise ValueError('Backup destination must be a new file') from error
        try:
            with closing(self.connect()) as source, closing(sqlite3.connect(destination)) as target:
                source.backup(target)
        except BaseException:
            destination.unlink(missing_ok=True)
            raise
        return destination


def read_document(connection, name):
    row = connection.execute('SELECT value FROM documents WHERE name=?', (name,)).fetchone()
    if row is None:
        raise KeyError(name)
    return json.loads(row[0])


def write_document(connection, name, value):
    connection.execute('INSERT INTO documents VALUES (?, ?) ON CONFLICT(name) DO UPDATE SET value=excluded.value',
                       (name, json.dumps(value, ensure_ascii=False)))
