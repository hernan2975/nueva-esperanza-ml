import numpy as np
import joblib
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from pathlib import Path

# Generar datos sintéticos realistas (basados en historial de Guatrache)
np.random.seed(2025)
n = 150
X = np.column_stack([
    np.random.randint(55, 65, n),      # días ciclo
    np.random.uniform(30, 60, n),     # precip 30d
    np.random.uniform(25, 30, n),     # temp max
    np.random.uniform(0.35, 0.55, n), # ndvi_60d
    np.random.choice([0, 1], n),      # híbrido
    np.random.randint(70, 90, n),     # prof suelo
    np.random.uniform(6.2, 7.0, n)    # pH
])
# Rendimiento realista: depende de NDVI y precip
y = (X[:, 3] * 120 + X[:, 1] * 0.3 + X[:, 2] * -0.5 + 
     X[:, 4] * 3 + X[:, 5] * 0.1 + np.random.normal(0, 3, n))

# Entrenar modelo liviano
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
model = Ridge(alpha=1.0)
model.fit(X_scaled, y)

# Guardar modelo + scaler
Path("data/models").mkdir(parents=True, exist_ok=True)
joblib.dump({
    "model": model,
    "scaler": scaler,
    "features": ["dias_ciclo", "precip_30d", "temp_max_prom", "ndvi_60d", 
                "es_hibrido", "prof_suelo_cm", "ph_suelo"]
}, "data/models/yield_predictor_v2.joblib")

# Stress detector: no necesita entrenamiento (es regla basada)
# Pero guardamos un placeholder para consistencia
joblib.dump({"version": "1.0", "method": "color_texture_analysis"}, 
            "data/models/stress_detector_v1.joblib")

print("✅ Modelos generados en data/models/")
