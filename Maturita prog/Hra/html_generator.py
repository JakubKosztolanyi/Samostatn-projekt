import os  # práce se soubory a cestami
import sys  # práce s argumenty a systémovou cestou

# přidá složku kde je tento soubor do python path aby šlo importovat další soubory
sys.path.append(os.path.dirname(__file__))

from databaze import nacti_score  # import funkce která načte score z databáze


def aktualizuj_html():  # funkce která vytvoří HTML stránku s tabulkou score

    data = nacti_score()  # načte všechna score z databáze

    rows = ""  # proměnná kde se bude postupně skládat HTML tabulka
    pozice = 1  # počáteční pozice hráče v tabulce

    for id, jmeno, body, datum in data:  # projde všechny záznamy z databáze

        rows += f"""
<tr>
<td>{pozice}</td>
<td>{jmeno}</td>
<td>{body}</td>
<td>{datum}</td>
</tr>
"""  # vytvoří jeden řádek tabulky

        pozice += 1  # zvýší pořadí hráče


    html = f"""  # vytvoří kompletní HTML stránku
<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="UTF-8">
<title>Hra – Score</title>
<link rel="stylesheet" href="style.css">  <!-- připojení CSS stylu -->
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

{rows}  <!-- sem se vloží všechny řádky tabulky -->

</tbody>

</table>

<a class="back" href="index.html">← Zpět do menu</a>  <!-- odkaz zpět do menu -->

</div>

</body>
</html>
"""

    base = os.path.dirname(__file__)  # zjistí složku kde je tento soubor
    path = os.path.join(base, "..", "Web", "hra.html")  # vytvoří cestu k HTML souboru

    with open(path, "w", encoding="utf-8") as f:  # otevře soubor hra.html pro zápis
        f.write(html)  # zapíše do něj vygenerované HTML