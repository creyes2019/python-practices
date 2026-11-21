"""
RPA de ejemplo: captura de Google Maps en PDF
==============================================

¿Qué es un RPA?
    RPA (Robotic Process Automation) es un programa que imita lo que haría
    una persona frente a la computadora: abrir el navegador, escribir,
    hacer click, esperar, guardar archivos... de forma automática y repetible.

¿Qué hace este robot?
    1. Obtiene una o varias direcciones (desde Excel o escritas por teclado).
    2. Abre Google Maps en Chrome y busca cada dirección.
    3. Toma una captura de pantalla del resultado.
    4. Convierte la captura en un archivo PDF.

Estructura del archivo (de lo general a lo particular):
    1. Configuración  -> todos los valores que se pueden ajustar, en un solo lugar
    2. Bitácora       -> registro (log) de lo que hace el robot
    3. Utilidades     -> funciones de apoyo: reintentos, PDF, nombres de archivo
    4. Navegador      -> acciones sobre la página web (Selenium)
    5. Robot          -> el proceso completo: iniciar -> procesar -> finalizar
    6. Punto de entrada
    7. Retos para el alumno (al final del archivo)

Librerías necesarias:
    pip install selenium pillow openpyxl

Ejecución:
    python robot.py
"""

import functools
import logging
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

# Carpeta donde vive este archivo; las demás rutas se construyen a partir de ella
# para que el robot funcione sin importar desde dónde se ejecute.
BASE_DIR = Path(__file__).resolve().parent


# ---------------------------------------------------------------------------
# 1. Configuración
# ---------------------------------------------------------------------------
# Un buen RPA no tiene valores "escondidos" dentro del código: todo lo que
# podría cambiar (rutas, tiempos, URLs) se concentra aquí.
# @dataclass genera automáticamente el constructor de la clase.

@dataclass
class Config:
    carpeta_logs: Path = BASE_DIR / "logs"            # bitácoras de cada ejecución
    carpeta_capturas: Path = BASE_DIR / "capturas"    # imágenes PNG
    carpeta_pdfs: Path = BASE_DIR / "pdfs"            # resultado final
    archivo_entrada: Path = BASE_DIR / "entrada.xlsx"  # opcional, columna "direccion"
    url_maps: str = "https://www.google.com/maps"
    reintentos: int = 3            # veces que se intenta cada dirección antes de darla por fallida
    espera_reintento: float = 2.0  # segundos entre un intento y otro
    espera_mapa: float = 5.0       # segundos para que el mapa termine de dibujarse
    espera_maxima: float = 15.0    # segundos máximos esperando un elemento de la página


# ---------------------------------------------------------------------------
# 2. Bitácora (logging)
# ---------------------------------------------------------------------------
# Un robot normalmente corre sin nadie mirando. La bitácora permite saber
# después qué hizo, cuánto tardó y dónde falló.
# Cada mensaje se muestra en consola y también se guarda en un archivo .log.

def configurar_logger(carpeta: Path) -> logging.Logger:
    carpeta.mkdir(parents=True, exist_ok=True)
    archivo = carpeta / f"robot_{datetime.now():%Y%m%d_%H%M%S}.log"

    logger = logging.getLogger("robot")
    logger.setLevel(logging.INFO)
    formato = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")

    for handler in (logging.StreamHandler(), logging.FileHandler(archivo, encoding="utf-8")):
        handler.setFormatter(formato)
        logger.addHandler(handler)

    return logger


# ---------------------------------------------------------------------------
# 3. Utilidades
# ---------------------------------------------------------------------------

