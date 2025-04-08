#Obtener géneros de películas de TMDB y guardarlos en un archivo JSON
import requests, json

def get_generos(api_key, filename='generos.json'):
    """
    Obtiene la lista de géneros de películas de la API de TMDB y la guarda en un archivo JSON.

    Args:
        api_key (str): La clave de API para autenticarse con TMDB.
        filename (str, optional): El nombre del archivo JSON para guardar los géneros. 
                                  Defaults to 'generos.json'.

    Returns:
        dict: Un diccionario donde las claves son los IDs de los géneros y los valores son los nombres.
              Retorna None si hay un error al obtener los géneros.
    """
    url = "https://api.themoviedb.org/3/genre/movie/list?language=es"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lanza una excepción para códigos de error HTTP
        data = response.json()
        genres = data.get('genres', [])
        
        # Filtrar géneros que tienen nombre
        filtered_genres = {genre['id']: genre['name'] for genre in genres if 'name' in genre}
        
        print(f"✓ Géneros guardados en {filename}")
        return filtered_genres
    
    except requests.exceptions.RequestException as e:
        print(f"✗ Error al obtener géneros: {e}")
        return None
    except Exception as e:
        print(f"✗ Error inesperado: {e}")
        return None



