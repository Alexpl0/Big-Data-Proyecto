import requests
import json
import matplotlib.pyplot as plt
import numpy as np
from obtenerservicio import provedoresget  # Importa tu función

url = "https://api.themoviedb.org/3/trending/movie/week?language=es-MX"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2Mjc0NWRiNGU4OGUwZGZjNDYzZGVmM2RjNzA5YjgyOSIsIm5iZiI6MTc0MzQ3Mzg4MC44NTIsInN1YiI6IjY3ZWI0Y2Q4YjBhOWFjNzQxNThiZTQ0ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.NyY98B0skjubdpbqaNejskiAlVKc3DqRv5c-wxN4r9U"
}

response = requests.get(url, headers=headers)

# Convertir la respuesta a un diccionario de Python
data = json.loads(response.text)

# Listas para almacenar datos filtrados
filtered_titles = []
filtered_scores = []
filtered_ids = []
providers_info = {}  # Para almacenar la información de proveedores

print("Obteniendo información de proveedores de streaming...")

# Filtrar películas que tienen proveedores de streaming
for movie in data.get('results', []):
    movie_id = movie.get('id')
    movie_title = movie.get('title', 'Sin título')
    movie_score = movie.get('vote_average', 0)
    
    # Obtener proveedores para esta película
    providers = provedoresget(movie_id)
    
    # Solo incluir películas con al menos un proveedor
    if providers:
        filtered_titles.append(movie_title)
        filtered_scores.append(movie_score)
        filtered_ids.append(movie_id)
        providers_info[movie_id] = providers
        print(f"✓ '{movie_title}' disponible en: {', '.join(providers.keys())}")
    else:
        print(f"✗ '{movie_title}' no está disponible en ningún servicio de streaming")

# Ordenar por calificación
movie_data = list(zip(filtered_titles, filtered_scores, filtered_ids))
movie_data.sort(key=lambda x: x[1], reverse=True)

# Separar datos ordenados
titles_sorted = [movie[0] for movie in movie_data]
scores_sorted = [movie[1] for movie in movie_data]
ids_sorted = [movie[2] for movie in movie_data]

# Verificar si hay películas con proveedores
if not filtered_titles:
    print("No se encontraron películas con proveedores de streaming disponibles.")
else:
    # Crear la gráfica con los datos filtrados y ordenados
    plt.figure(figsize=(14, 10))
    bars = plt.barh(titles_sorted, scores_sorted, color='skyblue')
    
    # Añadir etiquetas y título
    plt.xlabel('Calificación Promedio')
    plt.ylabel('Películas')
    plt.title('Películas Populares Disponibles en Servicios de Streaming')
    plt.xlim(0, 10)
    
    # Añadir los valores en las barras
    for i, bar in enumerate(bars):
        # Añadir calificación
        plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                f'{scores_sorted[i]:.1f}', 
                va='center')
        
        # Añadir proveedores disponibles
        providers_list = list(providers_info[ids_sorted[i]].keys())
        plt.text(0.1, bar.get_y() + bar.get_height()/2, 
                f"({', '.join(providers_list[:2])}{' y más' if len(providers_list) > 2 else ''})", 
                va='center', ha='left', fontsize=8, color='navy')
    
    # Ajustar diseño
    plt.tight_layout()
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    
    # Mostrar la gráfica
    plt.savefig('peliculas_con_streaming.png', dpi=300)
    plt.show()
    
    # Mostrar resumen
    print(f"\nSe encontraron {len(filtered_titles)} películas disponibles en servicios de streaming.")
    
    # Mostrar top 3 servicios más populares
    all_services = []
    for providers in providers_info.values():
        all_services.extend(providers.keys())
    
    from collections import Counter
    top_services = Counter(all_services).most_common(3)
    
    if top_services:
        print("\nServicios más populares:")
        for service, count in top_services:
            print(f"- {service}: {count} películas")

