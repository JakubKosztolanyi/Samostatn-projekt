from pygame import *  # import knihovny pygame pro tvorbu hry
import random  # pro generování náhodných čísel
from databaze import uloz_score  # funkce pro uložení score do databáze
from html_generator import aktualizuj_html  # funkce která aktualizuje HTML stránku se score

WINDOW_WIDTH = 500  # šířka okna hry
WINDOW_HEIGHT = 550  # výška okna hry

PLAYER_RADIUS = 20  # poloměr hráče (kreslí se jako kruh)
PLAYER_SPEED_X = 5  # rychlost pohybu hráče doleva/doprava
JUMP_SPEED = 15  # rychlost skoku

GRAVITY = 0.5  # gravitace která táhne hráče dolů
MAX_JUMP_HEIGHT = 150  # maximální výška mezi plošinami

PLATFORM_WIDTH = 72  # šířka plošiny
PLATFORM_HEIGHT = 18  # výška plošiny

FPS = 60  # počet snímků za sekundu


def spawn_platform(last_y, platforms):  # funkce pro vytvoření nové plošiny

    y = last_y - random.randint(80, MAX_JUMP_HEIGHT)  # náhodná výška nové plošiny
    x = random.randint(0, WINDOW_WIDTH - PLATFORM_WIDTH)  # náhodná pozice na ose X

    direction = random.choice([-1, 1])  # náhodný směr pohybu plošiny (doleva nebo doprava)

    platforms.append({  # přidání plošiny do seznamu
        "rect": Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT),  # obdélník plošiny
        "dir": direction  # směr pohybu
    })


def event_loop():  # zpracování událostí hry

    for e in event.get():  # projde všechny události

        if e.type == QUIT:  # pokud se zavře okno
            return False

        if e.type == KEYDOWN:  # pokud je stisknuta klávesa
            if e.key == K_ESCAPE:  # ESC ukončí hru
                return False

    return True  # jinak hra pokračuje


def spust_hru(jmeno):  # hlavní funkce která spustí hru

    init()  # inicializace pygame

    window = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # vytvoření okna hry
    display.set_caption("Hopík")  # název okna

    clock = time.Clock()  # objekt pro řízení FPS

    score = 0  # počáteční score

    player_x = WINDOW_WIDTH // 2  # startovní pozice hráče X
    player_y = WINDOW_HEIGHT - 40 - PLAYER_RADIUS  # startovní pozice hráče Y

    player_speed_y = 0  # vertikální rychlost hráče

    platforms = []  # seznam plošin

    ground = {  # vytvoření země
        "rect": Rect(0, WINDOW_HEIGHT - 20, WINDOW_WIDTH, 20),
        "dir": 0
    }

    platforms.append(ground)  # přidání země mezi plošiny

    last_platform_y = ground["rect"].y  # poslední výška plošiny

    for _ in range(7):  # vytvoření prvních plošin
        spawn_platform(last_platform_y, platforms)
        last_platform_y = platforms[-1]["rect"].y

    running = True  # proměnná řízení hlavního cyklu

    while running:  # hlavní herní smyčka

        running = event_loop()  # kontrola událostí

        keys = key.get_pressed()  # zjistí které klávesy jsou stisknuté

        if keys[K_LEFT]:
            player_x -= PLAYER_SPEED_X  # pohyb doleva

        if keys[K_RIGHT]:
            player_x += PLAYER_SPEED_X  # pohyb doprava

        prev_y = player_y  # uloží předchozí pozici hráče

        player_y -= player_speed_y  # posun hráče
        player_speed_y -= GRAVITY  # aplikace gravitace

        player_rect = Rect(  # vytvoření obdélníku hráče pro kolize
            player_x - PLAYER_RADIUS,
            player_y - PLAYER_RADIUS,
            PLAYER_RADIUS * 2,
            PLAYER_RADIUS * 2
        )

        # kolize s plošinami
        for plat in platforms:

            plat_top = plat["rect"].y  # horní část plošiny

            if prev_y + PLAYER_RADIUS <= plat_top <= player_y + PLAYER_RADIUS:  # kontrola pádu na plošinu

                if player_rect.colliderect(plat["rect"]):  # kolize hráče s plošinou

                    player_y = plat_top - PLAYER_RADIUS  # hráč se postaví na plošinu
                    player_speed_y = JUMP_SPEED  # hráč vyskočí
                    break


        # POSUN OBRAZOVKY
        if player_y < WINDOW_HEIGHT * 0.4:  # pokud hráč vyskočí vysoko

            shift = WINDOW_HEIGHT * 0.4 - player_y  # vypočítá posun
            player_y = WINDOW_HEIGHT * 0.4  # hráč zůstane na místě

            score += shift / 50  # zvýší score podle výšky

            for plat in platforms:
                plat["rect"].y += shift  # posun plošin dolů


        # odstranění starých plošin
        platforms = [p for p in platforms if p["rect"].y < WINDOW_HEIGHT + 100]  # odstraní plošiny mimo obraz

        last_platform_y = min([p["rect"].y for p in platforms])  # najde nejvyšší plošinu

        while last_platform_y > -MAX_JUMP_HEIGHT:  # generuje nové plošiny
            spawn_platform(last_platform_y, platforms)
            last_platform_y = platforms[-1]["rect"].y


        # pohyb plošin
        for plat in platforms:

            if plat != ground:  # země se nepohybuje

                plat["rect"].x += plat["dir"] * 2  # pohyb plošiny

                if plat["rect"].x <= 0 or plat["rect"].x + PLATFORM_WIDTH >= WINDOW_WIDTH:
                    plat["dir"] *= -1  # změna směru na okraji


        # konec hry
        if player_y > WINDOW_HEIGHT:  # hráč spadne dolů

            uloz_score(jmeno, int(score))  # uloží score do databáze
            aktualizuj_html()  # aktualizuje HTML tabulku score

            running = False  # ukončí hru


        # kreslení
        window.fill((255,255,255))  # vyplní pozadí bíle

        for plat in platforms:
            draw.rect(window,(0,0,0),plat["rect"])  # vykreslí plošiny

        draw.circle(window,(0,0,0),(int(player_x),int(player_y)),PLAYER_RADIUS)  # vykreslí hráče

        f = font.SysFont("",50)  # vytvoří font
        msg = f.render(str(int(score)),True,(100,100,100))  # vykreslí score

        window.blit(msg,(10,10))  # zobrazí score v okně

        display.update()  # aktualizuje obrazovku

        clock.tick(FPS)  # omezení FPS