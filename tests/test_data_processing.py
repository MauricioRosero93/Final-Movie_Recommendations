import unittest
import pandas as pd
import os
from surprise import Dataset, Reader

class TestDataProcessing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Cargar datos de prueba
        cls.ratings = pd.read_csv('data/ratings.csv')
        cls.movies = pd.read_csv('data/movies.csv')
        
    def test_data_loading(self):
        """Test que los datos se cargan correctamente"""
        self.assertGreater(len(self.ratings), 0, "No se cargaron ratings")
        self.assertGreater(len(self.movies), 0, "No se cargaron películas")
        
    def test_data_columns(self):
        """Test que los datos tienen las columnas esperadas"""
        expected_rating_cols = ['userId', 'movieId', 'rating', 'timestamp']
        expected_movie_cols = ['movieId', 'title', 'genres']
        
        for col in expected_rating_cols:
            self.assertIn(col, self.ratings.columns, f"Falta columna {col} en ratings")
            
        for col in expected_movie_cols:
            self.assertIn(col, self.movies.columns, f"Falta columna {col} en movies")
            
    def test_surprise_dataset(self):
        """Test que los datos se pueden cargar en formato Surprise"""
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(self.ratings[['userId', 'movieId', 'rating']], reader)
        self.assertIsNotNone(data, "No se pudo cargar datos en Surprise")

if __name__ == '__main__':
    unittest.main()