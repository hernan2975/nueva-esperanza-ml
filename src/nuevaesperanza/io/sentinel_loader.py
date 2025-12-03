import os
import zipfile
from pathlib import Path
from rasterio.io import MemoryFile
import numpy as np

class SentinelLoader:
    """
    Carga datos Sentinel-2 desde USB (sin internet).
    Espera archivos ZIP descargados previamente con: scripts/download_sentinel_offline.py
    """
    
    def load_ndvi_from_usb(self, usb_path: str, campo_id: str) -> float:
        """
        Busca ZIP con patrón: sentinel_guatrache_{campo_id}_*.zip
        Extrae banda NIR y RED para calcular NDVI.
        """
        usb = Path(usb_path)
        pattern = f"sentinel_guatrache_{campo_id}_*.zip"
        zips = list(usb.glob(pattern))
        
        if not zips:
            raise FileNotFoundError(f"No se encontró Sentinel-2 para {campo_id} en {usb_path}")
        
        # Tomar el más reciente
        latest = max(zips, key=os.path.getmtime)
        
        with zipfile.ZipFile(latest) as zf:
            # Buscar bandas B04 (rojo) y B08 (NIR)
            b4_files = [f for f in zf.namelist() if "B04_10m.jp2" in f]
            b8_files = [f for f in zf.namelist() if "B08_10m.jp2" in f]
            
            if not b4_files or not b8_files:
                raise ValueError("Faltan bandas B04 o B08 en el ZIP.")
            
            # Leer bandas (simplificado: asume 1 archivo c/u)
            with zf.open(b4_files[0]) as f:
                with MemoryFile(f.read()) as mem:
                    with mem.open() as src:
                        red = src.read(1).astype(float)
            
            with zf.open(b8_files[0]) as f:
                with MemoryFile(f.read()) as mem:
                    with mem.open() as src:
                        nir = src.read(1).astype(float)
        
        # Calcular NDVI
        with np.errstate(divide='ignore', invalid='ignore'):
            ndvi = (nir - red) / (nir + red)
        
        # Máscara de nubes (NDVI > 0.8 → descartar)
        ndvi = np.where(ndvi > 0.8, np.nan, ndvi)
        
        return float(np.nanmean(ndvi))
