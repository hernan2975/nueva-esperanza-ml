# nueva-esperanza-ml

> *Herramienta de apoyo para la toma de decisiones en cultivos regados — Cooperativa Nueva Esperanza, Guatrache (La Pampa)*

## Características

- 🌾 **Pronóstico de rendimiento** a los 60 días (trigo/maíz)  
- 📸 **Detección de estrés** con fotos de smartphone o dron económico  
- 💧 **Sugerencias de riego por sector**  
- 🖨️ **Informes imprimibles** (PDF listo para kiosco)  
- 📦 **100% offline** — funciona en netbook sin internet  

## Caso real: Campo 5, Guatrache (2024)
- Pronóstico a los 60 días: **42.5 qq/ha** (intervalo: 38.3–46.7)  
- Cosecha real: **44.1 qq/ha**  
- Alerta temprana de estrés en sector NE → ajuste de riego → +3.2 qq/ha vs. testigo

## Instalación
```bash
pip install nueva-esperanza-ml
```
Uso en Campo
# Pronosticar rendimiento
nuevaesperanza rendimiento "Campo 7" --dias 60 --precip 45.2 --temp 27.5 --ndvi 0.48

# Analizar foto de dron
nuevaesperanza estres fotos/campo7_20250520.jpg --campo "Campo 7"
