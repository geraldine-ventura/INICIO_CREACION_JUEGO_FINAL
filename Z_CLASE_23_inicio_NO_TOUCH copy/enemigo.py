# from player import
import pygame
from constantes import *
from auxiliar import Auxiliar
from bullet import *
from plataforma import *  ############exttra
import time


class Enemy(pygame.sprite.Sprite):
    # CLASE_23_inicio_juego/images/caracters/enemies/ork_sword/WALK/WALK_000.png
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
        enemy_group,
        p_scale=1,
        interval_time_jump=100,
    ) -> None:
        # Llame al inicializador de la clase base
        super().__init__()
        self.walk_r = Auxiliar.getSurfaceFromSeparateFiles(
            "Z_CLASE_23_inicio_NO_TOUCH/images/caracters/enemies/ork_sword/WALK/WALK_00{0}.png",
            0,
            7,
            scale=p_scale,
        )
        self.walk_l = Auxiliar.getSurfaceFromSeparateFiles(
            "Z_CLASE_23_inicio_NO_TOUCH/images/caracters/enemies/ork_sword/WALK/WALK_00{0}.png",
            0,
            7,
            flip=True,
            scale=p_scale,
        )
        self.stay_r = Auxiliar.getSurfaceFromSeparateFiles(
            "Z_CLASE_23_inicio_NO_TOUCH/images/caracters/enemies/ork_sword/IDLE/IDLE_00{0}.png",
            0,
            7,
            scale=p_scale,
        )
        self.stay_l = Auxiliar.getSurfaceFromSeparateFiles(
            "Z_CLASE_23_inicio_NO_TOUCH/images/caracters/enemies/ork_sword/IDLE/IDLE_00{0}.png",
            0,
            7,
            flip=True,
            scale=p_scale,
        )
        ##-----------dead-enemy-path---------->
        self.enemy_dead_r = Auxiliar.getSurfaceFromSeparateFiles(
            "Z_CLASE_23_inicio_NO_TOUCH/images/caracters/enemies/ork_sword/DIE/DIE_00{0}.png",
            0,
            6,
            flip=False,
            scale=p_scale,
        )
        self.enemy_dead_l = Auxiliar.getSurfaceFromSeparateFiles(
            "Z_CLASE_23_inicio_NO_TOUCH/images/caracters/enemies/ork_sword/DIE/DIE_00{0}.png",
            0,
            6,
            flip=True,
            scale=p_scale,
        )

        ##---------enemy_shoot_path----------->

        self.enemy_shoot_r = Auxiliar.getSurfaceFromSeparateFiles(
            "Z_CLASE_23_inicio_NO_TOUCH/images/caracters/enemies/ork_sword/DIE/DIE_00{0}.png",
            1,
            3,
            flip=False,
            scale=p_scale,
            repeat_frame=2,
        )
        self.enemy_shoot_l = Auxiliar.getSurfaceFromSeparateFiles(
            "Z_CLASE_23_inicio_NO_TOUCH/images/caracters/enemies/ork_sword/DIE/DIE_00{0}.png",
            1,
            3,
            flip=True,
            scale=p_scale,
            repeat_frame=2,
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
        head_collition_width = self.rect.width / 2
        head_collition_height = self.rect.height / 3

        # nueva caja de colisión llamada head_collition_rect en la cabeza del enemigo.
        self.head_collition_rect = pygame.Rect(
            x + self.rect.width / 4, y, head_collition_width, head_collition_height
        )
        self.collition_rect = pygame.Rect(
            x + self.rect.width / 3, y, self.rect.width / 3, self.rect.height
        )
        self.ground_collition_rect = pygame.Rect(self.collition_rect)
        self.ground_collition_rect.height = GROUND_COLLIDE_H
        self.ground_collition_rect.y = y + self.rect.height - GROUND_COLLIDE_H

        self.is_jump = False
        self.is_fall = False
        self.is_shoot = False
        self.is_knife = False
        self.is_dead = False

        self.tiempo_transcurrido_animation = 0
        self.frame_rate_ms = frame_rate_ms
        self.tiempo_transcurrido_move = 0
        self.move_rate_ms = move_rate_ms
        self.y_start_jump = 0
        self.jump_height = jump_height

        self.tiempo_transcurrido = 0
        self.tiempo_last_jump = 0  # en base al tiempo transcurrido general
        self.interval_time_jump = interval_time_jump
        ###################################
        self.knife_count = 0  # Variable para contar las acuchilladas
        # ... resto de las inicializaciones
        self.enemy_group = enemy_group  # Guarda el grupo como un atributo

    def receive_knife_damage(self):
        self.lives -= 1
        self.knife_count += 1

        if self.lives <= 0:
            enemies_hit = pygame.sprite.spritecollide(self, self.enemy_group, False)
            for enemy in enemies_hit:
                enemy.kill()  # Elimina el enemigo del grupo
                self.spawn_new_enemies()  # Crea nuevos enemigos

        elif self.knife_count >= 3:
            self.receive_shoot()

        # Espera 3 segundos antes de desaparecer
        time.sleep(3)
        self.is_alive = False

    def spawn_new_enemies(self):
        # Lógica para crear nuevos enemigos
        # Puedes ajustar esto según la necesidad de tu juego
        for _ in range(2):  # Crea dos nuevos enemigos
            new_enemy = Enemy(x=200, y=300, speed=10)
            self.enemy_group.add(new_enemy)

    def reset_animation(self):
        # Lógica para restablecer la animación del enemigo
        # Puedes adaptar esto según lo que necesites hacer
        self.frame = 0
        self.animation = self.stay_r  # Ajusta esto según la lógica de tu juego

    def change_x(self, delta_x):
        self.rect.x += delta_x
        self.collition_rect.x += delta_x
        self.ground_collition_rect.x += delta_x

        # Actualizar la posición de la caja de colisión en la cabeza
        self.head_collition_rect.x += delta_x

    def change_y(self, delta_y):
        self.rect.y += delta_y
        self.collition_rect.y += delta_y
        self.ground_collition_rect.y += delta_y

        # Actualizar la posición de la caja de colisión en la cabeza
        self.head_collition_rect.y += delta_y

    # erificará si el rectángulo de la cabeza del enemigo (head_collition_rect),
    # colisiona con el rectángulo del jugador durante un salto
    def check_jump_collision(self, player_rect):
        if self.head_collition_rect.colliderect(player_rect):
            print("¡Colisión con salto detectada! Cambio de animación a dead.")
            self.animation = (
                self.enemy_dead_r
                if self.direction == DIRECTION_R
                else self.enemy_dead_l
            )
            self.reset_animation()  # Restablezco la animación después de cambiarla

    # ...
    def receive_shoot(self, bullet_group):
        # Verifica la colisión con el grupo de balas del jugador
        hits = pygame.sprite.spritecollide(self, bullet_group, True)
        if hits:
            print("Colisión con enemigo detectada! Cambia de animación a dead.")
            # Colisión con disparo del jugador, cambiar animación a dead
            self.is_dead = True
            # Restablece la animación después de cambiarla
            self.reset_animation()
            # Realiza otras acciones necesarias en caso de colisión

    """ 
    # En la clase Enemy
    def receive_shoot(self, bullet_group, bullet_pos):
        # Verifica la colisión con el grupo de balas del jugador
        hits = pygame.sprite.spritecollide(self, bullet_group, True)
        if hits:
            print("Colisión con enemigo detectada! Cambia de animación a dead.")
            # Colisión con disparo del jugador, cambiar animación a dead
            self.is_dead = True
            # Restablece la animación después de cambiarla
            self.reset_animation()
            # Realiza otras acciones necesarias en caso de colisión """

    # lógica de cambio de dirección
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
                if self.contador <= 50:
                    self.move_x = -self.speed_walk
                    self.animation = self.walk_l
                elif 50 < self.contador <= 100:
                    self.move_x = self.speed_walk
                    self.animation = self.walk_r
                else:
                    self.contador = 0

                self.change_x(self.move_x)
                self.contador += 1

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

    # lógica para reiniciar el contador de frames cuando alcanza la longitud de la animación:
    def do_animation(self, delta_ms):
        self.tiempo_transcurrido_animation += delta_ms
        if self.tiempo_transcurrido_animation >= self.frame_rate_ms:
            self.tiempo_transcurrido_animation = 0
            self.frame = (self.frame + 1) % len(self.animation)

    def update(self, delta_ms, plataform_list):
        self.do_movement(delta_ms, plataform_list)
        self.do_animation(delta_ms)

    def draw(self, screen):
        if DEBUG:
            pygame.draw.rect(screen, color=(255, 0, 0), rect=self.collition_rect)
            pygame.draw.rect(
                screen, color=(255, 255, 0), rect=self.ground_collition_rect
            )
            # Dibujar la caja de colisión en la cabeza
            pygame.draw.rect(screen, color=(0, 255, 0), rect=self.head_collition_rect)

        self.image = self.animation[self.frame]
        screen.blit(self.image, self.rect)
