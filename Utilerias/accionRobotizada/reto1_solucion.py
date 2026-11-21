"""
SOLUCIÓN RETO 1 — Reporte único en PDF
=======================================

Además de un PDF por dirección, genera "pdfs/reporte_maps.pdf" con todas
las capturas juntas, una por página.

Idea clave: HERENCIA.
    RobotReporte hereda todo el comportamiento de Robot y sólo agrega
    dos cosas: recordar cada captura y, al final, unirlas en un PDF.
    robot.py no se modifica.

Ejecución:
    python reto1_solucion.py
"""

from pathlib import Path

from PIL import Image

from robot import Config, Robot


class RobotReporte(Robot):
    def __init__(self, config: Config):
        super().__init__(config)       # todo lo que ya hacía el Robot original
        self.capturas: list[Path] = []  # nuevo: rutas de las capturas exitosas

    def capturar_direccion(self, direccion: str) -> Path:
        # 1) Hacer el proceso normal (buscar, capturar, PDF individual).
        pdf = super().capturar_direccion(direccion)

        # 2) Recordar la captura. El PNG tiene el mismo nombre que el PDF.
        self.capturas.append(self.config.carpeta_capturas / f"{pdf.stem}.png")
        return pdf

    def finalizar(self):
        # El reporte se crea antes de cerrar, cuando ya se procesó todo.
        if self.capturas:
            self.crear_reporte()
        else:
            self.log.warning("No hubo capturas exitosas; no se genera el reporte")
        super().finalizar()  # cerrar Chrome y escribir el resumen, como siempre

    def crear_reporte(self):
        ruta = self.config.carpeta_pdfs / "reporte_maps.pdf"

        # Abrir todas las imágenes y convertirlas a RGB (el PDF no admite transparencia).
        paginas = [Image.open(captura).convert("RGB") for captura in self.capturas]

        # La primera imagen "guarda" el PDF y las demás se agregan como páginas.
        primera, resto = paginas[0], paginas[1:]
        primera.save(ruta, "PDF", resolution=100, save_all=True, append_images=resto)

        self.log.info(f"Reporte con {len(paginas)} páginas: {ruta}")


if __name__ == "__main__":
    RobotReporte(Config()).ejecutar()
