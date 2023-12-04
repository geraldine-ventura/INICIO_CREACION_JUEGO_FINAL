import pygame
from enemigo import Enemy
from constantes import *
from auxiliar import Auxiliar


# Agrega esta línea·.me aparece que no se puede accesder a estab linea

# Resto de tu código...


# from gui_form_menu_game_l1 import *
import math
from sound import *


class Bullet(pygame.sprite.Sprite):
    def __init__(
        self,
        owner,
        x_init,
        y_init,
        x_end,
        y_end,
        speed,
        path,
        frame_rate_ms,
        move_rate_ms,
        direction,  # Agrega el parámetro direction aquí
        width=5,
        height=5,
    ):
        super().__init__()
        self.direction = direction
        self.tiempo_transcurrido_move = 0
        self.image = pygame.image.load(path).convert()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.x = x_init
        self.y = y_init
        self.owner = owner
        self.rect.x = x_init
        self.rect.y = y_init
        self.frame_rate_ms = frame_rate_ms
        self.move_rate_ms = move_rate_ms

        angle = math.atan2(y_end - y_init, x_end - x_init)
        print("El angulo en grados es:", int(angle * 180 / math.pi))

        self.move_x = math.cos(angle) * speed
        self.move_y = math.sin(angle) * speed

        self.is_active = True

        self.owner = owner  # Propietario de la bala (puede ser el jugador o un enemigo)
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x_init
        self.rect.y = y_init

        # Atributos adicionales de la bala%%%%%***********++
        self.x_end = x_end
        self.y_end = y_end
        self.speed = speed

        self.width = width
        self.height = height

        # **********************

    def change_x(self, delta_x):
        self.x = self.x + delta_x
        self.rect.x = int(self.x)

    def change_y(self, delta_y):
        self.y = self.y + delta_y
        self.rect.y = int(self.y)

    def is_on_platform(self, plataform_list):
        for platform in plataform_list:
            if self.rect.colliderect(platform.rect):
                return True
        return False

    def do_movement(self, delta_ms, plataform_list, enemy_group, player_1):
        self.tiempo_transcurrido_move += delta_ms
        if self.tiempo_transcurrido_move >= self.move_rate_ms:
            self.tiempo_transcurrido_move = 0
            self.change_x(self.move_x)
            self.change_y(self.move_y)
            self.check_impact(enemy_group, player_1)

    def do_animation(self, delta_ms):
        self.tiempo_transcurrido_animation += delta_ms
        if self.tiempo_transcurrido_animation >= self.frame_rate_ms:
            self.tiempo_transcurrido_animation = 0
            pass

    def check_impact(self, enemy_group, player_1):
        if self.is_active:
            # Lógica de colisión con enemigos
            for enemy_element in enemy_group:
                if isinstance(enemy_element, Enemy) and self.rect.colliderect(
                    enemy_element.rect
                ):
                    print("Impacto bullet para enemigo detectado ")
                    self.is_active = False
                    enemy_element.receive_shoot(self.rect)
                    if impact_sound:
                        impact_sound.play()

            # Lógica de colisión con jugador
            if self.rect.colliderect(player_1.rect):
                print("Impacto bullet para jugador detectado ")
                self.is_active = False
                player_1.receive_shoot(self.rect)

                # Contador de disparos en el jugador
                player_1.shots_fired += 1
                if player_1.shots_fired >= 3:
                    # Duplicar enemigos
                    enemy1 = Enemy(
                        x=450,
                        y=400,
                        speed_walk=6,
                        speed_run=5,
                        gravity=14,
                        jump_power=30,
                        frame_rate_ms=150,
                        move_rate_ms=50,
                        jump_height=140,
                        p_scale=0.08,
                        interval_time_jump=300,
                    )
                    enemy2 = Enemy(
                        x=900,
                        y=400,
                        speed_walk=6,
                        speed_run=5,
                        gravity=14,
                        jump_power=30,
                        frame_rate_ms=150,
                        move_rate_ms=50,
                        jump_height=140,
                        p_scale=0.08,
                        interval_time_jump=300,
                        enemy_group=enemy_group,
                    )
                    enemy_group.add(enemy1, enemy2)
                    player_1.shots_fired = 0

    def update(self, delta_ms, plataform_list, enemy_group, player_1):
        self.do_movement(delta_ms, plataform_list, enemy_group, player_1)

    def draw(self, screen):
        if self.is_active:
            if DEBUG:
                pygame.draw.rect(screen, color=(255, 0, 0), rect=self.collition_rect)
            screen.blit(self.image, self.rect)
