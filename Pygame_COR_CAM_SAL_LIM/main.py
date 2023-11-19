import pygame as pg

from models.constantes import ALTO_VENTANA, ANCHO_VENTANA, FPS
from models.player.main_player import Jugador

screen = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pg.init()

# Crea un objeto Clock que se utilizará para controlar la velocidad de los fotogramas del juego.
clock = pg.time.Clock()

# Carga una imagen de fondo y la escala para que coincida con las dimensiones de la ventana del juego.
back_img = pg.image.load("Pygame_COR_CAM_SAL_LIM/assets/img/background/goku_house.png")
back_img = pg.transform.scale(back_img, (ANCHO_VENTANA, ALTO_VENTANA))


juego_ejecutandose = True

# Crea una instancia de la clase Jugador con ciertos parámetros de inicialización.

vegeta = Jugador(0, 0, frame_rate=70, speed_walk=20, speed_run=40)

# Inicia un bucle que se ejecutará mientras la variable juego_ejecutandose sea verdadera.
while juego_ejecutandose:
    # print(delta_ms)

    # Obtiene una lista de eventos de pygame y itera sobre ellos.
    lista_eventos = pg.event.get()
    for event in lista_eventos:
        match event.type:
            case pg.KEYDOWN:
                # Detecta si se presiona la tecla espaciadora y llama al método jump de la instancia de Jugador.
                if event.key == pg.K_SPACE:
                    vegeta.jump(True)

            # case pg.KEYUP:
            #     if event.key == pg.K_SPACE:
            #         print('Estoy SOLTANDO el espacio')

            case pg.QUIT:  # Detecta si se presiona el botón de cerrar la ventana y establece la variable juego_ejecutandose en Falso para salir del bucle.
                print("Estoy CERRANDO el JUEGO")
                juego_ejecutandose = False
                break

    # Obtiene una lista de teclas presionadas en el momento.
    lista_teclas_presionadas = pg.key.get_pressed()

    # Detecta si se presiona la tecla de flecha derecha y no se presiona la tecla de flecha izquierda, y llama al método walk con dirección "Right".
    if lista_teclas_presionadas[pg.K_RIGHT] and not lista_teclas_presionadas[pg.K_LEFT]:
        vegeta.walk("Right")
    if lista_teclas_presionadas[pg.K_LEFT] and not lista_teclas_presionadas[pg.K_RIGHT]:
        vegeta.walk("Left")

        # Detecta si no se presionan las teclas de flecha derecha ni izquierda, y llama al método stay
    if (
        not lista_teclas_presionadas[pg.K_RIGHT]
        and not lista_teclas_presionadas[pg.K_LEFT]
    ):
        vegeta.stay()

        # Detecta si se presiona la tecla de flecha derecha y la tecla Mayús izquierda, y no se presiona la tecla de flecha izquierda, y llama al método run con dirección "Right".
    if (
        lista_teclas_presionadas[pg.K_RIGHT]
        and lista_teclas_presionadas[pg.K_LSHIFT]
        and not lista_teclas_presionadas[pg.K_LEFT]
    ):
        vegeta.run("Right")
    if (
        lista_teclas_presionadas[pg.K_LEFT]
        and lista_teclas_presionadas[pg.K_LSHIFT]
        and not lista_teclas_presionadas[pg.K_RIGHT]
    ):
        vegeta.run("Left")

    # Dibuja la imagen de fondo en la ventana del juego.
    screen.blit(back_img, back_img.get_rect())

    # Controla la velocidad de los fotogramas y devuelve el tiempo transcurrido desde el último fotograma en milisegundos.
    delta_ms = clock.tick(FPS)

    # Actualiza y dibuja al personaje principal en la pantalla.
    vegeta.update(delta_ms)

    vegeta.draw(screen)

    # Actualiza la pantalla.
    pg.display.update()

pg.quit()  # Cierra pygame al salir del bucle principal
