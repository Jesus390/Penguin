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


class Ahorcado(Entidad):

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
        # Guardamos la palabra en minúsculas para evitar problemas de capitalización
        self.__palabra = random.choice(self.__palabras).lower()
        self.__ocultar_letras()
        print(self.__monigote())
        print(" ".join(self.__palabra_oculta))
    
    def entrada(self):
        while True:
            prompt = input(">> ").strip().lower() # Limpia espacios y pasa a minúsculas
            if len(prompt) == 1 and prompt.isalpha():
                return prompt
            print("Notice: Ingresa un único carácter válido (A-Z).")
    
    def update(self, entrada):
        acierto = False
        # Recorremos todas las letras ocultas usando una copia de las llaves
        # para poder modificar el diccionario dentro del bucle sin errores
        for i in list(self.__letras_ocultas.keys()):
            if entrada == self.__letras_ocultas[i]:
                del self.__letras_ocultas[i]
                self.__palabra_oculta[i] = entrada
                acierto = True # Marcamos que encontramos al menos una coincidencia
                
        if not acierto:
            self.__vidas -= 1
            print("La letra no existe.")
    
    def verificar(self):
        # El juego termina si te quedas sin vidas (derrota) o si ya no quedan letras ocultas (victoria)
        if self.__vidas == 0:
            print(f"\n¡Perdiste! La palabra era: {self.__palabra}")
            return True
        if len(self.__letras_ocultas) == 0:
            print(f"\n¡Felicidades, ganaste! Adivinaste la palabra: {self.__palabra}")
            return True
        return False 

    def renderizar(self):
        render = self.__monigote()
        return render + "\n\n" + " ".join(self.__palabra_oculta)

    def __ocultar_letras(self):
        """Oculta las letras de la palabra garantizando el porcentaje correcto"""
        self.__palabra_oculta = list(self.__palabra)
        len_palabra_secreta = len(self.__palabra)
        objetivo_ocultas = int((len_palabra_secreta * 40) / 100)
        
        # Si la palabra es muy corta, nos aseguramos de ocultar al menos 1 letra
        if objetivo_ocultas == 0:
            objetivo_ocultas = 1

        while len(self.__letras_ocultas) < objetivo_ocultas:
            id_letra = random.randrange(0, len_palabra_secreta)
            # Evitamos duplicar índices para no generar un bucle infinito
            if id_letra not in self.__letras_ocultas:
                self.__letras_ocultas[id_letra] = self.__palabra[id_letra]
                self.__palabra_oculta[id_letra] = "_"


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



class Adivinanza(Entidad):
    def play(self):
        return "Jugando Adivinanza"

    def entrada(self):
        paso = input(">>")
        return paso
    
    def verificar(self):
        return True
    
    def update(self, entrada):
        return "Juego actualizado"
    
    def renderizar(self):
        return "Juego renderizado"

class DescubrePalabra(Entidad):

    def play(self):
        return "Jugando Descubre la Palabra"

    def entrada(self):
        paso = input(">>")
        return paso
    
    def verificar(self):
        return True
    
    def update(self, entrada):
        return "Juego actualizado"
    
    def renderizar(self):
        return "Juego renderizado"
