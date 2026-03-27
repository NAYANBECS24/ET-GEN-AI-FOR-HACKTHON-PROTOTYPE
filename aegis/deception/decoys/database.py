import sqlite3
from pathlib import Path


def init_fake_db(path: str = "decoy.db") -> Path:
    db_path = Path(path)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS accounts(id INTEGER PRIMARY KEY, owner TEXT, balance REAL)")
    cur.execute("INSERT INTO accounts(owner, balance) VALUES('northwind-holdings', 424242.42)")
    conn.commit()
    conn.close()
    return db_path


if __name__ == "__main__":
    print(init_fake_db())
