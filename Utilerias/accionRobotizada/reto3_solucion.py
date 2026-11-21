"""
SOLUCIÓN RETO 3 — Encabezado con la dirección en cada captura
==============================================================

Agrega arriba de cada captura una franja de color con la dirección buscada
y la fecha, y vuelve a generar el PDF con esa imagen.

Idea clave: HERENCIA + edición de imágenes con Pillow.
    RobotConEncabezado deja que Robot haga todo el proceso normal y después
    "decora" la captura antes de rehacer el PDF. robot.py no se modifica.

Coordenadas en Pillow:
    El punto (0, 0) es la esquina SUPERIOR izquierda.
    x crece hacia la derecha, y crece hacia ABAJO.

Ejecución:
    python reto3_solucion.py
"""

from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from robot import Config, Robot, imagen_a_pdf

ALTO_FRANJA = 90           # píxeles de la franja superior
COLOR_FRANJA = "#1F4E79"   # azul oscuro
COLOR_TEXTO = "white"


def cargar_fuente(tamano: int):
    """Arial existe en Windows; si no se encuentra, se usa la fuente de Pillow."""
    try:
        return ImageFont.truetype("arial.ttf", tamano)
    except OSError:
        return ImageFont.load_default(size=tamano)


class RobotConEncabezado(Robot):
    def capturar_direccion(self, direccion: str) -> Path:
        # 1) Proceso normal: buscar, capturar y generar el PDF.
        pdf = super().capturar_direccion(direccion)

        # 2) Agregar el encabezado a la captura.
        png = self.config.carpeta_capturas / f"{pdf.stem}.png"
        self.agregar_encabezado(png, direccion)

        # 3) Rehacer el PDF con la imagen ya decorada (sobrescribe el anterior).
        imagen_a_pdf(png, pdf)
        self.log.info(f"Encabezado agregado: {pdf.name}")
        return pdf

    def agregar_encabezado(self, png: Path, direccion: str):
        with Image.open(png) as captura:
            ancho, alto = captura.size

            # Lienzo nuevo: igual de ancho, pero más alto para que quepa la franja.
            # Al crearlo con el color de la franja, la parte de arriba ya queda pintada.
            lienzo = Image.new("RGB", (ancho, alto + ALTO_FRANJA), COLOR_FRANJA)

            # Pegar la captura original justo debajo de la franja.
            lienzo.paste(captura, (0, ALTO_FRANJA))

        # Escribir el texto sobre la franja.
        dibujo = ImageDraw.Draw(lienzo)
        dibujo.text((20, 12), direccion, font=cargar_fuente(36), fill=COLOR_TEXTO)
        dibujo.text((20, 56), f"Capturado: {datetime.now():%d/%m/%Y %H:%M}",
                    font=cargar_fuente(22), fill=COLOR_TEXTO)

        # Sobrescribir el PNG con la versión decorada.
        lienzo.save(png)


if __name__ == "__main__":
    RobotConEncabezado(Config()).ejecutar()
