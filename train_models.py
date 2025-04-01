import pandas as pd
from surprise import Dataset, Reader, KNNBasic, SVD
from surprise.model_selection import train_test_split
import pickle
import time
import os

# Cargar datos
ratings = pd.read_csv('data/ratings.csv')
movies = pd.read_csv('data/movies.csv')

# Verificación mínima de datos clave (añadido)
print("\nVerificación de datos clave:")
print(f"¿Existe usuario 1? {'Sí' if 1 in ratings['userId'].values else 'No'}")
print(f"¿Existe película 1? {'Sí' if 1 in ratings['movieId'].values else 'No'}")
print(f"Ejemplo de ratings para usuario 1: {ratings[ratings['userId'] == 1].head(1)}")
print(f"Ejemplo de ratings para película 1: {ratings[ratings['movieId'] == 1].head(1)}")

# Preparar datos para Surprise
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

# Dividir datos en entrenamiento y prueba
trainset, testset = train_test_split(data, test_size=0.2, random_state=42)  # Añadido random_state

# Entrenar modelo KNNBasic
print("\nEntrenando modelo KNN...")
start_time = time.time()
knn_model = KNNBasic()
knn_model.fit(trainset)
knn_training_time = time.time() - start_time

# Entrenar modelo SVD
print("Entrenando modelo SVD...")
start_time = time.time()
svd_model = SVD()
svd_model.fit(trainset)
svd_training_time = time.time() - start_time

# Crear directorio de modelos si no existe
os.makedirs('models', exist_ok=True)

# Guardar modelos y tiempos
with open('models/training_times.pkl', 'wb') as f:
    pickle.dump({
        'knn_training_time': knn_training_time,
        'svd_training_time': svd_training_time
    }, f)

with open('models/knn_model.pkl', 'wb') as f:
    pickle.dump(knn_model, f)

with open('models/svd_model.pkl', 'wb') as f:
    pickle.dump(svd_model, f)

# Crear enlace al modelo actual
with open('models/svd_model_current.pkl', 'wb') as f:
    pickle.dump(svd_model, f)

print("\nModelos entrenados y guardados exitosamente.")
print(f"Tiempo KNN: {knn_training_time:.2f}s | Tiempo SVD: {svd_training_time:.2f}s")