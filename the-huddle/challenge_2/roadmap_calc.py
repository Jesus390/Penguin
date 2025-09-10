from abc import ABC, abstractmethod
from heapq import heapify, heappop, heappush

import os
import time

class Mapa():
    def __init__(self, filas:int, columnas:int, *, inicio:tuple=None, fin:tuple=None):
        self.filas = filas
        self.columnas = columnas
        self.mapa = [['⬜' for _ in range(columnas)] for _ in range(filas)]
        self.obstaculos = []
        self.inicio = None
        self.fin = None

    def agregar_obstaculo(self, posicion:tuple, obstaculo:str="🚧"):
        fila, columna = posicion
        if self.posicion_dentro((fila, columna)):
            self.obstaculos.append((fila, columna)) 
            self.mapa[fila][columna] = obstaculo
 
    def quitar_obstaculo(self, posicion:tuple):
        if posicion in self.obstaculos:
            fila, columna = posicion
            self.obstaculos.remove(posicion)
            self.mapa[fila][columna] = '⬜'

    def agregar_inicio(self, posicion:tuple):
        print(f"self.filas {self.filas}, self.columnas {self.columnas}")
        if self.posicion_dentro(posicion):
            self.inicio = posicion
            fila, columna = self.inicio
            self.mapa[fila][columna] = '🟢'
            print(f"Posicion inicial agregada en {self.inicio}")
        else:
            print("Posicion fuera del mapa")
    
    def agregar_fin(self, posicion:tuple):
        if self.posicion_dentro(posicion):
            self.fin = posicion
            fila, columna = self.fin
            self.mapa[fila][columna] = '🔴'
            print(f"Posicion final agregada en {self.fin}")
        else:
            print("Posicion fuera del mapa")

    def actualizar_punto_inicio(self, posicion:tuple):
        if self.posicion_dentro(posicion):
            self.mapa[self.inicio[0]][self.inicio[1]] = '⬜'
            self.inicio = posicion
            self.mapa[self.inicio[0]][self.inicio[1]] = '🟢'

    def actualizar_punto_fin(self, posicion:tuple):
        if self.posicion_dentro(posicion):
            self.mapa[self.fin[0]][self.fin[1]] = '⬜'
            self.fin = posicion
            self.mapa[self.fin[0]][self.fin[1]] = '🔴'

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
    
    def marcar_ruta(self, ruta: list):
        for fila, columna in ruta:
            if self.mapa[fila][columna] == '⬜':
                self.mapa[fila][columna] = '🟦'

    def posicion_dentro(self, posicion:tuple):
        fila, columna = posicion
        return 0 <= fila < self.filas and 0 <= columna < self.columnas
    
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
                if columna == '⬜' or columna == '🟢' or columna == '🔴' or columna == '🟦':
                    nodos.append((f, c))

        # movimientos posibles
        # abajo     =>  ( 1, 0)
        # arriba    =>  (-1, 0)
        # derecha   =>  ( 0, 1)
        # izquierda =>  ( 0,-1)
        movimientos = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        # obtener lista de adyacencia (diccionario)
        adyacencias = {}
        for nodo in nodos:
            adyacencia_lista_aux = {}
            nodo_fila, nodo_columna = nodo
            for movimiento in movimientos:
                mov_fila, mov_columna = movimiento
                tmp_moviento = (nodo_fila + mov_fila, nodo_columna + mov_columna)
                if self.posicion_dentro(tmp_moviento) and tmp_moviento in nodos:
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
        self.mapa = mapa
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
        return self.ruta_corta(self.mapa.inicio, self.mapa.fin)    

######################################################################

class CalculadoraDeRutasFactory(ABC):
    @abstractmethod
    def crear_calculadora_de_rutas(self, mapa: Mapa):
        pass

class DijkstraFactory(CalculadoraDeRutasFactory):
    def crear_calculadora_de_rutas(self, mapa: Mapa):
        return Dijkstra(mapa)

#######################################################################

class SistemaDeRutas:
    def __init__(self, factory: CalculadoraDeRutasFactory, mapa: Mapa):
        self.calculadora = factory.crear_calculadora_de_rutas(mapa)

    def ejecutar(self):
        return self.calculadora.calcular()

#######################################################################

class ICliente(ABC):
    @abstractmethod
    def run(self):
        pass

