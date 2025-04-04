import csv
import random
import time
from datetime import datetime, timedelta
from kafka import KafkaProducer
import json

# Configuración
KAFKA_SERVER = 'localhost:9092'
TOPIC = 'movielog1'
OUTPUT_FILE = 'data/kafka_stream_simulation.csv'

# Inicializar productor de Kafka
producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Generar datos simulados
def generate_simulated_data(num_entries=10000):
    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        fieldnames = ['timestamp', 'user_id', 'action', 'movie_id', 'rating', 'response_time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        start_time = datetime.now() - timedelta(days=30)
        
        for i in range(num_entries):
            # Generar timestamp incremental
            timestamp = start_time + timedelta(minutes=i*5)
            timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            
            user_id = random.randint(1, 1000)
            movie_id = random.randint(1, 10000)
            
            # Generar diferentes tipos de eventos
            event_type = random.choice(['recommendation', 'watch', 'rating'])
            
            if event_type == 'recommendation':
                action = f"recommendation request server_{random.randint(1,5)}, status 200"
                movie_ids = ",".join(str(random.randint(1, 10000)) for _ in range(20))
                result = f"result: {movie_ids}"
                response_time = random.uniform(0.1, 0.8)
                writer.writerow({
                    'timestamp': timestamp_str,
                    'user_id': user_id,
                    'action': f"{action}, {result}",
                    'response_time': response_time
                })
                # Enviar a Kafka
                producer.send(TOPIC, {
                    'time': timestamp_str,
                    'userid': user_id,
                    'message': f"{action}, {result}, {response_time}"
                })
            elif event_type == 'watch':
                action = f"GET /data/m/{movie_id}/{random.randint(1, 120)}.mpg"
                writer.writerow({
                    'timestamp': timestamp_str,
                    'user_id': user_id,
                    'action': action
                })
                producer.send(TOPIC, {
                    'time': timestamp_str,
                    'userid': user_id,
                    'message': action
                })
            else:  # rating
                rating = random.randint(1, 5)
                action = f"GET /rate/{movie_id}={rating}"
                writer.writerow({
                    'timestamp': timestamp_str,
                    'user_id': user_id,
                    'action': action,
                    'movie_id': movie_id,
                    'rating': rating
                })
                producer.send(TOPIC, {
                    'time': timestamp_str,
                    'userid': user_id,
                    'message': action
                })
            
            if i % 1000 == 0:
                print(f"Generated {i} entries")
    
    producer.flush()
    print(f"Simulation complete. Data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_simulated_data()