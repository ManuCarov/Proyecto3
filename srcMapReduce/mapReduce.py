from mrjob.job import MRJob
from mrjob.step import MRStep
import csv
from io import StringIO

class MRPromedioTemperatura(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_temp,
                   reducer=self.reducer_compute_avg)
        ]

    def mapper_get_temp(self, _, line):
        # Ignorar encabezado
        if line.startswith("date"):
            return
        # Parseo manual del CSV
        try:
            reader = csv.reader(StringIO(line))
            for row in reader:
                fecha = row[0]           # 2022-01-01
                temp = float(row[1])    # 25.8
                mes = fecha[:7]         # 2022-01
                yield mes, (temp, 1)
        except:
            pass

    def reducer_compute_avg(self, mes, temp_count_pairs):
        suma_temp = 0.0
        count = 0
        for temp, c in temp_count_pairs:
            suma_temp += temp
            count += c
        promedio = suma_temp / count if count > 0 else 0
        yield mes, round(promedio, 2)

if __name__ == '__main__':
    MRPromedioTemperatura.run()