def reintentar(veces: int, espera: float):
    """
    Decorador que vuelve a ejecutar una función si lanza un error.

    En la web es común que algo falle una vez (la página tardó, se cortó
    el internet) y funcione al segundo intento. Si después de `veces`
    intentos sigue fallando, el error se deja pasar para que se registre.
    """
    def decorador(func):
        @functools.wraps(func)  # conserva el nombre original de la función
        def envoltura(*args, **kwargs):
            logger = logging.getLogger("robot")
            for intento in range(1, veces + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as error:
                    logger.warning(f"{func.__name__} falló (intento {intento}/{veces}): {error}")
                    if intento == veces:
                        raise
                    time.sleep(espera)
        return envoltura
    return decorador


def imagen_a_pdf(imagen: Path, pdf: Path) -> Path:
    """Convierte una imagen PNG/JPG en un PDF de una página usando Pillow."""
    from PIL import Image

    pdf.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(imagen) as img:
        # El formato PDF no admite transparencia, por eso se convierte a RGB.
        img.convert("RGB").save(pdf, "PDF", resolution=100)
    return pdf


def nombre_archivo_seguro(texto: str, largo: int = 60) -> str:
    """
    Convierte un texto en un nombre de archivo válido.
    Ej.: "Av. Juárez #10, CDMX" -> "Av__Juárez__10__CDMX"
    Windows no permite caracteres como \\ / : * ? " < > | en los nombres.
    """
    limpio = "".join(c if c.isalnum() or c in " -_" else "_" for c in texto)
    return "_".join(limpio.split())[:largo] or "sin_nombre"


# ---------------------------------------------------------------------------
# 4. Navegador (Selenium)
# ---------------------------------------------------------------------------
# Selenium controla un navegador real (Chrome) desde Python.
# Esta clase "envuelve" Selenium con métodos de nombre sencillo para que
# el proceso del robot se lea casi como instrucciones en español.

class Navegador:
    def __init__(self, espera_maxima: float):
        from selenium import webdriver
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.ui import WebDriverWait

        self.Keys = Keys
        self.EC = EC
        self.driver = webdriver.Chrome()   # abre una ventana nueva de Chrome
        self.driver.maximize_window()
        # WebDriverWait espera "hasta que" se cumpla una condición, con un límite
        # de tiempo. Es mejor que time.sleep() porque no espera de más.
        self.espera = WebDriverWait(self.driver, espera_maxima)

    def abrir(self, url: str):
        self.driver.get(url)

    def escribir(self, selector_css: str, texto: str):
        """Espera a que exista el campo, lo limpia y escribe el texto."""
        elemento = self.espera.until(
            self.EC.presence_of_element_located(("css selector", selector_css))
        )
        elemento.clear()
        elemento.send_keys(texto)
        return elemento

    def presionar_enter(self, elemento):
        elemento.send_keys(self.Keys.ENTER)

    def esperar_url(self, *fragmentos: str):
        """Espera hasta que la URL contenga alguno de los fragmentos indicados."""
        self.espera.until(lambda d: any(f in d.current_url for f in fragmentos))

    def captura(self, ruta: Path) -> Path:
        """Guarda como imagen lo que se ve en la ventana del navegador."""
        ruta.parent.mkdir(parents=True, exist_ok=True)
        self.driver.save_screenshot(str(ruta))
        return ruta

    def cerrar(self):
        self.driver.quit()


# ---------------------------------------------------------------------------
# 5. Robot
# ---------------------------------------------------------------------------
# Todo RPA sigue el mismo ciclo de vida:
#   iniciar   -> preparar el entorno (abrir aplicaciones, iniciar sesión)
#   procesar  -> repetir la tarea para cada registro de entrada
#   finalizar -> cerrar todo y reportar resultados, aunque haya errores

class Robot:
    def __init__(self, config: Config):
        self.config = config
        self.log = configurar_logger(config.carpeta_logs)
        self.navegador = None
        self.exitosos = 0
        self.fallidos = 0

    # --- Ciclo de vida -----------------------------------------------------

    def iniciar(self):
        self.log.info("=== Iniciando robot ===")
        self.navegador = Navegador(self.config.espera_maxima)

    def obtener_direcciones(self) -> list[str]:
        """
        Devuelve la lista de direcciones a procesar.
          - Si existe entrada.xlsx, lee la columna "direccion" (procesamiento masivo).
          - Si no, pide una dirección por teclado.
        """
        archivo = self.config.archivo_entrada
        if not archivo.exists():
            direccion = input("Escribe la dirección a buscar en Google Maps: ").strip()
            return [direccion] if direccion else []

        from openpyxl import load_workbook
        hoja = load_workbook(archivo, read_only=True).active
        filas = list(hoja.iter_rows(values_only=True))
        columna = filas[0].index("direccion")  # posición de la columna según el encabezado
        return [str(fila[columna]) for fila in filas[1:] if fila[columna]]

    def capturar_direccion(self, direccion: str) -> Path:
        """
        La tarea principal, para UNA dirección:
        buscar en Maps -> esperar -> capturar -> convertir a PDF.
        Devuelve la ruta del PDF generado.
        """
        self.log.info(f"Buscando en Google Maps: {direccion}")

        # 1) Abrir Maps y escribir la dirección en el buscador.
        #    "#searchboxinput" es el id de la caja de búsqueda de Maps; se agrega
        #    "input[name='q']" como alternativa por si Google cambia la página.
        self.navegador.abrir(self.config.url_maps)
        caja = self.navegador.escribir("#searchboxinput, input[name='q']", direccion)
        self.navegador.presionar_enter(caja)

        # 2) Cuando Maps encuentra el lugar, la URL cambia a .../place/... o .../search/...
        #    Después se esperan unos segundos extra para que se dibuje el mapa.
        self.navegador.esperar_url("/place/", "/search/")
        time.sleep(self.config.espera_mapa)

        # 3) Captura y PDF. Se agrega fecha y hora al nombre para no sobrescribir archivos.
        nombre = f"{nombre_archivo_seguro(direccion)}_{datetime.now():%Y%m%d_%H%M%S}"
        png = self.navegador.captura(self.config.carpeta_capturas / f"{nombre}.png")
        pdf = imagen_a_pdf(png, self.config.carpeta_pdfs / f"{nombre}.pdf")
        self.log.info(f"PDF generado: {pdf}")
        return pdf

    def procesar(self):
        direcciones = self.obtener_direcciones()
        self.log.info(f"{len(direcciones)} direcciones por procesar")

        # Se aplica el decorador "a mano" porque el número de reintentos viene de Config.
        capturar_con_reintentos = reintentar(
            self.config.reintentos, self.config.espera_reintento
        )(self.capturar_direccion)

        for direccion in direcciones:
            # Si una dirección falla, se registra y el robot continúa con la siguiente.
            try:
                capturar_con_reintentos(direccion)
                self.exitosos += 1
            except Exception as error:
                self.fallidos += 1
                self.log.error(f"No se pudo procesar '{direccion}': {error}")

    def finalizar(self):
        if self.navegador:
            self.navegador.cerrar()
        self.log.info(f"=== Fin: {self.exitosos} exitosos, {self.fallidos} fallidos ===")

    def ejecutar(self):
        """Ejecuta el ciclo completo. 'finally' garantiza que siempre se cierre Chrome."""
        inicio = time.perf_counter()
        try:
            self.iniciar()
            self.procesar()
        except Exception:
            self.log.exception("Error fatal en el robot")
        finally:
            self.finalizar()
            self.log.info(f"Duración: {time.perf_counter() - inicio:.2f} s")


# ---------------------------------------------------------------------------
# 6. Punto de entrada
# ---------------------------------------------------------------------------
# Este bloque sólo se ejecuta cuando se corre "python robot.py",
# no cuando el archivo se importa desde otro programa.

if __name__ == "__main__":
    Robot(Config()).ejecutar()


# ---------------------------------------------------------------------------
# 7. Retos para el alumno
# ---------------------------------------------------------------------------
# Resuelve cada reto en un archivo nuevo, SIN modificar robot.py.
# Pista general: crea una clase que herede de Robot y sobrescribe sólo los
# métodos que necesites, llamando a super() para reutilizar lo que ya existe:
#
#     from robot import Config, Robot
#
#     class MiRobot(Robot):
#         def capturar_direccion(self, direccion):
#             pdf = super().capturar_direccion(direccion)  # hace todo lo de siempre
#             ...                                          # y aquí agregas lo tuyo
#             return pdf
#
#
# RETO 1 — Reporte único en PDF                       (archivo: reto1_solucion.py)
#   Además de un PDF por dirección, genera "pdfs/reporte_maps.pdf" con todas
#   las capturas juntas, una por página.
#   Pistas:
#     - Guarda en una lista la ruta de cada captura PNG. La captura tiene el
#       mismo nombre que el PDF: carpeta_capturas / f"{pdf.stem}.png"
#     - Crea el reporte en finalizar(), cuando ya se procesaron todas.
#     - Pillow crea PDFs de varias páginas así:
#         primera.save(ruta, "PDF", save_all=True, append_images=[resto...])
#
#
# RETO 2 — Bitácora de resultados en Excel            (archivo: reto2_solucion.py)
#   Al terminar, genera "resultados.xlsx" con una fila por dirección y las
#   columnas: direccion | estado ("OK" o "ERROR") | pdf | fecha
#   Así el usuario sabe qué direcciones fallaron sin leer el .log.
#   Pistas:
#     - Guarda la lista de direcciones en obtener_direcciones().
#     - Guarda en un diccionario {direccion: ruta_pdf} las que sí funcionaron
#       (en capturar_direccion). Las que no estén ahí, fallaron.
#     - Escribe el Excel en finalizar() con openpyxl (Workbook, ws.append, wb.save).
#
#
# RETO 3 — Encabezado con la dirección en cada captura  (archivo: reto3_solucion.py)
#   Agrega arriba de cada captura una franja de color con la dirección buscada
#   y la fecha, para que el PDF se identifique a simple vista.
#   Pistas:
#     - Después de super().capturar_direccion(), abre el PNG con Image.open(),
#       crea una imagen nueva más alta: Image.new("RGB", (ancho, alto + franja), color)
#       y pega la captura debajo de la franja con .paste(captura, (0, franja)).
#     - Escribe el texto con ImageDraw.Draw(imagen).text((x, y), texto, font=..., fill=...)
#       La fuente se carga con ImageFont.truetype("arial.ttf", 32).
#     - Guarda el PNG y vuelve a generar el PDF con imagen_a_pdf(png, pdf).
