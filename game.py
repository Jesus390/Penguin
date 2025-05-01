# Gameplay - d:-)

# Colores Ansi
ansi_color_rojo = "\033[0;49;31m"
ansi_color_verde = "\033[0;49;32m"
ansi_color_amarillo = "\033[0;49;33m"

ansi_bg_rojo = "\033[7;49;31m"
ansi_bg_verde = "\033[7;49;32m"
ansi_bg_amarillo = "\033[7;49;33m"

ansi_end = "\033[0m"

# lista de las palabras que estara oculta
lista_palabras_a_encontrar = ['Playa', 'Manta', 'Vista','Noche','Altar',
                  'Silla','Metro','Justo','Caída','Fuego',
                  'Tumba','Hongo','Cayos','Arena',]


# Imprime una linea horizontal
# Se utiliza para separar textos al imprimir 
def separador(caracter='-', longitud=50):
    print(caracter * longitud)


# Retorna un numero para el indice de una lista
# PD.: esto seria el indice para obtener la palabra oculta
def get_palabra_oculta(lista):
    longitud_lista = len(lista)
    while True:
        try:
            indice = int(input(f"Ingresa un numero entre 0 y {longitud_lista}"))
            if indice > longitud_lista or indice < 0: 
                print(f"{ansi_color_rojo}Error{ansi_end}: ingresa un numero entre 0 y {len(lista)}")    
                continue
            print("Se ha generado una palabra oculta.")
            separador()
            return indice
        except:
            print(f"{ansi_color_rojo}Error{ansi_end}: ingresa un numero entre 0 y {len(lista)}")


# Retorna la palabra ingresada por el usuario
# Obs.: solamente retorna si la palabra cumple con una longitud dada
def get_palabra(cantidad_caracteres):
    palabra = input(f"Ingrese una palabra de {cantidad_caracteres} caracteres.")
    while not len(palabra) == cantidad_caracteres:
        separador()
        print(f"{ansi_color_rojo}Error{ansi_end}: la longitud ingresada de la palabra debe ser {cantidad_caracteres}.\nPalabra: {palabra}, longitud: {len(palabra)}")
        palabra = input(f"Ingrese una palabra de {cantidad_caracteres}")
    return palabra


# Crea una grilla de la lista dada
def imprimir_grilla(lista):
    formato = ("+" + "-"*3)*len(lista) + "+\n"
    aux = "\t" + formato
    # aux += "+\n"
    for i, elemento in enumerate(lista):
        if i == 0:
            aux += "\t"
        aux +=  "| " + elemento + " " if i < len(lista)-1 else "| " + elemento + " |\n" 
    aux += "\t" + formato
    print(aux)


def obtener_fila_verificada(palabra_a_encontrar, palabra_ingresada):
    # Segundo paso: definir la cantidad de letras de la palabra a encontrar.
    cantidad_de_letras_de_palabra_a_encontrar = 5

    # Tercer paso: Crear una lista vacia para guardar las letras verificadas.
    letras_verificadas = []

    # Cuarto paso: se recorre cada posicion de la palabra.
    for posicion in range(cantidad_de_letras_de_palabra_a_encontrar):
        # Quinto paso: comparar las letras en la misma posicion.
        las_letras_son_iguales = palabra_a_encontrar[posicion] == palabra_ingresada[posicion]

        # Sexto paso: se verifica si la letra existe en la palabra.
        la_letra_existe_en_la_palabra = palabra_ingresada[posicion] in palabra_a_encontrar

        if las_letras_son_iguales:
            letras_verificadas.append(ansi_color_verde + palabra_ingresada[posicion] + ansi_end)
            # letras_verificadas.append("[" + palabra_ingresada[posicion] + "]")
        elif la_letra_existe_en_la_palabra:
            letras_verificadas.append(ansi_color_amarillo + palabra_ingresada[posicion] + ansi_end)
            # letras_verificadas.append("(" + palabra_ingresada[posicion] + ")")
        else:
            letras_verificadas.append(ansi_color_rojo + palabra_ingresada[posicion] + ansi_end)
            # letras_verificadas.append(palabra_ingresada[posicion])
        
    return letras_verificadas


print(f"\t{ansi_bg_verde}*** ADIVINA LA PALABRA OCULTA!!!{ansi_end}")
separador()

# Solicita al usuario un numero dado la cantidad de elementos que
# contiene la lista de las palabras ocultas
indice_palabra_oculta = get_palabra_oculta(lista_palabras_a_encontrar)

# Obtenemos la palabra que estará oculta
palabra_a_encontrar = lista_palabras_a_encontrar[indice_palabra_oculta]

# Muestra una pequeña información para el usuario
print("INFO")
print(f"{ansi_color_verde}- Si la letra existe y está en la posición correcta la letra será de color verde.{ansi_end}")
print(f"{ansi_color_amarillo}- Si la letra existe y no está en la posición correcta la letra será de color amarilla.{ansi_end}")
print(f"{ansi_color_rojo}- Si la letra no existe en la palabra oculta será de color roja.{ansi_end}")
separador()

# Cantidad de intentos
intentos = 3
print("Intentos: 3")
separador()

# Recorremos cantidad de intentos disponibles
while intentos > 0:
    
    # Solicita una palabra al usuario
    # PD.: continua solicitando hasta que el usuario ingrese una
    # palabra con la longitud pasada como argumento
    palabra_ingresada = get_palabra(5)

    # Verifica si las letras de la palabra ingresada por el usuario
    # son iguales o están en la palabra oculta
    valor = obtener_fila_verificada(palabra_a_encontrar, palabra_ingresada)

    # Imprime una grilla alrededor de los datos verficados
    imprimir_grilla(valor)

    # Muestra los intentos faltantes
    intentos -= 1
    print(f'{ansi_bg_amarillo}- Te quedan {intentos} intentos.{ansi_end}')
    separador()
    
    # Verifica si la palabra oculta es igual a la palabra ingresada por
    # el usuario
    if palabra_a_encontrar == palabra_ingresada:        
        separador()
        print(f"\t  {ansi_color_verde}Felicidades, Ganaste!!!{ansi_end}")
        separador()
        break
else:
    print(f'{ansi_color_rojo}===> TE QUEDASTE SIN INTENTOS <==={ansi_end}')
    print(f'- La palabra oculta es: {ansi_color_verde}{palabra_a_encontrar}{ansi_end}')





