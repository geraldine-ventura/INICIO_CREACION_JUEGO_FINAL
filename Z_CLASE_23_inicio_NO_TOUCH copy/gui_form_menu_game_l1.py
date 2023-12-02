import pygame
from pygame.locals import *
from constantes import *
from gui_form import Form
from gui_button import Button
from gui_textbox import TextBox
from gui_progressbar import ProgressBar

from player import Player
from enemigo import Enemy
from plataforma import Plataform
from background import Background
from bullet import Bullet
from botin import *
from sound import *


class FormGameLevel1(Form):
    def __init__(
        self,
        name,
        master_surface,
        x,
        y,
        w,
        h,
        color_background,
        color_border,
        active,
        enemy_group,
    ):
        super().__init__(
            name,
            master_surface,
            x,
            y,
            w,
            h,
            color_background,
            color_border,
            active,
        )
        self.enemy_group = enemy_group

        # Resto de tu código...

        self.player_1 = Player(
            x=0,
            y=0,
            # width=40,
            # height=40,
            speed_walk=20,
            speed_run=20,
            gravity=20,
            jump_power=20,
            frame_rate_ms=10,
            move_rate_ms=1000,
            jump_height=10,
            # p_scale: int = 1,
            # interval_time_jump: int = 100
            p_scale=1,
            interval_time_jump=100,
        )

        # player_1 ver para corregir

        self.boton1 = Button(
            master=self,
            x=0,
            y=0,
            w=140,
            h=50,
            color_background=None,
            color_border=None,
            image_background="Z_CLASE_23_inicio_NO_TOUCH/images/gui/set_gui_01/Comic_Border/Buttons/Button_L_02.png",
            on_click=self.on_click_boton1,
            on_click_param="form_menu_B",
            text="BACK",
            font="Verdana",
            font_size=30,
            font_color=C_WHITE,
        )
        self.boton2 = Button(
            master=self,
            x=200,
            y=0,
            w=140,
            h=50,
            color_background=None,
            color_border=None,
            image_background="Z_CLASE_23_inicio_NO_TOUCH/images/gui/set_gui_01/Comic_Border/Buttons/Button_M_02.png",
            on_click=self.on_click_boton1,
            on_click_param="form_menu_B",
            text="PAUSE",
            font="Verdana",
            font_size=30,
            font_color=C_WHITE,
        )
        self.boton_shoot = Button(
            master=self,
            x=400,
            y=0,
            w=140,
            h=50,
            color_background=None,
            color_border=None,
            image_background="Z_CLASE_23_inicio_NO_TOUCH/images/gui/set_gui_01/Comic_Border/Buttons/Button_M_02.png",
            on_click=self.on_click_shoot,  # boton disparar enemys
            on_click_param="form_menu_B",
            text="SHOOT",
            font="Verdana",
            font_size=30,
            font_color=C_WHITE,
        )

        self.pb_lives = ProgressBar(
            master=self,
            x=500,
            y=50,
            w=240,
            h=50,
            color_background=None,
            color_border=None,
            image_background="Z_CLASE_23_inicio_NO_TOUCH/images/gui/set_gui_01/Comic_Border/Bars/Bar_Background01.png",
            image_progress="Z_CLASE_23_inicio_NO_TOUCH/images/gui/set_gui_01/Comic_Border/Bars/Bar_Segment05.png",
            value=5,
            value_max=5,
        )

        self.widget_list = [self.boton1, self.boton2, self.boton_shoot, self.pb_lives]
        self.render()
        # --- GAME ELEMENTS ---
        self.static_background = Background(
            x=0,
            y=0,
            width=w,
            height=h,  # ver
            path="Z_CLASE_23_inicio_NO_TOUCH/images/back/depositphotos_56565763-stock-illustration-seamless-background-fabulous-night-forest (1).jpg",
        )

        self.player_1 = Player(
            x=0,
            y=400,
            speed_walk=8,
            speed_run=20,
            gravity=14,
            jump_power=30,
            frame_rate_ms=150,
            move_rate_ms=250,
            jump_height=140,
            p_scale=0.2,
            interval_time_jump=300,
        )

        # lo defino como un atributo de la instancia (self.player_rect), en lugar de una variable local.
        self.player_ground_collition_rect = self.player_1.ground_collition_rect

        ##------------------------------------------------------ # Crear el grupo de enemigos----------------------

        self.enemy_group = pygame.sprite.Group()

        # Crear instancias de enemigos y agregarlas al grupo
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
            enemy_group=self.enemy_group,
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
            enemy_group=self.enemy_group,
        )

        self.enemy_group.add(enemy1, enemy2)

        # *gregar mas plataformas a JUEGO_GAME_FINAL1
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

    def on_click_boton1(self, parametro):
        self.set_active(parametro)

    def on_click_shoot(self, parametro):
        for enemy_element in self.enemy_group:
            bullet = Bullet(
                enemy_element,
                enemy_element.rect.centerx,
                enemy_element.rect.centery,
                self.player_1.rect.centerx,
                self.player_1.rect.centery,
                10,
                path="Z_CLASE_23_inicio_NO_TOUCH/images/gui/set_gui_01/Comic_Border/Bars/Bar_Segment05.png",
                frame_rate_ms=80,
                move_rate_ms=50,
                width=6,
                height=6,
                direction="left",
            )
            """ self.bullet_group.add(bullet)  #!! """

    def render(self):  # extra para buscar soluci de self.widget_list
        if self.color_background is not None:
            self.surface.fill(self.color_background)

    def update(self, lista_eventos, keys, delta_ms):
        for aux_widget in self.widget_list:
            aux_widget.update(lista_eventos)

        """ for bullet in self.player_instance.bullet_list:
            bullet.update(delta_ms, self.plataform_list, self.enemy_group) """

        """ # Eliminar balas que estén fuera de la pantalla o hayan colisionado
        self.bullet_list = [
            bullet for bullet in self.bullet_list if bullet.is_alive()
        ] """

        for enemy_element in self.enemy_group:
            enemy_element.update(delta_ms, self.plataform_list)

        self.player_1.events(delta_ms, keys)
        self.player_1.update(delta_ms, self.plataform_list)

        self.pb_lives.value = self.player_1.lives

    def draw(self):
        super().draw()
        self.static_background.draw(self.surface)

        for aux_widget in self.widget_list:
            aux_widget.draw()

        for plataforma in self.plataform_list:
            plataforma.draw(self.surface)

        frutas_group.draw(self.surface)

        for enemy_element in self.enemy_group:
            enemy_element.draw(self.surface)

        self.player_1.draw(self.surface)

        """ for bullet in self.bullet_list:
            bullet.draw(self.surface) """


# Detener sonidos al salir del juego
stop_sounds()
