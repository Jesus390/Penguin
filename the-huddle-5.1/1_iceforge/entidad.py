from abc import ABC, abstractmethod
import random

class JuegoDeLetras(ABC):
    '''
    Clase Base
    Todo juego relacionados a letras tipo adivinanza debe 
    hereder de está clase
    '''

    @abstractmethod
    def seleccionar_palabra(nivel):
        """Este método debe implementarse por las clases hijas"""
        pass

    @abstractmethod
    def get_palabra():
        """Este método debe implementarse por las clases hijas"""
        pass

class Ahorcado(JuegoDeLetras):
    """"Juego del Ahorcado"""

    def __init__(self):
        # Palabra generada
        self.__palabra_secreta = None

        # Lista de palabras a generar según el nivel seleccionado
        self.__lista_de_palabras = {
            "1": ["uno", "auto", "juego", "tres"],
            "2": ["familias", "archivo", "ahorcado", "proyecto"],
            "3": ["condicionales", "vocabulario", "interacciones"]
        }

    def seleccionar_palabra(self, nivel):
        """Selecciona una palabra"""
        self.__palabra_secreta = random.choice(self.__lista_de_palabras[str(nivel)])

    def get_palabra(self):
        """"Devuelve la palabra secreta generada"""
        return self.__palabra_secreta
    
    def ocultar_letras(self, nivel=40):
        """Oculta las letras de la palabra"""
        letras_ocultas = {}
        palabra_oculta = list(self.__palabra_secreta)
        len_palabra_secreta = len(self.__palabra_secreta)
        while len(letras_ocultas) < int((len_palabra_secreta*nivel)/100):
            id_letra = random.randrange(0, len_palabra_secreta)
            letras_ocultas[id_letra] = self.__palabra_secreta[id_letra]
            palabra_oculta[id_letra] = "_"

        return "".join(palabra_oculta)



