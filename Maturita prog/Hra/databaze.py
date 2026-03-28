import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "hramenu.db")


def vytvor_db():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hrac(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jmeno TEXT UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hra(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nazev TEXT UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS score(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hrac_id INTEGER,
        hra_id INTEGER,
        body INTEGER,
        datum TEXT,
        FOREIGN KEY (hrac_id) REFERENCES hrac(id),
        FOREIGN KEY (hra_id) REFERENCES hra(id)
    )
    """)

    cursor.execute("INSERT OR IGNORE INTO hra (nazev) VALUES (?)", ("Hopík",))

    conn.commit()
    conn.close()


def uloz_score(jmeno, body):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    datum = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("INSERT OR IGNORE INTO hrac (jmeno) VALUES (?)", (jmeno,))
    cursor.execute("SELECT id FROM hrac WHERE jmeno=?", (jmeno,))
    hrac_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM hra WHERE nazev=?", ("Hopík",))
    hra_id = cursor.fetchone()[0]

    cursor.execute("""
    INSERT INTO score (hrac_id, hra_id, body, datum)
    VALUES (?, ?, ?, ?)
    """, (hrac_id, hra_id, body, datum))

    conn.commit()
    conn.close()


def nacti_score():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT hrac.jmeno, score.body, score.datum
    FROM score
    JOIN hrac ON score.hrac_id = hrac.id
    JOIN hra ON score.hra_id = hra.id
    ORDER BY score.body DESC
    """)

    data = cursor.fetchall()

    conn.close()
    return data


def smaz_score(id):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM score WHERE id=?", (id,))
    conn.commit()

    conn.close()