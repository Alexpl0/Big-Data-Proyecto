import requests
from collections import Counter

def obtener_genero_casting(movie_id):        
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?language=es-MX"  # Corrige la interpolación de movie_id

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2Mjc0NWRiNGU4OGUwZGZjNDYzZGVmM2RjNzA5YjgyOSIsIm5iZiI6MTc0MzQ3Mzg4MC44NTIsInN1YiI6IjY3ZWI0Y2Q4YjBhOWFjNzQxNThiZTQ0ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.NyY98B0skjubdpbqaNejskiAlVKc3DqRv5c-wxN4r9U"
    }

    response = requests.get(url, headers=headers)
    data = response.json()  # Convertir la respuesta a un diccionario de Python

    # Filtrar las primeras 10 entradas (order <= 9)
    casting = data.get("cast", [])
    primeros_10 = [actor for actor in casting if actor.get("order", 10) <= 9]

    # Contar las ocurrencias de gender: 1 y gender: 2
    contador_generos = Counter(actor.get("gender") for actor in primeros_10)

    # Obtener los resultados
    gender_1_count = contador_generos.get(1, 0)
    gender_2_count = contador_generos.get(2, 0)

    return gender_1_count, gender_2_count

if __name__ == "__main__":
    # Ejemplo de uso
    movie_id = 1265623  # Reemplaza con un ID de película válido (por ejemplo, el ID de "Fight Club")
    try:
        gender_1, gender_2 = obtener_genero_casting(movie_id)
        print(f"En los primeros 10 actores del casting de la película con ID {movie_id}:")
        print(f"- Gender 1 (Femenino): {gender_1}")
        print(f"- Gender 2 (Masculino): {gender_2}")
    except Exception as e:
        print(f"Error al obtener los datos: {e}")