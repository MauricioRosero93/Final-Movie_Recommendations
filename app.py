from flask import Flask, jsonify, request, render_template
#from prometheus_metrics import RECOMMENDATIONS_COUNT, RESPONSE_TIME
import pickle
import pandas as pd
from datetime import datetime
import os
import time
from prometheus_client import start_http_server, Counter, Histogram


RECOMMENDATIONS_COUNT = Counter('recommendations_total', 'Total de recomendaciones generadas')
RESPONSE_TIME = Histogram('response_time_seconds', 'Tiempo de respuesta del endpoint /recommend')
RATINGS_COUNTER = Counter(
    'movie_ratings_total',
    'Total de ratings registrados por valoración',
    ['stars'] 
)

#start_http_server(8000, addr='0.0.0.0') 

# Cargar modelos y datos
with open('models/svd_model.pkl', 'rb') as f:
    model = pickle.load(f)

movies = pd.read_csv('data/movies.csv') 

app = Flask(__name__)

# Obtener título de las películas
def get_movie_title(movie_id):
    """Obtiene el título de una película por su ID"""
    movie = movies[movies['movieId'] == movie_id]
    return movie.iloc[0]['title'] if not movie.empty else None

# Registra llamadas al endpoint /recommend
def log_interaction(user_id, recommendations, response_time):
    """Registra llamadas al endpoint /recommend"""
    os.makedirs("monitoring", exist_ok=True)
    pd.DataFrame([{
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": user_id,
        "recommendations": "|".join(map(str, recommendations)),
        "response_time_ms": response_time,
        "num_recommendations": len(recommendations)
    }]).to_csv(
        "monitoring/recommendations_log.csv",
        mode='a',
        header=not os.path.exists("monitoring/recommendations_log.csv"),
        index=False,
        quoting=1
    )

# Endpoints
@app.route('/recommend/<int:user_id>', methods=['GET'])
def recommend(user_id):
    start_time = time.time()
    movie_titles = recommend_movies(user_id)
    # Registro de métricas
    RESPONSE_TIME.observe(time.time() - start_time)
    RECOMMENDATIONS_COUNT.inc()
    log_interaction(
        user_id=user_id,
        recommendations=movie_titles,
        response_time=int((time.time() - start_time) * 1000)
    )
    return jsonify(movie_titles)


def recommend_movies(user_id, n=20):
    all_movies = movies['movieId'].unique()
    predictions = [model.predict(user_id, movie_id) for movie_id in all_movies]
    top_movies = sorted(predictions, key=lambda x: x.est, reverse=True)[:n]
    return [get_movie_title(pred.iid) for pred in top_movies]



@app.route('/rate/<int:movie_id>=<int:rating>', methods=['GET'])
def rate_movie(movie_id, rating):
    """Endpoint para calificar películas"""
    # Validaciones
    if not 1 <= rating <= 5:
        return jsonify({"error": "El rating debe ser entre 1 y 5"}), 400
    
    movie_title = get_movie_title(movie_id)
    if not movie_title:
        return jsonify({"error": f"Película con ID {movie_id} no encontrada"}), 404

    # Registrar rating
    os.makedirs("monitoring", exist_ok=True)
    pd.DataFrame([{
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_ip": request.remote_addr,  # Opcional: registrar IP
        "movie_id": movie_id,
        "movie_title": movie_title,
        "rating": rating
    }]).to_csv(
        "monitoring/ratings_log.csv",
        mode='a',
        header=not os.path.exists("monitoring/ratings_log.csv"),
        index=False,
        quoting=1
    )

    RATINGS_COUNTER.labels(stars=str(rating)).inc()

    return jsonify({
        "status": "success",
        "message": f"Calificacion registrada: {rating} estrellas para '{movie_title}'"
    })

@app.route('/monitoring')
def show_monitoring():
    try:
        # Carga de datos con manejo de errores
        recs = pd.read_csv("monitoring/recommendations_log.csv", on_bad_lines='skip') \
            if os.path.exists("monitoring/recommendations_log.csv") else pd.DataFrame()
        
        ratings = pd.read_csv("monitoring/ratings_log.csv", on_bad_lines='skip') \
            if os.path.exists("monitoring/ratings_log.csv") else pd.DataFrame()

        # Preparación de tablas con alineación izquierda
        tables = []
        table_titles = []
        
        if not recs.empty:
            tables.append(recs.to_html(
                classes='table table-striped table-hover',
                justify='left',
                index=False
            ))
            table_titles.append("📽️ Historial de Recomendaciones")
        
        if not ratings.empty:
            tables.append(ratings.to_html(
                classes='table table-striped table-hover',
                justify='left',
                index=False
            ))
            table_titles.append("Calificaciones Registradas")

        return render_template(
            'monitoring.html',
            tables=tables,
            table_titles=table_titles,
            now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            no_data=len(tables) == 0
        )

    except Exception as e:
        app.logger.error(f"Error en monitoring: {str(e)}")
        return render_template(
            'monitoring.html',
            error_message=str(e),
            now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

# 4. Configuración inicial
if __name__ == '__main__':
    start_http_server(8000, addr='0.0.0.0')
    app.run(host='0.0.0.0', port=8082, debug=False)
