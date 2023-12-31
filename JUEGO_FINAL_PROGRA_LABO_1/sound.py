# sounds.py

import pygame.mixer

pygame.mixer.init()


def generar_musica(path: str, volumen: float):
    """
    Función que se encarga de generar una música de fondo para mi juego
    Recibe el path donde se ubique mi música y el volumen de la misma
    """
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(volumen)


def generar_sonido(path: str, volumen: float):
    """
    Función que se encarga de generar un sondi
    Recibe el path en donde se encuentra ese sonido y el volumen del mismo
    Retorna el sonido para esperar a que se ejecute
    """
    sonido = pygame.mixer.Sound(path)
    sonido.set_volume(volumen)
    return sonido


def generar_texto(fuente: str, tamaño: float, contenido: str, color: tuple):
    """
    Función que se encarga de generar un texto.
    Recibe la fuente, el tamaño de la misma, el contenido de ese texto y el color
    Retorna la superficie de ese texto
    """
    fuente = pygame.font.SysFont("Arial", tamaño)
    return fuente.render(contenido, True, color)


# Cargar sonidos
sound_bullet_hit_enemy = pygame.mixer.Sound(
    "JUEGO_FINAL_PROGRA_LABO_1/images/tileset/forest/Objects/shoot.mp3"
)
sound_bullet_hit_player = pygame.mixer.Sound(
    "JUEGO_FINAL_PROGRA_LABO_1/images/tileset/forest/Objects/shoot.mp3"
)
# Carga el sonido desde un archivo
impact_sound = pygame.mixer.Sound(
    "JUEGO_FINAL_PROGRA_LABO_1/images/tileset/forest/Objects/shoot.mp3"
)


# Detener sonidos al salir del juego
def stop_sounds():
    pygame.mixer.quit()
