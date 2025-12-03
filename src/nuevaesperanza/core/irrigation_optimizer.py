import numpy as np
from typing import List, Tuple, Dict

class IrrigationOptimizer:
    """
    Optimiza riego por sectores en pivote central usando zonificación histórica.
    Basado en: productividad pasada + NDVI actual + tipo de suelo.
    """
    
    def zonificar(self, 
                  ndvi_historico: List[float], 
                  ndvi_actual: float,
                  tipo_suelo: str = "arcilloso") -> Dict:
        """
        Retorna zonas de manejo: alta, media, baja productividad.
        """
        # Umbrales calibrados con datos de Guatrache 2020–2024
        if tipo_suelo == "arenoso":
            alto = 0.65
            medio = 0.50
        else:  # arcilloso/limoso (predominante en Guatrache)
            alto = 0.70
            medio = 0.55
        
        prom_historico = np.mean(ndvi_historico) if ndvi_historico else 0.5
        
        # Ajuste por condición actual
        delta = ndvi_actual - prom_historico
        
        if ndvi_actual >= alto and delta >= 0:
            zona = "alta"
            ajuste_riego = 0  # mantener
        elif ndvi_actual >= medio:
            zona = "media"
            ajuste_riego = -5 if delta < -0.05 else 0  # reducir 5% si cae rápido
        else:
            zona = "baja"
            ajuste_riego = 10  # aumentar 10% (posible déficit)
        
        return {
            "zona": zona,
            "ndvi_prom_historico": round(prom_historico, 3),
            "ndvi_actual": round(ndvi_actual, 3),
            "ajuste_riego_porcentaje": ajuste_riego,
            "recomendacion": self._recomendacion(zona, ajuste_riego, tipo_suelo)
        }
    
    def _recomendacion(self, zona: str, ajuste: int, suelo: str) -> str:
        if zona == "alta":
            return "Mantener riego. Monitorear cada 7 días."
        elif zona == "media":
            if ajuste < 0:
                return f"Reducir riego {abs(ajuste)}%. Verificar uniformidad de aspersores."
            else:
                return "Mantener riego. Sector estable."
        else:  # baja
            if suelo == "arenoso":
                return f"Aumentar riego {ajuste}%. Aplicar en ciclos cortos (evitar percolación)."
            else:
                return f"Aumentar riego {ajuste}%. Verificar presión y obstrucciones."
