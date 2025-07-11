from abc import ABC, abstractmethod
from heapq import heapify, heappop, heappush

class Mapa():
    def __init__(self, filas:tuple, columnas:tuple, *, inicio:tuple=None, fin:tuple=None):
        self.filas = filas
        self.columnas = columnas
        self.mapa = [['.' for _ in range(columnas)] for _ in range(filas)]
        self.obstaculos = []
        self.inicio = None
        self.fin = None

    def agregar_obstaculo(self, posicion, obstaculo:str="X"):
        fila, columna = posicion
        if self.posicion_dentro((fila, columna)) and self.es_celda_accesible((fila, columna)):
            self.mapa[fila][columna] = obstaculo

    def quitar_obstaculo(self, posicion:tuple):
        fila, columna = posicion
        self.mapa[fila][columna] = '.'

    def es_celda_accesible(self, posicion:tuple):
        fila, columna = posicion
        if self.posicion_dentro((fila, columna)):
            return self.mapa[fila][columna] == '.'

    def mostrar(self):
        for columnas in self.mapa:
            print(''.join(columnas))
        print()

    def posicion_dentro(self, posicion):
        fila, columna = posicion
        return 0 > fila <= self.filas and 0 < columna <= self.columnas

    def graph(self):
        return

######################################################################

class ICalculadoraDeRutas(ABC):
    @abstractmethod
    def calcular(self, mapa:Mapa):
        pass

class Dijkstra(ICalculadoraDeRutas):
    def __init__(self, mapa:Mapa):
        self.graph = mapa.graph()

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

    def calcular(self):
        self.ruta_corta()    

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

