# Proyecto3

## Datos

### ¿De donde proviene?
Los datos provienen de la API de Open-Meteo y corresponden al clima diario en Medellín durante 2022. El archivo `clima_medellin_2022.csv` contiene columnas de fecha, temperatura máxima diaria y precipitación acumulada.

### ¿Por qué estos datos?
Elegimos este dataset porque permite aplicar MapReduce para conteos, promedios mensuales y detección de tendencias climáticas en un entorno real.

### ¿Cómo obtuvimos el CSV del JSON?
El JSON original fue convertido a CSV usando Python (`json_to_csv.py`).

## Ejecución del proyecto

### Creación del bucket

Para comenzar, es necesario crear un bucket en Amazon S3 que servirá como repositorio central para todos los archivos del proyecto.

#### Pasos para crear el bucket:

1. Ingresa a la consola de AWS y dirígete al servicio **S3**.
2. Haz clic en **“Crear bucket”**.
3. Configura los siguientes parámetros:
   - **Nombre del bucket**: Ingresa un nombre único (por ejemplo: `proyecto-clima-medellin`).

4. En la sección **Propiedades de objetos**:
   - Activa la opción **“ACL habilitadas”**.
   - Selecciona **“Escritor de objetos”**.

5. En la sección **Configuración del bloqueo de acceso público**:
   - **Desactiva** la opción **“Bloquear todo el acceso público”**.
   - Marca la casilla de advertencia para confirmar que comprendes los riesgos.

6. Finalmente, haz clic en **“Crear bucket”**.

---

#### Estructura interna del bucket

Una vez creado el bucket, debes organizarlo con las siguientes carpetas:

- `logs/`: Carpeta utilizada para almacenar los logs generados por EMR.
- `data/`: Carpeta donde se guardarán los datos procesados por el job de MapReduce.
- `main/`: Contendrá los datos de entrada, por ejemplo el archivo `clima_medellin_2022.csv`.
- `src/`: Contendrá el código fuente y dependencias, como:
  - `mapReduce.py`
  - `requirements.txt`

### Creación del EMR Cluster

Para ejecutar el procesamiento de datos mediante Hadoop y MapReduce, se necesita un clúster EMR. A continuación, se detallan los pasos para su configuración y despliegue.

---

#### 1. Configuración del clúster

1. Ingresa al servicio **Amazon EMR** y haz clic en **"Create cluster"**.

2. En la sección **Name and Applications**:
   - **Name**: `emr-MyClusterEMR`
   - **Amazon EMR release**: `emr-6.14.0`
   - **Application bundle**: Selecciona `Custom`
   - Haz clic en **“Customize your application bundle”**

3. En **Applications included in bundle**, selecciona los siguientes componentes:
   - Flink 1.17.1
   - HCatalog 3.1.3
   - Hue 4.11.0
   - Livy 0.7.1
   - Spark 3.4.1
   - Tez 0.10.2
   - ZooKeeper 3.5.10
   - Hadoop 3.3.3
   - Sqoop 1.4.7
   - Hive 3.1.3
   - JupyterHub 1.5.0
   - Zeppelin 0.10.1
   - Oozie 5.1.0

4. En la opción: AWS Glue Data Catalog settings
   - Active la casilla: Use the AWS Glue Data Catalog to provide an external metastore for your
application.
   - Active la casilla: Use for Hive table metadataUse for Spark table metadata

---

#### 2. Configuración del clúster

- **Cluster type**: `Uniform Instance Groups`

- **Instance types**:
  - **Primary node**: `m4.large`
  - **Core node**: `m4.large`
  - **Task node**: `m4.large`

- **Cluster scaling**:
  - Opción: `Set cluster size manually`
  - Tamaño predeterminado para los nodos Core y Task

- **Cluster termination**:
  - Desactivar la opción **"Use termination protection"**

---

#### 3. Configuración de logs

- Activa la casilla **“Publish cluster-specific logs to Amazon S3”**
- Ubicación S3: selecciona la carpeta `logs` creada previamente (por ejemplo: `s3://<tu-bucket>/logs`)

---

