import requests
import json
import matplotlib.pyplot as plt
from collections import defaultdict
import sys
import os

# Add parent directory to path to make imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Imports
from filtros.obtener_sexo import obtener_genero_casting  # Importa la función para obtener y guardar géneros
from filtros.filtro_servicio import peliculas_streaming  # Importa la función para obtener películas de streaming

# Crear un diccionario para contar protagonistas por género
conteo_generos = defaultdict(int)

# Obtener la lista de películas
peliculas = peliculas_streaming()

# Iterar sobre cada película y obtener el género del casting
for pelicula in peliculas:
    movie_id = pelicula.get('id')  # Asegúrate de que 'id' sea la clave correcta para el identificador de la película
    
    if movie_id:
        # Obtener el conteo de géneros para esta película
        mujeres_en_pelicula, hombres_en_pelicula = obtener_genero_casting(movie_id)
        
        # Sumar al conteo total
        conteo_generos['Mujer'] += mujeres_en_pelicula
        conteo_generos['Hombre'] += hombres_en_pelicula
        
        print(f"Película ID: {movie_id}, Mujeres: {mujeres_en_pelicula}, Hombres: {hombres_en_pelicula}")

# Mostrar los resultados
print("Conteo de protagonistas por género:")
for genero, cantidad in conteo_generos.items():
    print(f"{genero}: {cantidad}")

# Generar una gráfica de pastel
plt.figure(figsize=(8, 8))
plt.pie(
    conteo_generos.values(),
    labels=conteo_generos.keys(),
    autopct='%1.1f%%',
    startangle=90,
    colors=['blue', 'pink']  # Puedes personalizar los colores
)
plt.title('Distribución de protagonistas por género')
plt.axis('equal')  # Asegura que el gráfico sea un círculo

# Crear el directorio "graficas" si no existe
graficas_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'graficas')
if not os.path.exists(graficas_dir):
    os.makedirs(graficas_dir)

# Guardar la gráfica utilizando una ruta absoluta
plt.savefig(os.path.join(graficas_dir, 'genero_casting.png'))
plt.show()

