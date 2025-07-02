import random
from heapq import heapify, heappop, heappush

class Graph:
    def __init__(self, graph: dict={}):
        self.graph = graph

    def distancias_cortas(self, source):
        distancias = {node: float("inf") for node in self.graph}
        distancias[source] = 0 # se inicializa la fuente en cero
        
        nodos_visitados = set()

        pq = [(0, source)]
        heapify(pq)

        while pq:
            distancia_actual, nodo_actual = heappop(pq)

            if nodo_actual in nodos_visitados:
                continue

            nodos_visitados.add(nodo_actual)

            for nodo_vecino, distancia_nodo_vecino in self.graph[nodo_actual].items():
                distancia_aux = distancia_actual + distancia_nodo_vecino
                if distancia_aux < distancias[nodo_vecino]:
                    distancias[nodo_vecino] = distancia_aux
                    heappush(pq, (distancia_aux, nodo_vecino))

        predecesores = {node: None for node in self.graph}
        for node, distancia in distancias.items():
            for vecino, distancia_vecino in self.graph[node].items():
                if distancias[vecino] == distancia + distancia_vecino:
                    predecesores[vecino] = node

        return distancias, predecesores
    
    def ruta_corta(self, source, target):
        _, predecesores = self.distancias_cortas(source)

        ruta = []
        nodo_actual = target

        while nodo_actual:
            ruta.append(nodo_actual)
            nodo_actual = predecesores[nodo_actual]

        ruta.reverse()
        return ruta
    
emojis = {
    "casa" : ['🏠'],
    "camino": {
        "derecha": ['➡'],
        "izquierda": ['⬅'],
        "adelante": ['⬆'],
        "atras": ['⬇'],
        "cuadrado_blanco": "⬜",
        "cuadrado_negro": "⬛",
        "triangulo_arriba": "▲",
        "triangulo_abajo": "▼",
        "triangulo_derecha": "▶",
        "triangulo_izquierda": "◀",
        "circulo": "⭕",
        "ruta": "🏁",
    },
    "arbol": ['🌳', '🌴', '🌻'],
    "obstaculo": ['🚧', '🪨 ', '💧'],
    "partidas": {
        "inicial": '🟢', 
        "final": '🔴'
    }
}

emoji_inicio = emojis['partidas']['inicial']
emoji_final = emojis['partidas']['final']
camino_principal = emojis['camino']['cuadrado_blanco']
camino_corto = emojis['camino']['cuadrado_negro']

def crear_mapa(filas, columnas):
    '''Creamos un mapa con emojis con filas y columnas'''
    return [[emojis['casa'][0] for _ in range(columnas)] for _ in range(filas)]
    
def print_mapa(mapa):
    '''Imprimimos el mapa con emojis'''

    # cantidad_borde, longitud del mapa    
    cantidad_borde = int(len(mapa[0]))

    # imprime borde del mapa
    print(f"+{'='*((cantidad_borde*2))}+")
    for row in mapa:
        print(f"|{''.join(row)}|")
    # imprime borde del mapa
    print(f"+{'='*((cantidad_borde*2))}+")

def crear_caminos_cuadricula(mapa):
    '''Creamos un camino en el mapa'''

    # x_filas, factor de escala
    if len(mapa) < 60:
        x_filas = .2
    else:
        x_filas = .3

    # y_columnas, factor de escala
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
                mapa[i][j] = camino_principal
            elif j%camino_columnas == 0:
                mapa[i][j] = camino_principal
            elif i%camino_filas == 0:
                mapa[i][j] = camino_principal

def get_caminos(mapa):
    '''retorna caminos disponibles'''

    caminos_disponibles = []
    cantidad = 0
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == camino_principal:
                caminos_disponibles.append((i, j))
                cantidad += 1
    return caminos_disponibles, cantidad

