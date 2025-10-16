class Tablero:
    color = "⬜"

    def __init__(self, alto:int=10, ancho:int=10):
        self.alto = alto
        self.ancho = ancho
        self._tablero = None

    def crear(self):
        self._tablero = [[self.color for _ in range(self.ancho)] for _ in range(self.alto)]

    def mostrar(self):
        print("🟨" + ("🟨" * self.ancho) + "🟨")
        for fila in self._tablero:
            print("🟨" + ("".join(fila)) + "🟨")
        print("🟨" + ("🟨" * self.ancho) + "🟨")

class Laberinto(Tablero):
    def __init__(self, alto:int=10, ancho:int=10):
        super().__init__(alto, ancho)
        self._punto_inicial = None

    def punto_inicial(self, punto_inicial=None):
        self._punto_inicial = punto_inicial if punto_inicial else (0, 0)
        x, y = self._punto_inicial
        self._tablero[self._punto_inicial[0]][self._punto_inicial[1]] = "🟩"

    def punto_final(self, punto_final=None):
        self._punto_final = punto_final if punto_final else (self.ancho-1, self.alto-1)
        x, y = self._punto_final
        self._tablero[x][y] = "🟥"


if __name__ == "__main__":
    lab = Laberinto(10, 10)
    lab.crear()
    lab.punto_inicial((1, 1))
    lab.punto_final((6, 6))
    lab.mostrar()
