import requests 
import json 
import time 
import random 
from kafka import KafkaProducer 

producer = KafkaProducer( 
  bootstrap_servers=['localhost:9092'], 
  value_serializer=lambda x: json.dumps(x).encode('utf-8') 
) 

# URL oficila de datos abiertos colombia 
def get_exterior_data():
    url = "https://www.datos.gov.co/resource/y399-rzwf.json"
    response = requests.get(url)
    if response.status_code != 200:
        print("Error al obtener los datos del portal")
        return []
    data = response.json()

  # Obtener datos
    clean_data = []
    for d in data:
        try:
            edad = int(d.get("edad", 0))
            if edad == 0:
                edad = random.randint(25, 40)
        except:
            edad = random.randint(25, 40)

        clean_data.append({
            "pais": random.choice(["COLOMBIA", "MEXICO", "CHILE", "ARGENTINA", "PERU", "ESPAÑA", "USA", "ECUADOR"]),
            "ciudad": d.get("ciudad", "N/A"),
            "edad": edad,
            "genero": d.get("genero", "N/A"),
            "nivel_educativo": d.get("nivel_educativo", "N/A"),
            "anio": d.get("anio", "2025"),
            "fecha": time.strftime("%Y-%m-%d %H:%M:%S")
        })
    return clean_data

print("Descargando y enviando datos al topic 'exterior_data'...")
exterior_data = get_exterior_data()

if not exterior_data:
    print("No hay datos válidos para enviar")
else:
    i = 0
    while True:
        record = random.choice(exterior_data)
        record["timestamp"] = int(time.time())

        producer.send('exterior_data', value=record)
        print(f"[{i}] Enviado: {record}")
        i += 1
        time.sleep(2)

  
