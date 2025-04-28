FROM python:3.11-slim

WORKDIR /code

# 1. Actualiza pip
RUN pip install --upgrade pip

# 2. Instala primero NumPy (versión <2.0)
COPY requirements.txt .
RUN pip install --no-cache-dir numpy<2.0

# 3. Instala el resto de dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copia el código y expone puerto
COPY . .
EXPOSE 8501

CMD ["streamlit","run","app.py","--server.port=8501","--server.address=0.0.0.0"]
