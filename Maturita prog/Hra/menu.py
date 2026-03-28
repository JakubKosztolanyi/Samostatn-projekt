import pygame
import sys
import os

# fix importů – přidá složku skriptu do cesty
sys.path.insert(0, os.path.dirname(__file__))

from databaze import vytvor_db
from Hra import spust_hru

# inicializace pygame
pygame.init()

# vytvoření databáze při spuštění
vytvor_db()

# rozměry okna
WIDTH = 500
HEIGHT = 600

okno = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hopík - Menu")

# barvy
WHITE = (245, 245, 245)
BLACK = (30, 30, 30)
BLUE = (70, 130, 255)
BLUE_LIGHT = (120, 170, 255)

# fonty
title_font = pygame.font.Font(None, 80)
font = pygame.font.Font(None, 40)

# vstupní pole pro jméno
input_box = pygame.Rect(150, 250, 200, 45)

# globální proměnné
jmeno_hrace = ""
aktivni = False


def button(text, x, y, w, h, action=None):
    """
    Vykreslí interaktivní tlačítko v pygame okně.

    Tlačítko reaguje na pohyb myši (hover efekt) a kliknutí.
    Při najetí myší se změní barva. Při kliknutí se zavolá
    předaná funkce action.

    Args:
        text (str): Text zobrazený na tlačítku.
        x (int): X souřadnice tlačítka.
        y (int): Y souřadnice tlačítka.
        w (int): Šířka tlačítka.
        h (int): Výška tlačítka.
        action (callable, optional): Funkce zavolaná po kliknutí. Výchozí None.
    """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # hover efekt – změní barvu při najetí myší
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(okno, BLUE_LIGHT, (x, y, w, h), border_radius=8)

        # kliknutí zavolá akci
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(okno, BLUE, (x, y, w, h), border_radius=8)

    # vykreslení textu na střed tlačítka
    txt = font.render(text, True, WHITE)
    okno.blit(txt, (x + w / 2 - txt.get_width() / 2, y + h / 2 - txt.get_height() / 2))


def start_game():
    """
    Spustí hru pokud je zadáno jméno hráče.

    Zkontroluje zda pole jmeno_hrace není prázdné
    a pokud ne, zavolá funkci spust_hru() s daným jménem.
    """
    global jmeno_hrace

    # spustí hru pouze pokud je zadáno jméno
    if jmeno_hrace.strip() != "":
        spust_hru(jmeno_hrace)


def quit_game():
    """
    Ukončí pygame a celou aplikaci.

    Zavolá pygame.quit() pro správné uvolnění zdrojů
    a sys.exit() pro ukončení programu.
    """
    pygame.quit()
    sys.exit()


def menu():
    """
    Spustí hlavní menu hry Hopík.

    Zobrazí název hry, vstupní pole pro jméno hráče
    a tlačítka Start hry / Konec. Zpracovává události
    klávesnice (psaní jména, Backspace) a myši (kliknutí
    na tlačítka, aktivace vstupního pole).

    Smyčka běží dokud hráč neukončí aplikaci.
    """
    global jmeno_hrace, aktivni

    while True:

        # vyplnění pozadí
        okno.fill(WHITE)

        # nadpis hry
        title = title_font.render("Hopík", True, BLACK)
        okno.blit(title, (WIDTH / 2 - title.get_width() / 2, 120))

        # popisek vstupního pole
        label = font.render("Zadej jméno:", True, BLACK)
        okno.blit(label, (WIDTH / 2 - label.get_width() / 2, 210))

        # vstupní pole – modré pokud aktivní, jinak černé
        pygame.draw.rect(okno, BLUE if aktivni else BLACK, input_box, 2, border_radius=6)

        # zobrazení zadaného jména
        text_surface = font.render(jmeno_hrace, True, BLACK)
        okno.blit(text_surface, (input_box.x + 8, input_box.y + 8))

        # tlačítka
        button("Start hry", 150, 330, 200, 50, start_game)
        button("Konec", 150, 400, 200, 50, quit_game)

        # zpracování událostí
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                quit_game()

            # kliknutí myší – aktivace vstupního pole
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    aktivni = True
                else:
                    aktivni = False

            # psaní jména do vstupního pole
            if event.type == pygame.KEYDOWN and aktivni:
                if event.key == pygame.K_BACKSPACE:
                    # smazání posledního znaku
                    jmeno_hrace = jmeno_hrace[:-1]
                else:
                    # maximálně 12 znaků
                    if len(jmeno_hrace) < 12:
                        jmeno_hrace += event.unicode

        pygame.display.update()


menu()