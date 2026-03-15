from pygame import *
import random
from databaze import uloz_score
from html_generator import aktualizuj_html

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 550

PLAYER_RADIUS = 20
PLAYER_SPEED_X = 5
JUMP_SPEED = 15

GRAVITY = 0.5
MAX_JUMP_HEIGHT = 150

PLATFORM_WIDTH = 72
PLATFORM_HEIGHT = 18

FPS = 60


def spawn_platform(last_y, platforms):

    y = last_y - random.randint(80, MAX_JUMP_HEIGHT)
    x = random.randint(0, WINDOW_WIDTH - PLATFORM_WIDTH)

    direction = random.choice([-1, 1])

    platforms.append({
        "rect": Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT),
        "dir": direction
    })


def event_loop():

    for e in event.get():

        if e.type == QUIT:
            return False

        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                return False

    return True


def spust_hru(jmeno):

    init()

    window = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    display.set_caption("Hopík")

    clock = time.Clock()

    score = 0

    player_x = WINDOW_WIDTH // 2
    player_y = WINDOW_HEIGHT - 40 - PLAYER_RADIUS

    player_speed_y = 0

    platforms = []

    ground = {
        "rect": Rect(0, WINDOW_HEIGHT - 20, WINDOW_WIDTH, 20),
        "dir": 0
    }

    platforms.append(ground)

    last_platform_y = ground["rect"].y

    for _ in range(7):
        spawn_platform(last_platform_y, platforms)
        last_platform_y = platforms[-1]["rect"].y

    running = True

    while running:

        running = event_loop()

        keys = key.get_pressed()

        if keys[K_LEFT]:
            player_x -= PLAYER_SPEED_X

        if keys[K_RIGHT]:
            player_x += PLAYER_SPEED_X

        prev_y = player_y

        player_y -= player_speed_y
        player_speed_y -= GRAVITY

        player_rect = Rect(
            player_x - PLAYER_RADIUS,
            player_y - PLAYER_RADIUS,
            PLAYER_RADIUS * 2,
            PLAYER_RADIUS * 2
        )

        # kolize s plošinami
        for plat in platforms:

            plat_top = plat["rect"].y

            if prev_y + PLAYER_RADIUS <= plat_top <= player_y + PLAYER_RADIUS:

                if player_rect.colliderect(plat["rect"]):

                    player_y = plat_top - PLAYER_RADIUS
                    player_speed_y = JUMP_SPEED
                    break


        # POSUN OBRAZOVKY
        if player_y < WINDOW_HEIGHT * 0.4:

            shift = WINDOW_HEIGHT * 0.4 - player_y
            player_y = WINDOW_HEIGHT * 0.4

            score += shift / 50

            for plat in platforms:
                plat["rect"].y += shift


        # odstranění starých plošin
        platforms = [p for p in platforms if p["rect"].y < WINDOW_HEIGHT + 100]

        last_platform_y = min([p["rect"].y for p in platforms])

        while last_platform_y > -MAX_JUMP_HEIGHT:
            spawn_platform(last_platform_y, platforms)
            last_platform_y = platforms[-1]["rect"].y


        # 🔹 POHYB PLOŠIN (toto chybělo)
        for plat in platforms:

            if plat != ground:

                plat["rect"].x += plat["dir"] * 2

                if plat["rect"].x <= 0 or plat["rect"].x + PLATFORM_WIDTH >= WINDOW_WIDTH:
                    plat["dir"] *= -1


        # konec hry
        if player_y > WINDOW_HEIGHT:

            uloz_score(jmeno, int(score))
            aktualizuj_html()

            running = False


        # kreslení
        window.fill((255,255,255))

        for plat in platforms:
            draw.rect(window,(0,0,0),plat["rect"])

        draw.circle(window,(0,0,0),(int(player_x),int(player_y)),PLAYER_RADIUS)

        f = font.SysFont("",50)
        msg = f.render(str(int(score)),True,(100,100,100))

        window.blit(msg,(10,10))

        display.update()

        clock.tick(FPS)