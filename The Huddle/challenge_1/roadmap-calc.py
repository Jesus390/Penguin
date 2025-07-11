from heapq import heapify, heappop, heappush

import random
import os
import time

def clear():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Linux and MacOS
        os.system('clear')


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
        "cuadrado_blanco": "⬜",
        "cuadrado_negro": "⬛",
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
    # print(camino_filas, camino_columnas, len(mapa), len(mapa[0]))

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
            if mapa[i][j] == camino_principal or mapa[i][j] == camino_corto or mapa[i][j] == emoji_inicio or mapa[i][j] == emoji_final:
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

def marcar_punto_inicial(mapa):
    '''agrega el punto de inicio al mapa'''
    while True:
        fila = int(input("Ingresa la fila donde deseas empezar: "))

        columna = int(input("Ingresa la columna donde deseas empezar: "))
        caminos_disponibles = get_caminos(mapa)
        if fila >= 0 and fila < len(mapa) and columna >= 0 and columna < len(mapa[0]) and mapa[fila][columna] == camino_principal:
            mapa[fila][columna] = emojis['partidas']['inicial']
            break
        print("Posicion no disponible.")
    return (fila, columna)

def marcar_punto_final(mapa):
    '''agrega el punto de fin al mapa'''
    while True:
        fila = int(input("Ingresa la fila donde deseas finalizar: "))
        columna = int(input("Ingresa la columna donde deseas finalizar: "))
        caminos_disponibles = get_caminos(mapa)
        if fila >= 0 and fila < len(mapa) and columna >= 0 and columna < len(mapa[fila]) and mapa[fila][columna] == camino_principal:
            mapa[fila][columna] = emojis['partidas']['final']
            break
        print("Posicion no disponible.")
    return (fila, columna)

def get_nodo_del_nodo_actual(nodo_actual, caminos):
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # caminos = get_caminos(mapa)
    nodos_adyacentes = {}
    for movimiento in movimientos:
        nodo_siguiente = (nodo_actual[0]+movimiento[0], nodo_actual[1]+movimiento[1])
        if nodo_siguiente in caminos:
            nodos_adyacentes[nodo_siguiente] = 1
    return nodos_adyacentes

def crear_adyacencia_de_mapa(mapa):
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
        if mapa[i][j] == emoji_inicio:
            mapa[i][j] = emoji_inicio
        elif mapa[i][j] == emoji_final:
            mapa[i][j] = emoji_final
        else:
            mapa[i][j] = camino_corto
    return mapa

def agregar_obstaculos_manual(mapa):
    fila_tmp = len(mapa)
    columna_tmp = len(mapa[0])
    while True:
        print('Ingrese un obstaculo.')
        fila = int(input('Ingrese la fila: '))
        columna = int(input('Ingrese la columna: '))
        if 0 <= fila < fila_tmp or 0 <= columna < columna_tmp and mapa[fila][columna] == camino_principal:
            mapa[fila][columna] = emojis['obstaculo'][0]
            break

def init_mapa(filas, columnas):
    '''inicializa el mapa'''
    # crea el tablero
    mapa = crear_mapa(filas, columnas)

    # crea los caminos en el mapa
    crear_caminos_cuadricula(mapa)

    # agrega obstaculos al mapa
    agregar_obstaculos(mapa)

    # agrega arboles al mapa
    agregar_arbol(mapa)

    print_mapa(mapa)

    return mapa

def mostrar_ruta(mapa):
    # Punto inicial
    inicio = marcar_punto_inicial(mapa)
    clear()
    print_mapa(mapa)

    # Punto final
    fin = marcar_punto_final(mapa)
    clear()
    print_mapa(mapa)

    print("Procesando camino ...")

    # Lista de adyacencia
    lista_adyacencia = crear_adyacencia_de_mapa(mapa)

    # Instancia de la clase Graph, para el algoritmo de Dijkstra
    grafo = Graph(lista_adyacencia)

    # Ruta más corta
    ruta = grafo.ruta_corta(inicio, fin)
    time.sleep(1)
    clear()

    # Imprime la ruta
    update_mapa(mapa, ruta)
    print_mapa(mapa)

def obtener_posicion_emoji(mapa, emoji):
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == emoji:
                return (i, j)

def limpiar_ruta(mapa):
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == camino_corto:
                mapa[i][j] = camino_principal

