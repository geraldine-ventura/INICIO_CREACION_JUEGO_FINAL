import pygame as pg


# Define una clase llamada SurfaceManager. Esta clase se utiliza para gestionar
# superficies (imágenes) en el juego.


class SurfaceManager:
    # Define un método estático llamado get_surface_from_spritesheet
    @staticmethod
    def get_surface_from_spritesheet(
        img_path: str, cols: int, rows: int, step=1, flip: bool = False
    ) -> list[pg.surface.Surface]:
        # Crea una lista vacía llamada sprites_list que se llenará con las superficies de los sprites.
        sprites_list = list()

        # Luego, carga la imagen desde la ruta especificada en img_path utilizando pg.image.load y
        # la almacena en la variable surface_img.
        surface_img = pg.image.load(img_path)
        frame_width = int(surface_img.get_width() / cols)
        frame_height = int(surface_img.get_height() / rows)

        # Inicia dos bucles anidados para iterar sobre las filas y columnas de la hoja de sprites.
        # El bucle interior utiliza step para avanzar a través de las columnas.
        for row in range(rows):
            for column in range(0, cols, step):
                # Calcula las coordenadas (x, y) de la esquina superior izquierda de cada sprite en la hoja de sprites.
                x_axis = column * frame_width
                y_axis = row * frame_height

                # Crea una subsuperficie (sprite individual) utilizando pg.surface.subsurface con las coordenadas
                # calculadas y las dimensiones de cada sprite.
                frame_surface = surface_img.subsurface(
                    x_axis, y_axis, frame_width, frame_height
                )

                # Si el parámetro flip es True, voltea horizontalmente la subsuperficie utilizando pg.transform.flip.
                if flip:
                    frame_surface = pg.transform.flip(frame_surface, True, False)

                # Añade la subsuperficie a la lista sprites_list.
                sprites_list.append(frame_surface)
        return sprites_list
