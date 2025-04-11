def generar_tabla_resumida(tabla_combinada):
    """
    Genera la tabla resumen con las sumas de 'Neto' agrupadas por 'Cód.Obra' y 'Titulo obra'.
    """
    tabla_combinada['Neto'] = tabla_combinada['Neto'].str.replace(",", "").astype(float)
    tabla_resumida = tabla_combinada.groupby(['Cód.Obra', 'Titulo obra / Nombre'], as_index=False)['Neto'].sum()
    tabla_resumida.rename(columns={'Neto': 'Suma Neto'}, inplace=True)
    return tabla_resumida
