# Importamos Flask, Response y jsonify para construir la API
from flask import Flask, Response, jsonify
import csv  # Para leer el archivo CSV

# Creamos una instancia de la aplicación Flask
app = Flask(__name__)

# Ruta del archivo CSV que será leído
CSV_FILE_PATH = "promedio_temp.csv"

# Ruta de la API que sirve el contenido del CSV en formato JSON
@app.route('/csv')
def serve_csv():
    try:
        # Abrimos el archivo CSV en modo lectura
        with open(CSV_FILE_PATH, newline='') as csvfile:
            # Usamos DictReader para leer cada fila como un diccionario
            reader = csv.DictReader(csvfile)
            data = list(reader)  # Convertimos el lector en una lista de diccionarios
        # Retornamos los datos como JSON
        return jsonify(data)
    except Exception as e:
        # Si ocurre algún error, retornamos el mensaje de error y código 500
        return {"error": str(e)}, 500

# Punto de entrada principal de la aplicación
if __name__ == '__main__':
    # Ejecutamos la app en el puerto 5000 accesible desde cualquier IP
    app.run(host='0.0.0.0', port=5000)
