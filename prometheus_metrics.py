from prometheus_client import start_http_server, Counter, Histogram
import time

# Definición de métricas (globales para ser usadas en app.py)
RECOMMENDATIONS_COUNT = Counter(
    'recommendations_total', 
    'Total de recomendaciones generadas'
)
RESPONSE_TIME = Histogram(
    'response_time_seconds', 
    'Tiempo de respuesta del endpoint /recommend',
    buckets=[0.1, 0.5, 1.0, 2.0]  # Rangos personalizados para el histograma
)

def start_metrics_server():
    """Inicia el servidor de métricas en el puerto 8000"""
    start_http_server(8000, addr='0.0.0.0')