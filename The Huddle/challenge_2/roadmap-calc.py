class CreadorDeMapa():
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.mapa = [[None for _ in range(columnas)] for _ in range(filas)]


class Entidades:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna


if __name__=="__main__":
    creador_mapa = CreadorDeMapa(5, 5)
    print(creador_mapa.mapa)