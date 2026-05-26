from entidad import Ahorcado, Adivinanza, DescubrePalabra

class Game:
    def __init__(self):
        # Almacenamos las clases (no las instancias) para poder crear 
        # un objeto fresco y limpio cada vez que se elija jugar
        self.__lista_juegos = [Ahorcado, Adivinanza, DescubrePalabra]
        self.__juego = None

    def menu(self):
        """Imprime el menú y retorna la instancia del juego elegido o sale"""
        menu = """
        +===================================+

        |        .:::: JUEGOS ::::.         |
        |-----------------------------------|
        |    1. Ahorcado                    |
        |    2. Adivinanza                  |
        |    3. Descubre la Palabra         |
        |-----------------------------------|
        |    0. Salir                       |
        +===================================+
        """
        while True:
            print(menu)
            try:
                opcion = int(input(">> "))
                
                if opcion == 0:
                    print("Programa terminado.")
                    exit()
                
                # Validamos que esté dentro del rango de opciones disponibles (1 a 3)
                if 1 <= opcion <= len(self.__lista_juegos):
                    # Creamos una instancia nueva (ej. Ahorcado()) usando el índice corregido
                    return self.__lista_juegos[opcion - 1]()
                
                print("Notice: Opción inválida. Elige un número del menú.")
            except ValueError:
                print("Notice: Por favor, ingresa un número válido.")

    def run(self):
        while True:
            # Obtenemos un juego nuevo con sus variables reseteadas
            self.__juego = self.menu()

            # Inicializa los parámetros del juego
            self.__juego.play()

            # Bucle del juego en ejecución
            while not self.__juego.verificar():
                entrada = self.__juego.entrada()
                self.__juego.update(entrada)
                
                # Renderizamos solo si el juego sigue activo tras la actualización
                if not self.__juego.verificar():
                    print(self.__juego.renderizar())
