# CODIGO PARA GENERO MAS POPULAR

import requests
import json
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from filtros.obtener_genero import get_generos  # Importa la función para obtener y guardar géneros
from filtros.obtenerservicio import provedoresget  # Importa la función provedoresget desde el archivo obtenerservicio.py


def analizar_generos_populares(api_key):
    """
    Obtiene las películas más populares de la semana, extrae sus géneros y genera un gráfico de pastel
    mostrando la distribución de los géneros más populares.

    Args:
        api_key (str): La clave de API para autenticarse con TMDB.
    """
    url = "https://api.themoviedb.org/3/trending/movie/week?language=es-MX"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2Mjc0NWRiNGU4OGUwZGZjNDYzZGVmM2RjNzA5YjgyOSIsIm5iZiI6MTc0MzQ3Mzg4MC44NTIsInN1YiI6IjY3ZWI0Y2Q4YjBhOWFjNzQxNThiZTQ0ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.NyY98B0skjubdpbqaNejskiAlVKc3DqRv5c-wxN4r9U"  # Define el encabezado de autorización con el token de acceso a la API
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        trending_movies_data = response.json()
        trending_movies = trending_movies_data.get('results', [])

        # Obtener todos los IDs de géneros de las películas populares
        genre_ids = []
        for movie in trending_movies:
            genre_ids.extend(movie.get('genre_ids', []))

        # Contar la frecuencia de cada género
        genre_counts = Counter(genre_ids)

        # Obtener la lista de géneros desde la API
        generos = get_generos(api_key)
        if not generos:
            print("Error al obtener la lista de géneros.")
            return

        # Preparar datos para el gráfico de pastel
        genre_names = [generos.get(genre_id, 'Desconocido') for genre_id, count in genre_counts.most_common()]
        genre_counts_values = [count for genre_id, count in genre_counts.most_common()]

        # Crear el gráfico de pastel
        plt.figure(figsize=(10, 8))
        plt.pie(genre_counts_values, labels=genre_names, autopct='%1.1f%%', startangle=140)
        plt.title('Géneros de Películas Más Populares de la Semana')
        plt.axis('equal')  # Equal aspect ratio asegura que el pastel se dibuje como un círculo.

        plt.savefig('../graficas/generos_populares.png')  # Guarda el gráfico en la carpeta "graficas" usando un path relativo
        plt.show()
       

    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos de la API: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")


if __name__ == "__main__":
    api_key = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2Mjc0NWRiNGU4OGUwZGZjNDYzZGVmM2RjNzA5YjgyOSIsIm5iZiI6MTc0MzQ3Mzg4MC44NTIsInN1YiI6IjY3ZWI0Y2Q4YjBhOWFjNzQxNThiZTQ0ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.NyY98B0skjubdpbqaNejskiAlVKc3DqRv5c-wxN4r9U"  # Reemplaza con tu clave de API
    analizar_generos_populares(api_key)