def actualizar_mostrar_ruta(mapa):
    index_inicio = obtener_posicion_emoji(mapa, emoji_inicio)
    index_fin = obtener_posicion_emoji(mapa, emoji_final)

    print("Procesando nuevo camino...")
    time.sleep(1)
    
    # Lista de adyacencia
    lista_adyacencia = crear_adyacencia_de_mapa(mapa)

    # Instancia de la clase Graph, para el algoritmo de Dijkstra
    grafo = Graph(lista_adyacencia)

    # Ruta más corta
    ruta = grafo.ruta_corta(index_inicio, index_fin)
    time.sleep(1)
    clear()

    # Imprime la ruta
    update_mapa(mapa, ruta)
    print_mapa(mapa)



def cambiar_punto_inicial(mapa):
    # Punto inicial
    index_fila, index_columna = obtener_posicion_emoji(mapa, emoji_inicio)
    while True:
        fila = int(input("Ingrese nuevo punto inicial(fila): "))
        columna = int(input("Ingrese nuevo punto inicial(columna): "))

        if (fila, columna) == (index_fila, index_columna):
            print(f"Nuevo punto no valido {fila, columna}.")
            print("Misma posición seleccionada, por favor vuelva a ingresar...")
            continue
        
        clear()
        mapa[index_fila][index_columna] = camino_principal
        mapa[fila][columna] = emoji_inicio
        limpiar_ruta(mapa)
        actualizar_mostrar_ruta(mapa)
        break


def cambiar_punto_final(mapa):
    # Punto final
    index_fila, index_columna = obtener_posicion_emoji(mapa, emoji_final)
    while True:
        fila = int(input("Ingrese nuevo punto final(fila): "))
        columna = int(input("Ingrese nuevo punto final(columna): "))

        if (fila, columna) == (index_fila, index_columna):
            print(f"Nuevo punto no valido {fila, columna}.")
            print("Misma posición seleccionada, por favor vuelva a ingresar...")
            continue
        
        clear()
        mapa[index_fila][index_columna] = camino_principal
        mapa[fila][columna] = emoji_final
        limpiar_ruta(mapa)
        actualizar_mostrar_ruta(mapa)
        break

def agregar_obstaculo_random(mapa):
    # Agregar obstaculos random
    caminos_diponibles = get_caminos(mapa)
    # r = random.choices(caminos_diponibles[0])
    # print(r)
    fila, columna = random.choices(caminos_diponibles[0])[0]
    mapa[fila][columna] = random.choice(emojis['obstaculo'])

    clear()
    print("Se agrego un obstaculo random en la posicion: ", fila, columna)
    print_mapa(mapa)

    actualizar_mostrar_ruta(mapa)
    

def agregar_obstaculo(mapa):
    # Agregar obstaculos
    caminos_disponibles = get_caminos(mapa)
    while True:
        fila = int(input("Ingrese fila para agregar obstaculo: "))
        columna = int(input("Ingrese columna para agregar obstaculo: "))
        if (fila, columna) in caminos_disponibles[0]:
            mapa[fila][columna] = random.choice(emojis['obstaculo'])
            clear()
            print("Se agrego un obstaculo en la posicion: ", fila, columna)
            limpiar_ruta(mapa)
            print_mapa(mapa)
            actualizar_mostrar_ruta(mapa)
            break
        print("Posicion no valida, por favor vuelva a ingresar...")
    

if __name__ == "__main__":
    filas, columnas = 21, 26
    mapa = init_mapa(filas, columnas)

    # Muestra la ruta mas corta desde el punto inicial
    # al punto final
    mostrar_ruta(mapa)

    while True:
        print(
            '''
+ Seleccione una opción:
\t1. Cambiar punto inicial
\t2. Cambiar punto final
\t3. Agregar obstaculo random
\t4. Agregar obstaculo manual
=====================================
0. Salir
'''
        )
        opcion = input("Ingrese opción: ")
        if opcion == "0":
            break
        elif opcion == "1":
            cambiar_punto_inicial(mapa)
        elif opcion == "2":
            cambiar_punto_final(mapa)
        elif opcion == "3":
            agregar_obstaculo_random(mapa)
        elif opcion == "4":
            agregar_obstaculo(mapa)
        else:
            print("Opción no válida. Por favor, vuelva a intentarlo.")
