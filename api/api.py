# Flask: Crea la aplicación Flask
# jsonify: Convierte datos Python (como diccionarios y listas) a formato JSON y los devuelve como respuesta HTTP.
#request: Permite acceder a la información de la solicitud HTTP, como parámetros o datos del cuerpo de la solicitud.
# send_from_directory: Sirve archivos estáticos desde un directorio específico, como archivos HTML, imágenes, etc.
# import os: Importa la biblioteca estándar de Python para interactuar con el sistema operativo, especialmente útil para trabajar con rutas de archivos y directorios.
# import nbformat: Importa la biblioteca nbformat, que es parte del ecosistema de Jupyter. Esta librería permite leer y escribir archivos de notebooks de Jupyter en formato .ipynb.

from flask import Flask, jsonify, request, send_from_directory
import os
import nbformat

#Crea una instancia de la aplicación Flask.
# __name__ es un argumento que le dice a Flask cómo buscar recursos como archivos estáticos y plantillas. Aquí se usa para configurar el nombre del módulo.
# static_folder='static' le indica a Flask que los archivos estáticos (como CSS, JavaScript e imágenes) estarán en el directorio llamado static.

app = Flask(__name__, static_folder='static')

#DOCUMENTS_FOLDER = 'documentos': Define una constante que especifica el nombre del directorio donde se almacenan los archivos .ipynb. En este caso, el directorio se llama documentos.
# app.config['DOCUMENTS_FOLDER'] = DOCUMENTS_FOLDER: Esta línea guarda la ruta del directorio donde están los notebooks Jupyter en la configuración de la aplicación. Esto es útil si se necesita acceder a la ruta desde diferentes partes de la aplicación.

# Directorio donde están los documentos .ipynb
DOCUMENTS_FOLDER = 'documentos'  #que contiene la ruta al directorio donde están guardados los documentos.
app.config['DOCUMENTS_FOLDER'] = DOCUMENTS_FOLDER

#@app.route('/'): Esta es una ruta que corresponde a la URL raíz de la aplicación (es decir, http://127.0.0.1:5000/). Los usuarios que visiten esta URL accederán a la función home.
# def home():: Define la función home que se ejecutará cuando un usuario visite la URL raíz.
# return send_from_directory('static', 'index.html'):
# Flask va a devolver el archivo index.html ubicado en el directorio static.
# Esto significa que al visitar la página de inicio (/), el servidor Flask servirá el archivo index.html que puede ser la página de presentación o el frontend de la API.

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

#@app.route('/documentos', methods=['GET']): Esta es una ruta HTTP para la URL /documentos, que acepta solicitudes GET. Cuando un cliente hace una solicitud GET a esta ruta, se ejecuta la función obtener_documentos.
# def obtener_documentos():: Define la función obtener_documentos, que maneja la lógica para devolver la lista de documentos en la carpeta documentos.
# archivos = [f for f in os.listdir(DOCUMENTS_FOLDER) if f.endswith('.ipynb')]:
# Usa os.listdir(DOCUMENTS_FOLDER) para obtener una lista de todos los archivos en el directorio documentos.
# Filtra solo los archivos que terminan en .ipynb (los notebooks Jupyter).
# if not archivos:: Verifica si la lista archivos está vacía (es decir, si no hay archivos .ipynb en el directorio).
# return jsonify({"mensaje": "No hay archivos .ipynb en el directorio."}), 404: Si no se encuentran archivos .ipynb, se devuelve un mensaje en formato JSON con el código de estado HTTP 404 (No encontrado).
# return jsonify(archivos), 200: Si se encuentran archivos .ipynb, se devuelve una lista de los archivos en formato JSON con el código de estado HTTP 200 (Éxito).
# except FileNotFoundError:: Si la carpeta documentos no existe, captura el error FileNotFoundError.
# return jsonify({"mensaje": "No se encontró el directorio de documentos"}), 404: Si la carpeta no se encuentra, devuelve un mensaje de error con el código de estado 404.