#### 4. Seguridad y llaves

- **EC2 Key pair**:
  - Selecciona la llave SSH existente (por ejemplo: `emr-key.pem`) para acceder al clúster.

- **IAM Roles**:
  - **Service Role**: `EMR_DefaultRole`
  - **EC2 Instance Profile**: `EMR_EC2_DefaultRole`

---

#### 5. Lanzamiento y verificación

Haz clic en **Create cluster** y espera aproximadamente 20 minutos hasta que el estado del clúster cambie a **“Waiting”**, lo cual indica que está listo para ejecutar trabajos.

---

### Acceso al clúster vía SSH

1. Dirígete al servicio **EC2** en la consola de AWS.
2. Ve a la sección **Security Groups**.
3. Selecciona el grupo de seguridad asociado al nodo **Primary (Master)**.
4. Haz clic en **Inbound rules > Edit inbound rules > Add rule**.
   - **Type**: `SSH`
   - **Source**: `Anywhere (0.0.0.0/0)`
5. Haz clic en **Save rules**.

Una vez hecho esto, podrás conectarte al clúster usando SSH:

```bash
ssh -i emr-key.pem hadoop@<EC2-Master-Public-IP>
```

### Dentro del cluster

#### Descargar archivo desde S3

```bash
aws s3 cp s3://<tu-bucket>/main/clima_medellin_2022.csv .
ls -lh clima_medellin_2022.csv
```
Se descarga el archivo `clima_medellin_2022.csv` desde el bucket S3 y se verifica su existencia con `ls`.

#### Subir los datos al HDFS

```bash
hdfs dfs -mkdir -p /user/hadoop/datos
hdfs dfs -copyFromLocal clima_medellin_2022.csv /user/hadoop/datos/
hdfs dfs -ls /user/hadoop/datos/
```
Se crea un directorio en HDFS (si no existe), se sube el archivo descargado y se confirma que está presente en HDFS.

#### Descargar el código del MapReduce

```bash
aws s3 cp s3://<tu-bucket>/src/mapReduce.py .
aws s3 cp s3://<tu-bucket>/src/requirements.txt .
```
Se descargan el script del MapReduce y el archivo de dependencias desde S3.

#### Crear entorno virtual e instalar dependencias

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```
Se crea un entorno virtual de Python, se activa y se instalan las dependencias necesarias.

#### Ejecutar el MapReduce usando los datos en HDFS

```bash
python mapReduce.py hdfs:///user/hadoop/datos/clima_medellin_2022.csv -r hadoop --output-dir hdfs:///user/hadoop/salida_promedio_temp
```
Se ejecuta el script `mapReduce.py` sobre los datos alojados en HDFS, generando un directorio de salida con los resultados.

#### Verificar los resultados generados por MapReduce

```bash
hdfs dfs -ls /user/hadoop/salida_promedio_temp
hdfs dfs -cat /user/hadoop/salida_promedio_temp/part-*
```
Se lista el contenido de la carpeta de salida y se muestran los resultados producidos por MapReduce. Puede haber múltiples archivos `part-*`.

#### Crear un archivo `promedio_temp.csv` consolidado

```bash
echo "mes,temperatura_promedio" > promedio_temp.csv && \
hdfs dfs -cat /user/hadoop/salida_promedio_temp/part-* | tr -d '"' >> promedio_temp.csv
```
Se crea un archivo CSV local consolidando todos los resultados en un único archivo con cabecera.

#### Subir el resultado consolidado al HDFS

```bash
hdfs dfs -put -f promedio_temp.csv /user/hadoop/salida_promedio_temp.csv
```
El archivo `promedio_temp.csv` se sube nuevamente al HDFS para mantener una copia procesada.

#### Descargar el resultado y cargarlo en S3

```bash
hdfs dfs -get /user/hadoop/salida_promedio_temp.csv salida_promedio_temp.csv

aws s3 cp salida_promedio_temp.csv s3://<tu-bucket>/data/salida_promedio_temp.csv
```
Finalmente, se descarga el archivo desde HDFS al sistema local y luego se carga al bucket S3 en la carpeta `data`.

