"""
Calculadora sencilla con interfaz gráfica (tkinter).

Conceptos que se practican en este programa:
    - Crear ventanas, etiquetas y botones con tkinter.
    - Organizar elementos con pack() y grid().
    - Programación orientada a objetos: una clase que guarda el "estado"
      de la calculadora (el número en pantalla, el operador elegido, etc.).
    - Diccionarios que guardan funciones (lambda) para no usar muchos if.
    - Eventos: responder a clics del ratón y a teclas del teclado.
    - Manejo de errores con try / except (división entre cero).

Cómo funciona por dentro (idea general):
    La calculadora recuerda tres cosas:
        1. actual     -> el número que se está escribiendo (texto en pantalla).
        2. acumulado  -> el primer número de la operación (antes del operador).
        3. operador   -> la operación elegida (+, −, ×, ÷).
    Al presionar "=", se aplica: acumulado <operador> actual.

Ejecutar:
    python crearCalculadora.py
"""

import tkinter as tk

# ---------------------------------------------------------------------------
# CONSTANTES DE COLORES
# Se escriben en MAYÚSCULAS por convención: indican valores que no cambian.
# Tenerlos aquí arriba permite cambiar el estilo de toda la app en un solo lugar.
# ---------------------------------------------------------------------------
COLOR_FONDO = "#0f172a"            # Fondo de la ventana (azul muy oscuro)
COLOR_PANTALLA = "#22d3ee"         # Color del número grande (cian)
COLOR_OPERACION = "#94a3b8"        # Color del texto pequeño de la operación (gris)
COLOR_BOTON = "#1e293b"            # Botones de números
COLOR_BOTON_OPERADOR = "#22d3ee"   # Botones + − × ÷
COLOR_BOTON_ESPECIAL = "#334155"   # Botones C, ⌫, %, ±
COLOR_IGUAL = "#f43f5e"            # Botón = (rojo, para que destaque)

# ---------------------------------------------------------------------------
# DISTRIBUCIÓN DEL TECLADO
# Es una lista de listas: cada lista interna es una FILA de botones.
# Así el programa crea los botones recorriendo esta estructura,
# en lugar de escribir 20 botones a mano.
# ---------------------------------------------------------------------------
BOTONES = [
    ["C", "⌫", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "−"],
    ["1", "2", "3", "+"],
    ["±", "0", ".", "="],
]

# ---------------------------------------------------------------------------
# OPERADORES
# Diccionario que relaciona cada símbolo con una función.
# "lambda a, b: a + b" es una función pequeña sin nombre que recibe dos
# números y devuelve el resultado.
#
# Ejemplo de uso:
#     OPERADORES["+"](2, 3)  ->  5
#
# Ventaja: en vez de escribir if operador == "+": ... elif operador == "−": ...
# solo buscamos la función en el diccionario y la llamamos.
# ---------------------------------------------------------------------------
OPERADORES = {
    "+": lambda a, b: a + b,
    "−": lambda a, b: a - b,
    "×": lambda a, b: a * b,
    "÷": lambda a, b: a / b,
}

# ---------------------------------------------------------------------------
# TECLAS DEL TECLADO FÍSICO
# Traduce la tecla que presiona el usuario al botón equivalente.
# Por ejemplo, en el teclado se escribe "*" pero en pantalla usamos "×".
# Las claves como "Return" o "BackSpace" son los nombres que tkinter
# usa para las teclas especiales (Enter, Retroceso, etc.).
# ---------------------------------------------------------------------------
TECLAS = {
    "*": "×", "/": "÷", "-": "−", "+": "+", "%": "%", ".": ".", ",": ".",
    "Return": "=", "KP_Enter": "=", "=": "=",
    "BackSpace": "⌫", "Escape": "C", "Delete": "C",
}


