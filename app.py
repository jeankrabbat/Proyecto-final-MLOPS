# --------------------------------------------
# IMPORTS
# --------------------------------------------
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib
import io
from autots import AutoTS

# --------------------------------------------
# SET PAGE CONFIG FIRST
# --------------------------------------------
st.set_page_config(page_title="✈️ Predicción de Pasajeros", layout="centered")

# --------------------------------------------
# LOAD MODEL
# --------------------------------------------
@st.cache_resource
def load_model():
    model = joblib.load("model/autots_model.pkl")
    return model

model = load_model()

# --------------------------------------------
# STREAMLIT INTERFACE
# --------------------------------------------
st.title("✈️ Predicción de Tráfico de Pasajeros")
st.markdown(
    """
    Bienvenido a la app de predicción de tráfico de pasajeros.  
    Selecciona cuántos meses quieres predecir y visualiza los resultados.
    """
)

# Input: ¿Cuántos meses quieres predecir?
months_to_predict = st.number_input(
    "¿Cuántos meses quieres predecir?",
    min_value=1,
    max_value=36,
    value=12,
    step=1
)

# Botón para lanzar predicción
if st.button("🔮 Predecir"):

    with st.spinner('Calculando predicción... ⏳'):

        # Ajustar forecast_length en el modelo
        model.forecast_length = months_to_predict

        # Predecir
        prediction = model.predict()
        forecast_df = prediction.forecast

    st.success("✅ Predicción realizada correctamente.")

    # Mostrar gráfico
    st.subheader("📈 Gráfico de Predicciones")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(forecast_df.index, forecast_df['Total Pax'], marker='o', linestyle='--', color='royalblue')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Total Pax')
    ax.set_title('Predicción de Tráfico de Pasajeros')
    ax.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Mostrar tabla
    st.subheader("📋 Tabla de Predicciones")
    st.dataframe(forecast_df)

    # Descargar predicción
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        forecast_df.to_excel(writer, index=True, sheet_name='Predicciones')
    st.download_button(
        label="⬇️ Descargar Predicciones en Excel",
        data=output.getvalue(),
        file_name='predicciones_pasajeros.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

# Footer
st.markdown("---")
st.caption("Desarrollado por Jean Carlo Rabbat y Jorge Chaves para nuestra clase de MLOps con el profesor Jorge Zapata 🚀")