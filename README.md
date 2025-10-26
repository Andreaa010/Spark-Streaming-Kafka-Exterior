# Análisis en tiempo real de datos demográficos de ciudadanos en el exterior mediante Apache Kafka y Spark Streaming

## Descripcion
Esta solución implementa una arquitectura de procesamiento de datos en tiempo real utilizando Apache Kafka y Apache Spark Structured Streaming.

## Objetivo 
El objetivo del análisis es procesar en tiempo real la información recibida de esas personas en el exterior y observar tendencias demográficas y de volumen agrupadas por país.

---

### Instrucciones para su ejecución
Para realizar la ejecucion de las herramientas se debe de tener instalado:
- Apache Kafka y Zookeeper.
- Apache Spark 3.5.6.
- Python 3

Una vez instalado los servcicios se procede a iniciarel servidor zookeeper con el siguiente comando:

```bash
sudo /opt/Kafka/bin/zookeeper-server-start.sh /opt/Kafka/config/zookeeper.properties &
```

Luego iniciamos el servicio kafka con el comando:

```bash
sudo /opt/Kafka/bin/kafka-server-start.sh /opt/Kafka/config/server.properties &
```

Para la ejecucion del analisis debemos de crear el topic con el siguiente comando:
```bash
/opt/Kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic exterior_data 
```

Una vez creados los archivos llamados kafka_producer_exterior.py y spark_streaming_consumer_exterior.py con sus respectivos codigos, debemos de abrir otra terminal para ejecutar los siguientes comandos en una terminal distinta para su correcto ejecucion:

En una terminal ejecutamos primero:
```bash
python3 kafka_producer_exterior.py 
```

Luego en la otra terminal ejecutamos:
```bash
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.6 spark_streaming_consumer_exterior.py
```

Y de esta forma podemos ver el análisis que estudia en tiempo real los registros de ciudadanos en el exterior, midiendo el número de registros y la edad promedio por país a partir de los datos abiertos de Colombia.
Utilizando Apache Kafka para la transmisión de datos y Apache Spark Streaming para el procesamiento en vivo y la generación de estadísticas por intervalos de tiempo.

Autor: Andrea Arias Bermúdez
