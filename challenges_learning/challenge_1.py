from colorama import Fore, Back, Style, init

import os
import time

# Limpia la terminal
def clear_window():
    os.system('cls' if os.name == 'nt' else 'clear')

# Tiempo de espera para que el mensaje desaparezca
def waiting_msg(tiempo=1.5):
    time.sleep(tiempo)

init() # setup colorama

class Persona:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

class Registro(Persona):

    def __init__(self, name):
        super().__init__(name)
        self._registros = {}
    
    # 1. Crea una tarea nueva
    def create_tarea(self, tarea, estado):
        tarea = tarea.upper()
        estado = estado.upper()
        
        if tarea in self._registros.keys():
            return False
        
        self._registros[tarea] = estado
        
        return True

    # 2. Modifica el estado de una tarea
    def set_tarea(self, tarea, estado):
        tarea = tarea.upper()
        estado = estado.upper()
        
        if not tarea in self._registros.keys():
            return False
        
        self._registros[tarea] = estado
        
        return True

    # 3. Elimina una tarea
    def delete_tarea(self, tarea):
        
        tarea = tarea.upper()
        
        if not tarea in self._registros.keys():
            return False
        
        del self._registros[tarea]
        
        return True

    # 4. Muesta todas las tareas
    def show_tareas(self):
        aux = Fore.GREEN + '------------------------\n' + Style.RESET_ALL
        
        for k, v in self._registros.items():
            if v.lower() == 'pendiente':
                aux += f'- {k}: {Fore.RED + v + Style.RESET_ALL}\n'
            if v.lower() == 'en progreso':
                aux += f'- {k}: {Fore.YELLOW + v + Style.RESET_ALL}\n'
            elif v.lower() == 'completada':
                aux += f'- {k}: {Fore.GREEN + v + Style.RESET_ALL}\n'
        
        aux += Fore.GREEN + '------------------------\n' + Style.RESET_ALL
        
        print(aux)

###############################
#   Variables Globales
###############################

# Estados disponibles para los Registros
# estados = (f'{Fore.YELLOW}pendiente{Style.RESET_ALL}', f'{Fore.MAGENTA}en progreso{Style.RESET_ALL}', f'{Fore.GREEN}completada{Style.RESET_ALL}')
estados = ('pendiente', 'en progreso', 'completada')

# Acciones del Menu principal
# acciones_del_menu = ('agregar', 'modificar', 'eliminar', 'mostrar', 'salir')
menu = {1:'agregar', 2:'modificar', 3:'eliminar', 4:'mostrar', 5: 'Cambiar nombre usuario', 0:'salir'}

# cantidad de caracteres a imprimir para
# la separacion de contendios
len_caracter = 50


###############################
#   Funciones - extras
###############################

# Imprime el menu principal
def print_menu(menu, name):
    print(f"{(Fore.BLUE + '=' + Style.RESET_ALL) * len_caracter}")
    print(f"\t\t{Back.BLUE} REGISTRAR TAREAS {Style.RESET_ALL} ({Fore.CYAN}{name}{Style.RESET_ALL})")
    
    for i, accion in menu.items():
        print(f"{Fore.GREEN}{i}{Style.RESET_ALL}. {accion.capitalize()}")
    
    print(f"{(Fore.BLUE + '=' + Style.RESET_ALL) * len_caracter}")

# Imprime los valores de la tarea
def print_estados(estados):
    print('-' * len_caracter)
    print(f'Seleccione un estado: ')
    print_estados
    
    for i, estado in enumerate(estados):
        print(f'{Fore.GREEN}{i+1}{Style.RESET_ALL}. {estado.capitalize()}')
    
    print('-' * len_caracter)

# Retorna el nombre de usuario para el registro
def get_username(msg="Ingrese su nombre"):
    nombre = input(f"{Back.YELLOW} {msg} {Style.RESET_ALL}: ")

    if nombre == '':
        nombre = "persona"
    
    clear_window()
    
    return nombre.upper()

# Imprime un mensaje de tipo:
# Informativo: info (default)
# Error: error
def print_mensaje(mensaje, tipo='info'):
    if tipo == 'error':
        print(f"{Fore.RED}Error{Style.RESET_ALL}: {mensaje}")
    else:
        print(f"{Fore.YELLOW}Info{Style.RESET_ALL}: {mensaje}")

# Valida la opcion ingresada por el usuario
def validar_opcion(opcion, rango):
    return True if opcion in rango else False

# Retorna la opcion del menu
def get_opcion_menu(menu, name):
    while True:
        try:
            opcion = int(input(f'{Back.YELLOW} Seleccione una opción del Menu {Style.RESET_ALL}: '))
            
            if validar_opcion(opcion, menu.keys()):
                return opcion
            
            clear_window()
            print_mensaje("seleccione una opción del menu: ", 'error')
            waiting_msg()
            clear_window()
            print_menu(menu, name)
        
        except:
            clear_window()
            print_mensaje("ingrese un número valido.", 'error')
            waiting_msg()
            clear_window()
            print_menu(menu, name)

