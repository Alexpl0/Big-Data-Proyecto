import requests


def provedoresget(movie_id): #Es una función que obtiene los proveedores de servicios de streaming para una película específica
    """
    Obtiene los proveedores de servicios de streaming para una película específica.
    
    Args:
        movie_id (int): El ID de la película.
        
    Returns:
        dict: Un diccionario con los proveedores de servicios de streaming.
    """
    # URL para obtener los proveedores de servicios de streaming
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2Mjc0NWRiNGU4OGUwZGZjNDYzZGVmM2RjNzA5YjgyOSIsIm5iZiI6MTc0MzQ3Mzg4MC44NTIsInN1YiI6IjY3ZWI0Y2Q4YjBhOWFjNzQxNThiZTQ0ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.NyY98B0skjubdpbqaNejskiAlVKc3DqRv5c-wxN4r9U"
    }

    response = requests.get(url, headers=headers)

    #Convertir la respuesta a un diccionario de Python
    data = response.json()
    # Extraer los proveedores de servicios de streaming
    providers = data.get('results', {}).get('MX', {}).get('flatrate', []) # Cambia 'MX' por el código de país que necesites
    # Crear un diccionario para almacenar los proveedores
    providers_dict = {}
    for provider in providers:
        logo_path = provider.get('logo_path', '')
        provider_name = provider.get('provider_name', 'Sin nombre')
        providers_dict[provider_name] = logo_path

    #devuelve solo los provedores que tengan nombre
    providers_dict = {k: v for k, v in providers_dict.items() if k != 'Sin nombre'}
    return providers_dict
