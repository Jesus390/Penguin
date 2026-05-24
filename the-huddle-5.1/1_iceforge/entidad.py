from abc import ABC, abstractmethod

import random

class Entidad(ABC):
    """Clase abstracta para gestionar juegos de letras, palabras"""

    @abstractmethod
    def play(self):
        """configuración inicial del juego"""
        pass

    @abstractmethod
    def entrada(self):
        """entrada del usuario para comparar con la respuesta"""
        pass
    
    @abstractmethod
    def verificar(self):
        """verifica si el juego termino"""
        pass

    @abstractmethod
    def update(self, estado):
        """actualiza el estado del juego"""
        pass
    
    @abstractmethod
    def renderizar(self):
        """imprime el estado"""
        pass


class Ahorcado(Entidad  ):

    def __init__(self):
        self.__vidas = 6
        self.__palabras = ["Participantes", "Completa", "Victoria", "Adivinanza", "Matemáticas"]
        self.__palabra = ""
        self.__letras_ocultas = {}
        self.__palabra_oculta = []

    def play(self):
        print("""
\t\t.: Ahorcado :.
El ahorcado es un clásico juego de adivinanzas de lápiz y papel.
Un jugador piensa en una palabra secreta y los demás intentan 
descubrirla arriesgando letras una por una. Por cada letra errónea, 
se dibuja progresivamente la figura de un monigote en una horca; 
si el dibujo se completa antes de adivinarla, el jugador pierde.
""")

        self.__palabra = random.choice(self.__palabras)
        self.__palabra_oculta = self.__ocultar_letras()
        print(self.__monigote())
        print("".join(self.__palabra_oculta))
    
    def entrada(self):
        while True:
            prompt = input(">>")
            if len(prompt) == 1:
                return prompt
            print("Notice: Ingresa un carácter.")
    
    def update(self, entrada):
        for i, letra in self.__letras_ocultas.items():
            if entrada == letra:
                del self.__letras_ocultas[i]
                self.__palabra_oculta[i] = letra
                break
        else:
            self.__vidas = self.__vidas - 1
            print("La letra no existe.")
    
    def verificar(self):
       return True if self.__vidas == 0 else False 

    def renderizar(self):
        render = self.__monigote()
        return render + "\n\n" + "".join(self.__palabra_oculta)

    def __ocultar_letras(self):
        """Oculta las letras de la palabra"""
        self.__palabra_oculta = list(self.__palabra)
        len_palabra_secreta = len(self.__palabra)
        while len(self.__letras_ocultas) < int((len_palabra_secreta*40)/100): # 40% de letras ocultas de la palabra original
            id_letra = random.randrange(0, len_palabra_secreta)
            self.__letras_ocultas[id_letra] = self.__palabra[id_letra]
            self.__palabra_oculta[id_letra] = "_"
        return self.__palabra_oculta
    
    def __monigote(self):
        dibujar_monigote = {
            6: "\t._____._\n\t|/_\\_/_\\\n\t|      |\n\t|\n\t|\n\t|\n\t|", 
            5: "\t._____._\n\t|/_\\_/_\\\n\t|      |\n\t|      O\n\t|\n\t|\n\t|", 
            4: "\t._____._\n\t|/_\\_/_\\\n\t|      |\n\t|      O\n\t|      |\n\t|\n\t|", 
            3: "\t._____._\n\t|/_\\_/_\\\n\t|      |\n\t|      O\n\t|     /|\n\t|\n\t|\n", 
            2: "\t._____._\n\t|/_\\_/_\\\n\t|      |\n\t|      O\n\t|     /|\\\n\t|\n\t|\n", 
            1: "\t._____._\n\t|/_\\_/_\\\n\t|      |\n\t|      O\n\t|     /|\\\n\t|     / \n\t|\n", 
            0: "\t._____._\n\t|/_\\_/_\\\n\t|      |\n\t|      O\n\t|     /|\\\n\t|     / \\\n\t|" 
        }       
        return dibujar_monigote[self.__vidas]


