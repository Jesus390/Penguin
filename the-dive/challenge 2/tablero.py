class Tablero:
    color = "⬜"

    def __init__(self, alto=10, ancho=10):
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
    def __init__(self, alto=10, ancho=10):
        super().__init__(alto, ancho)

    def crear(self):
        pass
    

if __name__=="__main__":
    tablero = Tablero(ancho=20)
    tablero.crear()
    tablero.mostrar()