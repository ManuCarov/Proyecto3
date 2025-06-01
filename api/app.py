from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
import requests
import io

app = FastAPI()

PUBLIC_CSV_URL = "https://bucket-telematica.s3.us-east-1.amazonaws.com/data/salida_promedio_temp.csv"

def obtener_datos():
    response = requests.get(PUBLIC_CSV_URL)
    response.raise_for_status()
    csv_content = response.content.decode("utf-8")
    lines = csv_content.strip().splitlines()
    header = lines[0].split(",")
    if header != ["mes", "temperatura_promedio"]:
        return []
    data = []
    for line in lines[1:]:
        parts = line.split("\t")
        if len(parts) != 2:
            continue
        mes, temp_str = parts
        try:
            temperatura = float(temp_str)
            data.append({"mes": mes, "temperatura_promedio": temperatura})
        except ValueError:
            continue
    return data

@app.get("/api/datos")
def api_datos():
    try:
        data = obtener_datos()
        return JSONResponse(content={"datos": data})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@app.get("/archivo")
def archivo_html():
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
            async function cargarDatos() {
                try {
                    const res = await fetch('/api/datos');
                    const json = await res.json();
                    if(json.error) {
                        document.body.innerHTML += '<p>Error: ' + json.error + '</p>';
                        return;
                    }
                    const tbody = document.querySelector('#tabla-datos tbody');
                    json.datos.forEach(item => {
                        const tr = document.createElement('tr');
                        tr.innerHTML = `<td>${item.mes}</td><td>${item.temperatura_promedio.toFixed(2)}</td>`;
                        tbody.appendChild(tr);
                    });
                } catch (err) {
                    document.body.innerHTML += '<p>Error cargando datos.</p>';
                }
            }
            cargarDatos();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
