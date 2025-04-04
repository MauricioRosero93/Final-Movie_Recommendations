import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import pandas as pd
from data_validation.schema import validate_schema

def load_and_validate_data():
    ratings = pd.read_csv('data/ratings.csv')
    if not validate_schema(ratings):
        raise ValueError("Invalid data schema")
    return ratings

def preprocess_data(ratings):
    # Eliminar duplicados
    ratings = ratings.drop_duplicates()
    # Eliminar ratings fuera de rango
    ratings = ratings[(ratings['rating'] >= 1) & (ratings['rating'] <= 5)]
    return ratings