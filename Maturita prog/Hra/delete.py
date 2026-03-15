import sys
from html_generator import aktualizuj_html
from databaze import smaz_score


query = sys.argv[1] if len(sys.argv) > 1 else ""

if "id=" in query:

    id = query.split("=")[1]

    smaz_score(id)

    aktualizuj_html()

    print("Score smazáno")