import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import pandas as pd

def validate_schema(data):
    required_columns = {'userId', 'movieId', 'rating'}
    if not required_columns.issubset(data.columns):
        return False
    
    if not pd.api.types.is_numeric_dtype(data['userId']):
        return False
    
    if not pd.api.types.is_numeric_dtype(data['movieId']):
        return False
    
    if not pd.api.types.is_numeric_dtype(data['rating']):
        return False
    
    return True