import sqlite3  # knihovna pro práci s SQLite databází
import os       # knihovna pro práci se soubory a cestami
from datetime import datetime  # práce s datem a časem

# vytvoří cestu k databázi hramenu.db ve stejné složce jako je tento soubor
DB_PATH = os.path.join(os.path.dirname(__file__), "hramenu.db")


def vytvor_db():
                                    # připojení k databázi (pokud neexistuje, vytvoří se)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()              # kurzor slouží k provádění SQL příkazů

                                        # vytvoření tabulky score pokud ještě neexistuje
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS score(
        id INTEGER PRIMARY KEY AUTOINCREMENT,  
        jmeno TEXT,                            
        body INTEGER,                          
        datum TEXT                             
    )
    """)

    conn.commit()  # uloží změny v databázi
    conn.close()   # zavře spojení s databází


def uloz_score(jmeno, body):
    # připojení k databázi
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # získá aktuální datum ve formátu RRRR-MM-DD
    datum = datetime.now().strftime("%Y-%m-%d")

    # vloží nový záznam do tabulky score
    cursor.execute(
        "INSERT INTO score (jmeno, body, datum) VALUES (?, ?, ?)",
        (jmeno, body, datum)  # hodnoty které se vloží do databáze
    )

    conn.commit()  # uloží změny
    conn.close()   # zavře databázi


def nacti_score():
    # připojení k databázi
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # vybere všechny záznamy z tabulky score
    # ORDER BY body DESC znamená seřazení podle bodů od nejvyššího
    cursor.execute("SELECT id,jmeno,body,datum FROM score ORDER BY body DESC")

    data = cursor.fetchall()  # načte všechny řádky z výsledku dotazu

    conn.close()  # zavře databázi
    return data   # vrátí načtená data


def smaz_score(id):
    # připojení k databázi
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # smaže záznam z tabulky score podle ID
    cursor.execute("DELETE FROM score WHERE id=?", (id,))
    conn.commit()  # uloží změny

    conn.close()  # zavře databázi