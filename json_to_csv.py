import json
import csv

with open("./clima_medellin_2022.json") as f:
    data = json.load(f)

with open("clima_medellin_2022.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["date", "temperature_max", "precipitation"])
    for i in range(len(data["daily"]["time"])):
        writer.writerow([
            data["daily"]["time"][i],
            data["daily"]["temperature_2m_max"][i],
            data["daily"]["precipitation_sum"][i]
        ])
