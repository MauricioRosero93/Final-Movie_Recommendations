import requests
import time
import sys

base_url = "http://localhost:8082/recommend"
user_ids = range(1, 51)  # 50 user_ids
total_requests = 2000
successful_requests = 0

print(f"Enviando {total_requests} solicitudes...")

start_time = time.time()

for i in range(total_requests):
    user_id = user_ids[i % len(user_ids)]  
    try:
        response = requests.get(f"{base_url}/{user_id}", timeout=3.0)  
        if response.status_code == 200:
            successful_requests += 1
            # Sobrescribe la misma línea con el número de solicitudes exitosas
            sys.stdout.write(f"\rSolicitudes exitosas: {successful_requests}")
            sys.stdout.flush() 
    except requests.exceptions.RequestException as e:
        print(f"\nError en la solicitud para user_id {user_id}: {e}")  

end_time = time.time()
total_time = end_time - start_time

print(f"\nPruebas completadas.") 
print(f"Solicitudes exitosas: {successful_requests}")
print(f"Tiempo total: {total_time} segundos")