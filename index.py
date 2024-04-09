from flask import Flask, request, render_template, flash, redirect, url_for
import os
import pandas as pd
import codecs
from app.read import leer_archivo_excel

app = Flask(__name__)
app.secret_key = "clave_secreta"  # Clave secreta para usar flash en Flask

# Define la configuración del directorio de carga
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def crear_directorio_uploads():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

# Definir la ruta al directorio donde se encuentra el archivo Excel
directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_archivo_excel = os.path.join(directorio_actual, 'BW - Formato para Carga de Datos  RCSA - Financieras.xlsx')

@app.route('/leer_excel/<nombre_hoja>')
def leer_excel(nombre_hoja):
    datos_excel = leer_archivo_excel(ruta_archivo_excel, nombre_hoja, 4)
    if datos_excel is not None:
        return render_template('mostrar_excel.html', datos=datos_excel.to_html())
    else:
        return "Error al leer el archivo Excel."

@app.route('/', methods=['GET', 'POST'])
def principal():
    encabezados_iguales = None
    encabezados_no_coincidentes_plano = []
    encabezados_no_coincidentes_excel = []
    campos_con_descripciones = []
    comparacion_encabezados = []  

    if request.method == 'POST':
        archivo_plano = request.files['archivo_plano']
        if archivo_plano.filename != '':
            nombre, extension = os.path.splitext(archivo_plano.filename)
            if extension.lower() == '.txt':
                archivo_plano_path = os.path.join(app.config['UPLOAD_FOLDER'], archivo_plano.filename)
                archivo_plano.save(archivo_plano_path)
                
                # Verificar la codificación del archivo
                with open(archivo_plano_path, 'rb') as f:
                    encabezado = f.readline()
                    if encabezado.startswith(codecs.BOM_UTF8):
                        flash('El archivo debe estar codificado en ANSI.', 'error')
                        os.remove(archivo_plano_path)
                        return redirect(url_for('principal'))

                # Leer el archivo plano y reemplazar los NaN con cadenas vacías
                df_plano = pd.read_csv(archivo_plano_path, sep='\t')
                df_plano = df_plano.where(pd.notnull(df_plano), '')  # Reemplazar NaN con cadenas vacías

                # Obtener los encabezados del archivo plano después de reemplazar NaN
                encabezados_plano = df_plano.columns.tolist()

                archivo_excel = 'BW - Formato para Carga de Datos  RCSA - Financieras.xlsx'
                nombre_hoja = 'Datos Clientes'
                inicio_tabla = 4
                fin_tabla = 90
                columnas = "A:G"
                datos_excel = leer_archivo_excel(archivo_excel, nombre_hoja, inicio_tabla, fin_tabla, columnas)
                
                if datos_excel is not None:
                    columna_excel = datos_excel['Nombre del Campo\nen la Tabla de Importación tblIMPORT_CUSTOMERS '].tolist()

                    encabezados_iguales = [header for header in encabezados_plano if header in columna_excel]
                    encabezados_no_coincidentes_plano = [header for header in encabezados_plano if header not in columna_excel]
                    encabezados_no_coincidentes_excel = [header for header in columna_excel if header not in encabezados_plano]

                    descripcion_campos_financieros = datos_excel['Descripción del Campo - Financieras'].tolist()
                    campos_minimos_obligatorios = datos_excel['Campos Minimos Obligatorios para el Sistema\nRMC - Financieras'].tolist()
                    obligatoriedad_sb_uafe = datos_excel['Obligatoriedad de Organismos de Control SB y UAFE- Financieras'].tolist()
                    obligatoriedad_matriz_riesgo = datos_excel['Obligatoriedad para Matrices de Riesgo (RDP) - Financieras'].tolist()

                    campos_con_descripciones = [(columna_excel, descripcion, campos_minimos_obligatorios, obligatorio_sb_uafe, obligatorio_matriz_riesgo) for columna_excel, descripcion, campos_minimos_obligatorios, obligatorio_sb_uafe, obligatorio_matriz_riesgo in zip(columna_excel, descripcion_campos_financieros, campos_minimos_obligatorios, obligatoriedad_sb_uafe, obligatoriedad_matriz_riesgo)]

                    comparacion_encabezados = []

                    for header in encabezados_plano:
                        if header in encabezados_iguales:
                            comparacion_encabezados.append('Si')
                        else:
                            comparacion_encabezados.append('No existe')
                    
                    for header in encabezados_no_coincidentes_excel:
                        comparacion_encabezados.append('No existe')

                else:
                    flash('No se pudo leer el archivo Excel.', 'error')
                    os.remove(archivo_plano_path)
                    return redirect(url_for('principal'))
            else:
                flash('Solo se permiten archivos de tipo TXT.', 'error')
                return redirect(url_for('principal'))

    return render_template('formulario.html', encabezados_iguales=encabezados_iguales, 
                           encabezados_no_coincidentes_plano=encabezados_no_coincidentes_plano,
                           encabezados_no_coincidentes_excel=encabezados_no_coincidentes_excel,
                           campos_con_descripciones=campos_con_descripciones,
                           comparacion_encabezados=comparacion_encabezados)

                           
if __name__ == '__main__':
    crear_directorio_uploads()
    app.run(debug=True, port=5017)