import unittest
from app import app
import json

class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.testing = True
        cls.client = app.test_client()
    
    def test_recommendation_endpoint(self):
        """Test que el endpoint de recomendaciones funciona"""
        response = self.client.get('/recommend/1')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, dict, "La respuesta debería ser un JSON")
        
        # Verificar estructura de la respuesta
        self.assertIn('recommendations', data)
        self.assertIn('status', data)
        self.assertIn('model_used', data)
    
        # Verificar que las recomendaciones son una lista
        self.assertIsInstance(data['recommendations'], list)
        self.assertGreater(len(data['recommendations']), 0, "Debería devolver recomendaciones")
    
    def test_invalid_user(self):
        """Test con usuario no existente"""
        response = self.client.get('/recommend/999999')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('recommendations', data)
    
    def test_health_check(self):
        """Test del endpoint de salud"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertIn('model_loaded', data)

if __name__ == '__main__':
    unittest.main()