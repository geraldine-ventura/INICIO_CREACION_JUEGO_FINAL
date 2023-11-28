import pygame

from bullet import Bullet
from constantes import *
from auxiliar import Auxiliar


class Player:
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
        self.stay_r = Auxiliar.getSurfaceFromSeparateFiles(
            "Z_CLASE_23_inicio_NO_TOUCH/images/caracters/players/cowgirl/Idle ({0}).png",
            1,
            10,
            flip=False,
            scale=p_scale,
        )
        self.stay_l = Auxiliar.getSurfaceFromSeparateFiles(
            "Z_CLASE_23_inicio_NO_TOUCH/images/caracters/players/cowgirl/Idle ({0}).png",
            1,
            10,
            flip=True,
            scale=p_scale,
        )
        self.jump_r = Auxiliar.getSurfaceFromSeparateFiles(
            "Z_CLASE_23_inicio_NO_TOUCH/images/caracters/players/cowgirl/Jump ({0}).png",
            1,
            10,
            flip=False,
            scale=p_scale,
        )
        self.jump_l = Auxiliar.getSurfaceFromSeparateFiles(
            "Z_CLASE_23_inicio_NO_TOUCH/images/caracters/players/cowgirl/Jump ({0}).png",
            1,
            10,
            flip=True,
            scale=p_scale,
        )
        self.walk_r = Auxiliar.getSurfaceFromSeparateFiles(
            "Z_CLASE_23_inicio_NO_TOUCH/images/caracters/players/cowgirl/Run ({0}).png",
            1,
            8,
            flip=False,
            scale=p_scale,
        )
        self.walk_l = Auxiliar.getSurfaceFromSeparateFiles(
            "Z_CLASE_23_inicio_NO_TOUCH/images/caracters/players/cowgirl/Run ({0}).png",
            1,
            8,
            flip=True,
            scale=p_scale,
        )

        ##-----------run-path---------->
        self.run_r = Auxiliar.getSurfaceFromSeparateFiles(
            "Z_CLASE_23_inicio_NO_TOUCH/images/caracters/players/cowgirl/Slide ({0}).png",
            1,
            5,
            flip=False,
            scale=p_scale,
        )
        self.run_l = Auxiliar.getSurfaceFromSeparateFiles(
            "Z_CLASE_23_inicio_NO_TOUCH/images/caracters/players/cowgirl/Slide ({0}).png",
            1,
            5,
            flip=True,
            scale=p_scale,
        )

        ##-----------dead-player-path---------->
        self.player_dead_r = Auxiliar.getSurfaceFromSeparateFiles(
            "Z_CLASE_23_inicio_NO_TOUCH/images/caracters/players/cowgirl/Dead ({0}).png",
            1,
            10,
            flip=False,
            scale=p_scale,
        )
        self.player_dead_l = Auxiliar.getSurfaceFromSeparateFiles(
            "Z_CLASE_23_inicio_NO_TOUCH/images/caracters/players/cowgirl/Dead ({0}).png",
            1,
            10,
            flip=True,
            scale=p_scale,
        )

        ##---------player_shoot_path----------->

        self.player_shoot_r = Auxiliar.getSurfaceFromSeparateFiles(
            "Z_CLASE_23_inicio_NO_TOUCH/images/caracters/players/cowgirl/Shoot ({0}).png",
            1,
            3,
            flip=False,
            scale=p_scale,
            repeat_frame=2,
        )
        self.player_shoot_l = Auxiliar.getSurfaceFromSeparateFiles(
            "Z_CLASE_23_inicio_NO_TOUCH/images/caracters/players/cowgirl/Shoot ({0}).png",
            1,
            3,
            flip=True,
            scale=p_scale,
            repeat_frame=2,
        )

        ##-----------knife-path---------->
        self.knife_r = Auxiliar.getSurfaceFromSeparateFiles(
            "Z_CLASE_23_inicio_NO_TOUCH/images/caracters/players/cowgirl/Melee ({0}).png",
            1,
            7,
            flip=False,
            scale=p_scale,
            repeat_frame=1,
        )
        self.knife_l = Auxiliar.getSurfaceFromSeparateFiles(
            "Z_CLASE_23_inicio_NO_TOUCH/images/caracters/players/cowgirl/Melee ({0}).png",
            1,
            7,
            flip=True,
            scale=p_scale,
            repeat_frame=1,
        )

        # Inicializa las propiedades del jugador, como su posición (__move_x y __move_y)
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
        self.bullet_list = []  # puedo crearlo en otro lado esta lista mas genrico

        self.enemy_list = []
        ###----------------COALISIONES---------->>>>>>>>>>>>>>>>>>>>>
        # está definiendo un rectángulo de colisión que es más estrecho que el rectángulo original
        # y está desplazado hacia la derecha en un tercio del ancho del rectángulo original.
        self.collition_rect = pygame.Rect(
            x + self.rect.width / 3, y, self.rect.width / 3, self.rect.height
        )

        # estas líneas crean y configuran un rectángulo de colisión específicamente diseñado
        # para la detección de colisiones con el suelo
        self.ground_collition_rect = pygame.Rect(self.collition_rect)
        self.ground_collition_rect.height = GROUND_COLLIDE_H
        self.ground_collition_rect.y = y + self.rect.height - GROUND_COLLIDE_H
        ###-------------------------->>>>>>>>>>>>>>>>>>>>>

        self.is_jump = False
        self.is_fall = False
        self.is_run = False
        self.is_shoot = False
        self.is_knife = False

        self.tiempo_transcurrido_animation = 0
        self.frame_rate_ms = frame_rate_ms
        self.tiempo_transcurrido_move = 0
        self.move_rate_ms = move_rate_ms
        self.y_start_jump = 0
        self.jump_height = jump_height

        self.tiempo_transcurrido = 0
        self.tiempo_last_jump = 0  # en base al tiempo transcurrido general
        self.interval_time_jump = interval_time_jump

    ### CORREGIR COALICIONES ---------verr no funka------------------------>>>>>>>>>>>>>>>>>>>>>>>>>>

    def receive_shoot(self, direction, player_rect):
        from bullet import Bullet  # Importa solo cuando sea necesario

        print("player_rect:", player_rect)

        if self.ground_collition_rect.colliderect(player_rect):
            print("Colisión con enemigo detectada! Cambio de animación a dead.")
            if direction == DIRECTION_R:
                self.animation = self.player_dead_r
            else:
                self.animation = self.player_dead_l
            self.reset_animation()  # Restablezco la animación después de cambiarla

            self.lives -= 1
            print("Vidas restantes:", self.lives)

            if self.lives <= 0:
                print("Game Over")
                # dejo la logica para reiniciar el juego, mostrar un mensaje, etc.

    ### --------------------- !!------>------------------------------------>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    """     # ≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤nuevo # ≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤nuevo       

    def crate_bullet(self):
        if self.is_looking_ritght:
            direcion = self.rect.righ
            direcion_str = "right"
        else:
            direcion = self.rect.left
            direcion_str = "left"
            return kiBlast(
                direcion, self.rect.centery, direcion_str, True
            )  # explosion de ki

    def cooldown_ready_to_action(self) -> bool:
        curent_time = pygame.time.get_ticks()
        return curent_time - self.ki_blast_time >= self.ki_blast_cooldown  # enfriarse

    def recharge(self):
        if not self.ready_to_attack:
            if self.cooldown_redy_to_action():
                self.ready_to_atack = True

    def charge_ki(self, charge: bool):
        if charge:
            if not self.is_charging and charge:
                if (
                    self.actual_animation != self.charge_l
                    and self.actual_animation != self.charge_r
                ):
                    self.is_charging = True

                    if self.is_looking_rigth:
                        self.cambiar_animacion(self.charge_r)
                        self.sound_player("charge_ssj1", "play")
                    else:
                        self.cambiar_animacion(self.charge_l)
                        self.move_x = 0
                        self.move_y = 0

    def shoot_ki_blast(self):  # dispara laser
       if self.actual_animation != self._ki_blast_l and self.actual_animation != self.ki_blast_r:
        if self.is_looking_rigth:
            self.cambiar_animacion(self.shoot_ki_blast_r)
        else
            self.cambiar_animacion(self.shoot_ki_blast_l)

        if self.cooldown_redy_to_action():
            print("!aaaaaaa!!!")

        self.sound_player("ki_blast", "play")
        self.bullet_group.add(self.create_bullet())
        # self.ready_to_atack= False
        self.ki_blast_time = pygame.time.get_ticks

        if (
            self.actual_animation != self._ki_blast_l
            and self.actual_animation != self.ki_blast_r
        ):
            if self.is_looking_rigth:
                self.cambiar_animacion(self.shoot_ki_blast_r)
            else:
                self.cambiar_animacion(self.shoot_ki_blast_l)

    # ≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤nuevo # ≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤≤ """

    def walk(self, direction):
        if self.is_jump == False and self.is_fall == False:
            if self.direction != direction or (
                self.animation != self.walk_r and self.animation != self.walk_l
            ):
                self.frame = 0
                self.direction = direction
                if direction == DIRECTION_R:
                    self.move_x = self.speed_walk
                    self.animation = self.walk_r
                else:
                    self.move_x = -self.speed_walk
                    self.animation = self.walk_l

    ### corregir //se llama slice=run
    def run(self, direction):
        if self.is_jump == False and self.is_fall == False:
            if self.direction != direction or (
                self.animation != self.run_r and self.animation != self.run_l
            ):
                self.frame = 0
                self.direction = direction
                if direction == DIRECTION_R:
                    self.move_x = self.speed_walk
                    self.animation = self.run_r
                else:
                    self.move_x = -self.speed_walk
                    self.animation = self.run_l

    ####----------shoot/disparar------>>>>>>>>>>>>
    def shoot(self, on_off=True):
        self.is_shoot = on_off
        if on_off == True and self.is_jump == False and self.is_fall == False:
            bullet_1 = Bullet(
                owner=self,
                x_init=self.rect.right,
                y_init=self.rect.center[1],
                x_end=ANCHO_VENTANA,
                y_end=self.rect.y,
                speed=40,
                path="JUEGO_FINAL1/images/caracters/players/warrior_woman_01/1_IDLE_000.png",
                frame_rate_ms=100,
                move_rate_ms=100,
                width=5,
                height=5,
            )
            self.bullet_list.append(bullet_1)

            if (
                self.animation != self.player_shoot_r
                and self.animation != self.player_shoot_l
            ):
                self.frame = 0
                self.is_shoot = True
                if self.direction == DIRECTION_R:
                    self.animation = self.player_shoot_r
                else:
                    self.animation = self.player_shoot_l

    def reset_animation(self):
        # Restablece la animación a la posición inicial (stay)
        if self.direction == DIRECTION_R:
            self.animation = self.stay_r
        else:
            self.animation = self.stay_l
        self.frame = 0

    def receive_knife(self):
        self.lives -= 1
        # Puedes realizar acciones adicionales cuando el jugador recibe un ataque de cuchillo
        # self.reset_animation()

    ####----------knife/acuchillar------>>>>>>>>>>>>
    def knife(self, on_off=True):
        self.is_knife = on_off
        if on_off == True and self.is_jump == False and self.is_fall == False:
            if self.animation != self.knife_r and self.animation != self.knife_l:
                self.frame = 0
                if self.direction == DIRECTION_R:
                    self.animation = self.knife_r
                else:
                    self.animation = self.knife_l

    ####----------jump/saltar------>>>>>>>>>>>>
    def jump(self, on_off=True):
        if on_off and self.is_jump == False and self.is_fall == False:
            self.y_start_jump = self.rect.y
            if self.direction == DIRECTION_R:
                self.move_x = int(self.move_x / 2)
                self.move_y = -self.jump_power
                self.animation = self.jump_r
            else:
                self.move_x = int(self.move_x / 2)
                self.move_y = -self.jump_power
                self.animation = self.jump_l
            self.frame = 0
            self.is_jump = True
        if on_off == False:
            self.is_jump = False
            self.stay()

    ####----------stay/detener------>>>>>>>>>>>>
    def stay(self):
        if self.is_knife or self.is_shoot:
            return

        if self.animation != self.stay_r and self.animation != self.stay_l:
            if self.direction == DIRECTION_R:
                self.animation = self.stay_r
            else:
                self.animation = self.stay_l
            self.move_x = 0
            self.move_y = 0
            self.frame = 0

    ####----------others------>>>>>>>>>>>>>>>>>
    def change_x(self, delta_x):
        self.rect.x += delta_x
        # self.rect.x += int(self.move_x)

        self.collition_rect.x += delta_x
        self.ground_collition_rect.x += delta_x

    def change_y(self, delta_y):
        self.rect.y += delta_y
        self.collition_rect.y += delta_y
        self.ground_collition_rect.y += delta_y

    def do_movement(self, delta_ms, plataform_list, enemy_list):
        self.tiempo_transcurrido_move += delta_ms
        if self.tiempo_transcurrido_move >= self.move_rate_ms:
            self.tiempo_transcurrido_move = 0

            if abs(self.y_start_jump - self.rect.y) > self.jump_height and self.is_jump:
                self.move_y = 0

            self.change_x(self.move_x)
            self.change_y(self.move_y)

        if not self.is_on_plataform(plataform_list):
            if self.move_y == 0:
                self.is_fall = True
                self.change_y(self.gravity)

                # Itera sobre la lista de enemigos y llama al método check_jump_collision durante el salto
                for enemy in enemy_list:
                    enemy.check_jump_collision(self.collition_rect)
        else:
            if self.is_jump:
                self.jump(False)
            self.is_fall = False

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
                # print(self.frame)
            else:
                self.frame = 0

    def update(self, delta_ms, plataform_list, enemy_shoot_rect=None):
        self.do_movement(delta_ms, plataform_list, self.enemy_list)
        self.do_animation(delta_ms)

        if enemy_shoot_rect:
            self.check_collision(enemy_shoot_rect)

    def check_collision(self, enemy_shoot_rect):
        # Otras líneas de código...
        # Supongamos que tienes valores adecuados para direction y player_rect
        direction = "izquierda"  # Reemplaza esto con el valor correcto
        player_rect = pygame.Rect(0, 0, 10, 10)  # Reemplaza esto con el valor correcto
        self.receive_shoot(direction, player_rect)

        # Realiza la detección de colisiones aquí
        if self.ground_collition_rect.colliderect(enemy_shoot_rect):
            print("Colisión con disparo del enemigo")
            # Colisión detectada, llama al método dead
            self.direction = (
                DIRECTION_R  # Proporciona la dirección correcta según tu lógica
            )
            self.player_rect = (
                self.ground_collition_rect
            )  # Usa el rectángulo correcto del jugador
            self.receive_shoot(self.direction, self.rect)

    def draw(self, screen):
        if DEBUG:
            pygame.draw.rect(screen, color=(255, 0, 0), rect=self.collition_rect)
            pygame.draw.rect(
                screen, color=(255, 255, 0), rect=self.ground_collition_rect
            )

        self.image = self.animation[self.frame]
        screen.blit(self.image, self.rect)

    #######-----------------------EVENTS------------------------------------>>>>>>>>>>>>>>>>>>
    def events(self, delta_ms, keys):
        self.tiempo_transcurrido += delta_ms

        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.walk(DIRECTION_L)

        if not keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
            self.walk(DIRECTION_R)

        #######---------------------------run------------------->>>>>>>>>>>>>>>>>>
        if keys[pygame.K_RIGHT] and keys[pygame.K_LSHIFT] and not keys[pygame.K_LEFT]:
            self.run(DIRECTION_R)
        if keys[pygame.K_LEFT] and keys[pygame.K_LSHIFT] and not keys[pygame.K_RIGHT]:
            self.run(DIRECTION_L)

        #######---------------------------dead------------------->>>>>>>>>>>>>>>>>>
        # Detecta si se colisiono con una bala al jugador
        #  y llama al método dead con dirección "Right". ///ARREGLAR LA COALISION!!!!!

        #######---------------------------stay------------------->>>>>>>>>>>>>>>>>>
        if (
            not keys[pygame.K_LEFT]
            and not keys[pygame.K_RIGHT]
            and not keys[pygame.K_SPACE]
        ):
            self.stay()
        if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT] and not keys[pygame.K_SPACE]:
            self.stay()
        #######---------------------------jump------------------->>>>>>>>>>>>>>>>>>
        if keys[pygame.K_SPACE]:
            if (
                self.tiempo_transcurrido - self.tiempo_last_jump
            ) > self.interval_time_jump:  # es la cantidad mínima de tiempo que debe transcurrir entre saltos.
                self.jump(
                    True
                )  # verifica si ha pasado suficiente tiempo desde el último salto
                self.tiempo_last_jump = self.tiempo_transcurrido
        #######----------------------shoot/knife------------------------ ------>>>>>
        if not keys[pygame.K_a]:
            self.shoot(False)

        if not keys[pygame.K_a]:
            self.knife(False)
        #######---------------------------shoot------------------->>>>>>>>>>>>>>>>>>
        if keys[pygame.K_s] and not keys[pygame.K_a]:
            self.shoot()

            """ self.reset_animation()  # Resetea la animación después de disparar """

        #######---------------------------knife------------------->>>>>>>>>>>>>>>>>>
        if keys[pygame.K_a] and not keys[pygame.K_s]:
            self.knife()

            """ self.reset_animation()  # Resetea la animación después de realizar el ataque con cuchillo """