import pandas as pd

def combinar_tablas(tablas):
    """
    Combina todas las tablas procesadas en una sola.
    """
    return pd.concat(tablas, ignore_index=True)
