import pygame


class Fruta(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path, p_scale):
        super().__init__()
        self.image = pygame.image.load(image_path)  # Cargar la imagen desde el archivo
        self.rect = self.image.get_rect(topleft=(x, y))
        self.p_scale = p_scale


""" m(x=400, y=500, width=50, height=50, type=0))
        self.plataform_list.append(Plataform(x=450, y=500, width=50, height=50, type=1))
        self.plataform_list.append(Plataform(x=500, y=500, width=50, height=50, type=2)) """

# Crear instancias de Fruta
fruta_1 = Fruta(
    420,
    400,
    10,
    10,
    "Z_CLASE_23_inicio_NO_TOUCH copy/images/food/apple/apple__x1_iconic_png_1354829396.png",
    0.1,
)
fruta_2 = Fruta(
    600,
    300,
    10,
    10,
    "Z_CLASE_23_inicio_NO_TOUCH copy/images/food/banana/banana__x1_iconic_png_1354829403.png",
    0.005,
)
fruta_3 = Fruta(
    800,
    200,
    10,
    10,
    "Z_CLASE_23_inicio_NO_TOUCH copy/images/food/carrot/carrot__x1_iconic_png_1354829739.png",
    0.08,
)

# Crear un grupo de frutas y agregar las instancias al grupo
frutas_group = pygame.sprite.Group(fruta_1, fruta_2, fruta_3)
