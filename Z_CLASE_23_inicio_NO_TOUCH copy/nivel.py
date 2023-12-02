# nivel.py
import pygame
from botin import Fruta


class Nivel:
    def __init__(self):
        # ... otras inicializaciones ...

        # Crea instancias de frutas en posiciones específicas del nivel
        self.frutas_group = pygame.sprite.Group()
        fruta_1 = Fruta(
            300,
            200,
            "Z_CLASE_23_inicio_NO_TOUCH copy/images/food/banana/apple__x1_iconic_png_1354829396.png",
        )
        fruta_2 = Fruta(
            300,
            400,
            "Z_CLASE_23_inicio_NO_TOUCH copy/images/food/banana/banana__x1_iconic_png_1354829403.png",
        )
        self.frutas_group.add(fruta_1, fruta_2)