class Calculadora:
    """
    Representa la calculadora completa: su interfaz y su lógica.

    Atributos (el "estado" de la calculadora):
        actual (str): número que se muestra en pantalla. Se guarda como texto
            porque así es fácil agregarle dígitos: "12" + "3" -> "123".
        acumulado (float | None): primer número de la operación.
            None significa "todavía no hay ninguno".
        operador (str | None): operación pendiente ("+", "−", "×" o "÷").
        reiniciar_entrada (bool): si es True, el próximo dígito que se
            escriba REEMPLAZA al número de la pantalla en lugar de agregarse.
            Se activa después de elegir un operador o de ver un resultado.
    """

    def __init__(self, ventana):
        """
        Constructor: se ejecuta una sola vez al crear la calculadora.
        Prepara el estado inicial y construye la interfaz.

        Parámetro:
            ventana (tk.Tk): la ventana principal donde se dibuja todo.
        """
        self.ventana = ventana

        # Estado inicial: pantalla en 0, sin operación pendiente
        self.actual = "0"
        self.acumulado = None
        self.operador = None
        self.reiniciar_entrada = False

        # Configuración de la ventana
        ventana.title("Calculadora")
        ventana.configure(bg=COLOR_FONDO)
        ventana.resizable(False, False)   # El usuario no puede cambiar el tamaño

        # Etiqueta pequeña superior: muestra la operación pendiente (ej. "200 +")
        # anchor="e" alinea el texto a la derecha ("e" = east / este)
        self.etiqueta_operacion = tk.Label(ventana, text="", anchor="e",
                                           font=("Segoe UI", 14),
                                           fg=COLOR_OPERACION, bg=COLOR_FONDO)
        # fill="x" hace que la etiqueta ocupe todo el ancho de la ventana
        self.etiqueta_operacion.pack(fill="x", padx=20, pady=(20, 0))

        # Etiqueta grande: el número actual
        self.etiqueta_pantalla = tk.Label(ventana, text=self.actual, anchor="e",
                                          font=("Consolas", 40, "bold"),
                                          fg=COLOR_PANTALLA, bg=COLOR_FONDO)
        self.etiqueta_pantalla.pack(fill="x", padx=20, pady=(0, 15))

        self.crear_botones()

        # bind() conecta un EVENTO con una función.
        # "<Key>" = cualquier tecla presionada -> llama a tecla_presionada()
        ventana.bind("<Key>", self.tecla_presionada)

    # =======================================================================
    # INTERFAZ
    # =======================================================================

    def crear_botones(self):
        """
        Crea todos los botones recorriendo la lista BOTONES y los acomoda
        en una cuadrícula (grid) de 5 filas por 4 columnas.
        """
        # Frame = contenedor invisible que agrupa los botones
        teclado = tk.Frame(self.ventana, bg=COLOR_FONDO)
        teclado.pack(padx=15, pady=(0, 20))

        # enumerate() devuelve la posición (índice) y el valor al mismo tiempo.
        # fila = 0, 1, 2...   textos = ["C", "⌫", "%", "÷"], ...
        for fila, textos in enumerate(BOTONES):
            for columna, texto in enumerate(textos):

                # Elegimos colores según el tipo de botón
                if texto == "=":
                    fondo, letra = COLOR_IGUAL, COLOR_FONDO
                elif texto in OPERADORES:
                    fondo, letra = COLOR_BOTON_OPERADOR, COLOR_FONDO
                elif texto in ("C", "⌫", "%", "±"):
                    fondo, letra = COLOR_BOTON_ESPECIAL, COLOR_PANTALLA
                else:
                    fondo, letra = COLOR_BOTON, "white"

                # IMPORTANTE: "lambda t=texto: self.presionar(t)"
                # Cada botón necesita recordar SU propio texto. Si escribiéramos
                # "lambda: self.presionar(texto)", todos los botones usarían el
                # último valor del ciclo ("="). Con t=texto se "congela" el valor
                # en el momento en que se crea cada botón.
                tk.Button(teclado, text=texto, width=4, height=1,
                          font=("Segoe UI", 20, "bold"), fg=letra, bg=fondo,
                          relief="flat", activebackground=COLOR_OPERACION,
                          cursor="hand2",
                          command=lambda t=texto: self.presionar(t)
                          ).grid(row=fila, column=columna, padx=4, pady=4)

    def tecla_presionada(self, evento):
        """
        Se ejecuta cada vez que el usuario presiona una tecla.

        Parámetro:
            evento: objeto que tkinter envía con información de la tecla.
                evento.char   -> el carácter escrito ("5", "+", ...)
                evento.keysym -> el nombre de la tecla ("Return", "BackSpace", ...)
        """
        if evento.char.isdigit():              # ¿Es un número del 0 al 9?
            self.presionar(evento.char)
        elif evento.keysym in TECLAS:          # ¿Es una tecla especial conocida?
            self.presionar(TECLAS[evento.keysym])
        elif evento.char in TECLAS:            # ¿Es un símbolo conocido?
            self.presionar(TECLAS[evento.char])
        # Cualquier otra tecla se ignora

    # =======================================================================
    # LÓGICA PRINCIPAL
    # =======================================================================

    def presionar(self, texto):
        """
        Punto central de la calculadora: TODOS los botones y teclas llegan aquí.
        Decide qué hacer según el texto del botón y después refresca la pantalla.

        Parámetro:
            texto (str): el botón presionado ("7", "+", "=", "C", ...)
        """
        # Si había un error en pantalla, cualquier botón empieza de nuevo
        if self.actual == "Error" and texto != "C":
            self.limpiar()

        if texto.isdigit():
            self.agregar_digito(texto)
        elif texto == ".":
            self.agregar_punto()
        elif texto in OPERADORES:
            self.elegir_operador(texto)
        elif texto == "=":
            self.calcular()
        elif texto == "C":
            self.limpiar()
        elif texto == "⌫":
            self.borrar()
        elif texto == "±":
            self.cambiar_signo()
        elif texto == "%":
            self.porcentaje()

        # Después de cualquier acción, mostramos el nuevo estado
        self.actualizar_pantalla()

    def agregar_digito(self, digito):
        """
        Agrega un dígito al número en pantalla.

        Ejemplos:
            pantalla "0"  + "5"  -> "5"    (el cero inicial se reemplaza)
            pantalla "12" + "3"  -> "123"  (se concatena el texto)
        """
        if self.reiniciar_entrada or self.actual == "0":
            # Empezamos un número nuevo
            self.actual = digito
            self.reiniciar_entrada = False
        elif len(self.actual) < 15:
            # Límite de 15 caracteres para que el número quepa en pantalla
            self.actual += digito

    def agregar_punto(self):
        """Agrega el punto decimal, evitando que haya dos puntos en el mismo número."""
        if self.reiniciar_entrada:
            # Si se empieza un número con ".", se convierte en "0."
            self.actual = "0"
            self.reiniciar_entrada = False
        if "." not in self.actual:
            self.actual += "."

    def elegir_operador(self, operador):
        """
        Guarda el número actual y la operación elegida.
        Ejemplo: al escribir "8" y presionar "+", se guarda acumulado = 8
        y operador = "+". El siguiente número que se escriba será el segundo.

        Si ya había una operación pendiente, primero la resuelve.
        Así se pueden encadenar: 2 + 3 + 4  ->  (2 + 3) = 5, luego 5 + 4.
        """
        if self.operador and not self.reiniciar_entrada:
            self.calcular()
            if self.actual == "Error":
                return
        # float() convierte el texto "8" en el número 8.0 para poder operar
        self.acumulado = float(self.actual)
        self.operador = operador
        self.reiniciar_entrada = True

    def calcular(self):
        """
        Realiza la operación pendiente: acumulado <operador> actual.
        Ejemplo: acumulado = 8, operador = "+", actual = "2"  ->  "10"
        """
        if self.operador is None:
            return   # No hay nada que calcular

        # try / except: intentamos la operación y, si falla, manejamos el error
        # en lugar de que el programa se cierre.
        try:
            funcion = OPERADORES[self.operador]
            resultado = funcion(self.acumulado, float(self.actual))
            self.actual = self.formatear(resultado)
        except ZeroDivisionError:
            # Python lanza este error al dividir entre cero
            self.actual = "Error"

        # La operación terminó: limpiamos lo pendiente
        self.acumulado = None
        self.operador = None
        self.reiniciar_entrada = True

    # =======================================================================
    # BOTONES ESPECIALES
    # =======================================================================

    def limpiar(self):
        """Botón C: regresa la calculadora a su estado inicial."""
        self.actual = "0"
        self.acumulado = None
        self.operador = None
        self.reiniciar_entrada = False

    def borrar(self):
        """
        Botón ⌫: borra el último dígito escrito.
        [:-1] toma el texto completo excepto el último carácter: "123"[:-1] -> "12"
        """
        if self.reiniciar_entrada:
            return   # No se borran dígitos de un resultado
        self.actual = self.actual[:-1]
        if self.actual in ("", "-"):
            self.actual = "0"

    def cambiar_signo(self):
        """Botón ±: convierte un número positivo en negativo y viceversa."""
        if self.actual != "0":
            if self.actual.startswith("-"):
                self.actual = self.actual[1:]        # "-5" -> "5"
            else:
                self.actual = "-" + self.actual      # "5"  -> "-5"

    def porcentaje(self):
        """
        Botón %: divide el número entre 100.

        En sumas y restas el porcentaje se calcula sobre el primer número,
        como en las calculadoras comunes:
            200 + 10%  ->  10% de 200 = 20  ->  200 + 20 = 220
        En multiplicaciones y divisiones solo divide entre 100:
            50 × 10%   ->  50 × 0.1 = 5
        """
        valor = float(self.actual) / 100
        if self.operador in ("+", "−") and self.acumulado is not None:
            valor *= self.acumulado
        self.actual = self.formatear(valor)
        self.reiniciar_entrada = True

    # =======================================================================
    # UTILIDADES
    # =======================================================================

    @staticmethod
    def formatear(numero):
        """
        Convierte un número en texto bonito para la pantalla.

        @staticmethod indica que este método no usa "self": funciona igual
        sin importar el estado de la calculadora.

        Ejemplos:
            5.0       -> "5"        (quita el ".0" innecesario)
            2.5       -> "2.5"
            0.1 + 0.2 -> "0.3"      (en Python da 0.30000000000000004;
                                     ".10g" redondea a 10 cifras significativas)
        """
        if numero == int(numero) and abs(numero) < 1e15:
            return str(int(numero))
        return f"{numero:.10g}"

    def actualizar_pantalla(self):
        """Muestra en las etiquetas el estado actual de la calculadora."""
        self.etiqueta_pantalla.config(text=self.actual)

        # Si hay una operación pendiente, la mostramos arriba (ej. "200 +")
        if self.operador:
            self.etiqueta_operacion.config(
                text=f"{self.formatear(self.acumulado)} {self.operador}")
        else:
            self.etiqueta_operacion.config(text="")


# ---------------------------------------------------------------------------
# PUNTO DE ENTRADA
# Este bloque solo se ejecuta si corremos el archivo directamente
# (python crearCalculadora.py), y NO cuando otro archivo lo importa.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    ventana = tk.Tk()          # 1. Crear la ventana principal
    Calculadora(ventana)       # 2. Construir la calculadora dentro de ella
    ventana.mainloop()         # 3. Mantener la ventana abierta esperando eventos
