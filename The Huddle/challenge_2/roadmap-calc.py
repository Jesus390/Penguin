class Mapa():
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.mapa = [[None for _ in range(columnas)] for _ in range(filas)]


class Entidades:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
