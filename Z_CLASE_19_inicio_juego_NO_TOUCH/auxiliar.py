import pygame as pg


class SurfaceManager:
    @staticmethod
    def getSurfaceFromSpriteSheet(path, columnas, filas, flip=False, step=1):
        lista = []
        surface_imagen = pg.image.load(path)
        fotograma_ancho = int(surface_imagen.get_width() / columnas)
        fotograma_alto = int(surface_imagen.get_height() / filas)
        x = 0
        for columna in range(0, columnas, step):
            for fila in range(filas):
                x = columna * fotograma_ancho
                y = fila * fotograma_alto
                surface_fotograma = surface_imagen.subsurface(
                    x, y, fotograma_ancho, fotograma_alto
                )
                if flip:
                    surface_fotograma = pg.transform.flip(
                        surface_fotograma, True, False
                    )
                lista.append(surface_fotograma)
        return lista
