# Importamos las librerías necesarias para trabajar con JSON y CSV
import json
import csv

# Abrimos el archivo JSON que contiene los datos del clima
with open("./clima_medellin_2022.json") as f:
    data = json.load(f)  # Cargamos el contenido del JSON como un diccionario de Python

# Abrimos (o creamos) un archivo CSV para escribir los datos extraídos
with open("clima_medellin_2022.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)  # Creamos un escritor CSV
    # Escribimos la fila de encabezado con los nombres de las columnas
    writer.writerow(["date", "temperature_max", "precipitation"])
    
    # Recorremos los datos diarios por índice
    for i in range(len(data["daily"]["time"])):
        # Escribimos una fila por cada día con fecha, temperatura máxima y precipitación
        writer.writerow([
            data["daily"]["time"][i],
            data["daily"]["temperature_2m_max"][i],
            data["daily"]["precipitation_sum"][i]
        ])
