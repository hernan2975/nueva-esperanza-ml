import cv2
import numpy as np

class StressDetector:
    """
    Detecta estrés hídrico/nutricional en cultivos usando SOLO imágenes RGB.
    Funciona con fotos de smartphone o dron económico (ej: DJI Mini).
    """
    
    def analyze_image(self, image_path: str) -> dict:
        """
        Retorna: {
            "zona_estres": float,  # % de imagen con posible estrés
            "indice_color": float, # 0–1: más amarillo/rojizo = más estrés
            "textura_irregular": bool,
            "recomendacion": str
        }
        """
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"No se pudo cargar {image_path}")
        
        # Convertir a HSV — más estable que RGB bajo distintas luces
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Canal S (saturación): baja saturación = hojas pálidas
        saturacion_prom = hsv[:, :, 1].mean() / 255.0
        
        # Canal H (tono): tonos amarillos/rojizos (30–60 y 0–10 en HSV)
        hue = hsv[:, :, 0]
        amarillo = ((hue > 25) & (hue < 35)).sum()
        rojizo = ((hue > 0) & (hue < 10)).sum()
        total_pixeles = hue.size
        indice_color = (amarillo + rojizo) / total_pixeles
        
        # Textura: desviación estándar local (baja = uniforme = sano)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        textura_irregular = laplacian_var < 100  # umbral calibrado en campo
        
        zona_estres = max(saturacion_prom * 0.3 + indice_color * 0.7, 0.0)
        
        if zona_estres > 0.4:
            recomendacion = "Verificar riego en sector. Posible déficit hídrico o falta de nitrógeno."
        elif zona_estres > 0.2:
            recomendacion = "Monitorear en 7 días. Zona con leve estrés."
        else:
            recomendacion = "Cultivo en buen estado."
        
        return {
            "zona_estres": round(zona_estres * 100, 1),
            "indice_color": round(indice_color, 3),
            "textura_irregular": textura_irregular,
            "recomendacion": recomendacion
        }
