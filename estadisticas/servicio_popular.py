# CODIGO PARA SERVICIO MAS POPULAR

import requests
import json
import matplotlib.pyplot as plt
from collections import defaultdict
from filtros.filtro_servicio import peliculas_streaming  # Importa la función peliculas_streaming desde el archivo filtro_servicio.py

# Llama a la función peliculas_streaming para obtener la lista de películas con proveedores de streaming
servicio_popular = peliculas_streaming()

# Crear un diccionario para acumular la popularidad por proveedor
popularidad_por_proveedor = defaultdict(float)

# Procesar los datos para acumular la popularidad de cada proveedor
for pelicula in servicio_popular:
    proveedores = pelicula.get("streaming_providers", [])
    popularidad = pelicula.get("popularity", 0)
    for proveedor in proveedores:
        popularidad_por_proveedor[proveedor] += popularidad

# Agrupar proveedores que coinciden en la primera palabra
agrupados_por_proveedor = defaultdict(float)
for proveedor, popularidad in popularidad_por_proveedor.items():
    primera_palabra = proveedor.split()[0]  # Obtener la primera palabra del nombre del proveedor
    agrupados_por_proveedor[primera_palabra] += popularidad

# Ordenar los proveedores por popularidad
proveedores_ordenados = sorted(agrupados_por_proveedor.items(), key=lambda x: x[1], reverse=True)

# Separar los nombres de los proveedores y sus popularidades
proveedores = [item[0] for item in proveedores_ordenados]
popularidades = [item[1] for item in proveedores_ordenados]

# Crear una gráfica de barras
plt.figure(figsize=(10, 6))
plt.bar(proveedores, popularidades, color='skyblue')
plt.xlabel('Proveedores de Streaming')
plt.ylabel('Popularidad Acumulada')
plt.title('Proveedor de Streaming Más Popular')
plt.bar_label(plt.bar(proveedores, popularidades), padding=3)  # Añadir etiquetas a las barras

plt.xticks(rotation=90, ha='right')  # Rotar etiquetas del eje x para mejor legibilidad
plt.grid(axis='y', linestyle='--', alpha=0.7)  # Añadir líneas de cuadrícula para facilitar la lectura
plt.tight_layout()

# Mostrar la gráfica
plt.savefig('../graficas/proveedor_popular.png')  # Guarda la gráfica en un archivo PNG con una resolución de 300 DPI
plt.show()
