import sqlite3
import os
from datetime import datetime

# cesta k databázovému souboru – vždy ve stejné složce jako tento skript
DB_PATH = os.path.join(os.path.dirname(__file__), "hramenu.db")


def vytvor_db():
    """
    Vytvoří databázi a potřebné tabulky, pokud ještě neexistují.

    Tabulky:
        hrac  – uchovává jména hráčů (unikátní)
        hra   – uchovává názvy her (unikátní)
        score – uchovává výsledky hráčů s vazbou na hrace a hru

    Po vytvoření tabulek vloží výchozí záznam hry 'Hopík'.
    """
    # připojení k databázi
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # zapnutí podpory cizích klíčů (nutné pro DELETE ON CASCADE)
    cursor.execute("PRAGMA foreign_keys = ON")

    # tabulka hráčů – jméno musí být unikátní
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hrac(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jmeno TEXT UNIQUE
    )
    """)

    # tabulka her – název musí být unikátní
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hra(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nazev TEXT UNIQUE
    )
    """)

    # tabulka skóre – při smazání hráče nebo hry se smažou i jejich záznamy
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS score(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hrac_id INTEGER,
        hra_id INTEGER,
        body INTEGER,
        datum TEXT,
        FOREIGN KEY (hrac_id) REFERENCES hrac(id) ON DELETE CASCADE,
        FOREIGN KEY (hra_id) REFERENCES hra(id) ON DELETE CASCADE
    )
    """)

    # vloží výchozí hru pokud ještě neexistuje
    cursor.execute("INSERT OR IGNORE INTO hra (nazev) VALUES (?)", ("Hopík",))

    conn.commit()
    conn.close()


def uloz_score(jmeno, body):
    """
    Uloží skóre hráče do databáze.

    Pokud hráč ještě neexistuje, automaticky ho vytvoří.
    Skóre se váže na hru 'Hopík' a aktuální datum.

    Args:
        jmeno (str): Jméno hráče.
        body (int): Dosažené skóre.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # zapnutí podpory cizích klíčů
    cursor.execute("PRAGMA foreign_keys = ON")

    # aktuální datum ve formátu YYYY-MM-DD
    datum = datetime.now().strftime("%Y-%m-%d")

    # vloží hráče pokud ještě neexistuje
    cursor.execute("INSERT OR IGNORE INTO hrac (jmeno) VALUES (?)", (jmeno,))

    # načte ID hráče
    cursor.execute("SELECT id FROM hrac WHERE jmeno=?", (jmeno,))
    hrac_id = cursor.fetchone()[0]

    # načte ID hry Hopík
    cursor.execute("SELECT id FROM hra WHERE nazev=?", ("Hopík",))
    hra_id = cursor.fetchone()[0]

    # uloží záznam skóre
    cursor.execute("""
    INSERT INTO score (hrac_id, hra_id, body, datum)
    VALUES (?, ?, ?, ?)
    """, (hrac_id, hra_id, body, datum))

    conn.commit()
    conn.close()


def nacti_score():
    """
    Načte všechna skóre z databáze seřazená sestupně podle počtu bodů.

    Používá JOIN přes tabulky hrac, score a hra.

    Returns:
        list[tuple]: Seznam záznamů ve formátu (jmeno, body, datum).
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # JOIN přes všechny tabulky, seřazeno od nejvyššího skóre
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
    """
    Smaže záznam skóre z databáze podle jeho ID.

    Args:
        id (int): ID záznamu skóre v tabulce score.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # zapnutí podpory cizích klíčů
    cursor.execute("PRAGMA foreign_keys = ON")

    # smazání záznamu podle ID
    cursor.execute("DELETE FROM score WHERE id=?", (id,))
    conn.commit()

    conn.close()


def uprav_score(id, nove_body):
    """
    Upraví počet bodů u existujícího záznamu skóre.

    Args:
        id (int): ID záznamu skóre v tabulce score.
        nove_body (int): Nová hodnota skóre.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # aktualizace skóre podle ID
    cursor.execute("UPDATE score SET body=? WHERE id=?", (nove_body, id))
    conn.commit()

    conn.close()