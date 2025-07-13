from abc import ABC, abstractmethod
from heapq import heapify, heappop, heappush

class Mapa():
    def __init__(self, filas:tuple, columnas:tuple, *, inicio:tuple=None, fin:tuple=None):
        self.filas = filas
        self.columnas = columnas
        self.mapa = [['⬜' for _ in range(columnas)] for _ in range(filas)]
        self.obstaculos = []
        self.inicio = None
        self.fin = None

    def agregar_obstaculo(self, posicion:tuple, obstaculo:str="X"):
        fila, columna = posicion
        if self.posicion_dentro((fila, columna)) and self.es_celda_accesible((fila, columna)):
            self.mapa[fila][columna] = obstaculo
 
    def quitar_obstaculo(self, posicion:tuple):
        fila, columna = posicion
        self.mapa[fila][columna] = '.'

    def agregar_casas_random(self, factor_de_cantidad:float=.3):
        import random
        cantidad = self.filas * factor_de_cantidad
        for fila in range(self.filas):
            for _ in range(int(cantidad)):
                self.mapa[fila][random.randint(0, self.columnas-1)] = '🏠'

    def es_celda_accesible(self, posicion:tuple):
        fila, columna = posicion
        if self.posicion_dentro((fila, columna)):
            return self.mapa[fila][columna] == '.'

    def mostrar(self):
        for columnas in self.mapa:
            print(''.join(columnas))
        print()

    def posicion_dentro(self, posicion:tuple):
        fila, columna = posicion
        return 0 > fila <= self.filas and 0 < columna <= self.columnas
    
    ########################################################
    #
    #   Funciones auxiliares para algoritmos de busqueda
    #
    ########################################################

    def diccionario_de_adyacencia(self):
        # obtener los nodos del camino
        nodos = []
        for f, filas in enumerate(self.mapa):
            for c, columna in enumerate(filas):
                if columna == '⬜':
                    nodos.append((f, c))

        # movimientos posibles
        # abajo     =>  ( 1, 0)
        # arriba    =>  (-1, 0)
        # derecha   =>  ( 0, 1)
        # izquierda =>  ( 0,-1)
        movimientos = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        # obtener lista de adyacencia (diccionario)
        adyacencias = {}
        adyacencia_lista_aux = {}
        for nodo in nodos:
            nodo_fila, nodo_columna = nodo
            for movimiento in movimientos:
                mov_fila, mov_columna = movimiento
                tmp_moviento = (nodo_fila + mov_fila, nodo_columna + mov_columna)
                if self.posicion_dentro(tmp_moviento):
                    adyacencia_lista_aux[tmp_moviento] = 1
            adyacencias[nodo] = adyacencia_lista_aux

        return adyacencias

######################################################################

class ICalculadoraDeRutas(ABC):
    @abstractmethod
    def calcular(self, mapa:Mapa):
        pass

class Dijkstra(ICalculadoraDeRutas):
    def __init__(self, mapa:Mapa):
        self.diccionario_de_adyacencia = mapa.diccionario_de_adyacencia()

    def distancias_cortas(self, source:tuple):
        distancias = {node: float("inf") for node in self.diccionario_de_adyacencia}
        distancias[source] = 0 # se inicializa la fuente en cero
        
        nodos_visitados = set()

        pq = [(0, source)]
        heapify(pq)

        while pq:
            distancia_actual, nodo_actual = heappop(pq)

            if nodo_actual in nodos_visitados:
                continue

            nodos_visitados.add(nodo_actual)

            for nodo_vecino, distancia_nodo_vecino in self.diccionario_de_adyacencia[nodo_actual].items():
                distancia_aux = distancia_actual + distancia_nodo_vecino
                if distancia_aux < distancias[nodo_vecino]:
                    distancias[nodo_vecino] = distancia_aux
                    heappush(pq, (distancia_aux, nodo_vecino))

        predecesores = {node: None for node in self.diccionario_de_adyacencia}
        for node, distancia in distancias.items():
            for vecino, distancia_vecino in self.diccionario_de_adyacencia[node].items():
                if distancias[vecino] == distancia + distancia_vecino:
                    predecesores[vecino] = node

        return distancias, predecesores
    
    def ruta_corta(self, source:tuple, target:tuple):
        _, predecesores = self.distancias_cortas(source)

        ruta = []
        nodo_actual = target

        while nodo_actual:
            ruta.append(nodo_actual)
            nodo_actual = predecesores[nodo_actual]

        ruta.reverse()
        return ruta

    def calcular(self):
        self.ruta_corta(self.mapa.inicio, self.mapa.fin)    

######################################################################

class CalculadoraDeRutasFactory(ABC):
    @abstractmethod
    def crear_calculadora_de_rutas(self):
        pass

class DijkstraFactory(CalculadoraDeRutasFactory):
    def crear_calculadora_de_rutas(self):
        return Dijkstra()

#######################################################################

class SistemaDeRutas:
    def __init__(self, factory: CalculadoraDeRutasFactory):
        self.calculadora = factory.crear_calculadora_de_rutas()

    def ejecutar(self):
        self.calculadora.calcular()

#######################################################################

class Cliente():
    def cli(self):
        '''Muestra la interfaz gráfica en en linea de comando (CLI)'''
        pass

    def tkinter(self):
        '''Muestra la interfaz gráfica en pantalla utilizando la librería Tkinter'''
        pass