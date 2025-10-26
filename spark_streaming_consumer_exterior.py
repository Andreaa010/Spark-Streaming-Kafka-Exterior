from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, avg, count, window
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

spark = SparkSession.builder \ 
        .appName("KafkaSparkStreaming_ExteriorData") \ 
        .getOrCreate() 
spark.sparkContext.setLogLevel("WARN") 

# Definir el esquema de los datos de entrada 
schema = StructType([ 
    StructField("pais", StringType(), True),  
    StructField("ciudad", StringType(), True), 
    StructField("edad", IntegerType(), True), 
    StructField("genero", StringType(), True), 
    StructField("nivel_educativo", StringType(), True), 
    StructField("anio", StringType(), True), 
    StructField("fecha", StringType(), True) 
]) 

# Lectura de stream desde kafka 
df = spark.readStream \ 
    .format("kafka") \ 
    .option("kafka.bootstrap.servers", "localhost:9092") \ 
    .option("subscribe", "exterior_data") \ 
    .load() 

# Extraer el valor y convertir a JSON 
json_df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

# Crear una ventana temporal para analizar datos 
agg_df = json_df.groupBy( 
    window(col("fecha").cast("timestamp"), "30 seconds"), 
    col("pais") 
).agg( 
    count("*").alias("num_registros"), 
    avg("edad").alias("edad_promedio") 
).orderBy("window") 

# Muestra los resultados en consola 
query = (
  agg_df.writeStream
  .outputMode("complete")
  .format("console")
  .option("truncate", False) 
  .option("numRows", 50) 
  .start()
)
query.awaitTermination()
