import pdfplumber
import pandas as pd
import re
from backend.utils import obtener_neto, obtener_codigo_obra, obtener_posiciones_delimitadores
from backend.constants import DELIMITADORES, COLUMNAS

def extraer_y_procesar_tablas(pdf_path):
    """
    Extrae y procesa tablas desde un PDF.
    """
    
    tablas_procesadas = []

    with pdfplumber.open(pdf_path) as pdf:
        for num_pagina, pagina in enumerate(pdf.pages, start=1):
            tablas = pagina.extract_tables()
            if tablas:
                for tabla in tablas:
                    # Convertir la tabla en un DataFrame
                    df = pd.DataFrame(tabla)
                    
                    # Filtrar filas que NO comienzan con "Concepto:" ni "Total Concepto:"
                    df_filtrado = df[
                        ~df[0].astype(str).str.startswith("Concepto:") &
                        ~df[0].astype(str).str.startswith("Total Concepto:")
                    ]
                    
                    # Verificar si el DataFrame tiene contenido antes de continuar
                    if not df_filtrado.empty:
                        nuevo_df = pd.DataFrame(columns=COLUMNAS)  # Crear nuevo DataFrame con todas las columnas

                        # Procesar las filas una por una
                        for _, fila in df_filtrado.iterrows():
                            fila_str = " ".join(str(celda).strip() for celda in fila if pd.notna(celda))  # Concatenar toda la fila
                            
                            (posicion, posicion_final) = obtener_posiciones_delimitadores(fila_str)

                            if (posicion is not None) and (posicion_final is not None):
                                # Separar la fila en las dos partes
                                parte_titulo_nombre = fila_str[:posicion]
                                parte_resto = fila_str[posicion_final:]
                                
                                # Verificar si parte_resto tiene un salto de línea al final
                                if parte_resto.__contains__("\n"):
                                    parte_resto = parte_resto.split("\n", 1)[0].strip()  # Remover '\n' y lo que sigue
                                
                                nueva_fila = []
                                nueva_fila.append(parte_titulo_nombre) # Agregar criterios_titulo_nombre

                                codigo_obra = obtener_codigo_obra(parte_resto)
                                nueva_fila.append(codigo_obra)
                                
                                resultado = obtener_neto(parte_resto)
                                if resultado is not None:
                                    nueva_fila.append(resultado)
                                else:
                                    nueva_fila.append("0")

                                # Añadir la fila procesada al nuevo DataFrame
                                nuevo_df.loc[len(nuevo_df)] = nueva_fila
                        
                        nuevo_df.reset_index(drop=True, inplace=True)  # Reiniciar el índice
                        
                        # Guardar la tabla procesada
                        tablas_procesadas.append(nuevo_df)
                    else:
                        print(f"Tabla descartada en la página {num_pagina}: No tiene encabezado válido.")

    return tablas_procesadas
