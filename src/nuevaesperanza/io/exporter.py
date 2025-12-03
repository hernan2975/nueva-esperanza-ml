import os
from pathlib import Path
from jinja2 import Template
from weasyprint import HTML
from datetime import datetime

# Plantilla bilingüe: español + alemán bajo (Plautdietsch)
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Informe: {{ campo }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 2cm; }
        .header { text-align: center; border-bottom: 2px solid #264653; padding-bottom: 10px; }
        .section { margin: 20px 0; }
        .bilingual { display: flex; }
        .es, .pd { width: 48%; padding: 5px; }
        .es { border-right: 1px dashed #ccc; }
        .highlight { background: #fff3cd; padding: 8px; border-left: 4px solid #ffc107; }
        .footer { margin-top: 30px; font-size: 0.9em; color: #6c757d; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Informe Técnico — {{ campo }}</h1>
        <p>Cooperativa Nueva Esperanza, Guatrache • {{ fecha }}</p>
    </div>

    {% if tipo == "estres" %}
    <div class="section">
        <h2>🔍 Análisis de Estrés</h2>
        <div class="highlight">
            <div class="bilingual">
                <div class="es"><strong>Zona con posible estrés:</strong> {{ resultado.zona_estres }}%</div>
                <div class="pd"><strong>Bereich met möglichen Strees:</strong> {{ resultado.zona_estres }}%</div>
            </div>
        </div>
        
        <div class="bilingual">
            <div class="es">
                <h3>Recomendación</h3>
                <p>{{ resultado.recomendacion }}</p>
            </div>
            <div class="pd">
                <h3>Aunrood</h3>
                <p>{{ resultado.recomendacion_pd }}</p>
            </div>
        </div>
    </div>
    {% endif %}

    <div class="footer">
        <p><em>Este informe fue generado con nueva-esperanza-ml — herramienta libre para la cooperativa.</em></p>
        <p>Espacio para notas del técnico:</p>
        <div style="border: 1px dashed #ccc; min-height: 60px;"></div>
    </div>
</body>
</html>
"""

def exportar_informe_pdf(campo: str, tipo: str, resultado: dict, imagen_path: str = None):
    """Genera PDF bilingüe (español + plautdietsch)."""
    
    # Traducción simple al alemán bajo (ajustable por la cooperativa)
    if tipo == "estres":
        if "deficit hídrico" in resultado["recomendacion"]:
            resultado["recomendacion_pd"] = "Wotaamangel — mieh Wota geewa."
        elif "falta de nitrógeno" in resultado["recomendacion"]:
            resultado["recomendacion_pd"] = "Niet genooch Nitroogen — Dünger prööwa."
        elif "Monitorear" in resultado["recomendacion"]:
            resultado["recomendacion_pd"] = "In 7 Daaje widder kieken."
        else:
            resultado["recomendacion_pd"] = "Alles joot."

    template = Template(TEMPLATE)
    html_str = template.render(
        campo=campo,
        tipo=tipo,
        resultado=resultado,
        fecha=datetime.now().strftime("%d/%m/%Y")
    )
    
    salida = Path("reports") / f"{campo}_{tipo}.pdf"
    salida.parent.mkdir(exist_ok=True)
    HTML(string=html_str).write_pdf(salida)