@app.route('/documentos', methods=['GET'])
def obtener_documentos():
    try:
        archivos = [f for f in os.listdir(DOCUMENTS_FOLDER) if f.endswith('.ipynb')]
        
        if not archivos:
            return jsonify({"mensaje": "No hay archivos .ipynb en el directorio."}), 404
        
        return jsonify(archivos), 200
    except FileNotFoundError:
        return jsonify({"mensaje": "No se encontró el directorio de documentos"}), 404
    
#@app.route('/documentos/contenido/<nombre>', methods=['GET']): Esta ruta maneja las solicitudes GET a la URL /documentos/contenido/<nombre>, donde <nombre> es el nombre del archivo .ipynb que queremos ver. Flask lo captura y lo pasa como argumento a la función ver_contenido_documento.
# def ver_contenido_documento(nombre):: Define la función que maneja la solicitud para obtener el contenido de un notebook específico.
# notebook_path = os.path.join(DOCUMENTS_FOLDER, nombre): Construye la ruta completa al archivo .ipynb utilizando el nombre del archivo proporcionado y la carpeta de documentos.
# if os.path.exists(notebook_path) and nombre.endswith('.ipynb'):: Verifica si el archivo existe en el sistema y si tiene la extensión .ipynb.
# with open(notebook_path, 'r', encoding='utf-8') as f:: Abre el archivo .ipynb en modo lectura, utilizando la codificación UTF-8.
# notebook_content = nbformat.read(f, as_version=4): Usa nbformat.read() para leer el contenido del notebook y cargarlo en un objeto que representa la estructura del notebook.
# El resto del bloque procesa las celdas del notebook:
# Itera sobre cada celda del notebook.
# Si la celda es de tipo code, extrae el código y las salidas generadas.
# Si la celda es de tipo markdown, simplemente extrae el texto.
# return jsonify(contenido), 200: Devuelve el contenido del notebook como una respuesta JSON con el código de estado HTTP 200.
# except Exception as e:: Si ocurre algún error, se captura y se devuelve un mensaje de error.

@app.route('/documentos/contenido/<nombre>', methods=['GET'])
def ver_contenido_documento(nombre):
    try:
        notebook_path = os.path.join(DOCUMENTS_FOLDER, nombre)
        
        if os.path.exists(notebook_path) and nombre.endswith('.ipynb'):
            with open(notebook_path, 'r', encoding='utf-8') as f:
                notebook_content = nbformat.read(f, as_version=4)

            contenido = []
            for cell in notebook_content.cells:
                if cell.cell_type == 'code':
                    cell_data = {
                        'tipo': 'código',
                        'contenido': cell.source,
                        'salidas': []
                    }

                    # Procesar las salidas de la celda de código
                    for output in cell.outputs:
                        if 'text' in output:
                            cell_data['salidas'].append({
                                'tipo': 'texto',
                                'contenido': output['text']
                            })
                        elif 'data' in output:
                            # Revisar si hay salida de imagen u otro tipo de datos
                            if 'image/png' in output['data']:
                                cell_data['salidas'].append({
                                    'tipo': 'imagen',
                                    'contenido': output['data']['image/png']
                                })
                            elif 'application/json' in output['data']:
                                cell_data['salidas'].append({
                                    'tipo': 'json',
                                    'contenido': output['data']['application/json']
                                })
                            elif 'text/html' in output['data']:
                                cell_data['salidas'].append({
                                    'tipo': 'html',
                                    'contenido': output['data']['text/html']
                                })
                    contenido.append(cell_data)
                
                elif cell.cell_type == 'markdown':
                    contenido.append({
                        'tipo': 'texto',
                        'contenido': cell.source
                    })
            
            return jsonify(contenido), 200
        else:
            return jsonify({'mensaje': 'Archivo no encontrado o formato incorrecto'}), 404
    except Exception as e:
        return jsonify({'mensaje': str(e)}), 500


# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
