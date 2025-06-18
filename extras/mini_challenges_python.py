"""
# Dia 1 - Inversión de una Cadena
Escribe un programa que invierta una cadena de caracteres dada por el
usuario.
"""

def invertir_cadena(cadena):
    cadena_invertida = ""
    for i in range(len(cadena) - 1, -1, -1):
        cadena_invertida += cadena[i]
    return cadena_invertida

cadena = input("Ingrese una cadena de caracteres: ")
cadena_invertida = invertir_cadena(cadena)
print("La cadena invertida es:", cadena_invertida)

"""# Dia 2 - Tabla de Multiplicar
Escribe un programa que muestre la tabla de multiplicar de un número
dado por el usuario.

"""

def tabla_multiplicar(numero):
    for i in range(1, 11):
        print(numero, "x", i, "=", numero * i)

numero = int(input("Ingrese un número: "))
tabla_multiplicar(numero)

"""# Dia 3 - Contar Vocales
Escribe un programa que cuente el número de vocales en una cadena
dada.

"""

def contar_vocales(cadena):
    vocales = "aeiouAEIOU"
    contador = 0
    for letra in cadena:
        if letra in vocales:
            contador += 1
    return contador

cadena = input("Ingrese una cadena de caracteres: ")
numero_vocales = contar_vocales(cadena)
print("El número de vocales en la cadena es:", numero_vocales)

"""# Dia 4 - Ordenar Lista
Escribe un programa que ordene una lista de números dada por el usuario
en orden ascendente.
"""

def ordenar_lista(lista):
    lista.sort()
    return lista

lista = input("Ingrese una lista de números separados por comas: ")
lista = [int(x) for x in lista.split(",")]
lista_ordenada = ordenar_lista(lista)
print("La lista ordenada es:", lista_ordenada)

"""# Dia 5 - Crear un Diccionario
Escribe un programa que cree un diccionario a partir de dos listas dadas:
una de claves y otra de valores.
"""

def crear_diccionario(claves, valores):
    diccionario = {}
    for i in range(len(claves)):
        diccionario[claves[i]] = valores[i]
    return diccionario

claves = input("Ingrese las claves del diccionario separados por comas: ")
claves = claves.split(",")
valores = input("Ingrese los valores del diccionario separados por comas: ")
valores = valores.split(",")
diccionario = crear_diccionario(claves, valores)
print("El diccionario creado es:", diccionario)

"""# Dia 6 - Conversión de Temperatura
Escribe un programa que convierta una temperatura dada en grados
Celsius a grados Fahrenheit.

"""

def celsius_a_fahrenheit(celsius):
    fahrenheit = (celsius * 9/5) + 32
    return fahrenheit

celsius = float(input("Ingrese la temperatura en grados Celsius: "))
fahrenheit = celsius_a_fahrenheit(celsius)
print("La temperatura en grados Fahrenheit es:", fahrenheit)

"""# Dia 7 - Juego de Piedra, Papel o Tijeras
Escribe un programa que permita al usuario jugar piedra, papel o tijeras
contra la computadora.

"""

import random
def jugar_piedra_papel_tijeras():
    opciones = ["piedra", "papel", "tijeras"]
    computadora = random.choice(opciones)
    usuario = input("Ingrese su elección (piedra, papel o tijeras): ")
    print("La computadora eligió:", computadora)
    if usuario == computadora:
        print("Empate")
    elif usuario == "piedra" and computadora == "tijeras":
        print("Ganaste")
    elif usuario == "papel" and computadora == "piedra":
        print("Ganaste")
    elif usuario == "tijeras" and computadora == "papel":
        print("Ganaste")
    else:
        print("Perdiste")

jugar_piedra_papel_tijeras()

"""# Dia 8 - Generador de Contraseñas Seguras
Escribe un programa que genere una contraseña segura de longitud
variable (entre 8 y 16 caracteres) que incluya letras mayúsculas,
minúsculas, números y símbolos.
"""

import random
def generar_contrasena(longitud):
    if longitud < 8 or longitud > 16:
        print("La longitud de la contraseña debe estar entre 8 y 16 caracteres")
        return
    caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    contrasena = ""
    for i in range(longitud):
        contrasena += random.choice(caracteres)
    return contrasena

longitud = int(input("Ingrese la longitud de la contraseña (entre 8 y 16 caracteres): "))
contrasena = generar_contrasena(longitud)
print("La contraseña generada es:", contrasena)