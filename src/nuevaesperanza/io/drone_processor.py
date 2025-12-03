import cv2
import numpy as np
from pathlib import Path

class DroneProcessor:
    """
    Procesa imágenes de dron/smartphone para análisis de estrés.
    Incluye corrección geométrica simple (para fotos no georreferenciadas).
    """
    
    def preprocess_image(self, image_path: str, output_size: Tuple[int, int] = (1024, 1024)) -> np.ndarray:
        """
        1. Corrige perspectiva (asume fotos cenitales)
        2. Normaliza iluminación
        3. Redimensiona
        """
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"No se pudo cargar {image_path}")
        
        # Corrección de perspectiva simple (asume que el pivote es circular)
        h, w = img.shape[:2]
        center = (w // 2, h // 2)
        radius = min(w, h) // 2 - 50
        
        # Recortar círculo
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.circle(mask, center, radius, 255, -1)
        img_circular = cv2.bitwise_and(img, img, mask=mask)
        
        # Normalización de iluminación (CLAHE en espacio LAB)
        lab = cv2.cvtColor(img_circular, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        l = clahe.apply(l)
        lab = cv2.merge((l, a, b))
        img_norm = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        # Redimensionar
        return cv2.resize(img_norm, output_size)
    
    def save_processed(self, img: np.ndarray, output_path: str):
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(output_path, img)
