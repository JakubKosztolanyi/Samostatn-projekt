import pygame
import sys
import os

# 🔥 fix importů
sys.path.insert(0, os.path.dirname(__file__))

from databaze import vytvor_db
from Hra import spust_hru

pygame.init()

vytvor_db()

WIDTH = 500
HEIGHT = 600

okno = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hopík - Menu")

WHITE = (245,245,245)
BLACK = (30,30,30)
BLUE = (70,130,255)
BLUE_LIGHT = (120,170,255)

title_font = pygame.font.Font(None, 80)
font = pygame.font.Font(None, 40)

input_box = pygame.Rect(150,250,200,45)

jmeno_hrace = ""
aktivni = False


def button(text,x,y,w,h,action=None):

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:

        pygame.draw.rect(okno,BLUE_LIGHT,(x,y,w,h),border_radius=8)

        if click[0] == 1 and action != None:
            action()

    else:
        pygame.draw.rect(okno,BLUE,(x,y,w,h),border_radius=8)

    txt = font.render(text,True,WHITE)

    okno.blit(txt,(x+w/2-txt.get_width()/2,y+h/2-txt.get_height()/2))


def start_game():

    global jmeno_hrace

    if jmeno_hrace.strip() != "":
        spust_hru(jmeno_hrace)


def quit_game():
    pygame.quit()
    sys.exit()


def menu():

    global jmeno_hrace, aktivni

    while True:

        okno.fill(WHITE)

        title = title_font.render("Hopík",True,BLACK)
        okno.blit(title,(WIDTH/2-title.get_width()/2,120))

        label = font.render("Zadej jméno:",True,BLACK)
        okno.blit(label,(WIDTH/2-label.get_width()/2,210))

        pygame.draw.rect(okno,BLUE if aktivni else BLACK,input_box,2,border_radius=6)

        text_surface = font.render(jmeno_hrace,True,BLACK)
        okno.blit(text_surface,(input_box.x+8,input_box.y+8))

        button("Start hry",150,330,200,50,start_game)
        button("Konec",150,400,200,50,quit_game)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if input_box.collidepoint(event.pos):
                    aktivni = True
                else:
                    aktivni = False

            if event.type == pygame.KEYDOWN and aktivni:

                if event.key == pygame.K_BACKSPACE:
                    jmeno_hrace = jmeno_hrace[:-1]

                else:

                    if len(jmeno_hrace) < 12:
                        jmeno_hrace += event.unicode

        pygame.display.update()


menu()