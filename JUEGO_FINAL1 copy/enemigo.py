import pygame
from constantes import *
from auxiliar import Auxiliar
from knife import *


class Enemy:
    def __init__(
        self,
        x,
        y,
        speed_walk,
        speed_run,
        gravity,
        jump_power,
        frame_rate_ms,
        move_rate_ms,
        jump_height,
        p_scale=1,
        interval_time_jump=100,
    ) -> None:
        self.walk_r = Auxiliar.getSurfaceFromSeparateFiles(
            "JUEGO_FINAL1/images/caracters/enemies/ork_sword/WALK/WALK_00{0}.png",
            0,
            7,
            scale=p_scale,
        )
        self.walk_l = Auxiliar.getSurfaceFromSeparateFiles(
            "JUEGO_FINAL1/images/caracters/enemies/ork_sword/WALK/WALK_00{0}.png",
            0,
            7,
            flip=True,
            scale=p_scale,
        )
        self.stay_r = Auxiliar.getSurfaceFromSeparateFiles(
            "JUEGO_FINAL1/images/caracters/enemies/ork_sword/IDLE/IDLE_00{0}.png",
            0,
            7,
            scale=p_scale,
        )
        self.stay_l = Auxiliar.getSurfaceFromSeparateFiles(
            "JUEGO_FINAL1/images/caracters/enemies/ork_sword/IDLE/IDLE_00{0}.png",
            0,
            7,
            flip=True,
            scale=p_scale,
        )

        ##-----------dead-enemy-path---------->
        self.enemy_dead_r = Auxiliar.getSurfaceFromSeparateFiles(
            "JUEGO_FINAL1/images/caracters/enemies/ork_sword/DIE/DIE_00{0}.png",
            0,
            6,
            flip=False,
            scale=p_scale,
        )
        self.enemy_dead_l = Auxiliar.getSurfaceFromSeparateFiles(
            "JUEGO_FINAL1/images/caracters/enemies/ork_sword/DIE/DIE_00{0}.png",
            0,
            6,
            flip=True,
            scale=p_scale,
        )

        ##---------enemy_knife_path----------->

        self.enemy_knife_r = Auxiliar.getSurfaceFromSeparateFiles(
            "JUEGO_FINAL1 copy/images/caracters/enemies/ork_sword/ATTAK/ATTAK_00{0}.png",
            1,
            6,
            flip=False,
            scale=p_scale,
            repeat_frame=1,
        )
        self.enemy_knife_l = Auxiliar.getSurfaceFromSeparateFiles(
            "JUEGO_FINAL1 copy/images/caracters/enemies/ork_sword/ATTAK/ATTAK_00{0}.png",
            1,
            6,
            flip=True,
            scale=p_scale,
            repeat_frame=1,
        )

        self.contador = 0
        self.frame = 0
        self.lives = 5
        self.score = 0
        self.move_x = 0
        self.move_y = 0
        self.speed_walk = speed_walk
        self.speed_run = speed_run
        self.gravity = gravity
        self.jump_power = jump_power
        self.animation = self.stay_r
        self.direction = DIRECTION_R
        self.image = self.animation[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collition_rect = pygame.Rect(
            x + self.rect.width / 3, y, self.rect.width / 3, self.rect.height
        )
        self.ground_collition_rect = pygame.Rect(self.collition_rect)
        self.ground_collition_rect.height = GROUND_COLLIDE_H
        self.ground_collition_rect.y = y + self.rect.height - GROUND_COLLIDE_H

        self.is_jump = False
        self.is_fall = False
        self.is_knife = False
        # Añadido para gestionar la animación de muerte
        self.is_dead = False

        self.tiempo_transcurrido_animation = 0
        self.frame_rate_ms = frame_rate_ms
        self.tiempo_transcurrido_move = 0
        self.move_rate_ms = move_rate_ms
        self.y_start_jump = 0
        self.jump_height = jump_height

        # receive_shoot(Enemy):------------------>
        self.tiempo_transcurrido = 0
        self.tiempo_last_jump = 0  # en base al tiempo transcurrido general
        self.interval_time_jump = interval_time_jump
        ####################>>>>>>>>>

        self.tiempo_transcurrido_ultimo_ataque = 0
        self.intervalo_ataque = (
            3000  # Intervalo de tiempo entre ataques de cuchillo en milisegundos
        )
        # ... va algo para self.is.active !!!!!!!!!!!!

        self.is_active = (
            True  # Agregar el atributo is_active y configurarlo según tus necesidades
        )

        self.knife_list = []

    def get_shoot_rect(self):
        # Devuelve el rectángulo de colisión del enemigo para detectar disparos
        return self.collition_rect

    def slash(self, on_off=True):
        if on_off and not self.is_dead:
            knife_enemy = Knife(
                owner=self,
                x_init=self.rect.right,
                y_init=self.rect.center[1],
                x_end=ANCHO_VENTANA,
                y_end=self.rect.y,
                speed=40,
                frame_rate_ms=100,
                move_rate_ms=100,
                width=5,
                height=5,
            )
            self.knife_list.append(knife_enemy)

    ####
    def receive_knife(self):
        self.lives -= 1
        # Verifica la colisión con el jugador solo si el enemigo está activo

    # receive_shoot(Enemy):------------------>
    def receive_shoot(self, direction, enemy_shoot_rect):
        if self.ground_collition_rect.colliderect(enemy_shoot_rect):
            print("Colision con enemigo detectada!Cambia de animacion dead")
            if direction == DIRECTION_R:
                self.animation = self.enemy_dead_r
            else:
                self.animation = self.enemy_dead_l

        self.lives -= 1
        print(self.lives)
        self.do_animation  # Restablece la animación después de cambiarla

    def change_x(self, delta_x):
        self.rect.x += delta_x
        self.collition_rect.x += delta_x
        self.ground_collition_rect.x += delta_x

    def change_y(self, delta_y):
        self.rect.y += delta_y
        self.collition_rect.y += delta_y
        self.ground_collition_rect.y += delta_y

    def do_movement(self, delta_ms, plataform_list):
        self.tiempo_transcurrido_move += delta_ms
        if self.tiempo_transcurrido_move >= self.move_rate_ms:
            self.tiempo_transcurrido_move = 0

            if not self.is_on_plataform(plataform_list):
                if self.move_y == 0:
                    self.is_fall = True
                    self.change_y(self.gravity)
            else:
                self.is_fall = False
                self.change_x(self.move_x)
                if self.contador <= 50:
                    self.move_x = -self.speed_walk
                    self.animation = self.walk_l
                    self.contador += 1
                elif self.contador <= 100:
                    self.move_x = self.speed_walk
                    self.animation = self.walk_r
                    self.contador += 1
                else:
                    self.contador = 0

    def is_on_plataform(self, plataform_list):
        retorno = False

        if self.ground_collition_rect.bottom >= GROUND_LEVEL:
            retorno = True
        else:
            for plataforma in plataform_list:
                if self.ground_collition_rect.colliderect(
                    plataforma.ground_collition_rect
                ):
                    retorno = True
                    break
        return retorno

    def do_animation(self, delta_ms):
        self.tiempo_transcurrido_animation += delta_ms
        if self.tiempo_transcurrido_animation >= self.frame_rate_ms:
            self.tiempo_transcurrido_animation = 0
            if self.frame < len(self.animation) - 1:
                self.frame += 1

            else:
                self.frame = 0

        """ if not self.is_dead:
            for knife_element in self.knife_list:
                knife_element.update(delta_ms, plataform_list, enemy_list, player_1) """

    def update(self, delta_ms, plataform_list, enemy_list, player_1):
        # Lógica de actualización de enemigo, incluyendo el manejo de cuchillos
        for knife_element in self.knife_list:
            knife_element.update(delta_ms, plataform_list, enemy_list, player_1)

        self.do_movement(delta_ms, plataform_list)
        self.do_animation(delta_ms)
        self.tiempo_transcurrido_ultimo_ataque += delta_ms

        if self.tiempo_transcurrido_ultimo_ataque >= self.intervalo_ataque:
            self.tiempo_transcurrido_ultimo_ataque = 0
            self.slash()

    def draw(self, screen):
        if not self.is_dead:
            for knife_element in self.knife_list:
                knife_element.draw(screen)

            self.image = self.animation[self.frame]
            screen.blit(self.image, self.rect)

    def events(self, delta_ms, player_1):
        self.tiempo_transcurrido += delta_ms

        # Lógica para realizar un ataque con cuchillo automáticamente cada intervalo de tiempo
        if self.tiempo_transcurrido >= self.intervalo_ataque:
            self.tiempo_transcurrido = 0
            self.slash()

        """ self.reset_animation()  # Resetea la animación después de realizar el ataque con cuchillo """
