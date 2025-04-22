Collecting workspace information# Análisis de Películas y Plataformas de Streaming

## Descripción General
Este proyecto analiza datos de películas obtenidos a través de la API de The Movie Database (TMDb) para identificar patrones de consumo, distribución por género, servicios de streaming más relevantes y tendencias semanales. El sistema automatizado conecta con la API, extrae información, la transforma y genera visualizaciones que representan aspectos clave del ecosistema actual de entretenimiento digital.

## Estructura del Proyecto
```
data-science-template/
├── documentacion/            # Documentación detallada del proyecto
│   ├── Documentacion12.ipynb # Notebook principal con análisis y resultados
│   └── .ipynb_checkpoints/   # Checkpoints del notebook
│
├── estadisticas/             # Scripts para análisis estadísticos
│   ├── genero_casting.py     # Análisis de distribución por género en elencos
│   ├── genero_popular.py     # Análisis de géneros más populares 
│   ├── pelicula_popular.py   # Análisis de películas más populares
│   └── servicio_popular.py   # Análisis de plataformas de streaming populares
│
├── filtros/                  # Scripts de procesamiento y filtrado
│   ├── crear_json_database.py # Generación de base de datos en JSON
│   ├── filtro_servicio.py    # Filtrado por disponibilidad en servicios
│   ├── obtener_genero.py     # Obtención de información de géneros
│   ├── obtener_sexo.py       # Obtención de información de género del elenco
│   └── obtenerservicio.py    # Obtención de información de servicios de streaming
│
├── graficas/                 # Visualizaciones generadas
│   ├── genero_casting.png    # Gráfica de distribución por género
│   ├── generos_populares.png # Gráfica de géneros más comunes
│   ├── peliculas_con_streaming.png # Gráfica de películas por servicio
│   └── proveedor_popular.png # Gráfica de popularidad por proveedor
│
├── movie_data/               # Datos extraídos y procesados
│   ├── peliculas_streaming.json # Películas con disponibilidad en streaming
│   └── generos.json          # Mapeo de IDs de géneros a nombres
│
├── tests/                    # Tests unitarios
├── requirements.txt          # Dependencias principales
├── dev-requirements.txt      # Dependencias para desarrollo
└── README.md                 # Este archivo
```

## Características Principales

### 1. Extracción de Datos
- Consume la API pública de TMDb para obtener películas populares
- Implementa paginación para obtener aproximadamente 10,000 películas únicas
- Filtra resultados por disponibilidad en plataformas de streaming

### 2. Análisis y Visualizaciones
- **Distribución de protagonistas por género**: Analiza el balance de género en los elencos
- **Géneros más populares**: Identifica tendencias actuales en géneros cinematográficos
- **Películas populares y su disponibilidad**: Relaciona calificaciones con servicios de streaming
- **Plataformas de streaming dominantes**: Evalúa qué servicios ofrecen más contenido popular

### 3. Resultados Clave
- Identificación de plataformas dominantes (Netflix, Disney+, Amazon Prime Video)
- Análisis de tendencias en géneros cinematográficos (aventura, acción, comedia)
- Evaluación de la representación de género en los elencos
- Distribución de calificaciones y métricas de popularidad

## Requisitos Técnicos
- Python 3.10+
- Bibliotecas principales:
  - pandas
  - matplotlib
  - numpy
  - requests
  - json
  - datetime

## Instalación y Ejecución

1. Clone este repositorio:
```bash
git clone https://github.com/usuario/data-science-template.git
cd data-science-template
```

2. Instale las dependencias:
```bash
pip install -r requirements.txt
```

3. Configure su token de API de TMDb:
Obtenga su token en [TMDb API](https://www.themoviedb.org/documentation/api) y actualice el token en los scripts de la carpeta filtros.

4. Ejecute los scripts de análisis:
```bash
python -m estadisticas.genero_popular
python -m estadisticas.servicio_popular
python -m estadisticas.pelicula_popular
python -m estadisticas.genero_casting
```

## Documentación
La documentación completa del proyecto se encuentra en el notebook Documentacion12.ipynb, que incluye:
- Metodología detallada
- Análisis exploratorio de datos
- Visualizaciones comentadas
- Conclusiones y hallazgos

## Contribuciones
Este proyecto fue desarrollado por Alejandro Pérez y Yusmany Rejopachi.

Para contribuir:
1. Fork el repositorio
2. Cree una nueva rama (`git checkout -b feature/nueva-funcionalidad`)
3. Realice sus cambios y haga commit (`git commit -m 'Añade nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abra un Pull Request

## Licencia
Este proyecto está disponible como código abierto bajo los términos de la licencia MIT.

## Referencias
- [The Movie Database (TMDb) API](https://www.themoviedb.org/documentation/api)
- [pandas - Python Data Analysis Library](https://pandas.pydata.org/)
- [matplotlib - Visualization Library](https://matplotlib.org/)
- [Requests: HTTP for Humans](https://docs.python-requests.org/)