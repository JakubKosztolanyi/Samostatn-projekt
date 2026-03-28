import sys

from html_generator import aktualizuj_html
from databaze import smaz_score


def zpracuj_argument(query):
    """
    Zpracuje argument z příkazové řádky a smaže příslušné skóre.

    Očekává argument ve formátu 'id=<číslo>', například 'id=3'.
    Pokud argument obsahuje 'id=', extrahuje ID, smaže záznam
    z databáze a aktualizuje HTML tabulku skóre.

    Args:
        query (str): Argument z příkazové řádky, např. 'id=3'.
    """
    # zkontroluje jestli argument obsahuje "id="
    if "id=" in query:

        # extrahuje číslo ID za znakem "="
        id = query.split("=")[1]

        # smaže záznam z databáze
        smaz_score(id)

        # aktualizuje HTML tabulku
        aktualizuj_html()

        print("Score smazáno")


# načte první argument z příkazové řádky, nebo prázdný řetězec
query = sys.argv[1] if len(sys.argv) > 1 else ""

zpracuj_argument(query)