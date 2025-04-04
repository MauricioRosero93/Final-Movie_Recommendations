# diagnosis.py
import pickle
from surprise import Dataset, Reader
import pandas as pd

# Cargar datos
ratings = pd.read_csv('data/ratings.csv')
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)
trainset = data.build_full_trainset()

print("\n=== Diagnóstico de Datos ===")
print(f"Total de ratings: {len(ratings)}")
print(f"Usuarios únicos: {len(trainset.all_users())}")
print(f"Películas únicas: {len(trainset.all_items())}")

# Verificar modelos
print("\n=== Verificación de Modelos ===")
with open('models/knn_model.pkl', 'rb') as f:
    knn = pickle.load(f)
    print("KNN cargado correctamente")

with open('models/svd_model.pkl', 'rb') as f:
    svd = pickle.load(f)
    print("SVD cargado correctamente")

# Ejemplo de predicción
print("\n=== Ejemplo de Predicción ===")
test_user = '1'
test_item = '1'
print(f"Prediciendo para usuario {test_user} y película {test_item}")

try:
    pred = knn.predict(test_user, test_item)
    print(f"KNN: {pred}")
except Exception as e:
    print(f"Error en KNN: {e}")

try:
    pred = svd.predict(test_user, test_item)
    print(f"SVD: {pred}")
except Exception as e:
    print(f"Error en SVD: {e}")