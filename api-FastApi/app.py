# Importamos FastAPI y los tipos de respuesta que vamos a usar
from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse

# Importamos 'requests' para descargar archivos por HTTP y 'io' en caso de procesamiento con buffers
import requests
import io

# Creamos una instancia de la aplicación FastAPI
app = FastAPI()

# URL pública del archivo CSV almacenado en un bucket S3
PUBLIC_CSV_URL = "https://bucket-telematica.s3.us-east-1.amazonaws.com/data/salida_promedio_temp.csv"

# Función para obtener los datos del archivo CSV y convertirlos en una lista de diccionarios
def obtener_datos():
    # Descargamos el contenido del CSV desde la URL
    response = requests.get(PUBLIC_CSV_URL)
    response.raise_for_status()  # Lanza excepción si ocurre un error al descargar

    # Decodificamos el contenido como texto UTF-8
    csv_content = response.content.decode("utf-8")

    # Dividimos el contenido por líneas
    lines = csv_content.strip().splitlines()

    # Verificamos que la primera línea sea el encabezado esperado
    header = lines[0].split(",")
    if header != ["mes", "temperatura_promedio"]:
        return []  # Si no es el formato correcto, retornamos una lista vacía

    data = []
    # Iteramos sobre las líneas de datos (ignorando la cabecera)
    for line in lines[1:]:
        # Dividimos cada línea por tabulación
        parts = line.split("\t")
        if len(parts) != 2:
            continue  # Si la línea no tiene 2 partes, la ignoramos

        mes, temp_str = parts
        try:
            # Convertimos la temperatura a número flotante
            temperatura = float(temp_str)
            # Agregamos el diccionario con mes y temperatura a la lista de resultados
            data.append({"mes": mes, "temperatura_promedio": temperatura})
        except ValueError:
            # Si hay un error al convertir la temperatura, ignoramos esa línea
            continue

    return data

# Endpoint de la API que retorna los datos en formato JSON
@app.get("/api/datos")
def api_datos():
    try:
        # Obtenemos los datos del CSV
        data = obtener_datos()
        # Retornamos la respuesta JSON
        return JSONResponse(content={"datos": data})
    except Exception as e:
        # Si ocurre algún error, lo retornamos en la respuesta con código 500
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Endpoint que sirve una página HTML con una tabla que muestra los datos del CSV
@app.get("/archivo")
def archivo_html():
    # HTML completo que construye una página con una tabla vacía que se llena con JavaScript
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8" />
        <title>Temperaturas Promedio</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 2rem; }
            table { border-collapse: collapse; width: 50%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
            th { background-color: #4CAF50; color: white; }
            tr:nth-child(even) { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1>Temperaturas Promedio por Mes</h1>
        <table id="tabla-datos">
            <thead>
                <tr><th>Mes</th><th>Temperatura Promedio (°C)</th></tr>
            </thead>
            <tbody></tbody>
        </table>
        <script>
            // Función asincrónica que carga los datos desde el endpoint /api/datos
            async function cargarDatos() {
                try {
                    const res = await fetch('/api/datos');
                    const json = await res.json();
                    if(json.error) {
                        document.body.innerHTML += '<p>Error: ' + json.error + '</p>';
                        return;
                    }
                    const tbody = document.querySelector('#tabla-datos tbody');
                    // Recorremos los datos y agregamos filas a la tabla
                    json.datos.forEach(item => {
                        const tr = document.createElement('tr');
                        tr.innerHTML = `<td>${item.mes}</td><td>${item.temperatura_promedio.toFixed(2)}</td>`;
                        tbody.appendChild(tr);
                    });
                } catch (err) {
                    // En caso de error al cargar los datos, lo mostramos en pantalla
                    document.body.innerHTML += '<p>Error cargando datos.</p>';
                }
            }
            // Ejecutamos la función al cargar la página
            cargarDatos();
        </script>
    </body>
    </html>
    """
    # Retornamos el HTML como respuesta
    return HTMLResponse(content=html_content)
