import pickle
from surprise import accuracy
from surprise.model_selection import train_test_split
from surprise import Dataset, Reader
import pandas as pd

def evaluate_model(model_path, testset):
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    predictions = model.test(testset)
    return accuracy.rmse(predictions)

def offline_evaluation():
    ratings = pd.read_csv('data/ratings.csv')
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)
    _, testset = train_test_split(data, test_size=0.2)
    
    knn_rmse = evaluate_model('models/knn_model.pkl', testset)
    svd_rmse = evaluate_model('models/svd_model.pkl', testset)
    
    return {'knn_rmse': knn_rmse, 'svd_rmse': svd_rmse}