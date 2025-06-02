from flask import Flask, Response, jsonify
import csv

app = Flask(__name__)

CSV_FILE_PATH = "promedio_temp.csv"

@app.route('/csv')
def serve_csv():
    try:
        with open(CSV_FILE_PATH, newline='') as csvfile:
            # Leer CSV
            reader = csv.DictReader(csvfile)
            data = list(reader)
        # Devolver JSON
        return jsonify(data)
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
