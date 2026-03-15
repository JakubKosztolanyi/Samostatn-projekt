import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "hramenu.db")


def vytvor_db():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS score(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jmeno TEXT,
        body INTEGER,
        datum TEXT
    )
    """)

    conn.commit()
    conn.close()


def uloz_score(jmeno, body):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    datum = datetime.now().strftime("%Y-%m-%d")

    cursor.execute(
        "INSERT INTO score (jmeno, body, datum) VALUES (?, ?, ?)",
        (jmeno, body, datum)
    )

    conn.commit()
    conn.close()


def nacti_score():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id,jmeno,body,datum FROM score ORDER BY body DESC")

    data = cursor.fetchall()

    conn.close()
    return data


def smaz_score(id):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM score WHERE id=?", (id,))
    conn.commit()

    conn.close()