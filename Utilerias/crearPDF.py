"""
crearPDF.py
===========
Genera un PDF con formato de factura usando la librería reportlab.

¿Qué hace?
    1. Define los datos de la factura: emisor, cliente, folio y conceptos.
    2. Arma el documento como una lista de "elementos" (párrafos, tablas, espacios)
       que reportlab acomoda en la página de arriba hacia abajo.
    3. Calcula subtotal, IVA y total a partir de los conceptos.
    4. Guarda el PDF en la misma carpeta que este script.

Conceptos clave de reportlab (módulo platypus):
    - SimpleDocTemplate: el documento; define tamaño de hoja y márgenes.
    - Flowables:         elementos que "fluyen" en la página (Paragraph, Table, Spacer).
                         Si no caben, pasan solos a la siguiente página.
    - Paragraph:         texto con estilo; acepta etiquetas tipo HTML (<b>, <br/>, <font>).
    - Table + TableStyle: tablas; el estilo se aplica por rangos de celdas.

Librerías que usa:
    - reportlab: genera archivos PDF desde Python.

Instalación:
    pip install reportlab

Uso:
    python crearPDF.py   -> crea factura_A-0001.pdf junto a este script
"""
from datetime import date    # Para obtener la fecha de hoy
from pathlib import Path     # Para manejar rutas de archivos sin importar el sistema operativo

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter          # Tamaño carta (8.5 x 11 pulgadas)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm                  # Permite medir en milímetros: 15 * mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

# ---------------------------------------------------------------------------
# CONFIGURACIÓN
# Constantes en MAYÚSCULAS: por convención indican valores que no cambian
# durante la ejecución. Cambiando estos colores se cambia todo el diseño.
# ---------------------------------------------------------------------------
COLOR_PRINCIPAL = colors.HexColor("#1F4E79")   # Azul oscuro: encabezados y total
COLOR_CLARO = colors.HexColor("#EAF1F8")       # Azul claro: fondos de filas
TASA_IVA = 0.16                                # 16 % de IVA

# ---------------------------------------------------------------------------
# DATOS DE EJEMPLO
# Usamos diccionarios para agrupar datos relacionados con nombres claros.
# En un sistema real estos datos vendrían de una base de datos o de un formulario.
# ---------------------------------------------------------------------------
emisor = {
    "nombre": "Desarrollo House S.A. de C.V.",
    "rfc": "DHO123456ABC",
    "direccion": "Av. Reforma 123, Col. Centro, CDMX, C.P. 06000",
    "telefono": "55 1234 5678",
    "correo": "facturacion@desarrollohouse.com",
}

cliente = {
    "nombre": "Cliente Ejemplo S.A. de C.V.",
    "rfc": "CEJ987654XYZ",
    "direccion": "Calle Falsa 456, Guadalajara, Jal., C.P. 44100",
    "correo": "contacto@clienteejemplo.com",
}

factura = {
    "folio": "A-0001",
    # strftime da formato a la fecha: %d día, %m mes, %Y año con 4 dígitos
    "fecha": date.today().strftime("%d/%m/%Y"),
    "metodo_pago": "PUE - Pago en una sola exhibición",
    "forma_pago": "03 - Transferencia electrónica",
}

# Lista de tuplas: cada tupla es un concepto (renglón) de la factura.
# Las tuplas se usan para datos fijos con posiciones conocidas.
conceptos = [
    # (cantidad, descripción, precio unitario)
    (1, "Desarrollo de aplicación web", 25000.00),
    (10, "Horas de soporte técnico", 450.00),
    (2, "Licencia anual de hosting", 1800.00),
    (1, "Configuración de dominio y SSL", 950.00),
]


def moneda(valor):
    """
    Da formato de dinero a un número.
    Ejemplo: 25000 -> "$25,000.00"
        ,   separa los miles con comas
        .2f muestra siempre 2 decimales
    """
    return f"${valor:,.2f}"