def agregar_obstaculos(mapa):
    '''agrega obstaculos al mapa'''
    caminos_disponibles = get_caminos(mapa)
    cantidad_obstaculos = caminos_disponibles[1] * 0.04
    for _ in range(int(cantidad_obstaculos)):
        x = random.choice(caminos_disponibles[0])
        caminos_disponibles[0].pop(caminos_disponibles[0].index(x))
        mapa[x[0]][x[1]] = random.choice(emojis['obstaculo'])

def agregar_arbol(mapa):
    '''agrega un arbol al mapa'''
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == emojis['casa'][0]:
                # obs.: validar si el indice existe
                if mapa[i][j-1] == emojis['casa'][0] and \
                mapa[i-1][j] == emojis['casa'][0] and \
                mapa[i-1][j] == emojis['casa'][0]:
                    mapa[i][j] = random.choice(emojis['arbol'])

def inicio(mapa):
    '''agrega el punto de inicio al mapa'''
    while True:
        fila = int(input("Ingresa la fila donde deseas empezar: "))
        columna = int(input("Ingresa la columna donde deseas empezar: "))
        caminos_disponibles = get_caminos(mapa)
        if fila >= 0 and fila < len(mapa) and columna >= 0 and columna < len(mapa[0]) and mapa[fila][columna] == camino_principal:
            mapa[fila][columna] = emojis['jugador'][0]
            break
        print("Posicion no disponible.")

def final(mapa):
    '''agrega el punto de fin al mapa'''
    while True:
        fila = int(input("Ingresa la fila donde deseas finalizar: "))
        columna = int(input("Ingresa la columna donde deseas finalizar: "))
        caminos_disponibles = get_caminos(mapa)
        if fila >= 0 and fila < len(mapa) and columna >= 0 and columna < len(mapa[fila]) and mapa[fila][columna] == camino_principal:
            mapa[fila][columna] = emojis['jugador'][1]
            break
        print("Posicion no disponible.")

def get_nodo_del_nodo_actual(nodo_actual, caminos):
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # caminos = get_caminos(mapa)
    nodos_adyacentes = {}
    for movimiento in movimientos:
        nodo_siguiente = (nodo_actual[0]+movimiento[0], nodo_actual[1]+movimiento[1])
        if nodo_siguiente in caminos:
            nodos_adyacentes[nodo_siguiente] = 1
    return nodos_adyacentes

def get_adj_dic(mapa):
    caminos_disponibles = get_caminos(mapa)
    graph = {}
    for camino in caminos_disponibles[0]:
        graph[camino] = get_nodo_del_nodo_actual(camino, caminos_disponibles[0])
    return graph

def get_adj_matriz(mapa):
    '''obtiene los nodos del mapa'''
    # matriz de adjacencia
    adj_matriz = []

    # longitud fila, columna
    len_fila = len(mapa)
    len_columna = len(mapa[0])

    # recorre la matriz
    # agrega 1 si es un camino caso contrario 0
    for i in range(len_fila):
        fila = []
        for j in range(len_columna):
            if mapa[i][j] == camino_principal:
                fila.append(1)
            else:
                fila.append(0)
        adj_matriz.append(fila)
    return adj_matriz

def print_adj_matriz(adj_matriz):
    '''imprime la matriz de adjacencia'''
    for row in adj_matriz:
        print(row)

def update_mapa(mapa, ruta):
    for i, j in ruta:
        mapa[i][j] = camino_corto
    return mapa

if __name__ == "__main__":
    filas = 21
    columnas = 26
    mapa = crear_mapa(filas, columnas)
    crear_caminos_cuadricula(mapa)
    agregar_obstaculos(mapa)
    agregar_arbol(mapa)
    print_mapa(mapa)
    ady_graph = get_adj_dic(mapa)
    dijkstra = Graph(ady_graph)

    inicio = (0, 0)
    final = (20, 21)
    print(dijkstra.graph)
    shortet_path = dijkstra.ruta_corta(inicio, final)
    mapa = update_mapa(mapa, shortet_path)
    print_mapa(mapa)