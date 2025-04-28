# Imagen base más ligera
FROM python:3.11-slim

# Evitar preguntas interactivas
ENV DEBIAN_FRONTEND=noninteractive

# Instalamos paquetes necesarios para compilar librerías
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo
WORKDIR /code

# Copiamos solo requirements primero
COPY requirements.txt .

# Actualizamos pip e instalamos dependencias
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de la app
COPY . .

# Puerto para Streamlit
EXPOSE 8501

# Comando para levantar la app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
