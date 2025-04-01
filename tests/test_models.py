import unittest
import pickle
from surprise import Dataset, Reader
from surprise.model_selection import train_test_split
import pandas as pd

class TestModels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Cargar datos de prueba
        cls.ratings = pd.read_csv('data/ratings.csv')
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(cls.ratings[['userId', 'movieId', 'rating']], reader)
        _, cls.testset = train_test_split(data, test_size=0.2)
        
        # Cargar modelos
        with open('models/knn_model.pkl', 'rb') as f:
            cls.knn = pickle.load(f)
        with open('models/svd_model.pkl', 'rb') as f:
            cls.svd = pickle.load(f)

    def test_model_predictions(self):
        """Verifica que los modelos pueden hacer predicciones"""
        # Buscar un ejemplo con rating conocido
        for uid, iid, r_ui in self.testset:
            if r_ui is not None:
                # KNN
                knn_pred = self.knn.predict(uid, iid)
                self.assertIsNotNone(knn_pred.est)
                
                # SVD
                svd_pred = self.svd.predict(uid, iid)
                self.assertIsNotNone(svd_pred.est)
                return
                
        self.skipTest("No se encontraron ratings conocidos en el testset")

    def test_model_performance(self):
        """Evalúa el rendimiento básico de los modelos"""
        # Encontrar usuarios y items conocidos
        known_samples = []
        for uid, iid, r_ui in self.testset:
            if (r_ui is not None and 
                not self.knn.default_prediction() and  # Verificar que no es predicción por defecto
                not self.svd.default_prediction()):
                known_samples.append((uid, iid, r_ui))
                if len(known_samples) >= 50:  # Limitar a 50 muestras
                    break
        
        if not known_samples:
            self.skipTest("No se encontraron muestras válidas para prueba")
            return

        # KNN
        knn_rmse = self.calculate_rmse(self.knn, known_samples)
        print(f"KNN RMSE: {knn_rmse}")
        self.assertLess(knn_rmse, 1.5)
        
        # SVD
        svd_rmse = self.calculate_rmse(self.svd, known_samples)
        print(f"SVD RMSE: {svd_rmse}")
        self.assertLess(svd_rmse, 1.5)

        def calculate_rmse(self, model, samples):
            """Calcula RMSE para un modelo dado"""
            errors = []
            for uid, iid, r_ui in samples:
                pred = model.predict(uid, iid)
                if pred is not None and pred.r_ui is not None:
                    errors.append((pred.r_ui - pred.est)**2)
            return (sum(errors)/len(errors))**0.5 if errors else float('inf')