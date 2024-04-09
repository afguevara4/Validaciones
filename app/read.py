import pandas as pd

def leer_archivo_excel(nombre_archivo, nombre_hoja, inicio_tabla, fin_tabla=None, columnas=None):
    try:
        # Leer el archivo Excel
        if fin_tabla and columnas:
            datos_excel = pd.read_excel(nombre_archivo, sheet_name=nombre_hoja, header=inicio_tabla, nrows=fin_tabla, usecols=columnas)
        else:
            datos_excel = pd.read_excel(nombre_archivo, sheet_name=nombre_hoja, header=inicio_tabla)
        
        # Reemplazar los valores NaN con cadenas vacías
        datos_excel = datos_excel.fillna('')  

        # Eliminar filas y columnas vacías
        datos_excel = datos_excel.dropna(how='all')  
        datos_excel = datos_excel.dropna(axis=1, how='all')  
        datos_excel.reset_index(drop=True, inplace=True)
        
        print("Nombres de las columnas:", datos_excel.columns.tolist())

        return datos_excel
    except Exception as e:
        print("Error al leer el archivo Excel:", e)
        return None
