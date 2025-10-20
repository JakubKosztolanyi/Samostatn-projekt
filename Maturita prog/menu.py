import pygame
import sys

pygame.init()

# --- Nastavení okna ---
šířka = 500
výška = 600
okno = pygame.display.set_mode((šířka, výška))
pygame.display.set_caption("Menu hry")

# --- Barvy ---
BÍLÁ = (255, 255, 255)
ČERNÁ = (0, 0, 0)
MODRÁ = (0, 120, 255)
SVĚTLÁ_MODRÁ = (100, 200, 255)

# --- Fonty ---
font = pygame.font.Font(None, 60)
font_tlačítko = pygame.font.Font(None, 50)

# --- Tlačítka ---
def kresli_tlačítko(text, x, y, w, h, barva, barva_hover, akce=None):
    myš = pygame.mouse.get_pos()
    klik = pygame.mouse.get_pressed()

    if x + w > myš[0] > x and y + h > myš[1] > y:
        pygame.draw.rect(okno, barva_hover, (x, y, w, h))
        if klik[0] == 1 and akce is not None:
            akce()
    else:
        pygame.draw.rect(okno, barva, (x, y, w, h))

    text_obj = font_tlačítko.render(text, True, ČERNÁ)
    okno.blit(text_obj, (x + (w - text_obj.get_width()) / 2, y + (h - text_obj.get_height()) / 2))

# --- Funkce akcí ---
def spustit_hru():
    hra_beží = True
    while hra_beží:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        okno.fill(BÍLÁ)
        text = font.render("Hra běží!", True, ČERNÁ)
        okno.blit(text, (šířka // 2 - text.get_width() // 2, výška // 2 - text.get_height() // 2))
        pygame.display.update()

def konec_hry():
    pygame.quit()
    sys.exit()

# --- Hlavní smyčka menu ---
def menu():
    while True:
        okno.fill(BÍLÁ)
        titul = font.render("Moje hra", True, ČERNÁ)
        okno.blit(titul, (šířka // 2 - titul.get_width() // 2, 150))

        kresli_tlačítko("Start", 150, 300, 200, 60, MODRÁ, SVĚTLÁ_MODRÁ, spustit_hru)
        kresli_tlačítko("Konec", 150, 400, 200, 60, MODRÁ, SVĚTLÁ_MODRÁ, konec_hry)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                konec_hry()

        pygame.display.update()

menu()
