import sys  # knihovna pro práci s argumenty z příkazové řádky

from html_generator import aktualizuj_html  # funkce která znovu vygeneruje HTML stránku se score
from databaze import smaz_score  # funkce která smaže score z databáze podle ID


# vezme argument z příkazové řádky
# pokud žádný argument není, uloží se prázdný řetězec
query = sys.argv[1] if len(sys.argv) > 1 else ""


# zkontroluje jestli argument obsahuje "id="
# např. id=3
if "id=" in query:

    # rozdělí text podle "=" a vezme druhou část
    # např. "id=3" -> ["id","3"] -> vezme "3"
    id = query.split("=")[1]

    # zavolá funkci která smaže score s daným ID z databáze
    smaz_score(id)

    # znovu vygeneruje HTML stránku aby se aktualizoval seznam score
    aktualizuj_html()

    # vypíše zprávu do konzole
    print("Score smazáno")