#!/usr/bin/env python3
"""
Descarga datos Sentinel-2 para Guatrache y los empaqueta para USB.
Requiere internet — se ejecuta desde casa/oficina, no en campo.
"""
import os
import sys
import zipfile
from datetime import datetime
import requests
from pathlib import Path

# Coordenadas aproximadas de Guatrache (centroide 10x10 km)
LAT, LON = -37.25, -63.85

def buscar_escenas(fecha: str, max_nubes: float = 20.0):
    """Busca escenas en el catálogo de Copernicus Open Access Hub (simulado con API pública)."""
    # En producción: usar sentinelsat o pystac-client
    # Aquí: simulación para demo (devuelve URL fija de ejemplo)
    return [{
        "id": "S2A_MSIL2A_20250615T143021_N0509_R125_T19HEH_20250615T181234",
        "fecha": "2025-06-15",
        "nubes": 12.5,
        "url": "https://sentinel-s2-l2a.example.com/S2A_MSIL2A_20250615T143021_N0509_R125_T19HEH_20250615T181234.zip"
    }]

def descargar_y_empaquetar(campo_id: str, fecha: str):
    escenas = buscar_escenas(fecha)
    if not escenas:
        print(f"❌ No hay escenas sin nubes para {fecha}")
        return False
    
    mejor = min(escenas, key=lambda x: abs(datetime.fromisoformat(x["fecha"]) - datetime.fromisoformat(fecha)))
    
    print(f"⏬ Descargando {mejor['id']} ({mejor['nubes']}% nubes)...")
    # Simular descarga
    zip_path = Path(f"sentinel_guatrache_{campo_id}_{mejor['fecha']}.zip")
    
    # En producción: requests.get(mejor["url"], stream=True)
    # Aquí: crear ZIP simulado
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("preview.jpg", b"FAKE_PREVIEW")
        zf.writestr("B04_10m.jp2", b"FAKE_BAND_DATA")
        zf.writestr("B08_10m.jp2", b"FAKE_BAND_DATA")
    
    print(f"✅ Generado: {zip_path}")
    print(f"\n➡️  Copie este archivo a una USB y llévelo al campo.")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python download_sentinel_offline.py --campo <ID> --fecha YYYY-MM-DD")
        sys.exit(1)
    
    campo_id = sys.argv[2] if sys.argv[1] == "--campo" else "1"
    fecha = sys.argv[4] if len(sys.argv) > 4 and sys.argv[3] == "--fecha" else datetime.now().strftime("%Y-%m-%d")
    
    descargar_y_empaquetar(campo_id, fecha)
