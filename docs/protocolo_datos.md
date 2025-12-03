# Protocolo de Datos — Privacidad y Calidad

## 🔒 Principios éticos
- Los datos son propiedad exclusiva de la **Cooperativa Nueva Esperanza**.  
- No se comparten con empresas, gobierno ni investigadores sin consentimiento por asamblea.  
- Los archivos brutos (`data/raw/`) se borran después de 2 campañas.

## 📋 Datos mínimos requeridos

| Variable | Cómo obtenerla | Frecuencia | Exactitud mínima |
|----------|----------------|------------|------------------|
| Días desde siembra | Calendario físico | Única vez | ±1 día |
| Precip. 30 días | Pluviómetro en campo | Semana | ±2 mm |
| Temp. máx. prom. | Termómetro en sombra | Diaria (promediar) | ±1°C |
| NDVI | Sentinel-2 o foto dron | Una vez a los 60 días | ±0.05 |
| Tipo de híbrido | Registro de compra | Por lote | Sí/No |
| Prof. suelo útil | Barreno manual | Por lote (cada 3 años) | ±5 cm |
| pH suelo | Kit de prueba económico | Por lote (cada 2 años) | ±0.3 |

## 🚫 Qué NO se registra
- Nombres de personas  
- Costos económicos  
- Decisiones internas de la cooperativa  
- Imágenes con personas o viviendas

## 📁 Estructura de archivos
data/
├── raw/ # Solo para entrenamiento (borrar después)
├── processed/ # Datos anonimizados (máx. 2 años)
└── models/ # Modelos entrenados (sí se guardan)
