# Guía para el Técnico Local — Cooperativa Nueva Esperanza

## 📅 Cronograma ideal por campaña

| Día | Actividad | Herramienta |
|-----|-----------|-------------|
| 55–65 | Pronóstico de rendimiento | `nuevaesperanza rendimiento ...` |
| 70 | Primera foto con dron/smartphone | `nuevaesperanza estres ...` |
| 90 | Segundo pronóstico + ajuste riego | Zonificación + `irrigation_optimizer` |
| 120 | Última verificación | Foto + análisis final |

## 📸 Cómo tomar fotos para análisis de estrés

1. **Momento**: 10:00–14:00 (luz estable, sin nubes gruesas)  
2. **Altura**:  
   - Drone: 30–40 m (≈4 ha por foto)  
   - Smartphone: desde camioneta, 2–3 m de altura  
3. **Encuadre**:  
   - Incluir el pivote central en el centro  
   - Evitar sombras largas (fotografiar con sol a espaldas)  
4. **Guardar como**: `campoX_fecha.jpg` (ej: `campo5_20250615.jpg`)

## 📊 Cómo medir NDVI sin dron multiespectral

1. Usar **Sentinel-2** (gratuito) vía USB:  
   - En computadora con internet, ejecutar:  
     ```bash
     python scripts/download_sentinel_offline.py --campo 5 --fecha 2025-06-15
     ```  
   - Copiar la carpeta `sentinel_guatrache_5_*.zip` a USB  
   - En netbook de campo:  
     ```bash
     nuevaesperanza rendimiento "Campo 5" --ndvi $(nuevaesperanza-ndvi-from-usb D:/)
     ```

## 🖨️ Cómo compartir resultados

- Imprimir el PDF generado en `reports/`  
- Pegar en el tablero de la sala de máquinas  
- Discutir en la reunión semanal de operarios

> ✅ **Importante**: Todos los datos permanecen en la cooperativa. Nada se sube a internet.
