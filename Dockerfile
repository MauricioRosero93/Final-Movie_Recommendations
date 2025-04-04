FROM python:3.9-slim

WORKDIR /app

# Instala dependencias del sistema primero
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia los requirements primero para cachear
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de archivos
COPY app.py .
COPY models/ ./models/
COPY data/ ./data/

# Verifica que los archivos existen
RUN ls -l models/ data/

EXPOSE 8082
CMD ["python", "app.py"]