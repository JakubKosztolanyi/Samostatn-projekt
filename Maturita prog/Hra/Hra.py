from pygame import *
import random
import sys
import os

# fix importů – přidá složku skriptu do cesty
sys.path.insert(0, os.path.dirname(__file__))

from databaze import uloz_score
from html_generator import aktualizuj_html

# konstanty okna
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 550

# konstanty hráče
PLAYER_RADIUS = 20
PLAYER_SPEED_X = 5
JUMP_SPEED = 15

# fyzika
GRAVITY = 0.5
MAX_JUMP_HEIGHT = 150

# konstanty plošin
PLATFORM_WIDTH = 72
PLATFORM_HEIGHT = 18

# snímky za sekundu
FPS = 60


def spawn_platform(last_y, platforms):
    """
    Vytvoří novou plošinu a přidá ji do seznamu plošin.

    Plošina se vygeneruje náhodně na ose X a ve výšce
    odvozené od poslední plošiny. Každá plošina má náhodný
    směr pohybu (doleva nebo doprava).

    Args:
        last_y (int): Y souřadnice poslední (nejvyšší) plošiny.
        platforms (list): Seznam plošin, do kterého se nová plošina přidá.
    """
    # náhodná výška a pozice nové plošiny
    y = last_y - random.randint(80, MAX_JUMP_HEIGHT)
    x = random.randint(0, WINDOW_WIDTH - PLATFORM_WIDTH)

    # náhodný směr pohybu (-1 doleva, 1 doprava)
    direction = random.choice([-1, 1])

    # přidání plošiny do seznamu
    platforms.append({
        "rect": Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT),
        "dir": direction
    })


def event_loop():
    """
    Zpracuje všechny pygame události v aktuálním snímku.

    Kontroluje zavření okna (QUIT) a stisknutí klávesy ESC.
    Pokud nastane jedna z těchto událostí, vrátí False
    a hra se ukončí.

    Returns:
        bool: True pokud hra má pokračovat, False pokud má skončit.
    """
    for e in event.get():

        # zavření okna
        if e.type == QUIT:
            return False

        # stisk klávesy ESC ukončí hru
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                return False

    return True


def spust_hru(jmeno):
    """
    Spustí hlavní herní smyčku hry Hopík.

    Inicializuje pygame, vytvoří okno, vygeneruje plošiny
    a spustí herní smyčku. Hráč se pohybuje šipkami doleva/doprava
    a automaticky skáče po plošinách. Čím výše hráč skočí,
    tím více bodů získá.

    Po pádu hráče mimo obrazovku se skóre uloží do databáze
    a aktualizuje se HTML tabulka výsledků.

    Args:
        jmeno (str): Jméno hráče zobrazené a ukládané ke skóre.
    """
    # inicializace pygame
    init()

    # vytvoření okna
    window = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    display.set_caption("Hopík")

    clock = time.Clock()

    # počáteční hodnoty
    score = 0
    player_x = WINDOW_WIDTH // 2
    player_y = WINDOW_HEIGHT - 40 - PLAYER_RADIUS
    player_speed_y = 0

    platforms = []

    # vytvoření země
    ground = {
        "rect": Rect(0, WINDOW_HEIGHT - 20, WINDOW_WIDTH, 20),
        "dir": 0
    }
    platforms.append(ground)

    # vygenerování prvních plošin
    last_platform_y = ground["rect"].y
    for _ in range(7):
        spawn_platform(last_platform_y, platforms)
        last_platform_y = platforms[-1]["rect"].y

    running = True

    while running:

        # zpracování událostí
        running = event_loop()

        # pohyb hráče podle stisknutých kláves
        keys = key.get_pressed()
        if keys[K_LEFT]:
            player_x -= PLAYER_SPEED_X
        if keys[K_RIGHT]:
            player_x += PLAYER_SPEED_X

        # uložení předchozí pozice pro detekci kolize
        prev_y = player_y

        # aplikace gravitace
        player_y -= player_speed_y
        player_speed_y -= GRAVITY

        # obdélník hráče pro kolize
        player_rect = Rect(
            player_x - PLAYER_RADIUS,
            player_y - PLAYER_RADIUS,
            PLAYER_RADIUS * 2,
            PLAYER_RADIUS * 2
        )

        # detekce kolize s plošinami
        for plat in platforms:
            plat_top = plat["rect"].y

            # hráč musí padat shora na plošinu
            if prev_y + PLAYER_RADIUS <= plat_top <= player_y + PLAYER_RADIUS:
                if player_rect.colliderect(plat["rect"]):
                    player_y = plat_top - PLAYER_RADIUS
                    player_speed_y = JUMP_SPEED
                    break

        # posun obrazovky když hráč vyskočí vysoko
        if player_y < WINDOW_HEIGHT * 0.4:
            shift = WINDOW_HEIGHT * 0.4 - player_y
            player_y = WINDOW_HEIGHT * 0.4
            score += shift / 50  # přičtení skóre podle výšky

            # posun všech plošin dolů
            for plat in platforms:
                plat["rect"].y += shift

        # odstranění plošin mimo obrazovku
        platforms = [p for p in platforms if p["rect"].y < WINDOW_HEIGHT + 100]

        # generování nových plošin nahoře
        last_platform_y = min([p["rect"].y for p in platforms])
        while last_platform_y > -MAX_JUMP_HEIGHT:
            spawn_platform(last_platform_y, platforms)
            last_platform_y = platforms[-1]["rect"].y

        # pohyb plošin doleva/doprava
        for plat in platforms:
            if plat != ground:
                plat["rect"].x += plat["dir"] * 2

                # odraz od okrajů okna
                if plat["rect"].x <= 0 or plat["rect"].x + PLATFORM_WIDTH >= WINDOW_WIDTH:
                    plat["dir"] *= -1

        # konec hry – hráč spadl dolů
        if player_y > WINDOW_HEIGHT:
            uloz_score(jmeno, int(score))
            aktualizuj_html()
            running = False

        # vykreslení
        window.fill((255, 255, 255))

        for plat in platforms:
            draw.rect(window, (0, 0, 0), plat["rect"])

        draw.circle(window, (0, 0, 0), (int(player_x), int(player_y)), PLAYER_RADIUS)

        # zobrazení skóre
        f = font.SysFont("", 50)
        msg = f.render(str(int(score)), True, (100, 100, 100))
        window.blit(msg, (10, 10))

        display.update()
        clock.tick(FPS)