import pygame
from pygame.locals import *
import sys
from constantes import *
from gui_form import Form
from gui_form_menu_A import FormMenuA
from gui_form_menu_B import FormMenuB
from gui_form_menu_C import FormMenuC
from gui_form_menu_game_l1 import FormGameLevel1

pygame.init()
flags = DOUBLEBUF
screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA), flags, 16)

clock = pygame.time.Clock()
enemy_group = pygame.sprite.Group()


form_menu_A = FormMenuA(
    name="form_menu_A",
    master_surface=screen,
    x=300,
    y=200,
    w=500,
    h=400,
    color_background=(255, 255, 0),
    color_border=(255, 0, 255),
    active=True,
)
form_menu_B = FormMenuB(
    name="form_menu_B",
    master_surface=screen,
    x=300,
    y=200,
    w=500,
    h=400,
    color_background=(0, 255, 255),
    color_border=(255, 0, 255),
    active=False,
)
form_menu_C = FormMenuC(
    name="form_menu_C",
    master_surface=screen,
    x=0,
    y=0,
    w=ANCHO_VENTANA,
    h=ALTO_VENTANA,
    color_background=(0, 255, 255),
    color_border=(255, 0, 255),
    active=False,
)

form_game_L1 = FormGameLevel1(
    name="form_game_L1",
    master_surface=screen,
    x=0,
    y=0,
    w=ANCHO_VENTANA,
    h=ALTO_VENTANA,
    color_background=(0, 255, 255),
    color_border=(255, 0, 255),
    active=False,
    enemy_group=enemy_group,
)

while True:
    lista_eventos = pygame.event.get()
    for event in lista_eventos:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Luego, se obtienen las teclas presionadas y el tiempo transcurrido desde la última llamada al método tick:

    keys = pygame.key.get_pressed()

    delta_ms = clock.tick(FPS)
    delta_sec = delta_ms / 1000.0  # Convierte a segundos>>>>>>>>>>>>>>

    aux_form_active = Form.get_active()
    if aux_form_active != None:  # Verifica si hay una forma activa.
        aux_form_active.update(lista_eventos, keys, delta_ms)
        aux_form_active.draw()  # Dibuja la forma activa en la pantalla.

    pygame.display.flip()  # actualiza la pantalla después de realizar cambios en la escena del juego
