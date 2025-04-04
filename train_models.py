import pandas as pd
from surprise import Dataset, Reader, KNNBasic, SVD
from surprise.model_selection import train_test_split
import pickle
import time

# Cargar datos
ratings = pd.read_csv('data/ratings.csv')
movies = pd.read_csv('data/movies.csv')

# Preparar datos para Surprise
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

# Dividir datos en entrenamiento y prueba
trainset, testset = train_test_split(data, test_size=0.2)

# Entrenar modelo KNNBasic y medir tiempo
start_time = time.time()
knn_model = KNNBasic()
knn_model.fit(trainset)
knn_training_time = time.time() - start_time

# Entrenar modelo SVD y medir tiempo
start_time = time.time()
svd_model = SVD()
svd_model.fit(trainset)
svd_training_time = time.time() - start_time


# Guardar tiempos de entrenamiento
with open('models/training_times.pkl', 'wb') as f:
    pickle.dump({'knn_training_time': knn_training_time, 'svd_training_time': svd_training_time}, f)

# Guardar modelos
with open('models/knn_model.pkl', 'wb') as f:
    pickle.dump(knn_model, f)

with open('models/svd_model.pkl', 'wb') as f:
    pickle.dump(svd_model, f)

print("Modelos entrenados y guardados.")