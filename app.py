from flask import Flask, jsonify
import pickle
import pandas as pd

# Cargar modelos y datos
with open('models/svd_model.pkl', 'rb') as f:
    model = pickle.load(f)

movies = pd.read_csv('data/movies.csv')

# Crear aplicación Flask
app = Flask(__name__)

# Función para generar recomendaciones
def recommend_movies(user_id, n=20):
    all_movies = movies['movieId'].unique()
    predictions = [model.predict(user_id, movie_id) for movie_id in all_movies]
    top_movies = sorted(predictions, key=lambda x: x.est, reverse=True)[:n]
    recommended_movie_ids = [pred.iid for pred in top_movies]
    recommended_movies = movies[movies['movieId'].isin(recommended_movie_ids)]
    return recommended_movies['title'].tolist()

# Ruta para obtener recomendaciones
@app.route('/recommend/<int:user_id>', methods=['GET'])
def recommend(user_id):
    recommendations = recommend_movies(user_id)
    return jsonify(recommendations)

# Iniciar servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)