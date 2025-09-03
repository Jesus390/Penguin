import random

class RandomNameChoice():
    def __init__(self, nombres:list, cantidad:int=1):
        self.nombres = self._puntuar_seleccion(nombres, cantidad)

    def choice(self):
        if len(list(self.nombres)) > 0:
            nombre = random.choice(list(self.nombres.keys()))
            self.nombres[nombre] -= 1
            if self.nombres[nombre] == 0:
                del self.nombres[nombre]
            return nombre
        return None

    def _puntuar_seleccion(self, nombres, cantidad):
        return {nombre:cantidad for nombre in nombres }

class Select():
    def __init__(self, obj_RNC:RandomNameChoice):
        self.obj_RNC = obj_RNC
    
    def select(self):
        return self.obj_RNC.choice()

class ReadFile():
    def __init__(self, path:str):
        self.path = path
        
    def get_nombres(self):
        nombres = []
        try:
            with open(self.path, 'r') as archivo:
                for linea in archivo:
                    nombres.append(linea.strip())
        except FileNotFoundError:   
            print("El archivo no existe")
        return nombres

if __name__ == "__main__":
    path = input("Ingrese el path del archivo: ")
    nombres = ReadFile(path).get_nombres()
    print(f"Nombres: {nombres}")

    posibilidad = int(input("Ingrese la cantidad de veces que se puede elegir cada nombre: "))
    obj = RandomNameChoice(nombres, posibilidad)
    select = Select(obj)

    if int(input("Seleccionar usuario... 1 si, 0 no: ")) == 1:
        while True:
            nombre = select.select()
            if nombre is None:
                print("No hay nombres disponibles")
                break
            print(f"El usuario seleccionado es: {nombre}")
            continuar = int(input("Desea, continuar... ? 1 si, 0 no: "))
            if continuar == 0: break