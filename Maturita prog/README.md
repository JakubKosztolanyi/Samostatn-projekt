# Hopík – maturitní projekt

Autor: Jakub Kosztolányi

## Popis projektu

Hopík je jednoduchá plošinová hra vytvořená v Pythonu pomocí knihovny pygame.

Hráč ovládá postavu, která skáče po pohybujících se plošinách a snaží se získat co nejvyšší skóre.

Výsledky hry se ukládají do databáze SQLite a zobrazují se na webové stránce.

Projekt obsahuje také admin rozhraní pro mazání výsledků.

---

## Použité technologie

- Python
- Pygame
- SQLite
- HTML
- CSS
- JavaScript

---

## Struktura projektu

```
MATURITA PROG/

Hra/
├── Hra.py
├── menu.py
├── databaze.py
├── html_generator.py
└── delete.py

Web/
├── index.html
├── hra.html
├── navod.html
├── informace.html
└── style.css

admin.py
```

---

## Instalace

1. Nainstalujte Python

2. Nainstalujte knihovnu pygame

```
pip install pygame
```

---

## Spuštění hry

```
py Hra/menu.py
```

---

## Admin správa databáze

Spusťte admin server:

```
py admin.py
```

Poté otevřete v prohlížeči: http://localhost:8000

Admin heslo lze změnit přímo v souboru `admin.py`.

---

## Databáze

Projekt používá databázi SQLite `hramenu.db`.

Databáze ukládá:

- jméno hráče
- skóre
- datum hry

Výsledky se automaticky zobrazují na stránce: `Web/hra.html`