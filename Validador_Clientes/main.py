import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from funciones import seleccionar_archivo_y_ejecutar, ejecutar_con_hoja_seleccionada, guardar_datos_seleccionados, obtener_seleccion
import Validaciones
from Validaciones import validacion_RS

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Interfaz Gráfica")

# Crear pestañas
pestañas = ttk.Notebook(ventana)

# Pestaña principal
pestana_principal = ttk.Frame(pestañas)
pestañas.add(pestana_principal, text="Principal")

# Pestaña adicional
pestana_adicional = ttk.Frame(pestañas)
pestañas.add(pestana_adicional, text="Adicional")

# Variables de control
archivo_seleccionado = tk.StringVar()
hojas_disponibles = []  # Variable para almacenar las hojas disponibles
df_relationship = validacion_RS.ejecutar_codigo

# Función para limpiar el TextBox
def limpiar_textbox():
    text_box.delete("1.0", tk.END)

# Función para guardar la selección actual en la lista global
def guardar_seleccion():
    # Obtener la selección actual
    datos_seleccionados = obtener_seleccion(text_box)

    # Añadir la selección a la lista global
    datos_seleccionados_lista.append(datos_seleccionados)

    # Limpiar el contenido actual del frame
    for widget in frame_selecciones_guardadas.winfo_children():
        widget.destroy()

    # Mostrar las selecciones guardadas en labels
    for i, seleccion in enumerate(datos_seleccionados_lista, start=1):
        label = ttk.Label(frame_selecciones_guardadas, text=f"{i}. {seleccion}")
        label.pack()
    
    print(datos_seleccionados_lista)

# Función para manejar el clic en el TextBox
def manejar_clic(event):
    # Obtener el índice de la línea clicada
    index = text_box.index(tk.CURRENT)
    
    # Realizar operaciones basadas en el índice (index)
    # Puedes imprimirlo o realizar cualquier otra operación aquí
    print(f"Índice clicado: {index}")

# Función para actualizar las hojas en el Listbox
def actualizar_hojas(listbox_hojas):
    hojas_disponibles = seleccionar_archivo_y_ejecutar(archivo_seleccionado)
    listbox_hojas.delete(0, tk.END)  # Limpiar el Listbox
    for hoja in hojas_disponibles:
        listbox_hojas.insert(tk.END, hoja)

# Lista para almacenar las selecciones guardadas
datos_seleccionados_lista = []

# Frame para contener los labels con las selecciones guardadas
frame_selecciones_guardadas = ttk.Frame(pestana_adicional)
frame_selecciones_guardadas.grid(row=1, column=0, columnspan=3, pady=10)

# Label para mostrar los datos seleccionados
label_datos_seleccionados = ttk.Label(pestana_adicional, text="Datos Seleccionados:")
label_datos_seleccionados.grid(row=0, column=0, columnspan=3, pady=10)

# Frame para contener los labels con los datos seleccionados
frame_datos_seleccionados = ttk.Frame(pestana_principal)
frame_datos_seleccionados.grid(row=2, column=0, columnspan=3, pady=10)

# Labels para mostrar los datos seleccionados
labels_datos_seleccionados = []

# Función para actualizar los labels con los datos seleccionados
def actualizar_labels(datos_seleccionados):
    # Limpiar el contenido actual del frame
    for widget in labels_datos_seleccionados:
        widget.destroy()
    
    # Dividir la cadena en líneas basadas en el salto de línea
    lineas = datos_seleccionados.split('\n')

    # Mostrar los nuevos datos seleccionados en labels
    for i, linea in enumerate(lineas, start=1):
        label = ttk.Label(frame_datos_seleccionados, text=f"{i}. {linea}")
        label.pack()
        labels_datos_seleccionados.append(label)

# Función para generar el informe de errores
def generar_informe():
    # Asegurarse de tener acceso a df_relationship
    global df_relationship

    print(df_relationship)
    print(datos_seleccionados_lista)

    # Llamar a la función para generar el informe de errores
    validacion_RS.generar_informe_errores(df_relationship, datos_seleccionados_lista)

# Crear y configurar los widgets en la pestaña principal
label_archivo = tk.Label(pestana_principal, text="Archivo:")
entry_archivo = tk.Entry(pestana_principal, textvariable=archivo_seleccionado, state="readonly")
button_seleccionar = tk.Button(pestana_principal, text="Seleccionar Archivo", command=lambda: seleccionar_archivo_y_ejecutar(archivo_seleccionado, listbox_hojas))
label_hojas = tk.Label(pestana_principal, text="Hojas disponibles:")
listbox_hojas = tk.Listbox(pestana_principal, selectmode=tk.SINGLE)
button_ejecutar = tk.Button(pestana_principal, text="Ejecutar", command=lambda: ejecutar_con_hoja_seleccionada(archivo_seleccionado, listbox_hojas, text_box))
text_box = tk.Text(pestana_principal, height=20, width=70)
button_limpiar = tk.Button(pestana_principal, text="Limpiar TextBox", command=limpiar_textbox)
button_guardar = tk.Button(pestana_principal, text="Generar Informe", command=lambda: generar_informe)

# Botón para guardar la selección y actualizar los labels
button_guardar_seleccion = ttk.Button(pestana_principal, text="Guardar Selección", command=guardar_seleccion)

# Asignar el evento clic al TextBox
text_box.bind("<ButtonRelease-1>", manejar_clic)

# Posicionar los widgets en la pestaña principal
label_archivo.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_archivo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
button_seleccionar.grid(row=0, column=2, padx=5, pady=5)
label_hojas.grid(row=1, column=0, padx=5, pady=5, sticky="e")
listbox_hojas.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
button_ejecutar.grid(row=1, column=2, padx=5, pady=5)
text_box.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
button_limpiar.grid(row=3, column=0, padx=5, pady=5)
button_guardar.grid(row=3, column=1, padx=5, pady=5)
button_guardar_seleccion.grid(row=4, column=0, columnspan=3, pady=10)

# Crear y configurar los widgets en la pestaña adicional (puedes personalizar según tus necesidades)
label_adicional = tk.Label(pestana_adicional, text="Contenido de la pestaña adicional")
label_adicional.grid(row=0, column=0, padx=5, pady=5)

# Pack de la pestaña
pestañas.pack(expand=1, fill="both")

# Iniciar el bucle de eventos
ventana.mainloop()
