def generar_tabla_resumida(tabla_combinada):
    """
    Genera la tabla resumen con las sumas de 'Neto' agrupadas por 'Cód.Obra' y 'Titulo obra / Nombre'.
    """
    # Limpieza y formato de la columna 'Neto'
    def limpiar_neto(valor):
        # Añadir '0' delante de valores que comienzan con '.'
        if valor.startswith("."):
            valor = "0" + valor
        # Reemplazar comas (separadores de miles)
        valor = valor.replace(",", "")
        # Convertir a flotante
        return float(valor)
    
    tabla_combinada['Neto'] = tabla_combinada['Neto'].apply(limpiar_neto)
    
    # Agrupar por 'Cód.Obra' y 'Titulo obra / Nombre' y sumar los valores de 'Neto'
    tabla_resumida = tabla_combinada.groupby(['Cód.Obra', 'Titulo obra / Nombre'], as_index=False)['Neto'].sum()
    tabla_resumida = tabla_resumida.sort_values(by='Neto', ascending=False)  # Orden descendente
    # Redondear los valores y agregar separadores de miles
    tabla_resumida['Neto'] = tabla_resumida['Neto'].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    
    # Renombrar la columna 'Neto' a 'Suma Neto'
    tabla_resumida.rename(columns={'Neto': 'Suma Neto'}, inplace=True)
    
    return tabla_resumida
