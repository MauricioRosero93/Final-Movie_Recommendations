import pickle
import time
from surprise import Dataset, Reader, KNNBasic, SVD
from surprise.model_selection import train_test_split
from pipeline.data_processing import load_and_validate_data, preprocess_data

def train_models():
    # Cargar y validar datos
    ratings = load_and_validate_data()
    ratings = preprocess_data(ratings)
    
    # Preparar datos para Surprise
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)
    trainset, _ = train_test_split(data, test_size=0.2)
    
    # Entrenar modelos
    knn_model = KNNBasic()
    svd_model = SVD()
    
    knn_model.fit(trainset)
    svd_model.fit(trainset)
    
    # Guardar modelos
    with open('models/knn_model.pkl', 'wb') as f:
        pickle.dump(knn_model, f)
    with open('models/svd_model.pkl', 'wb') as f:
        pickle.dump(svd_model, f)