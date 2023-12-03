import pygame
import math

# from gui_form_menu_game_l1 import *


class Knife:
    def __init__(
        self,
        owner,
        x_init,
        y_init,
        x_end,
        y_end,
        speed,
        frame_rate_ms,
        move_rate_ms,
        width=5,
        height=5,
    ):
        self.owner = owner
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x_init
        self.rect.y = y_init
        self.frame_rate_ms = frame_rate_ms
        self.move_rate_ms = move_rate_ms

        self.shots_fired = 0  # Atributo para contar los disparos del jugador

        angle = math.atan2(y_end - y_init, x_end - x_init)
        self.move_x = math.cos(angle) * speed
        self.move_y = math.sin(angle) * speed

        self.is_active = True

    def change_x(self, delta_x):
        self.rect.x += delta_x

    def change_y(self, delta_y):
        self.rect.y += delta_y

    def do_movement(self, delta_ms, plataform_list, enemy_group, player_1):
        if self.is_active:
            self.change_x(self.move_x)
            self.change_y(self.move_y)

    def check_impact(self, enemy_group, player_1):
        if self.is_active:
            # Verifica la colisión con los enemigos
            for enemy_element in enemy_group:
                if self.owner != enemy_element and self.rect.colliderect(
                    enemy_element.rect
                ):
                    print("slash de enemy detectado ")
                    # Realiza las acciones correspondientes al impacto con el enemigo

            # Verifica la colisión con el jugador
            if self.owner != player_1 and self.rect.colliderect(player_1.rect):
                print("slash de jugador detectado ")
                # Realiza las acciones correspondientes al impacto con el jugador
                # Verifica la colisión con el jugador solo si el enemigo está activo
                if self != player_1 and self.rect.colliderect(player_1.rect):
                    print("SLASH IMPACTO CON JUGADOR (clase knife)")
                    self.is_active = False
                    # Proporciona la dirección y el rectángulo del jugador al recibir el impacto
                    player_1.receive_shoot(self.move_x, player_1.rect)

    def update(self, delta_ms, plataform_list, enemy_group, player_1):
        self.do_movement(delta_ms, plataform_list, enemy_group, player_1)

    def draw(self, screen):
        if self.is_active:
            pygame.draw.rect(screen, color=(255, 0, 0), rect=self.rect)
            # Puedo ajustar esto según cómo quiera dibujar la cuchilla en pantalla