class ClienteCli(ICliente):
    '''Muestra la interfaz gráfica en en linea de comando (CLI)'''

    opciones_menu_principal = ['Salir', 'Agregar Obstaculos', 'Quitar Obstaculos', 'Cambiar Punto Inicial', 'Cambiar Punto Final']

    def clear(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def esperar(self, duracion):
        time.sleep(duracion)
    
    def limpiar_ruta_corta(self, mapa):
        for i in range(mapa.filas):
            for j in range(mapa.columnas):
                if mapa.mapa[i][j] == '🟦':
                    mapa.mapa[i][j] = '⬜'
        return mapa

    def actualizar_mapa(self, mapa: Mapa, factory: CalculadoraDeRutasFactory):
        mapa = self.limpiar_ruta_corta(mapa)
        sistema = SistemaDeRutas(factory, mapa)
        ruta_corta = sistema.ejecutar()
        mapa.marcar_ruta(ruta_corta)
        self.clear()
        mapa.mostrar()

    def mostrar_menu_principal(self):
        print("=" * 20)
        print("|\tMenu\t   |")
        print("=" * 20)
        for i, opcion in enumerate(self.opciones_menu_principal):
            if i == 0: continue
            print(f"{i}- {opcion}")
        print("-" * 30)
        print(f"0- {self.opciones_menu_principal[0]}\n\n")
        
    def seleccionar_opcion_menu(self):
        opcion = None
        while True:
            self.mostrar_menu_principal()
            try:
                opciones = list(range(len(self.opciones_menu_principal)))
                opcion = int(input("Selecciones una opción: "))
                if opcion in opciones:
                    return opcion
                print(f"Item número incorrecto: {opcion}")
            except Exception:
                print(f"Opción ingresada incorrecta: {opcion}")

    def run(self):
        cli = ClienteCli()

        filas = int(input("Filas: "))
        columnas = int(input("Columnas: "))

        cli.clear()

        print(f"Filas: {filas}, Columnas: {columnas}")
        mapa = Mapa(filas, columnas)
        mapa.mostrar()

        # agregar el punto inicial        
        fila_inicio = int(input("Fila punto inicial: "))
        columna_inicio = int(input("Columna punto inicial: "))
        mapa.agregar_inicio((fila_inicio, columna_inicio))
        # cli.esperar(1)
        cli.clear()
        print(f"Punto Inicial:\nFila: {fila_inicio}, Columna: {columna_inicio}")
        mapa.mostrar()

        # agregar el punto final
        fila_final = int(input("Fila punto final: "))
        columna_final = int(input("Columna punto final: "))
        mapa.agregar_fin((fila_final, columna_final))
        # cli.esperar(1)
        cli.clear()
        print(f"Punto Final:\nFila: {fila_inicio}, Columna: {columna_inicio}")
        mapa.mostrar()

        cli.esperar(1)
        cli.actualizar_mapa(mapa, DijkstraFactory())

        # factory = DijkstraFactory()
        # sistema = SistemaDeRutas(factory, mapa)
        # ruta_corta = sistema.ejecutar()
        # mapa.marcar_ruta(ruta_corta)
        # cli.clear()
        # mapa.mostrar()

        while True:
            opcion = self.seleccionar_opcion_menu()
            if opcion == 0:
                print("Saliendo del programa...")
                return
            elif opcion == 1:
                cli.clear()
                while True:
                    try:
                        fila = int(input("Fila (Agregar Obstaculo): "))
                        columna = int(input("Columna (Agregar Obstaculo): "))
                        if mapa.posicion_dentro((fila, columna)):
                            mapa.agregar_obstaculo((fila, columna))
                            break
                        else:
                            print("Posición fuera del mapa")
                    except ValueError:
                        print("Error: Debe ingresar un número")
                        cli.esperar(1)
                        cli.clear()
                cli.actualizar_mapa(mapa, DijkstraFactory())
            elif opcion == 2:
                cli.clear()
                while True:
                    try:
                        fila = int(input("Fila (Quitar Obstaculo): "))
                        columna = int(input("Columna (Quitar Obstaculo): "))
                        if mapa.posicion_dentro((fila, columna)):
                            mapa.quitar_obstaculo((fila, columna))
                            break
                        else:
                            print("Posición fuera del mapa")
                    except ValueError:
                        print("Error: Debe ingresar un número")
                        cli.esperar(1)
                        cli.clear()
                cli.actualizar_mapa(mapa, DijkstraFactory())
            elif opcion == 3:
                cli.clear()
                while True:
                    try:
                        fila = int(input("Fila (Nueva posición incial): "))
                        columna = int(input("Columna (Nueva posición inicial): "))
                        if mapa.posicion_dentro((fila, columna)):
                            mapa.actualizar_punto_inicio((fila, columna))
                            break
                        else:
                            print("Posición fuera del mapa")
                    except ValueError:
                        print("Error: Debe ingresar un número")
                        cli.esperar(1)
                        cli.clear()
                cli.actualizar_mapa(mapa, DijkstraFactory())
            elif opcion == 4:
                cli.clear()
                while True:
                    try:
                        fila = int(input("Fila (Nueva posición final): "))
                        columna = int(input("Columna (Nueva posición final): "))
                        if mapa.posicion_dentro((fila, columna)):
                            mapa.actualizar_punto_fin((fila, columna))
                            break
                        else:
                            print("Posición fuera del mapa")
                    except ValueError:
                        print("Error: Debe ingresar un número")
                        cli.esperar(1)
                        cli.clear()
                cli.actualizar_mapa(mapa, DijkstraFactory())



class ClienteTkinter(ICliente):
    '''Muestra la interfaz gráfica en pantalla utilizando la librería Tkinter'''
    def run(self):
        pass