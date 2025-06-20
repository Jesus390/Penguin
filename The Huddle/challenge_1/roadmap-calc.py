import random

def crear_mapa(filas, columnas):
    return [['🏠' for _ in range(columnas)] for _ in range(filas)]
    
def print_mapa(mapa):
    cantidad_borde = int(len(mapa[0]))
    print(f"+{'='*((cantidad_borde*3))}+")
    for row in mapa:
        print(f"|{' '.join(row)} |")
    print(f"+{'='*((cantidad_borde*3))}+")

def crear_caminos_cuadricula(mapa):
    if len(mapa) < 60:
        x_filas = .2
    else:
        x_filas = .3

    if len(mapa[0]) < 60:
        x_columnas = .2
    else:
        x_columnas = .3
    camino_filas = int(len(mapa)*x_filas)
    camino_columnas = int(len(mapa[0])*x_columnas)
    print(camino_filas, camino_columnas, len(mapa), len(mapa[0]))
    for i in range(len(mapa)):
        for j in range(len(mapa[0])):
            if i % camino_filas == 0 and j % camino_columnas == 0:
                mapa[i][j] = '⬛'
            elif j%camino_columnas == 0:
                mapa[i][j] = '⬛'
            elif i%camino_filas == 0:
                mapa[i][j] = '⬛'

def get_caminos(mapa):
    caminos_disponibles = []
    cantidad = 0
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == '⬛':
                caminos_disponibles.append((i, j))
                cantidad += 1
    return caminos_disponibles, cantidad

def agregar_obstaculos(mapa, caminos_disponibles):
    cantidad_obstaculos = caminos_disponibles[1] * 0.04
    for _ in range(int(cantidad_obstaculos)):
        x = random.choice(caminos_disponibles[0])
        caminos_disponibles[0].pop(caminos_disponibles[0].index(x))
        mapa[x[0]][x[1]] = random.choice(['🚧', '🪨 ', '💧'])

def agregar_arbol(mapa):
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == '🏠':
                if mapa[i][j-1] == '🏠' and mapa[i][j+1] == '🏠' and mapa[i-1][j] == '🏠' and mapa[i+1][j] == '🏠' and mapa[i-1][j] == '🏠':
                    mapa[i][j] = random.choice(['🌳', '🌴', '🌻'])

# Algoritmos


if __name__ == "__main__":
    filas = 26
    columnas = 41
    mapa = crear_mapa(filas, columnas)
    print_mapa(mapa)
    crear_caminos_cuadricula(mapa)
    print_mapa(mapa)
    caminos_disponbiles = get_caminos(mapa)
    agregar_obstaculos(mapa, caminos_disponbiles)
    agregar_arbol(mapa)
    print_mapa(mapa)
