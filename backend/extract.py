import pdfplumber
import pandas as pd
import re
from backend.utils import obtener_neto

def extraer_y_procesar_tablas(pdf_path):
    """
    Extrae y procesa tablas desde un PDF.
    """
    criterios_titulo_nombre = {
        "Titulo obra / Nombre": r"^.{1,50}"
    }

    criterios_resto = {
        "Prof.": r"^E\s",
        "Cód.Obra": r"^\d{7}",
        "%": r"^\d+(\.\d+)?|^\.\d+",
        "Fecha": r"^\d{2}/\d{2}/\d{4}",
        "Terr.": r"^",
        "Cant.": r"^\d+"
    }

    columnas = list(criterios_titulo_nombre.keys()) + list(criterios_resto.keys()) + ["Neto"]
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
                        nuevo_df = pd.DataFrame(columns=columnas)  # Crear nuevo DataFrame con todas las columnas

                        # Procesar las filas una por una
                        for _, fila in df_filtrado.iterrows():
                            fila_str = " ".join(str(celda).strip() for celda in fila if pd.notna(celda))  # Concatenar toda la fila
                            if " E " in fila_str:
                                # Separar la fila en las dos partes
                                parte_titulo_nombre, parte_resto = fila_str.split(" E ", 1)
                                parte_resto = "E " + parte_resto  # Añadir " E " al principio de parte_resto
                                
                                # Verificar si parte_resto tiene un salto de línea al final
                                if parte_resto.__contains__("\n"):
                                    #contenido_extra = parte_resto.split("\n", 1)[1].strip()  # Contenido después del '\n'
                                    parte_resto = parte_resto.split("\n", 1)[0].strip()  # Remover '\n' y lo que sigue
                                    #parte_titulo_nombre += f" {contenido_extra}"  # Agregar contenido extra a parte_titulo_nombre
                                
                                nueva_fila = []

                                # Procesar criterios_titulo_nombre
                                for columna, regex in criterios_titulo_nombre.items():
                                    match = re.search(regex, parte_titulo_nombre)
                                    if match:
                                        nueva_fila.append(match.group())
                                        parte_titulo_nombre = parte_titulo_nombre.replace(match.group(), "", 1).strip()
                                    else:
                                        nueva_fila.append(None)
                                
                                # Procesar criterios_resto
                                for columna, regex in criterios_resto.items():
                                    match = re.search(regex, parte_resto)
                                    if match:
                                        nueva_fila.append(match.group())
                                        parte_resto = parte_resto.replace(match.group(), "", 1).strip()
                                    else:
                                        nueva_fila.append(None)
                                
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
                        #print(f"Tabla válida encontrada en la página {num_pagina}:\n", nuevo_df)
                    else:
                        print(f"Tabla descartada en la página {num_pagina}: No tiene encabezado válido.")

    return tablas_procesadas
