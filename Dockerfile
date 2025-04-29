FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

# Instala las dependencias del sistema necesarias para numpy y matplotlib
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libatlas-base-dev \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    libpng-dev \
    libopenblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY requirements.txt .

# Primero actualiza pip, setuptools, wheel
RUN pip install --upgrade pip setuptools wheel

# Instala numpy primero
RUN pip install --no-cache-dir numpy==1.24.4

# Luego instala el resto
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
