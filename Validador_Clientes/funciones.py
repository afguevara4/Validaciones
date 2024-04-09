import pandas as pd
import tkinter as tk
from tkinter import filedialog
import Validaciones
from Validaciones import validacion_RS
import Funciones
from Funciones import funciones_Word

# Lista para almacenar los datos seleccionados
datos_seleccionados_lista = []

# Función para obtener las hojas disponibles en el archivo Excel
def obtener_hojas_disponibles(archivo_path):
    try:
        xls = pd.ExcelFile(archivo_path)
        return xls.sheet_names
    except Exception as e:
        print("Error al obtener las hojas del archivo:", e)
        return []
    
# Función para seleccionar el archivo Excel y ejecutar el código
def seleccionar_archivo_y_ejecutar(archivo_seleccionado, listbox_hojas):
    archivo_path = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=[("Archivos Excel", "*.xlsx *.xls")])
    if archivo_path:
        try:
            xls = pd.ExcelFile(archivo_path)
            hojas_disponibles = xls.sheet_names
            archivo_seleccionado.set(archivo_path)
            listbox_hojas.delete(0, tk.END)  # Limpiar el Listbox
            for hoja in hojas_disponibles:
                listbox_hojas.insert(tk.END, hoja)
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error al obtener las hojas del archivo: {e}")
            return


# Función para ejecutar el código con la hoja seleccionada
def ejecutar_con_hoja_seleccionada(archivo_seleccionado, lista_hojas, text_box):
    if not lista_hojas.curselection():
        tk.messagebox.showerror("Error", "No se ha seleccionado una hoja.")
        return

    nombre_hoja = lista_hojas.get(lista_hojas.curselection())
    archivo_path = archivo_seleccionado.get()
    if archivo_path:
        # Capturar la salida de ejecutar_codigo
        import sys
        import io
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout

        validacion_RS.ejecutar_codigo(archivo_path, nombre_hoja)

        #Dentro de tu función en funciones.py que llama a ejecutar_codigo
        #datos_seleccionados_lista, doc_informe = validacion_RS.ejecutar_codigo(archivo_path, nombre_hoja)
        #verificar_codigo_y_generar_informe(datos_seleccionados_lista, doc_informe)

        # Restaurar la salida estándar
        sys.stdout = old_stdout

        # Obtener la salida capturada
        output = new_stdout.getvalue()

        # Imprimir la salida en el TextBox
        text_box.delete("1.0", tk.END)  # Limpiar el TextBox
        text_box.insert(tk.END, output)  # Mostrar datos en el TextBox

# Función para obtener los datos seleccionados en el TextBox
def obtener_seleccion(text_box):
    # Obtener el índice del primer y último carácter seleccionado
    inicio_seleccion = text_box.index(tk.SEL_FIRST)
    fin_seleccion = text_box.index(tk.SEL_LAST)

    # Obtener la línea y el carácter inicial y final
    inicio_linea, inicio_char = map(int, inicio_seleccion.split("."))
    fin_linea, fin_char = map(int, fin_seleccion.split("."))

    # Obtener el texto de la línea seleccionada
    datos_seleccionados = text_box.get(f"{inicio_linea}.{inicio_char}", f"{fin_linea}.{fin_char}")

    print(datos_seleccionados)

    # Aplicar un tag al texto seleccionado para resaltarlo
    tag_name = "seleccion"
    text_box.tag_add(tag_name, f"{inicio_linea}.{inicio_char}", f"{fin_linea}.{fin_char}")
    text_box.tag_config(tag_name, background="yellow", foreground="black")

    return datos_seleccionados

def guardar_datos_seleccionados(text_box, archivo_path, nombre_hoja):
    datos_seleccionados = obtener_seleccion(text_box)
    if datos_seleccionados:
        datos_seleccionados_lista.append(datos_seleccionados)
        print("Datos seleccionados guardados:", datos_seleccionados_lista)

        # Ahora, realizar la validación de errores y generar el informe
        df_relationship = validacion_RS.ejecutar_codigo(archivo_path, nombre_hoja)
        texto_resaltado = obtener_seleccion(text_box)

        # Mensajes de depuración
        print("Texto resaltado:", texto_resaltado)
        print("Errores:", df_relationship)

        # Verificar si hay texto resaltado antes de llamar a la función generar_informe_errores
        if texto_resaltado:
            validacion_RS.generar_informe_errores(df_relationship, texto_resaltado)
            tk.messagebox.showinfo("Información", "Informe generado con éxito.")
        else:
            tk.messagebox.showinfo("Información", "No hay texto resaltado para generar el informe.")
    else:
        tk.messagebox.showinfo("Información", "No hay datos seleccionados para guardar.")

# Función para verificar el código de relación y generar el informe
