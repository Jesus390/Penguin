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
    """Juego de adivinar un acertijo con pistas"""

    def __init__(self):
        self.__acertijos = [
            {"pregunta": "Tengo agujeros pero guardo agua. ¿Qué soy?", "respuesta": "esponja"},
            {"pregunta": "Tengo llaves pero no abro cerraduras. ¿Qué soy?", "respuesta": "piano"},
            {"pregunta": "Cuanto más largo es, más corto se vuelve. ¿Qué es?", "respuesta": "vida"}
        ]
        self.__juego_actual = {}
        self.__intento_usuario = ""
        self.__intentos_restantes = 3
        self.__ganado = False

    def play(self):
        print("""
\t\t.: Adivinanza :.
Lee el acertijo atentamente e intenta resolverlo.
¡Tienes un máximo de 3 intentos!
""")
        self.__juego_actual = random.choice(self.__acertijos)
        self.__intentos_restantes = 3
        self.__ganado = False

    def entrada(self):
        while True:
            prompt = input("Tu respuesta >> ").strip().lower()
            if prompt:
                return prompt
            print("Notice: No puedes dejar la respuesta vacía.")

    def update(self, entrada):
        self.__intento_usuario = entrada
        if self.__intento_usuario == self.__juego_actual["respuesta"]:
            self.__ganado = True
        else:
            self.__intentos_restantes -= 1
            print(f"Respuesta incorrecta. Intentos restantes: {self.__intentos_restantes}")

    def verificar(self):
        if self.__ganado:
            print(f"\n¡Correcto! Has resuelto el acertijo.")
            return True
        if self.__intentos_restantes == 0:
            print(f"\n¡Perdiste! La respuesta correcta era: {self.__juego_actual['respuesta']}")
            return True
        return False

    def renderizar(self):
        if self.__ganado or self.__intentos_restantes == 0:
            return ""
        return f"\nAcertijo: {self.__juego_actual['pregunta']}"


class DescubrePalabra(Entidad):
    """Juego de ordenar letras desordenadas (Anagrama)"""

    def __init__(self):
        self.__banco_palabras = ["terminal", "consola", "arcade", "codigo", "computadora"]
        self.__palabra_secreta = ""
        self.__palabra_desordenada = ""
        self.__intento_usuario = ""
        self.__intentos_restantes = 4
        self.__ganado = False

    def play(self):
        print("""
\t\t.: Descubre la Palabra :.
Las letras de la palabra están completamente desordenadas.
Ordénalas correctamente. ¡Tienes 4 intentos!
""")
        self.__palabra_secreta = random.choice(self.__banco_palabras)
        self.__intentos_restantes = 4
        self.__ganado = False
        
        # Desordenar las letras garantizando que no queden igual a la original
        letras = list(self.__palabra_secreta)
        while "".join(letras) == self.__palabra_secreta:
            random.shuffle(letras)
        self.__palabra_desordenada = "".join(letras)

    def entrada(self):
        while True:
            prompt = input("Palabra ordenada >> ").strip().lower()
            if prompt.isalpha():
                return prompt
            print("Notice: Ingresa solo texto sin números ni espacios.")

    def update(self, entrada):
        self.__intento_usuario = entrada
        if self.__intento_usuario == self.__secreta_o_normalizada():
            self.__ganado = True
        else:
            self.__intentos_restantes -= 1
            print(f"No es la palabra correcta. Intentos restantes: {self.__intentos_restantes}")

    def verificar(self):
        if self.__ganado:
            print(f"\n¡Increíble! Descubriste la palabra: {self.__palabra_secreta}")
            return True
        if self.__intentos_restantes == 0:
            print(f"\nTe quedaste sin intentos. La palabra era: {self.__palabra_secreta}")
            return True
        return False

    def renderizar(self):
        if self.__ganado or self.__intentos_restantes == 0:
            return ""
        return f"\nLetras desordenadas: [ {', '.join(self.__palabra_desordenada.upper())} ]"

    def __secreta_o_normalizada(self):
        # Helper interno para comparar de forma segura
        return self.__palabra_secreta.lower()
