import pygame
from constantes import *
from player import Player
from enemigo import Enemy
from plataforma import Plataform
from background import Background
from bullet import Bullet


class FormGameLevel1:
    def __init__(self, w, h):
        # Inicializa el atributo surface
        self.surface = pygame.Surface((w, h))
        # --- GAME ELEMENTS ---
        self.static_background = Background(
            x=0,
            y=0,
            width=w,
            height=h,
            path="JUEGO_FINAL1/images/back/depositphotos_56565763-stock-illustration-seamless-background-fabulous-night-forest (1).jpg",
        )

        self.player_1 = Player(
            x=0,
            y=400,
            speed_walk=6,
            speed_run=12,
            gravity=14,
            jump_power=30,
            frame_rate_ms=100,
            move_rate_ms=50,
            jump_height=140,
            p_scale=0.2,
            interval_time_jump=300,
        )
        # lo defino como un atributo de la instancia (self.player_rect), en lugar de una variable local.
        self.player_ground_collition_rect = self.player_1.ground_collition_rect

        self.enemy_list = []
        self.enemy_list.append(
            Enemy(
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
        )
        self.enemy_list.append(
            Enemy(
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
            )
        )

        self.plataform_list = []
        self.plataform_list.append(Plataform(x=400, y=500, width=50, height=50, type=0))
        self.plataform_list.append(Plataform(x=450, y=500, width=50, height=50, type=1))
        self.plataform_list.append(Plataform(x=500, y=500, width=50, height=50, type=2))
        self.plataform_list.append(
            Plataform(x=600, y=430, width=50, height=50, type=12)
        )
        self.plataform_list.append(
            Plataform(x=650, y=430, width=50, height=50, type=14)
        )
        self.plataform_list.append(
            Plataform(x=750, y=360, width=50, height=50, type=12)
        )
        self.plataform_list.append(
            Plataform(x=800, y=360, width=50, height=50, type=13)
        )
        self.plataform_list.append(
            Plataform(x=850, y=360, width=50, height=50, type=13)
        )
        self.plataform_list.append(
            Plataform(x=900, y=360, width=50, height=50, type=14)
        )

    class FormGameLevel1:
        # ... (otras definiciones de la clase)

        def game_over(self):
            if self.player_1.lives <= 0:
                print("Game Over")
                # Cambiar la imagen del jugador a "dead"
                self.player_1.animation = self.player_1.player_dead_r
                self.player_1.reset_animation()  # Asegúrate de restablecer la animación después de cambiarla
                # Puedes realizar acciones adicionales aquí, como reiniciar el nivel o mostrar un mensaje de game over.

        def update(self, lista_eventos, keys, delta_ms):
            # Actualizar enemigos
            for enemy_element in self.enemy_list:
                enemy_element.update(
                    delta_ms, self.plataform_list, self.enemy_list, self.player_1
                )
                self.player_1.update(
                    delta_ms,
                    self.plataform_list,
                    enemy_shoot_rect=enemy_element.get_shoot_rect(),
                )

            # Verificar impacto con balas del jugador
            bullets_to_remove = []
            for bullet in self.player_1.bullet_list:
                for enemy_element in self.enemy_list:
                    if bullet.check_impact(enemy_element, self.player_1):
                        # Marcar la bala para eliminarla después de salir del bucle
                        bullets_to_remove.append(bullet)
                        # Resto del código para manejar el impacto

            # Eliminar balas marcadas para su eliminación
            for bullet in bullets_to_remove:
                self.player_1.bullet_list.remove(bullet)

            # Actualizar balas del jugador
            for bullet in self.player_1.bullet_list:
                bullet.update(
                    delta_ms, self.plataform_list, self.enemy_list, self.player_1
                )

            # Actualizar jugador
            self.player_1.events(delta_ms, keys)
            self.player_1.update(delta_ms, self.enemy_list, self.player_1)

            # Llamar a la función game_over si las vidas llegan a cero
            self.game_over()
