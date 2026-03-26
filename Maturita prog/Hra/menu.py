import pygame  # knihovna pro tvorbu her
import sys  # práce se systémem (např. ukončení programu)
import Hra as hra  # import hlavního souboru hry
from databaze import vytvor_db  # funkce která vytvoří databázi

vytvor_db()  # vytvoří databázi při spuštění programu

pygame.init()  # inicializace pygame

WIDTH = 500  # šířka okna
HEIGHT = 600  # výška okna

okno = pygame.display.set_mode((WIDTH, HEIGHT))  # vytvoření herního okna
pygame.display.set_caption("Hopík - Menu")  # název okna

WHITE = (245,245,245)  # barva pozadí
BLACK = (30,30,30)  # černá barva
BLUE = (70,130,255)  # barva tlačítek
BLUE_LIGHT = (120,170,255)  # světlejší barva při najetí myši

title_font = pygame.font.Font(None, 80)  # font pro název hry
font = pygame.font.Font(None, 40)  # font pro text

input_box = pygame.Rect(150,250,200,45)  # pole pro zadání jména

jmeno_hrace = ""  # proměnná pro jméno hráče
aktivni = False  # zda je aktivní textové pole


def button(text,x,y,w,h,action=None):  # funkce pro vytvoření tlačítka

    mouse = pygame.mouse.get_pos()  # pozice myši
    click = pygame.mouse.get_pressed()  # zjistí kliknutí myši

    if x+w > mouse[0] > x and y+h > mouse[1] > y:  # pokud je myš nad tlačítkem

        pygame.draw.rect(okno,BLUE_LIGHT,(x,y,w,h),border_radius=8)  # zvýrazní tlačítko

        if click[0] == 1 and action != None:  # pokud je kliknuto
            action()  # provede funkci tlačítka

    else:
        pygame.draw.rect(okno,BLUE,(x,y,w,h),border_radius=8)  # normální tlačítko

    txt = font.render(text,True,WHITE)  # vytvoří text tlačítka

    okno.blit(txt,(x+w/2-txt.get_width()/2,y+h/2-txt.get_height()/2))  # vykreslí text doprostřed


def start_game():  # funkce pro spuštění hry

    global jmeno_hrace

    if jmeno_hrace.strip() != "":  # zkontroluje zda je jméno vyplněné
        hra.spust_hru(jmeno_hrace)  # spustí hru a předá jméno hráče


def quit_game():  # funkce pro ukončení hry
    pygame.quit()  # ukončí pygame
    sys.exit()  # ukončí program


def menu():  # hlavní menu hry

    global jmeno_hrace, aktivni

    while True:  # nekonečný cyklus menu

        okno.fill(WHITE)  # vyplní pozadí

        title = title_font.render("Hopík",True,BLACK)  # vytvoří název hry
        okno.blit(title,(WIDTH/2-title.get_width()/2,120))  # vykreslí název

        label = font.render("Zadej jméno:",True,BLACK)  # text nad polem
        okno.blit(label,(WIDTH/2-label.get_width()/2,210))

        pygame.draw.rect(okno,BLUE if aktivni else BLACK,input_box,2)  # vykreslí pole pro jméno

        text_surface = font.render(jmeno_hrace,True,BLACK)  # vykreslí zadané jméno
        okno.blit(text_surface,(input_box.x+8,input_box.y+8))

        button("Start hry",150,330,200,50,start_game)  # tlačítko start hry
        button("Konec",150,400,200,50,quit_game)  # tlačítko konec

        for event in pygame.event.get():  # zpracování událostí

            if event.type == pygame.QUIT:  # zavření okna
                quit_game()

            if event.type == pygame.MOUSEBUTTONDOWN:  # kliknutí myší

                if input_box.collidepoint(event.pos):  # kliknutí do input boxu
                    aktivni = True
                else:
                    aktivni = False

            if event.type == pygame.KEYDOWN and aktivni:  # psaní do input boxu

                if event.key == pygame.K_BACKSPACE:  # mazání znaků
                    jmeno_hrace = jmeno_hrace[:-1]

                else:

                    if len(jmeno_hrace) < 12:  # maximální délka jména
                        jmeno_hrace += event.unicode  # přidá znak do jména

        pygame.display.update()  # aktualizace obrazovky


menu()  # spuštění menu