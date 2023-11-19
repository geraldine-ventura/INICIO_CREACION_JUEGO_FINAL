import pygame
import sys
from constantes import *
from player import Player

# Inicializar Pygame
pygame.init()

# Configurar la pantalla
screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
clock = pygame.time.Clock()

# Cargar imagen de fondo y escalarla
imagen_fondo = pygame.image.load(
    "CLASE_19_inicio_juego/images/locations/forest/all.png"
)
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO_VENTANA, ALTO_VENTANA))

# Crear instancia del jugador con valores predeterminados
player_1 = Player(0, 0, 4, 8, 8, 16, frame_rate_ms=100, move_rate_ms=50, jump_height=10)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Manejar eventos de teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_1.control("WALK_L")
            elif event.key == pygame.K_RIGHT:
                player_1.control("WALK_R")
            elif event.key == pygame.K_SPACE:
                # Aquí puedes manejar diferentes acciones según las teclas
                player_1.control("JUMP_R")
                player_1.control("RUN_R")

        elif event.type == pygame.KEYUP:
            if (
                event.key == pygame.K_LEFT
                or event.key == pygame.K_RIGHT
                or event.key == pygame.K_SPACE
            ):
                player_1.control("STAY")

    # Limpiar la pantalla con la imagen de fondo
    screen.blit(imagen_fondo, imagen_fondo.get_rect())

    # Actualizar y dibujar al jugador
    player_1.update()
    player_1.draw(screen)

    # Aquí puedes agregar la lógica para actualizar enemigos y dibujar el nivel

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad del bucle
    delta_ms = clock.tick(FPS)
