from flask import Flask, jsonify
import pickle
import pandas as pd
import numpy as np

# 1. Carga de datos y modelo (EXACTAMENTE como en tu Milestone 1)
with open('models/svd_model.pkl', 'rb') as f:
    model = pickle.load(f)

movies = pd.read_csv('data/movies.csv')

app = Flask(__name__)

# 2. Función de recomendación (igual que tu versión original)
def recommend_movies(user_id, n=20):
    # Tomar muestra representativa (mejor que todas las películas)
    sample_size = min(2000, len(movies))  # Más grande que antes pero manejable
    movie_sample = np.random.choice(movies['movieId'].unique(), size=sample_size, replace=False)
    
    predictions = []
    for movie_id in movie_sample:
        try:
            pred = model.predict(user_id, movie_id)
            predictions.append((movie_id, pred.est))
        except:
            continue
    
    # Ordenar igual que antes
    predictions.sort(key=lambda x: -x[1])
    top_movies = [m[0] for m in predictions[:n]]
    
    # Mismo formato de salida
    return movies[movies['movieId'].isin(top_movies)]['title'].tolist()

# 3. Endpoint idéntico
@app.route('/recommend/<int:user_id>', methods=['GET'])
def recommend(user_id):
    return jsonify(recommend_movies(user_id))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)