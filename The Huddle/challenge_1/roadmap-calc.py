import random

def crear_mapa(filas, columnas):
    return [[' # ' for _ in range(columnas)] for _ in range(filas)]
    
def print_mapa(mapa):
    cantidad_borde = int(len(mapa[0]))
    print(f"+{'='*((cantidad_borde*4)-1)}+")
    for row in mapa:
        print(f"|{' '.join(row)}|")
    print(f"+{'='*((cantidad_borde*4)-1)}+")

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
                mapa[i][j] = ' + '
            elif j%camino_columnas == 0:
                mapa[i][j] = ' . '
            elif i%camino_filas == 0:
                mapa[i][j] = ' . '

def get_caminos(mapa):
    caminos_disponibles = []
    cantidad = 0
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == ' . ' or mapa[i][j] == ' + ':
                caminos_disponibles.append((i, j))
                cantidad += 1
    return caminos_disponibles, cantidad

def agregar_obstaculos(mapa, caminos_disponibles):
    tmp_caminos_disponibles = caminos_disponibles[0].copy()
    cantidad_obstaculos = caminos_disponibles[1] * 0.02
    for _ in range(int(cantidad_obstaculos)):
        x = random.choice(tmp_caminos_disponibles)
        tmp_caminos_disponibles.pop(tmp_caminos_disponibles.index(x))
        mapa[x[0]][x[1]] = random.choice(['🧱 ', '🚧 ', '🪨 ', '🌊 '])
    # print(caminos_disponbiles[1])
    # print(cantidad_obstaculos)


def mostrar_valores(mapa):
    '''
    Usa valores para diferenciar terrenos:
    0: Camino libre.
    1: Edificio (obstáculo).
    2: Agua (obstáculo con ruta alternativa).
    3: Zonas bloqueadas temporalmente.
    '''
    tmp_mapa = mapa.copy()
    for i in range(len(tmp_mapa)):
        for j in range(len(tmp_mapa[0])):
            if tmp_mapa[i][j] == ' . ' or tmp_mapa[i][j] == ' + ':
                tmp_mapa[i][j] = str(0)
            elif tmp_mapa[i][j] == ' # ':
                tmp_mapa[i][j] = str(1)

    print_mapa(tmp_mapa)

# Ejemplo de uso de la función map
if __name__ == "__main__":
    filas = 15
    columnas = 30
    mapa = crear_mapa(filas, columnas)
    crear_caminos_cuadricula(mapa)
    print_mapa(mapa)
    caminos_disponbiles = get_caminos(mapa)
    agregar_obstaculos(mapa, caminos_disponbiles)
    print_mapa(mapa)
    # mostrar_valores(mapa)
    # agregar_terrenos()