import numpy as np
import rasterio
from rasterio.transform import from_origin

# Generar TIFF simulado (Sentinel-2 falso, 10m/pix, banda B8 - NIR)
width, height = 1098, 1098  # ≈100 ha
data = np.random.uniform(0.2, 0.8, (height, width)).astype(np.float32)

# Añadir patrón de pivote central (círculo con gradiente)
center_x, center_y = width // 2, height // 2
Y, X = np.ogrid[:height, :width]
dist = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
ndvi_sim = 0.3 + 0.5 * np.exp(-dist / 200)
data = np.clip(ndvi_sim + np.random.normal(0, 0.05, data.shape), 0.2, 0.8)

# Guardar como GeoTIFF simulado
transform = from_origin(300000, 6200000, 10, 10)  # Coordenadas UTM fijas (Guatrache aprox)
with rasterio.open(
    "data/samples/sentinel_preview.tif",
    'w',
    driver='GTiff',
    height=height,
    width=width,
    count=1,
    dtype=data.dtype,
    crs='EPSG:32720',  # UTM Zona 20S
    transform=transform,
    nodata=0
) as dst:
    dst.write(data, 1)

print("✅ data/samples/sentinel_preview.tif generado (simulado, 100 ha, pivote central).")
