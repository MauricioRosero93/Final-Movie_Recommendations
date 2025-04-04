import pickle
import time
from surprise import accuracy
from surprise.model_selection import train_test_split
from surprise import Dataset, Reader
from surprise import KNNBasic, SVD
import pandas as pd
import os

# Cargar datos
ratings = pd.read_csv('data/ratings.csv')
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)
trainset, testset = train_test_split(data, test_size=0.2)

# Cargar modelos
with open('models/knn_model.pkl', 'rb') as f:
    knn_model = pickle.load(f)

with open('models/svd_model.pkl', 'rb') as f:
    svd_model = pickle.load(f)

# Cargar tiempos de entrenamiento
with open('models/training_times.pkl', 'rb') as f:
    training_times = pickle.load(f)

knn_training_time = training_times['knn_training_time']
svd_training_time = training_times['svd_training_time']

# Evaluar precisión (RMSE)
def evaluate_model(model, testset):
    predictions = model.test(testset)
    return accuracy.rmse(predictions)

# Medir tiempo de inferencia
def measure_inference_time(model, testset):
    start_time = time.time()
    for _ in range(1000):  # Predecir 1000 veces
        model.predict(testset[0][0], testset[0][1])
    return (time.time() - start_time) / 1000  # Tiempo promedio por predicción

# Medir tamaño del modelo
def measure_model_size(model, filename):
    with open(filename, 'wb') as f:
        pickle.dump(model, f)
    return os.path.getsize(filename) / (1024 * 1024)  # Tamaño en MB

# Evaluar KNNBasic
knn_rmse = evaluate_model(knn_model, testset)
knn_inference_time = measure_inference_time(knn_model, testset)
knn_size = measure_model_size(knn_model, 'models/knn_model.pkl')

# Evaluar SVD
svd_rmse = evaluate_model(svd_model, testset)
svd_inference_time = measure_inference_time(svd_model, testset)
svd_size = measure_model_size(svd_model, 'models/svd_model.pkl')

# Mostrar resultados
print("KNNBasic:")
print(f"RMSE: {knn_rmse}, Tiempo de entrenamiento: {knn_training_time} s, Tiempo de inferencia: {knn_inference_time} ms, Tamaño: {knn_size} MB")

print("SVD:")
print(f"RMSE: {svd_rmse}, Tiempo de entrenamiento: {svd_training_time} s, Tiempo de inferencia: {svd_inference_time} ms, Tamaño: {svd_size} MB")