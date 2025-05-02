# 📊 Proyecto de Forecast de PAX usando AutoTS y Streamlit

Este proyecto fue realizado como parte del curso de MLOps. El objetivo es realizar un pipeline completo de machine learning, incluyendo entrenamiento, reentrenamiento, versionado, CI/CD y despliegue en la nube.

## 🚀 Integrantes
- Jean Carlo Rabbat Sanchez
- Jorge Chaves Zamora

## 🛠️ Tecnologías utilizadas
- Python 3.11
- Streamlit
- AutoTS
- GitHub Actions
- Docker
- DVC
- AWS S3

## 📈 Descripción del modelo
Utilizamos la librería **AutoTS** para generar un modelo de predicción de pasajeros (**PAX**) mensuales. Se calcula automáticamente la mejor combinación de modelos de series de tiempo.

## 🧑‍💻 Interacción con la aplicación Streamlit

Cuando ejecutes la aplicación, solo se solicitará la cantidad de meses que deseas predecir (con un máximo de 36 meses). Al presionar el botón de **Predecir**, la aplicación realizará los siguientes pasos:

1. **Gráfico de predicciones**: Se mostrará un gráfico con las predicciones de pasajeros para los meses seleccionados.
2. **Tabla de predicciones**: Una tabla con los meses y las respectivas predicciones de pasajeros.
3. **Descarga de los resultados**: Se proporcionará un botón para descargar los resultados en formato **Excel**.