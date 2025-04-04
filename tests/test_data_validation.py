import unittest
import pandas as pd
from data_validation.schema import validate_schema

class TestDataValidation(unittest.TestCase):
    def setUp(self):
        self.valid_data = pd.DataFrame({
            'userId': [1, 2, 3],
            'movieId': [101, 102, 103],
            'rating': [3.5, 4.0, 2.5]
        })
        
        self.invalid_data = pd.DataFrame({
            'userId': ['a', 'b', 'c'],
            'movieId': [101, 102, 103],
            'rating': [3.5, 4.0, 2.5]
        })

    def test_schema_validation(self):
        self.assertTrue(validate_schema(self.valid_data))
        self.assertFalse(validate_schema(self.invalid_data))

if __name__ == '__main__':
    unittest.main()