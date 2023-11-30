""" # fruta.py

import pygame


class Fruta(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


# Crear una instancia de Fruit con valores específicos
fruta = Fru(x=100, y=200, width=30, height=30)

# Crear un objeto pygame.Rect usando los atributos de la fruta
enemy_shoot_rect = pygame.Rect(fruta.x, fruta.y, fruta.width, fruta.height)
 """
""" # fruta.py

import pygame


class Fruta(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


# Crear una instancia de Fruit con valores específicos
fruta = Fru(x=100, y=200, width=30, height=30)

# Crear un objeto pygame.Rect usando los atributos de la fruta
enemy_shoot_rect = pygame.Rect(fruta.x, fruta.y, fruta.width, fruta.height)
 """
import pygame


class Fruta(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path):
        super().__init__()  # Llama al inicializador de la clase base
        self.image = pygame.Surface(
            (width, height)
        )  # Crea una superficie para el sprite
        self.image.fill(
            (255, 0, 0)
        )  # Rellena la superficie con un color rojo (solo como ejemplo)
        self.rect = self.image.get_rect(
            topleft=(x, y)
        )  # Obtiene el rectángulo del sprite


# Crear una instancia de Fruta
fruta_1 = Fruta(
    x=100,
    y=200,
    width=30,  # Ajusta el valor de width según tus necesidades
    height=30,  # Ajusta el valor de height según tus necesidades
    image_path="Z_CLASE_23_inicio_NO_TOUCH copy/images/gui/set_gui_01/Data_Border/Elements/Element02.png",
)


# Ahora, puedes acceder a la imagen y el rectángulo del sprite
enemy_shoot_rect = fruta_1.rect
