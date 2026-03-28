import os
import sys

# fix importu – přidá složku skriptu do cesty
sys.path.insert(0, os.path.dirname(__file__))

from databaze import nacti_score


def aktualizuj_html():
    """
    Vygeneruje HTML soubor s tabulkou skóre a uloží ho do složky Web/.

    Načte aktuální skóre z databáze pomocí nacti_score(),
    sestaví HTML tabulku se sloupci: pořadí, hráč, skóre, datum
    a výsledek zapíše do souboru Web/hra.html.

    Soubor je přepsán při každém volání funkce.
    """
    # načte data z databáze
    data = nacti_score()

    rows = ""
    pozice = 1

    # sestaví řádky tabulky pro každý záznam
    for jmeno, body, datum in data:

        rows += f"""
<tr>
<td>{pozice}</td>
<td>{jmeno}</td>
<td>{body}</td>
<td>{datum}</td>
</tr>
"""
        pozice += 1

    # sestaví celý HTML dokument
    html = f"""
<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="UTF-8">
<title>Hra – Score</title>
<link rel="stylesheet" href="style.css">
</head>

<body>

<div class="container">

<h1>🏆 SCORE TABULKA</h1>
<div class="subtitle">Nejlepší hráči</div>

<table>

<thead>
<tr>
<th>#</th>
<th>Hráč</th>
<th>Skóre</th>
<th>Datum</th>
</tr>
</thead>

<tbody>

{rows}

</tbody>

</table>

<a class="back" href="index.html">← Zpět do menu</a>

</div>

</body>
</html>
"""

    # uloží soubor do složky Web/
    base = os.path.dirname(__file__)
    path = os.path.join(base, "..", "Web", "hra.html")

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)