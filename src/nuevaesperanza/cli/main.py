import click
from pathlib import Path
from ..core.yield_predictor import YieldPredictor
from ..core.stress_detector import StressDetector
from ..io.exporter import exportar_informe_pdf

@click.group()
def cli():
    """nueva-esperanza-ml: ML para agricultura regada en Guatrache"""
    pass

@cli.command()
@click.argument("campo", type=str)
@click.option("--dias", type=int, required=True, help="Días desde siembra")
@click.option("--precip", type=float, required=True, help="Precip. últimos 30 días (mm)")
@click.option("--temp", type=float, default=28.0, help="Temp. máx. promedio (°C)")
@click.option("--ndvi", type=float, default=0.45, help="NDVI a los 60 días")
@click.option("--hibrido/--criollo", default=True)
@click.option("--suelo", type=int, default=80, help="Prof. suelo útil (cm)")
@click.option("--ph", type=float, default=6.5)
@click.option("--cultivo", type=click.Choice(["trigo", "maiz"]), default="trigo")
def rendimiento(campo, dias, precip, temp, ndvi, hibrido, suelo, ph, cultivo):
    """Pronostica rendimiento a cosecha."""
    predictor = YieldPredictor()
    resultado = predictor.predict(
        dias_ciclo=dias,
        precip_30d=precip,
        temp_max_prom=temp,
        ndvi_60d=ndvi,
        es_hibrido=hibrido,
        prof_suelo_cm=suelo,
        ph_suelo=ph,
        cultivo=cultivo
    )
    
    click.echo(f"\n🔍 Pronóstico para {campo}")
    click.echo(f"📅 Día {dias} del ciclo")
    click.echo(f"🌾 Rendimiento esperado: {resultado['qq_ha']} qq/ha")
    click.echo(f"📊 Intervalo 90%: {resultado['intervalo_90'][0]} – {resultado['intervalo_90'][1]} qq/ha")
    click.echo(f"🔍 Confianza: {resultado['confianza']}")
    
    # Guardar en CSV simple para planilla local
    Path("reports").mkdir(exist_ok=True)
    with open(f"reports/{campo}_rendimiento.csv", "w") as f:
        f.write("campo,dias,qq_ha,min_qq,max_qq,confianza\n")
        f.write(f"{campo},{dias},{resultado['qq_ha']},{resultado['intervalo_90'][0]},{resultado['intervalo_90'][1]},{resultado['confianza']}\n")
    
    click.echo(f"\n✅ Datos guardados: reports/{campo}_rendimiento.csv")

@cli.command()
@click.argument("imagen", type=click.Path(exists=True))
@click.option("--campo", type=str, required=True)
def estres(imagen, campo):
    """Analiza imagen de dron/smartphone para detectar estrés."""
    detector = StressDetector()
    resultado = detector.analyze_image(imagen)
    
    click.echo(f"\n🔍 Análisis de {Path(imagen).name} — Campo {campo}")
    click.echo(f"⚠️  Zona con posible estrés: {resultado['zona_estres']}%")
    click.echo(f"🎨 Índice de color (amarillo/rojo): {resultado['indice_color']}")
    click.echo(f"📏 Textura irregular: {'Sí' if resultado['textura_irregular'] else 'No'}")
    click.echo(f"\n💡 Recomendación: {resultado['recomendacion']}")
    
    # Generar informe PDF
    exportar_informe_pdf(campo, "estres", resultado, imagen)
    click.echo(f"\n📄 Informe generado: reports/{campo}_estres.pdf")
