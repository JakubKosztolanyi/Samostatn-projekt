from pygame import *
import random

window_x = 500
window_y = 550

init()
window = display.set_mode((window_x, window_y))
display.set_caption('Stick Jump!')
clock = time.Clock()

# Herní informace
info = {
    'score': 0,
    'high_score': 0
}

# Panáček (kolečko)
player_radius = 20
player_x = window_x // 2
player_y = window_y - 40 - player_radius  # startovní pozice nad zemí
player_speed_x = 0
player_speed_y = 0
max_speed_x = 5
jump_speed = 15
gravity = 0.5
max_jump_height = 150  # max vzdálenost, kterou panáček může přeskočit

# Platformy
platform_width = 72
platform_height = 18
platforms = []

# Zem / startovací plošina úplně dole
ground = {'rect': Rect(0, window_y - 20, window_x, 20), 'dir': 0}
platforms.append(ground)

# Funkce pro generování nové plošiny nad poslední existující
def spawn_platform(last_y):
    y = last_y - random.randint(80, max_jump_height)
    x = random.randint(0, window_x - platform_width)
    direction = random.choice([-1, 1])
    platforms.append({'rect': Rect(x, y, platform_width, platform_height), 'dir': direction})

# Inicializace několika plošin nad zemí
last_platform_y = ground['rect'].y
for _ in range(7):
    spawn_platform(last_platform_y)
    last_platform_y = platforms[-1]['rect'].y

# Události
def event_loop():
    for e in event.get():
        if e.type == QUIT:
            quit()
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()

# Hlavní smyčka
while True:
    event_loop()

    keys = key.get_pressed()

    # Pohyb panáčka
    if keys[K_LEFT]:
        player_speed_x = -max_speed_x
    elif keys[K_RIGHT]:
        player_speed_x = max_speed_x
    else:
        player_speed_x = 0

    player_x += player_speed_x

    # Uložíme předchozí Y pro kontrolu průchodu skrz plošinu
    prev_y = player_y
    player_y -= player_speed_y
    player_speed_y -= gravity

    # Skákání a kolize s plošinami
    player_rect = Rect(player_x - player_radius, player_y - player_radius, player_radius*2, player_radius*2)
    for plat in platforms:
        plat_top = plat['rect'].y
        if prev_y + player_radius <= plat_top <= player_y + player_radius and player_rect.colliderect(plat['rect']):
            player_y = plat_top - player_radius
            player_speed_y = jump_speed
            break

    # Posun plošin spolu s postavičkou
    if player_y < window_y * 0.4:
        shift = window_y * 0.4 - player_y
        player_y = window_y * 0.4
        info['score'] += shift / 50
        for plat in platforms:
            plat['rect'].y += shift

    # Odstranění starých plošin a generování nových
    platforms = [plat for plat in platforms if plat['rect'].y < window_y + 100]
    if platforms:
        last_platform_y = min([plat['rect'].y for plat in platforms])
    else:
        last_platform_y = window_y

    while last_platform_y > -max_jump_height:
        spawn_platform(last_platform_y)
        last_platform_y = platforms[-1]['rect'].y

    # Posun plošin do stran (mimo zem)
    for plat in platforms:
        if plat != ground:
            plat['rect'].x += plat['dir']*2
            if plat['rect'].x <= 0 or plat['rect'].x + platform_width >= window_x:
                plat['dir'] *= -1

    # Konec hry – pokud panáček spadne 
    if player_y > window_y:
        window.fill((255,255,255))
        f = font.SysFont('', 60)
        msg = f.render("GAME OVER", True, (255,0,0))
        window.blit(msg, (window_x//2 - msg.get_width()//2, window_y//2 - msg.get_height()//2))
        display.update()
        time.wait(2000)
        quit()

    # Kreslení
    window.fill((255,255,255))
    for plat in platforms:
        draw.rect(window, (0,0,0), (plat['rect'].x, plat['rect'].y, plat['rect'].width, plat['rect'].height))
    draw.circle(window, (0,0,0), (int(player_x), int(player_y)), player_radius)

    # Skóre
    f = font.SysFont('', 50)
    msg = f.render(str(int(info['score'])), True, (100,100,100))
    window.blit(msg, (10, msg.get_height() + 10))

    display.update()
    clock.tick(60)
    