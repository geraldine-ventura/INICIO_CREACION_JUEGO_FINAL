# nivel.py
import pygame
from botin import Fruta


class Nivel:
    def __init__(self):
        # ... otras inicializaciones ...

        # Crea instancias de frutas en posiciones específicas del nivel
        self.frutas_group = pygame.sprite.Group()
        fruta_1 = Fruta(100, 200, "ruta_a_la_imagen_1.png")
        fruta_2 = Fruta(300, 400, "ruta_a_la_imagen_2.png")
        self.frutas_group.add(fruta_1, fruta_2)
