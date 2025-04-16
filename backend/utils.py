import re
from backend.constants import DELIMITADORES

def obtener_neto(cadena):
    # Paso 1: Invertir la cadena
    cadena_invertida = cadena[::-1]
    
    # Paso 2: Obtener los primeros 10 caracteres
    primeros_10 = cadena_invertida[:10]

    numeros = primeros_10.split(" ", 1)[0]
    
    # Paso 3: Reinvertir los 10 caracteres
    primeros_10_reinvertidos = numeros[::-1]

    return primeros_10_reinvertidos

def obtener_codigo_obra(cadena):
    return cadena.strip()[:7]

def obtener_posiciones_delimitadores(fila_str):
    subcadena = fila_str[20:51]
    posicion = None
    posicion_final = None
    for delimitador in DELIMITADORES:
        if(delimitador in subcadena):
            # Obtener posición en la subcadena
            posicion_subcadena = subcadena.find(delimitador)
            # Calcular posición en el string original
            posicion = 20 + posicion_subcadena
            posicion_final = posicion + len(delimitador) - 1
    return posicion, posicion_final