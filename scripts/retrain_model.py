import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
import pickle
import os
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(filename='retrain.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def load_data():
    """Cargar datos de ratings"""
    try:
        ratings = pd.read_csv('data/ratings.csv')
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)
        return data
    except Exception as e:
        logging.error(f"Error loading data: {str(e)}")
        raise

def train_model(data):
    """Entrenar modelo SVD"""
    try:
        trainset, testset = train_test_split(data, test_size=0.2)
        
        # Modelo SVD con mejores hiperparámetros
        model = SVD(n_factors=100, n_epochs=20, lr_all=0.005, reg_all=0.02)
        model.fit(trainset)
        
        return model, testset
    except Exception as e:
        logging.error(f"Error training model: {str(e)}")
        raise

def evaluate_model(model, testset):
    """Evaluar modelo"""
    try:
        predictions = model.test(testset)
        rmse = sum((pred.r_ui - pred.est)**2 for pred in predictions)/len(predictions))**0.5
        return rmse
    except Exception as e:
        logging.error(f"Error evaluating model: {str(e)}")
        raise

def save_model(model, version):
    """Guardar modelo con versionado"""
    try:
        model_dir = 'models'
        os.makedirs(model_dir, exist_ok=True)
        
        # Guardar modelo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{model_dir}/svd_model_v{version}_{timestamp}.pkl"
        with open(filename, 'wb') as f:
            pickle.dump(model, f)
        
        # Actualizar modelo actual
        with open(f"{model_dir}/svd_model_current.pkl", 'wb') as f:
            pickle.dump(model, f)
        
        return filename
    except Exception as e:
        logging.error(f"Error saving model: {str(e)}")
        raise

def main():
    logging.info("Starting model retraining process")
    
    try:
        # Paso 1: Cargar datos
        data = load_data()
        logging.info("Data loaded successfully")
        
        # Paso 2: Entrenar modelo
        model, testset = train_model(data)
        logging.info("Model trained successfully")
        
        # Paso 3: Evaluar modelo
        rmse = evaluate_model(model, testset)
        logging.info(f"Model evaluated. RMSE: {rmse}")
        
        # Paso 4: Guardar modelo
        version = "1.1"  # Incrementar versión según cambios
        model_path = save_model(model, version)
        logging.info(f"Model saved to {model_path}")
        
        logging.info("Retraining process completed successfully")
        return True
    except Exception as e:
        logging.error(f"Retraining process failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)