import numpy as np
import joblib
from pathlib import Path

class YieldPredictor:
    """Pronostica rendimiento de trigo/maíz en qq/ha a los 60 días del ciclo."""
    
    def __init__(self, model_path=None):
        if model_path is None:
            model_path = Path(__file__).parent.parent.parent / "data" / "models" / "yield_predictor_v2.joblib"
        self.model = joblib.load(model_path)
        self.features = [
            "dias_ciclo", "precip_30d", "temp_max_prom", "ndvi_60d",
            "es_hibrido", "prof_suelo_cm", "ph_suelo"
        ]
    
    def predict(self, 
                dias_ciclo: int,
                precip_30d: float,
                temp_max_prom: float,
                ndvi_60d: float,
                es_hibrido: bool,
                prof_suelo_cm: int,
                ph_suelo: float,
                cultivo: str = "trigo") -> dict:
        """
        Retorna: {"qq_ha": float, "intervalo_90": (min, max), "confianza": str}
        """
        X = np.array([[
            dias_ciclo,
            precip_30d,
            temp_max_prom,
            ndvi_60d,
            int(es_hibrido),
            prof_suelo_cm,
            ph_suelo
        ]])
        
        qq_ha = self.model.predict(X)[0]
        
        # Intervalo basado en error histórico (no bootstrap — muy pesado para campo)
        if cultivo == "trigo":
            error = 4.2  # qq/ha (validado en Guatrache 2020–2024)
        else:
            error = 5.8
        
        return {
            "qq_ha": round(qq_ha, 1),
            "intervalo_90": (round(qq_ha - error, 1), round(qq_ha + error, 1)),
            "confianza": "alta" if ndvi_60d > 0.4 else "media"
        }
