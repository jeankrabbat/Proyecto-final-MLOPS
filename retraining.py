import pandas as pd
import matplotlib.pyplot as plt
import os
import joblib
from autots import AutoTS
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# --------------------------------------------
# CREATE DIRECTORIES
# --------------------------------------------
os.makedirs("model", exist_ok=True)

# --------------------------------------------
# READ THE DATASET
# --------------------------------------------
df = pd.read_excel("PAX.xlsx", engine='openpyxl')

# Asegurarse que 'Fecha' es datetime y 'Total Pax' no tiene nulos
df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
df = df.dropna(subset=['Fecha', 'Total Pax'])

# --------------------------------------------
# TRAINING WITH AutoTS
# --------------------------------------------
model = AutoTS(
    forecast_length=12,           
    frequency='M',                
    prediction_interval=0.9,
    ensemble="simple",            
    model_list=["ETS", "ARIMA", "FBProphet"],
    transformer_list="fast",      
    max_generations=3,            
    num_validations=2,
    validation_method="backwards"
)

model = model.fit(df, date_col='Fecha', value_col='Total Pax')

# --------------------------------------------
# PREDICTIONS
# --------------------------------------------
prediction = model.predict()
forecasts_df = prediction.forecast

# Guardar predicciones
forecasts_df.to_excel("model/forecasted_pax.xlsx")

# --------------------------------------------
# PLOT RESULTS
# --------------------------------------------
plt.figure(figsize=(12, 6))
plt.plot(df['Fecha'], df['Total Pax'], label='Valores Reales', marker='o')
plt.plot(forecasts_df.index, forecasts_df['Total Pax'], label='Predicciones Futuras', linestyle='--', marker='x')
plt.xlabel('Fecha')
plt.ylabel('Total Pax')
plt.title('Total de Pasajeros - Real vs Predicción')
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig("model/autots_predictions.png", dpi=120)
plt.close()

# --------------------------------------------
# SERIALIZING (Guardar el modelo .pkl)
# --------------------------------------------
joblib.dump(model, "model/autots_model.pkl")
print("✅ Modelo guardado correctamente en 'model/autots_model.pkl'.")

# --------------------------------------------
# METRICS CALCULATION (SIMPLE)
# --------------------------------------------

# Para métricas, comparar los últimos datos reales vs forecast si hay suficiente overlap
real = df['Total Pax'].values[-12:]  # Últimos 12 reales
predicted = forecasts_df['Total Pax'].values

# Chequeo de seguridad por si no hay suficientes reales
min_len = min(len(real), len(predicted))
real = real[:min_len]
predicted = predicted[:min_len]

# Calcular métricas
mae = mean_absolute_error(real, predicted)
rmse = np.sqrt(mean_squared_error(real, predicted))

# --------------------------------------------
# SAVE METRICS
# --------------------------------------------
with open("metrics.txt", "w") as f:
    f.write("## Métricas del Modelo\n")
    f.write(f"- MAE (Error absoluto medio): {mae:.2f}\n")
    f.write(f"- RMSE (Raíz del error cuadrático medio): {rmse:.2f}\n")

print("✅ Métricas guardadas en 'metrics.txt'.")