def crear_factura(ruta_salida):
    """
    Construye la factura y la guarda como PDF.

    Parámetros:
        ruta_salida: ruta del archivo PDF que se va a crear.

    Regresa:
        El total de la factura (subtotal + IVA).
    """
    # 1) CREAR EL DOCUMENTO
    # Se define el tamaño de hoja y los márgenes. str() porque reportlab
    # espera la ruta como texto y no como objeto Path.
    doc = SimpleDocTemplate(
        str(ruta_salida), pagesize=letter,
        leftMargin=18 * mm, rightMargin=18 * mm, topMargin=15 * mm, bottomMargin=15 * mm,
    )
    # doc.width es el ancho útil (hoja menos márgenes). Lo usamos para que
    # las columnas de las tablas se calculen como porcentajes del ancho.
    ancho = doc.width

    # 2) DEFINIR ESTILOS DE TEXTO
    # getSampleStyleSheet() trae estilos predefinidos ("Normal", "Title", ...).
    # ParagraphStyle crea un estilo nuevo; parent= hereda todo del estilo base
    # y solo cambiamos lo que nos interesa (tamaño, color, fuente).
    estilos = getSampleStyleSheet()
    normal = ParagraphStyle("normal", parent=estilos["Normal"], fontSize=9, leading=12)  # leading = interlineado
    titulo = ParagraphStyle("titulo", parent=normal, fontSize=22, leading=26,
                            textColor=COLOR_PRINCIPAL, fontName="Helvetica-Bold")
    blanco = ParagraphStyle("blanco", parent=normal, textColor=colors.white, fontName="Helvetica-Bold")

    # Aquí iremos agregando cada parte del PDF, en el orden en que aparecerá.
    elementos = []

    # 3) ENCABEZADO
    # Truco de diseño: una tabla de 1 fila x 2 columnas sirve para poner
    # contenido lado a lado (emisor a la izquierda, datos de factura a la derecha).
    info_emisor = Paragraph(
        f"<font size=13><b>{emisor['nombre']}</b></font><br/>"
        f"RFC: {emisor['rfc']}<br/>{emisor['direccion']}<br/>"
        f"Tel: {emisor['telefono']}<br/>{emisor['correo']}", normal)
    # Una tabla dentro de otra tabla: 3 filas alineadas a la derecha.
    info_factura = Table(
        [[Paragraph("FACTURA", titulo)],
         [Paragraph(f"<b>Folio:</b> {factura['folio']}", normal)],
         [Paragraph(f"<b>Fecha:</b> {factura['fecha']}", normal)]],
        colWidths=[ancho * 0.4])
    info_factura.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "RIGHT")]))

    encabezado = Table([[info_emisor, info_factura]], colWidths=[ancho * 0.6, ancho * 0.4])
    # TableStyle recibe una lista de reglas: (comando, celda_inicio, celda_fin, valores...)
    # Las celdas se indican como (columna, fila). -1 significa "la última".
    #   (0, 0), (-1, -1) -> desde la primera celda hasta la última = toda la tabla
    encabezado.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),                   # Alinear arriba
        ("LINEBELOW", (0, 0), (-1, 0), 2, COLOR_PRINCIPAL),    # Línea azul de 2 pt bajo la fila 0
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),               # Espacio interno inferior
    ]))
    # Spacer(ancho, alto) agrega espacio vertical en blanco entre elementos.
    elementos += [encabezado, Spacer(1, 8 * mm)]

    # 4) DATOS DEL CLIENTE Y DEL PAGO
    # Tabla de 2 filas x 2 columnas: la fila 0 son los títulos y la fila 1 el contenido.
    datos = Table([
        [Paragraph("FACTURAR A", blanco), Paragraph("DATOS DE PAGO", blanco)],
        [Paragraph(f"<b>{cliente['nombre']}</b><br/>RFC: {cliente['rfc']}<br/>"
                   f"{cliente['direccion']}<br/>{cliente['correo']}", normal),
         Paragraph(f"<b>Método:</b> {factura['metodo_pago']}<br/>"
                   f"<b>Forma:</b> {factura['forma_pago']}<br/><b>Moneda:</b> MXN", normal)],
    ], colWidths=[ancho * 0.55, ancho * 0.45])
    datos.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), COLOR_PRINCIPAL),   # Fila 0: fondo azul oscuro
        ("BACKGROUND", (0, 1), (-1, 1), COLOR_CLARO),       # Fila 1: fondo azul claro
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elementos += [datos, Spacer(1, 8 * mm)]

    # 5) TABLA DE CONCEPTOS
    # La primera fila son los encabezados de columna.
    filas = [["Cant.", "Descripción", "P. Unitario", "Importe"]]
    subtotal = 0
    # "Desempaquetado": cada tupla se separa directamente en 3 variables.
    for cantidad, descripcion, precio in conceptos:
        importe = cantidad * precio
        subtotal += importe   # Vamos acumulando para obtener el subtotal
        # La descripción va en un Paragraph para que haga salto de línea si es larga.
        filas.append([str(cantidad), Paragraph(descripcion, normal), moneda(precio), moneda(importe)])

    # repeatRows=1: si la tabla ocupa varias páginas, repite el encabezado en cada una.
    tabla = Table(filas, colWidths=[ancho * 0.1, ancho * 0.5, ancho * 0.2, ancho * 0.2], repeatRows=1)
    estilo_tabla = [
        ("BACKGROUND", (0, 0), (-1, 0), COLOR_PRINCIPAL),       # Encabezado azul
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),           # con texto blanco
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),        # y en negritas
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),                   # Columna 0 (cantidad) centrada
        ("ALIGN", (2, 0), (-1, -1), "RIGHT"),                   # Columnas de dinero a la derecha
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, colors.lightgrey), # Línea gris entre filas
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    # Filas "cebra": fondo claro en las filas pares para facilitar la lectura.
    # range(2, len(filas), 2) -> 2, 4, 6... (empieza en 2 para saltar el encabezado)
    for i in range(2, len(filas), 2):
        estilo_tabla.append(("BACKGROUND", (0, i), (-1, i), COLOR_CLARO))
    tabla.setStyle(TableStyle(estilo_tabla))
    elementos += [tabla, Spacer(1, 5 * mm)]

    # 6) TOTALES
    iva = subtotal * TASA_IVA
    total = subtotal + iva
    # hAlign="RIGHT" coloca la tabla completa del lado derecho de la página.
    # {TASA_IVA:.0%} convierte 0.16 en "16%".
    totales = Table([
        ["Subtotal", moneda(subtotal)],
        [f"IVA ({TASA_IVA:.0%})", moneda(iva)],
        ["TOTAL", moneda(total)],
    ], colWidths=[ancho * 0.2, ancho * 0.2], hAlign="RIGHT")
    totales.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BACKGROUND", (0, 2), (-1, 2), COLOR_PRINCIPAL),   # Fila 2 (TOTAL) resaltada
        ("TEXTCOLOR", (0, 2), (-1, 2), colors.white),
        ("FONTNAME", (0, 2), (-1, 2), "Helvetica-Bold"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    elementos += [totales, Spacer(1, 15 * mm)]

    # 7) PIE DE PÁGINA
    # alignment=1 significa centrado (0 = izquierda, 1 = centro, 2 = derecha).
    pie = ParagraphStyle("pie", parent=normal, alignment=1, textColor=colors.grey, fontSize=8)
    elementos.append(Paragraph(
        "Gracias por su preferencia.<br/>"
        "Este documento es una representación impresa de ejemplo y no tiene validez fiscal.", pie))

    # 8) GENERAR EL PDF
    # build() toma la lista de elementos, los acomoda en las páginas y escribe el archivo.
    doc.build(elementos)
    return total


# Este bloque solo se ejecuta cuando corremos el archivo directamente
# (python crearPDF.py), no cuando otro script lo importa con "import".
if __name__ == "__main__":
    # Path(__file__).with_name(...) crea una ruta en la misma carpeta del script,
    # pero con otro nombre de archivo. Así el PDF queda junto al código.
    salida = Path(__file__).with_name(f"factura_{factura['folio']}.pdf")
    total = crear_factura(salida)
    print(f"Factura generada: {salida} (Total: {moneda(total)})")
