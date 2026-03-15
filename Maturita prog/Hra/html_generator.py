import os
import sys

# přidá složku Hra do python path
sys.path.append(os.path.dirname(__file__))

from databaze import nacti_score


def aktualizuj_html():

    data = nacti_score()

    rows = ""
    pozice = 1

    for id, jmeno, body, datum in data:

        rows += f"""
<tr>
<td>{pozice}</td>
<td>{jmeno}</td>
<td>{body}</td>
<td>{datum}</td>
</tr>
"""

        pozice += 1


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

    base = os.path.dirname(__file__)
    path = os.path.join(base, "..", "Web", "hra.html")

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)