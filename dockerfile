# Usa una imagen base con Python
FROM python:3.9-slim

WORKDIR /app

# Copia los archivos necesarios
COPY requirements.txt .
COPY app.py .
COPY prometheus_metrics.py .
COPY data/ /app/data/  # Si necesitas datos
COPY models/ /app/models/  # Si usas modelos preentrenados

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone los puertos
EXPOSE 8082  # Para tu aplicación Flask
EXPOSE 8000  # Para las métricas de Prometheus

# Comando para iniciar ambos servicios
CMD ["sh", "-c", "python prometheus_metrics.py & python app.py"]