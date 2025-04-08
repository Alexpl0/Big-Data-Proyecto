import requests, json, os, time
from datetime import datetime

def get_movies_data(page_num):
    """Obtiene datos de películas populares de TMDB"""
    url = f"https://api.themoviedb.org/3/movie/popular?language=es-MX&page={page_num}&region=MX"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2Mjc0NWRiNGU4OGUwZGZjNDYzZGVmM2RjNzA5YjgyOSIsIm5iZiI6MTc0MzQ3Mzg4MC44NTIsInN1YiI6IjY3ZWI0Y2Q4YjBhOWFjNzQxNThiZTQ0ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.NyY98B0skjubdpbqaNejskiAlVKc3DqRv5c-wxN4r9U"
    }
    
    try:
        # Solicitud a la API
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Extracción de metadatos
        movies_in_page = len(data.get('results', []))
        total_pages = data.get('total_pages', 0)
        total_results = data.get('total_results', 0)
            
        # Información de la respuesta
        print(f"\n✓ Página {page_num}: {movies_in_page} películas obtenidas")
        print(f"Primeras películas en página {page_num}:")
        for i, movie in enumerate(data.get('results', [])[:3], 1):
            print(f"{i}. {movie.get('title', 'Sin título')} - Popularidad: {movie.get('popularity', 'N/A')}")
        
        if movies_in_page > 3:
            print(f"... y {movies_in_page - 3} películas más")
            
        return data, movies_in_page, total_pages, total_results, True
    except requests.exceptions.RequestException as e:
        print(f"\n✗ Error en página {page_num}: {str(e)}")
        return None, 0, 0, 0, False

# Configuración inicial
total_pages_to_fetch = 500
start_page = 1
total_movies_fetched = successful_requests = failed_requests = max_pages_available = 0
all_movies_data = []
output_dir = "movie_data"
timestamp_start = datetime.now().strftime("%Y%m%d_%H%M%S")

# Creación de directorio para datos
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print(f"Iniciando descarga de {total_pages_to_fetch} páginas... Inicio: {timestamp_start}")

# Bucle principal de recolección de datos
for page in range(start_page, start_page + total_pages_to_fetch):
    print(f"\n--- Procesando página {page} de {start_page + total_pages_to_fetch - 1} ---")
    
    # Obtención de datos por página
    data, movies_count, pages_available, total_results, success = get_movies_data(page)
    
    # Procesamiento de respuesta
    if success:
        if data and "results" in data:
            # Añadir número de página a cada película
            for movie in data["results"]:
                movie["page_number"] = page
            all_movies_data.extend(data["results"])
        
        total_movies_fetched += movies_count
        successful_requests += 1
        max_pages_available = max(max_pages_available, pages_available)
    else:
        failed_requests += 1
    
    # Detener si alcanzamos el límite de páginas disponibles
    if page >= pages_available > 0:
        print(f"\n¡Límite máximo de páginas alcanzado ({pages_available})!")
        break
    
    # Mostrar progreso periódicamente
    if page % 10 == 0:
        print(f"\n== Progreso: {page}/{total_pages_to_fetch} páginas procesadas ==")
        print(f"Películas obtenidas hasta ahora: {total_movies_fetched}")
    
    # Pausa entre solicitudes para respetar la API
    if page < start_page + total_pages_to_fetch - 1:
        time.sleep(1)

# Guardar resultados en archivo JSON
timestamp_end = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"{output_dir}/all_movies_data_{timestamp_start}_to_{timestamp_end}.json"

# Preparación de datos para guardar con metadatos
complete_data = {
    "metadata": {
        "total_movies": len(all_movies_data),
        "pages_processed": successful_requests,
        "start_timestamp": timestamp_start,
        "end_timestamp": timestamp_end
    },
    "results": all_movies_data
}

# Guardar archivo JSON
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(complete_data, f, ensure_ascii=False, indent=2)

# Cálculo y presentación de estadísticas finales
time_elapsed = datetime.strptime(timestamp_end, '%Y%m%d_%H%M%S') - datetime.strptime(timestamp_start, '%Y%m%d_%H%M%S')
avg_per_page = total_movies_fetched / successful_requests if successful_requests else 0
pct_processed = (successful_requests / max_pages_available * 100) if max_pages_available else 0

print(f"\n✓ Datos guardados en {filename}")
print("\n=== Estadísticas finales ===")
print(f"- Películas obtenidas: {total_movies_fetched} (únicas: {len(all_movies_data)})")
print(f"- Solicitudes: {successful_requests} exitosas, {failed_requests} fallidas")
print(f"- Páginas disponibles: {max_pages_available} ({pct_processed:.1f}% procesadas)")
print(f"- Promedio películas/página: {avg_per_page:.1f}")
print(f"- Tiempo total: {time_elapsed}")
print("\nProceso completado.")

