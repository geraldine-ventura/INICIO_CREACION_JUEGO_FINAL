import pygame
from enemigo import Enemy
from constantes import *
from auxiliar import Auxiliar

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
        direction,
        width=5,
        height=5,
    ) -> None:
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

    def shoot(self):
        # Este método parece estar creando una nueva bala, pero ya estás en una instancia de Bullet.
        # Considera si realmente necesitas crear otra bala aquí o si puedes usar la instancia actual.
        pass

    # En la clase Bullet
    def check_impact(self, enemy_group, player_1, bullet_group):
        if self.is_active:
            if hasattr(enemy_group, "__iter__"):
                for enemy_element in enemy_group:
                    if isinstance(enemy_element, Enemy) and self.rect.colliderect(
                        enemy_element.rect
                    ):
                        print("Impacto bullet para enemigo detectado ")
                        self.is_active = False
                        enemy_element.receive_shoot(bullet_group, self.rect)
                        if impact_sound:
                            impact_sound.play()
            else:
                print("Error: enemy_group no es iterable")

            if self.rect.colliderect(player_1.rect):
                print("Impacto bullet para jugador detectado ")
                self.is_active = False
                player_1.receive_shoot(player_1.direction, player_1.rect)

    def update(self, delta_ms, plataform_list, enemy_group, player_1):
        self.do_movement(delta_ms, plataform_list, enemy_group, player_1)

    def draw(self, screen):
        if self.is_active:
            if DEBUG:
                pygame.draw.rect(screen, color=(255, 0, 0), rect=self.rect)
            screen.blit(self.image, self.rect)
