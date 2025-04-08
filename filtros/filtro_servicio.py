#Funcion principal para obtener peliculas y proveedores de streaming

import requests
import json
from filtros.obtenerservicio import provedoresget  # Importa la función provedoresget desde el archivo obtenerservicio.py

def peliculas_streaming():
    """
    Obtiene las películas más populares de la semana y verifica si están disponibles en plataformas de streaming,
    realizando múltiples llamadas a la API para obtener más películas y guardando únicamente las que tienen proveedores de streaming.

    Returns:
        list: Lista de películas con información extendida, incluyendo las plataformas de streaming disponibles.
    """
    base_url = "https://api.themoviedb.org/3/trending/movie/week?language=es-MX&page={}"  # URL base de la API con soporte para paginación
    headers = {
        "accept": "application/json",  # Define el tipo de contenido aceptado en la respuesta como JSON
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2Mjc0NWRiNGU4OGUwZGZjNDYzZGVmM2RjNzA5YjgyOSIsIm5iZiI6MTc0MzQ3Mzg4MC44NTIsInN1YiI6IjY3ZWI0Y2Q4YjBhOWFjNzQxNThiZTQ0ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.NyY98B0skjubdpbqaNejskiAlVKc3DqRv5c-wxN4r9U"  # Define el encabezado de autorización con el token de acceso a la API
    }

    peliculas_con_proveedores = []  # Lista para almacenar las películas con proveedores de streaming

    print("Obteniendo información de proveedores de streaming...")  # Imprime un mensaje indicando que se está obteniendo la información de los proveedores de streaming

    # Realizar múltiples llamadas a la API (por ejemplo, 3 páginas)
    for page in range(1, 4):  # Iterar sobre las páginas 1, 2 y 3
        url = base_url.format(page)  # Formatear la URL con el número de página actual
        response = requests.get(url, headers=headers)  # Realiza una solicitud GET a la URL de la API con los encabezados especificados

        # Convertir la respuesta a un diccionario de Python
        data = json.loads(response.text)  # Convierte la respuesta de la API (en formato JSON) a un diccionario de Python

        # Iterar sobre las películas obtenidas de la API
        for movie in data.get('results', []):  # Itera sobre los resultados de la respuesta de la API (lista de películas)
            movie_id = movie.get('id')  # Obtiene el ID de la película
            movie_title = movie.get('title', 'Sin título')  # Obtiene el título de la película (si no tiene título, asigna 'Sin título')
            
            # Obtener proveedores para esta película
            providers = provedoresget(movie_id)  # Llama a la función provedoresget para obtener los proveedores de streaming para esta película
            
            # Agregar información de proveedores a la película si tiene al menos un proveedor
            if providers:  # Si la película tiene al menos un proveedor de streaming
                movie['streaming_providers'] = list(providers.keys())  # Agrega los nombres de los proveedores como una lista
                peliculas_con_proveedores.append(movie)  # Agrega la película con la información extendida a la lista
                #print(f"✓ '{movie_title}' disponible en: {', '.join(providers.keys())}")  # Imprime un mensaje indicando que la película está disponible en los proveedores especificados
            
    return peliculas_con_proveedores

if __name__ == '__main__':
    # Ejemplo de uso de la función
    peliculas = peliculas_streaming()
    #Convertimos a JSON la lista de películas
    with open('../movie_data/peliculas_streaming.json', 'w') as f: # Abre el archivo en modo escritura
        json.dump(peliculas, f, indent=4) # Guarda la lista de películas en un archivo JSON con una indentación de 4 espacios
        #Envia un mensaje indicando que se guardó la información
        print("✓ Información de películas guardada en 'peliculas_streaming.json'")