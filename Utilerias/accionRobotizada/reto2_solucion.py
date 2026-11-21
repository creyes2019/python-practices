"""
SOLUCIÓN RETO 2 — Bitácora de resultados en Excel
==================================================

Al terminar, genera "resultados.xlsx" con una fila por dirección:
    direccion | estado ("OK" o "ERROR") | pdf | fecha

Idea clave: HERENCIA.
    RobotConResultados hereda todo de Robot y sólo agrega:
      - recordar qué direcciones se pidieron,
      - recordar cuáles generaron PDF,
      - al final, escribir el Excel comparando ambas listas.
    robot.py no se modifica.

Ejecución:
    python reto2_solucion.py
"""

from datetime import datetime
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

from robot import BASE_DIR, Config, Robot


class RobotConResultados(Robot):
    def __init__(self, config: Config):
        super().__init__(config)
        self.direcciones: list[str] = []    # todas las que se pidieron
        self.pdfs: dict[str, Path] = {}     # sólo las exitosas: {direccion: ruta_pdf}

    def obtener_direcciones(self) -> list[str]:
        self.direcciones = super().obtener_direcciones()
        return self.direcciones

    def capturar_direccion(self, direccion: str) -> Path:
        pdf = super().capturar_direccion(direccion)
        # Si llegamos a esta línea es porque no hubo error.
        self.pdfs[direccion] = pdf
        return pdf

    def finalizar(self):
        if self.direcciones:
            self.guardar_resultados()
        super().finalizar()

    def guardar_resultados(self):
        ruta = BASE_DIR / "resultados.xlsx"
        fecha = f"{datetime.now():%Y-%m-%d %H:%M:%S}"

        wb = Workbook()
        ws = wb.active
        ws.title = "Resultados"
        ws.append(["direccion", "estado", "pdf", "fecha"])

        for direccion in self.direcciones:
            # Si la dirección no está en el diccionario, significa que falló.
            pdf = self.pdfs.get(direccion)
            estado = "OK" if pdf else "ERROR"
            ws.append([direccion, estado, pdf.name if pdf else "", fecha])

        # Formato: encabezado en azul y anchos de columna legibles.
        for celda in ws[1]:
            celda.font = Font(bold=True, color="FFFFFF")
            celda.fill = PatternFill("solid", fgColor="4472C4")
        for columna, ancho in zip("ABCD", (45, 10, 70, 20)):
            ws.column_dimensions[columna].width = ancho

        wb.save(ruta)
        self.log.info(f"Resultados guardados en: {ruta}")


if __name__ == "__main__":
    RobotConResultados(Config()).ejecutar()