# Retorna el valor de la tarea
def get_opcion_estado(estados, title):
    clear_window()
    print_title(title)
    print_estados(estados)
    while True:
        
        try:
            opcion = int(input(f'{Back.YELLOW} Seleccione un estado para la tarea {Style.RESET_ALL}: '))
            
            if validar_opcion(opcion, range(1, len(estados)+1)):
                return estados[opcion-1]
            
            # print_mensaje("seleccione una opción del menu.", 'error')
            error = ("seleccione una opción del menu.", 'error')
            # print_estados(estados)
            clear_window()
            print_title(title, error, estados)
        except:
            # print_mensaje("ingrese un número valido.", 'error')
            error = ("ingrese un número valido.", 'error')
            # print_estados(estados)
            clear_window()
            print_title(title, error, estados)

def print_title(title, error_msg=None, estados=None):
    print(f"{(Fore.BLUE + '=' + Style.RESET_ALL) * len_caracter}")
    print(f"\t\t{Fore.BLUE}{title.upper()}{Style.RESET_ALL}")
    print(f"{(Fore.BLUE + '=' + Style.RESET_ALL) * len_caracter}")
    
    if error_msg != None:
        print_mensaje(error_msg[0], error_msg[1])
    
    if estados != None:
        print_estados(estados)

def return_menu():
    _ = input(f"{Back.GREEN} ENTER: para volver al Menu Principal. {Style.RESET_ALL}")
    return True

###############################
###############################
###############################
#       Start program         #
###############################
###############################
###############################

nombre = get_username()

obj_registro = Registro(nombre)

print_menu(menu, nombre)

while True:
    opcion_menu = get_opcion_menu(menu, nombre)

    if opcion_menu == 0: # Termina el programa
        clear_window()
        
        print((Fore.BLUE + '=' + Style.RESET_ALL) * len_caracter)
        print("\t\tPROGRAMA FINALIZADO.")
        print((Fore.BLUE + '=' + Style.RESET_ALL) * len_caracter)

        waiting_msg(3)
        clear_window()        
        break

    # Crea una nueva tarea
    if opcion_menu == 1: # Crear
        # Limpia la terminal
        clear_window()
        
        # Título de la interfaz actual
        title = "agregar nueva tarea"

        # Muestra el título de la interfaz actual
        print_title(title)
        
        # Tarea ingresada por el usuario
        tarea = input(f"{Back.YELLOW} Ingrese el nombre de la tarea {Style.RESET_ALL}: ")

        # Estado ingresado por el usuario
        estado = get_opcion_estado(estados, title)
        
        # Verifica si la tarea se creo correctamente
        if obj_registro.create_tarea(tarea, estado):
            clear_window()
            print(f"{Back.GREEN}Registro creado con exito.{Style.RESET_ALL}")
            waiting_msg()
            clear_window()
        else:
            clear_window()
            print(f"{Back.RED}Error{Style.RESET_ALL}: no se pudo crear el registro.")
            waiting_msg()
            clear_window()
        print_menu(menu, nombre)
    
    # Modifica una tarea
    elif opcion_menu == 2: # Modifica
        # Limpia la terminal
        clear_window()        

        # Título de la interfaz actual
        title = "modificar tarea"

        # Muestra el título de la interfaz actual
        print_title(title)

        # Tarea ingresada por el usuario
        tarea = input(f"{Back.YELLOW}Ingrese el nombre de la tarea a modificar{Style.RESET_ALL}: ")

        # Nuevo estado para la tarea
        estado = get_opcion_estado(estados, title)
        
        # Verifica si la tarea fue modificada correctamente
        if obj_registro.set_tarea(tarea, estado):
            clear_window()
            print(f"{Back.GREEN}Tarea modificada con exito.{Style.RESET_ALL}")
            waiting_msg()
            clear_window()
        else:
            clear_window()
            print(f"{Fore.RED}Error{Style.RESET_ALL}: no se pudo modificar la tarea.")
            waiting_msg()
            clear_window()
        print_menu(menu, nombre)
        
    # Elimina una tarea
    elif opcion_menu == 3: # elimina
        # Limpia la terminal
        clear_window()        

        # Título de la interfaz actual
        title = "eliminar tarea"

        # Muestra el título de la interfaz actual
        print_title(title)

        tarea = input(f"{Back.YELLOW}Ingrese la tarea a eliminar{Style.RESET_ALL}: ")
                
        # Verifica si la tarea fue eliminada correctamente
        if obj_registro.delete_tarea(tarea):
            clear_window()
            print(f"{Back.GREEN}Tarea eliminada con exito.{Style.RESET_ALL}")
            waiting_msg()
            clear_window()
        else:
            clear_window()
            print(f"{Fore.RED}Error{Style.RESET_ALL}: no se pudo eliminar la tarea.")
            waiting_msg()
            clear_window()
        print_menu(menu, nombre)
        
    # Muestra el contenido del Registro
    elif opcion_menu == 4: # muestra
        clear_window()
        obj_registro.show_tareas()
       
        if return_menu():
            clear_window()
            print_menu(menu, nombre)
    
    # Cambia el nombre del usuario
    elif opcion_menu == 5:
        # Limpia la terminal
        clear_window()        

        # Título de la interfaz actual
        title = "cambiar nombre de usuario"

        # Muestra el título de la interfaz actual
        print_title(title)

        # nombre_nuevo = input(f"{Back.YELLOW}Ingrese el nuevo nombre del usuario{Style.RESET_ALL}: ")
        nombre = get_username("Ingrese el nuevo nombre del usuario")
        obj_registro.set_name = nombre

        clear_window()
        print(f"{Back.GREEN}Nombre cambiado con exito.{Style.RESET_ALL}")
        waiting_msg()
        clear_window()
        print_menu(menu, nombre)
