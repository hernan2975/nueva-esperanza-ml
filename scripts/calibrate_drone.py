#!/usr/bin/env python3
"""
Calibración de cámara de dron/smartphone para corrección de color.
Genera un archivo `calibration.json` para mejorar análisis de estrés.
"""
import cv2
import numpy as np
import json
from pathlib import Path

def calibrate_with_color_card(image_path: str):
    """
    Usa una tarjeta de color estándar (ej: X-Rite ColorChecker) para calibrar.
    Si no hay tarjeta, usa el verde promedio de cultivo sano como referencia.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"No se pudo cargar {image_path}")
    
    # Convertir a LAB
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # Asumir que el centro de la imagen es cultivo sano (verde)
    h, w = img.shape[:2]
    centro = img[h//2-50:h//2+50, w//2-50:w//2+50]
    lab_centro = cv2.cvtColor(centro, cv2.COLOR_BGR2LAB)
    
    # Valores de referencia para verde sano (LAB)
    L_ref, A_ref, B_ref = 60, -30, 30
    
    # Calcular ajustes
    L_ajuste = L_ref - np.mean(lab_centro[:, :, 0])
    A_ajuste = A_ref - np.mean(lab_centro[:, :, 1])
    B_ajuste = B_ref - np.mean(lab_centro[:, :, 2])
    
    calibracion = {
        "fecha": str(Path(image_path).stat().st_mtime),
        "ajustes_lab": {
            "L": round(L_ajuste, 2),
            "A": round(A_ajuste, 2),
            "B": round(B_ajuste, 2)
        },
        "nota": "Calibración automática (centro = verde sano). Para mayor precisión, usar tarjeta de color."
    }
    
    salida = Path("data/calibration.json")
    with open(salida, "w") as f:
        json.dump(calibracion, f, indent=2)
    
    print(f"✅ Calibración guardada en {salida}")
    print(f"Ajustes LAB: L{calibracion['ajustes_lab']['L']}, A{calibracion['ajustes_lab']['A']}, B{calibracion['ajustes_lab']['B']}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Uso: python calibrate_drone.py <foto_con_verde_sano.jpg>")
        print("Ej: python calibrate_drone.py fotos/calibracion_20250520.jpg")
        sys.exit(1)
    
    calibrate_with_color_card(sys.argv[1])
