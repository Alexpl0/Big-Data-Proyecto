#CODIGO PARA PELICULA MAS POPULAR

import requests
import json
import matplotlib.pyplot as plt
import numpy as np
from filtros.obtenerservicio import provedoresget  # Importa la función provedoresget desde el archivo obtenerservicio.py

url = "https://api.themoviedb.org/3/trending/movie/week?language=es-MX"  # Define la URL de la API de The Movie Database (TMDb) para obtener las películas de tendencia semanales en español de México

headers = {
    "accept": "application/json",  # Define el tipo de contenido aceptado en la respuesta como JSON
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2Mjc0NWRiNGU4OGUwZGZjNDYzZGVmM2RjNzA5YjgyOSIsIm5iZiI6MTc0MzQ3Mzg4MC44NTIsInN1YiI6IjY3ZWI0Y2Q4YjBhOWFjNzQxNThiZTQ0ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.NyY98B0skjubdpbqaNejskiAlVKc3DqRv5c-wxN4r9U"  # Define el encabezado de autorización con el token de acceso a la API
}

response = requests.get(url, headers=headers)  # Realiza una solicitud GET a la URL de la API con los encabezados especificados

# Convertir la respuesta a un diccionario de Python
data = json.loads(response.text)  # Convierte la respuesta de la API (en formato JSON) a un diccionario de Python

# Listas para almacenar datos filtrados
filtered_titles = []  # Lista para almacenar los títulos de las películas filtradas
filtered_scores = []  # Lista para almacenar las calificaciones de las películas filtradas
filtered_ids = []  # Lista para almacenar los IDs de las películas filtradas
providers_info = {}  # Para almacenar la información de proveedores (diccionario donde la clave es el ID de la película y el valor es la información de los proveedores)

print("Obteniendo información de proveedores de streaming...")  # Imprime un mensaje indicando que se está obteniendo la información de los proveedores de streaming

# Filtrar películas que tienen proveedores de streaming
for movie in data.get('results', []):  # Itera sobre los resultados de la respuesta de la API (lista de películas)
    movie_id = movie.get('id')  # Obtiene el ID de la película
    movie_title = movie.get('title', 'Sin título')  # Obtiene el título de la película (si no tiene título, asigna 'Sin título')
    movie_score = movie.get('vote_average', 0)  # Obtiene la calificación promedio de la película (si no tiene calificación, asigna 0)
    
    # Obtener proveedores para esta película
    providers = provedoresget(movie_id)  # Llama a la función provedoresget para obtener los proveedores de streaming para esta película
    
    # Solo incluir películas con al menos un proveedor
    if providers:  # Si la película tiene al menos un proveedor de streaming
        filtered_titles.append(movie_title)  # Agrega el título de la película a la lista de títulos filtrados
        filtered_scores.append(movie_score)  # Agrega la calificación de la película a la lista de calificaciones filtradas
        filtered_ids.append(movie_id)  # Agrega el ID de la película a la lista de IDs filtrados
        providers_info[movie_id] = providers  # Almacena la información de los proveedores en el diccionario providers_info
        print(f"✓ '{movie_title}' disponible en: {', '.join(providers.keys())}")  # Imprime un mensaje indicando que la película está disponible en los proveedores especificados
    else:
        print(f"✗ '{movie_title}' no está disponible en ningún servicio de streaming")  # Imprime un mensaje indicando que la película no está disponible en ningún servicio de streaming

# Ordenar por calificación
movie_data = list(zip(filtered_titles, filtered_scores, filtered_ids))  # Crea una lista de tuplas con los títulos, calificaciones e IDs de las películas filtradas
movie_data.sort(key=lambda x: x[1], reverse=True)  # Ordena la lista de tuplas en orden descendente según la calificación

# Separar datos ordenados
titles_sorted = [movie[0] for movie in movie_data]  # Crea una lista con los títulos de las películas ordenadas
scores_sorted = [movie[1] for movie in movie_data]  # Crea una lista con las calificaciones de las películas ordenadas
ids_sorted = [movie[2] for movie in movie_data]  # Crea una lista con los IDs de las películas ordenadas

# Verificar si hay películas con proveedores
if not filtered_titles:  # Si no se encontraron películas con proveedores de streaming
    print("No se encontraron películas con proveedores de streaming disponibles.")  # Imprime un mensaje indicando que no se encontraron películas con proveedores de streaming disponibles
else:
    # Crear la gráfica con los datos filtrados y ordenados
    plt.figure(figsize=(14, 10))  # Crea una nueva figura para el gráfico con un tamaño específico
    bars = plt.barh(titles_sorted, scores_sorted, color='skyblue')  # Crea un gráfico de barras horizontales con los títulos y calificaciones de las películas ordenadas
    
    # Añadir etiquetas y título
    plt.xlabel('Calificación Promedio')  # Añade una etiqueta al eje x
    plt.ylabel('Películas')  # Añade una etiqueta al eje y
    plt.title('Películas Populares Disponibles en Servicios de Streaming')  # Añade un título al gráfico
    plt.xlim(0, 10)  # Establece los límites del eje x (calificación de 0 a 10)
    
    # Añadir los valores en las barras
    for i, bar in enumerate(bars):  # Itera sobre cada barra en el gráfico
        # Añadir calificación
        plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                f'{scores_sorted[i]:.1f}', 
                va='center')  # Añade la calificación de la película al final de cada barra
        
        # Añadir proveedores disponibles
        providers_list = list(providers_info[ids_sorted[i]].keys())  # Obtiene la lista de proveedores para la película actual
        plt.text(0.1, bar.get_y() + bar.get_height()/2, 
                f"({', '.join(providers_list[:2])}{' y más' if len(providers_list) > 2 else ''})", 
                va='center', ha='left', fontsize=8, color='navy')  # Añade los nombres de los proveedores (hasta 2) al inicio de cada barra
    
    # Ajustar diseño
    plt.tight_layout()  # Ajusta automáticamente los parámetros del subplot para proporcionar un diseño compacto
    plt.grid(axis='x', linestyle='--', alpha=0.7)  # Añade una cuadrícula al eje x para facilitar la lectura
    
    # Mostrar la gráfica
    plt.savefig('../graficas/peliculas_con_streaming.png', dpi=300)  # Guarda la gráfica en un archivo PNG con una resolución de 300 DPI
    plt.show()  # Muestra la gráfica en una ventana
    
    # Mostrar resumen
    print(f"\nSe encontraron {len(filtered_titles)} películas disponibles en servicios de streaming.")  # Imprime el número de películas encontradas con proveedores de streaming
    
    # Mostrar top 3 servicios más populares
    all_services = []  # Crea una lista vacía para almacenar todos los servicios de streaming
    for providers in providers_info.values():  # Itera sobre los valores del diccionario providers_info (información de los proveedores)
        all_services.extend(providers.keys())  # Extiende la lista all_services con los nombres de los proveedores de cada película
    
    from collections import Counter  # Importa la clase Counter desde el módulo collections
    top_services = Counter(all_services).most_common(3)  # Cuenta la frecuencia de cada servicio en la lista all_services y obtiene los 3 más comunes
    
    if top_services:  # Si se encontraron servicios de streaming
        print("\nServicios más populares:")  # Imprime un encabezado indicando los servicios más populares
        for service, count in top_services:  # Itera sobre los servicios más populares y su frecuencia
            print(f"- {service}: {count} películas")  # Imprime el nombre del servicio y el número de películas en las que está disponible

