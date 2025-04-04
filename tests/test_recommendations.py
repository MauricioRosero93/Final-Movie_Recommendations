import unittest
from app import recommend_movies
import pandas as pd

class TestRecommendations(unittest.TestCase):
    def setUp(self):
        self.movies = pd.read_csv('data/movies.csv')

    def test_recommendations(self):
        recommendations = recommend_movies(1)
        self.assertEqual(len(recommendations), 20)
        self.assertTrue(all(isinstance(movie, str) for movie in recommendations))

if __name__ == '__main__':
    unittest.main()