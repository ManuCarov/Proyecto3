# Proyecto3

## Datos

### ¿De donde proviene?
Los datos provienen de la API de Open-Meteo y corresponden al clima diario en Medellín durante 2022. El archivo `clima_medellin_2022.csv` contiene columnas de fecha, temperatura máxima diaria y precipitación acumulada.

### ¿Por qué estos datos?
Elegimos este dataset porque permite aplicar MapReduce para conteos, promedios mensuales y detección de tendencias climáticas en un entorno real.

### ¿Cómo obtuvimos el CSV del JSON?
El JSON original fue convertido a CSV usando Python (`json_to_csv.py`).
