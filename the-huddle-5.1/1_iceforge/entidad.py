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
        self.__palabra = None

        # Lista de palabras a generar según el nivel seleccionado
        self.__palabras = {
            "1": ["uno", "auto", "juego", "tres"],
            "2": ["familias", "archivo", "ahorcado", "proyecto"],
            "3": ["condicionales", "vocabulario", "interacciones"]
        }

    def seleccionar_palabra(self, nivel):
        """Selecciona una palabra"""
        self.__palabra = random.choice(self.__palabras[str(nivel)])

    def get_palabra(self):
        """"Devuelve la palabra secreta generada"""
        return self.__palabra


