from models.auxiliar import SurfaceManager as sf
import pygame as pg
from models.constantes import ANCHO_VENTANA, DEBUG, ALTO_VENTANA


# Define una clase llamada Jugador que representa al personaje del juego.
class Jugador:
    # El método __init__ es el constructor de la clase. Inicializa las propiedades del jugador, como la posición inicial
    # (coord_x y coord_y), la velocidad de animación (frame_rate), las velocidades de caminar y correr, la gravedad y la altura del salto.
    def __init__(
        self,
        coord_x,
        coord_y,
        frame_rate=100,
        speed_walk=6,
        speed_run=12,
        gravity=16,
        jump=32,
    ):
        # Carga una superficie de sprites para la animación de reposo del jugador mirando hacia la derecha
        # utilizando el método ""get_surface_from_spritesheet" de la clase SurfaceManager.

        self.__iddle_r = sf.get_surface_from_spritesheet(
            "Pygame_COR_CAM_SAL_LIM/assets/img/player/iddle/player_idle.png", 5, 1
        )
        self.__iddle_l = sf.get_surface_from_spritesheet(
            "Pygame_COR_CAM_SAL_LIM/assets/img/player/iddle/player_idle.png",
            5,
            1,
            flip=True,
        )
        # flip=True se utiliza para espejar la imagen horizontalmente y crear la versión reflejada de la animación original.

        self.__walk_r = sf.get_surface_from_spritesheet(
            "Pygame_COR_CAM_SAL_LIM/assets/img/player/walk/player_walk.png", 6, 1
        )
        self.__walk_l = sf.get_surface_from_spritesheet(
            "Pygame_COR_CAM_SAL_LIM/assets/img/player/walk/player_walk.png",
            6,
            1,
            flip=True,
        )
        self.__run_r = sf.get_surface_from_spritesheet(
            "Pygame_COR_CAM_SAL_LIM/assets/img/player/run/player_run.png", 2, 1
        )
        self.__run_l = sf.get_surface_from_spritesheet(
            "Pygame_COR_CAM_SAL_LIM/assets/img/player/run/player_run.png",
            2,
            1,
            flip=True,
        )
        self.__jump_r = sf.get_surface_from_spritesheet(
            "Pygame_COR_CAM_SAL_LIM/assets/img/player/jump/player_jump.png", 6, 1
        )
        self.__jump_l = sf.get_surface_from_spritesheet(
            "Pygame_COR_CAM_SAL_LIM/assets/img/player/jump/player_jump.png",
            6,
            1,
            flip=True,
        )

        # Inicializa las propiedades del jugador, como su posición (__move_x y __move_y), velocidades, tiempo de animación, gravedad, etc.
        self.__move_x = coord_x
        self.__move_y = coord_y
        self.__speed_walk = speed_walk
        self.__speed_run = speed_run
        self.__frame_rate = frame_rate
        self.__player_move_time = 0
        self.__player_animation_time = 0
        self.__gravity = gravity
        self.__jump = jump
        self.__is_jumping = False
        self.__initial_frame = 0
        self.__actual_animation = self.__iddle_r
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__rect = self.__actual_img_animation.get_rect()
        self.__is_looking_right = True

    ###---------------------------------------------------------------------------------------->
    # Un método privado que configura las animaciones horizontales del jugador.
    def __set_x_animations_preset(
        self, move_x, animation_list: list[pg.surface.Surface], look_r: bool
    ):
        self.__move_x = move_x
        self.__actual_animation = animation_list
        self.__is_looking_right = look_r

    # Un método privado que configura las animaciones verticales del jugador, específicamente para el salto.
    def __set_y_animations_preset(self):
        self.__move_y = -self.__jump
        self.__move_x = (
            self.__speed_run if self.__is_looking_right else -self.__speed_run
        )
        self.__actual_animation = (
            self.__jump_r if self.__is_looking_right else self.__jump_l
        )
        self.__initial_frame = 0
        self.__is_jumping = True

    # Un método que se llama cuando el jugador está caminando. Cambia las animaciones y la dirección según la tecla presionada.
    def walk(self, direction: str = "Right"):
        match direction:
            case "Right":
                look_right = True
                self.__set_x_animations_preset(
                    self.__speed_walk, self.__walk_r, look_r=look_right
                )
            case "Left":
                look_right = False
                self.__set_x_animations_preset(
                    -self.__speed_walk, self.__walk_l, look_r=look_right
                )

    def run(self, direction: str = "Right"):
        self.__initial_frame = 0
        match direction:
            case "Right":
                look_right = True
                self.__set_x_animations_preset(
                    self.__speed_run, self.__run_r, look_r=look_right
                )
            case "Left":
                look_right = False
                self.__set_x_animations_preset(
                    -self.__speed_run, self.__run_l, look_r=look_right
                )

    # Un método que se llama cuando el jugador está en reposo. Ajusta las animaciones y la posición del jugador.
    def stay(self):
        if (
            self.__actual_animation != self.__iddle_l
            and self.__actual_animation != self.__iddle_r
        ):
            self.__actual_animation = (
                self.__iddle_r if self.__is_looking_right else self.__iddle_l
            )
            self.__initial_frame = 0
            self.__move_x = 0
            self.__move_y = 0

    def jump(self, jumping=True):
        if jumping and not self.__is_jumping:
            self.__set_y_animations_preset()
        else:
            self.__is_jumping = False
            self.stay()

    def __set_borders_limits(self):
        pixels_move = 0
        if self.__move_x > 0:
            pixels_move = (
                self.__move_x
                if self.__rect.x
                < ANCHO_VENTANA - self.__actual_img_animation.get_width()
                else 0
            )
        elif self.__move_x < 0:
            pixels_move = self.__move_x if self.__rect.x > 0 else 0
        return pixels_move

    def __set_borders_limits_y(self):
        pixels_move = 0
        if self.__move_y > 0:
            pixels_move = (
                self.__move_y
                if self.__rect.y
                < ALTO_VENTANA - self.__actual_img_animation.get_height()
                else 0
            )
        elif self.__move_y < 0:
            pixels_move = self.__move_y if self.__rect.y > 0 else 0
        return pixels_move

    # Un método que maneja el movimiento del jugador en función del tiempo delta_ms.
    def do_movement(self, delta_ms):
        self.__player_move_time += delta_ms
        if self.__player_move_time >= self.__frame_rate:
            self.__player_move_time = 0
            self.__rect.x += self.__set_borders_limits()
            self.__rect.y += self.__set_borders_limits_y()
            # Parte relacionado a saltar
            if self.__rect.y < 300:
                self.__rect.y += self.__gravity

    def do_animation(self, delta_ms):
        self.__player_animation_time += delta_ms
        if self.__player_animation_time >= self.__frame_rate:
            self.__player_animation_time = 0
            if self.__initial_frame < len(self.__actual_animation) - 1:
                self.__initial_frame += 1
            else:
                self.__initial_frame = 0
                # if self.__is_jumping:
                #     self.__is_jumping = False
                #     self.__move_y = 0

    # Un método que actualiza el estado del jugador en función del tiempo delta_ms.
    def update(self, delta_ms):
        self.do_movement(delta_ms)
        self.do_animation(delta_ms)

    # Un método que dibuja al jugador en la pantalla.
    # el método draw se encarga de renderizar visualmente al jugador en la pantalla del juego.
    def draw(self, screen: pg.surface.Surface):
        if DEBUG:
            # dibuja un rectángulo rojo (pg.draw.rect) alrededor del jugador para visualizar su posición.
            pg.draw.rect(screen, "red", self.__rect)
            # pg.draw.rect(screen, 'green', self.__rect.bottom)

        # Luego, obtiene la imagen actual de la animación en base al índice actual
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]

        # Utiliza screen.blit para colocar esa imagen en la posición definida por el rectángulo del jugador (self.__rect).
        screen.blit(self.__actual_img_animation, self.__rect)
