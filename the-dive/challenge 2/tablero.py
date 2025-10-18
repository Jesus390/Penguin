class Tablero:
    """
    Representa una matriz de NxM dimensión
    """
    color = "⬜"

    def __init__(self, alto:int=10, ancho:int=10):
        """
        Param
        =====
        alto: int, cantidad de filas del tablero
        ancho: int, cantidad de columnas del tablero
        _tablero: list, contiene la representación del tablero en una matriz NxM
        """
        self.alto = alto
        self.ancho = ancho
        self._tablero = None


    def crear(self):
        """
        Crea un matriz NxM que representa el tablero
        """
        self._tablero = [[self.color for _ in range(self.ancho)] for _ in range(self.alto)]


    def mostrar(self):
        """
        Muestra el contenido del tablero en cada casilla
        """
        print("🟨" + ("🟨" * self.ancho) + "🟨")
        
        for fila in self._tablero:
        
            print("🟨" + ("".join(fila)) + "🟨")
        
        print("🟨" + ("🟨" * self.ancho) + "🟨")



class Laberinto(Tablero):
    """
    Clase que crea laberintos en un tablero NxM
    """

    def __init__(self, alto:int=10, ancho:int=10):
        """"
        Param
        =====
        alto: int, la cantidad de filas para el laberinto
        ancho: int, la cantidad de columnas para el laberinto
        """
        super().__init__(alto, ancho)
        self._punto_inicial = None


    def punto_inicial(self, punto_inicial=None):
        '''
        Agrega punto inicial al tablero

        Param
        =====
        punto_inicial: tuple de dos valores enteros
        '''
        self._punto_inicial = punto_inicial if punto_inicial else (0, 0)
        
        x, y = self._punto_inicial
        
        self._tablero[self._punto_inicial[0]][self._punto_inicial[1]] = "🟩"


    def punto_final(self, punto_final=None):
        '''
        Agrega punto final al tablero

        Param
        =====
        punto_final: tuple de dos valores enteros
        '''
        self._punto_final = punto_final if punto_final else (self.ancho-1, self.alto-1)

        x, y = self._punto_final

        self._tablero[x][y] = "🟥"


if __name__ == "__main__":
    lab = Laberinto(10, 10)
    lab.crear()
    lab.punto_inicial((1, 1))
    lab.punto_final((6, 6))
    lab.mostrar()
