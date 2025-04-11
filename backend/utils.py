import re

def obtener_neto(cadena):
    # Paso 1: Invertir la cadena
    cadena_invertida = cadena[::-1]
    
    # Paso 2: Obtener los primeros 10 caracteres
    primeros_10 = cadena_invertida[:10]

    numeros = primeros_10.split(" ", 1)[0]
    
    # Paso 3: Reinvertir los 10 caracteres
    primeros_10_reinvertidos = numeros[::-1]

    return primeros_10_reinvertidos