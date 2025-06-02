# Importamos las clases necesarias de mrjob
from mrjob.job import MRJob
from mrjob.step import MRStep

# Para manejar lectura tipo CSV desde una línea
import csv
from io import StringIO

# Definimos una clase que hereda de MRJob para realizar MapReduce
class MRPromedioTemperatura(MRJob):

    # Definimos los pasos que tendrá el job: un mapper y un reducer
    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_temp,
                   reducer=self.reducer_compute_avg)
        ]

    # Mapper: procesa cada línea del archivo
    def mapper_get_temp(self, _, line):
        # Ignora la cabecera del CSV si comienza con 'date'
        if line.startswith("date"):
            return
        try:
            # Parseamos la línea como si fuera un archivo CSV
            reader = csv.reader(StringIO(line))
            for row in reader:
                # Extraemos la fecha y la temperatura
                fecha = row[0]           # Ejemplo: '2022-01-01'
                temp = float(row[1])    # Ejemplo: 25.8
                mes = fecha[:7]         # Extraemos el mes: '2022-01'
                # Emitimos la clave-valor: (mes, (temperatura, 1))
                yield mes, (temp, 1)
        except:
            # Si hay un error en el parseo, se ignora la línea
            pass

    # Reducer: recibe las temperaturas y cuentas por cada mes
    def reducer_compute_avg(self, mes, temp_count_pairs):
        suma_temp = 0.0
        count = 0
        # Suma todas las temperaturas y cuenta cuántas hay
        for temp, c in temp_count_pairs:
            suma_temp += temp
            count += c
        # Calcula el promedio
        promedio = suma_temp / count if count > 0 else 0
        # Emite el resultado redondeado
        yield mes, round(promedio, 2)

# Punto de entrada: corre el job cuando se ejecuta como script
if __name__ == '__main__':
    MRPromedioTemperatura.run()
