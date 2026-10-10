"""
crearRelojDigital.py
====================
Reloj con interfaz gráfica que se puede ver en modo digital o analógico.

¿Qué hace?
    1. Abre una ventana con dos botones para elegir el modo: Digital o Analógico.
    2. Modo digital: muestra la hora como texto (HH:MM:SS) y permite cambiar
       entre formato de 24 horas y de 12 horas (AM/PM).
    3. Modo analógico: dibuja una carátula con números, marcas y tres manecillas
       (horas, minutos y segundos) usando un Canvas ("lienzo" para dibujar).
    4. En ambos modos muestra la fecha en español debajo del reloj.
    5. Cada segundo vuelve a leer la hora del sistema y actualiza la pantalla.

Conceptos que se practican:
    - Programación orientada a objetos: una clase que guarda el estado del reloj.
    - Tkinter: ventanas, etiquetas (Label), botones, Radiobutton y Canvas.
    - Programación por eventos: el programa "espera" clics y temporizadores.
    - Trigonometría: seno y coseno para ubicar números y manecillas en el círculo.

Librerías que usa (todas vienen incluidas con Python, no hay que instalar nada):
    - tkinter:  crea la interfaz gráfica.
    - datetime: obtiene la fecha y hora actuales.
    - math:     funciones matemáticas (sin, cos, radians).

Uso:
    python crearRelojDigital.py
"""
import math                      # Para calcular posiciones en el círculo (seno, coseno)
import tkinter as tk             # Librería estándar de Python para interfaces gráficas
from datetime import datetime    # Para obtener la fecha y hora del sistema

# ---------------------------------------------------------------------------
# CONFIGURACIÓN
# Constantes en MAYÚSCULAS: por convención indican valores que no cambian
# durante la ejecución. Si queremos otro aspecto, solo cambiamos estos valores.
# ---------------------------------------------------------------------------

# strftime("%A") daría los días en inglés (o según el idioma del sistema),
# por eso usamos listas propias en español.
# El orden importa: weekday() devuelve 0 para lunes y 6 para domingo.
DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

# Colores en formato hexadecimal: #RRGGBB (rojo, verde, azul de 00 a ff)
COLOR_FONDO = "#0f172a"      # Azul muy oscuro
COLOR_HORA = "#22d3ee"       # Cian
COLOR_FECHA = "#94a3b8"      # Gris azulado
COLOR_SEGUNDERO = "#f43f5e"  # Rojo

# Ancho y alto (en píxeles) del lienzo donde se dibuja el reloj analógico
TAMANO_ANALOGICO = 320


class RelojDigital:
    """
    Ventana del reloj. Guarda los elementos de la interfaz y el estado actual
    (qué modo está activo y si la hora se muestra en 12 o 24 horas).
    """

    def __init__(self, ventana):
        """
        Constructor: se ejecuta una sola vez al crear el reloj.
        Aquí se crean todos los elementos de la interfaz.

        Parámetros:
            ventana: la ventana principal de Tkinter (creada con tk.Tk()).
        """
        # "self" es el propio objeto. Guardar algo en self.xxx permite usarlo
        # después desde cualquier otro método de la clase.
        self.ventana = ventana
        self.formato_24h = True

        # StringVar es una variable "especial" de Tkinter: los Radiobutton la
        # leen y la modifican solos. Guarda el modo elegido: "digital" o "analogico".
        self.modo = tk.StringVar(value="digital")

        # 1) CONFIGURAR LA VENTANA
        ventana.title("Reloj Digital")
        ventana.configure(bg=COLOR_FONDO)
        ventana.resizable(False, False)   # No permitir cambiar el tamaño (ancho, alto)

        # 2) SELECTOR DE MODO (botones Digital / Analógico)
        self.crear_selector()

        # 3) CONTENEDOR DEL RELOJ
        # Un Frame es una "caja" que agrupa otros elementos. Aquí dentro se
        # muestra el reloj digital O el analógico, nunca los dos a la vez.
        # pack() coloca el elemento en la ventana, uno debajo de otro.
        self.contenedor = tk.Frame(ventana, bg=COLOR_FONDO)
        self.contenedor.pack(padx=40)     # padx: margen a la izquierda y derecha

        # Reloj digital: una etiqueta de texto grande.
        # Consolas es una fuente "monoespaciada" (todos los caracteres miden
        # lo mismo), así los números no "bailan" cuando cambian.
        # Todavía no hacemos pack(): cambiar_modo() decide cuál se muestra.
        self.etiqueta_hora = tk.Label(self.contenedor, font=("Consolas", 64, "bold"),
                                      fg=COLOR_HORA, bg=COLOR_FONDO)

        # Reloj analógico: un Canvas es un área donde podemos dibujar líneas,
        # círculos y texto indicando coordenadas en píxeles.
        # highlightthickness=0 quita el borde que Tkinter pone por defecto.
        self.lienzo = tk.Canvas(self.contenedor, width=TAMANO_ANALOGICO,
                                height=TAMANO_ANALOGICO, bg=COLOR_FONDO,
                                highlightthickness=0)
        # La carátula no cambia, así que se dibuja una sola vez aquí.
        self.dibujar_caratula()

        # 4) FECHA (se ve en los dos modos)
        self.etiqueta_fecha = tk.Label(ventana, font=("Segoe UI", 16),
                                       fg=COLOR_FECHA, bg=COLOR_FONDO)
        self.etiqueta_fecha.pack(pady=(0, 10))   # pady=(arriba, abajo)

        # 5) BOTÓN 12h / 24h (solo se muestra en modo digital)
        # command=self.cambiar_formato: el método que se ejecuta al hacer clic.
        # Ojo: se pasa el método SIN paréntesis; Tkinter lo llamará después.
        self.boton_formato = tk.Button(ventana, text="Cambiar a 12h",
                                       command=self.cambiar_formato,
                                       font=("Segoe UI", 10), fg=COLOR_FONDO,
                                       bg=COLOR_HORA, relief="flat",
                                       activebackground=COLOR_FECHA, cursor="hand2")

        # 6) MOSTRAR EL MODO INICIAL Y ARRANCAR EL RELOJ
        self.cambiar_modo()
        self.actualizar()

    def crear_selector(self):
        """Crea los dos botones para elegir entre reloj digital y analógico."""
        selector = tk.Frame(self.ventana, bg=COLOR_FONDO)
        selector.pack(pady=(20, 0))

        # Un Radiobutton es una opción de un grupo donde solo una puede estar
        # elegida. Los botones del grupo comparten la misma variable (self.modo):
        # al hacer clic en uno, self.modo toma su "value".
        # indicatoron=False los dibuja como botones normales en lugar del
        # clásico circulito, y selectcolor es el color del botón elegido.
        for texto, valor in (("Digital", "digital"), ("Analógico", "analogico")):
            tk.Radiobutton(selector, text=texto, value=valor, variable=self.modo,
                           command=self.cambiar_modo, indicatoron=False,
                           font=("Segoe UI", 10), width=10, relief="flat",
                           fg=COLOR_FECHA, bg=COLOR_FONDO,
                           selectcolor=COLOR_HORA, activebackground=COLOR_FECHA,
                           cursor="hand2").pack(side="left", padx=2)  # side="left": uno al lado del otro

    def dibujar_caratula(self):
        """
        Dibuja la parte fija del reloj analógico: el círculo, las marcas
        de minutos y los números del 1 al 12.

        ¿Cómo se ubica un punto en el círculo?
            En el Canvas, el punto (0, 0) es la esquina SUPERIOR izquierda y
            la "y" crece hacia ABAJO. Para un ángulo medido desde las 12 en
            sentido horario:
                x = centro + distancia * sin(ángulo)
                y = centro - distancia * cos(ángulo)
            Ejemplos: 0° -> arriba (las 12), 90° -> derecha (las 3),
                      180° -> abajo (las 6), 270° -> izquierda (las 9).
        """
        centro = TAMANO_ANALOGICO / 2
        radio = centro - 10              # Dejamos 10 px de margen al borde

        # create_oval recibe las esquinas del cuadrado que contiene al círculo:
        # (x izquierda, y arriba, x derecha, y abajo)
        self.lienzo.create_oval(centro - radio, centro - radio,
                                centro + radio, centro + radio,
                                outline=COLOR_HORA, width=4)

        # MARCAS DE MINUTOS Y HORAS
        # Hay 60 marcas en 360°, una cada 6°.
        # Cada 5 marcas es una hora: esas se dibujan más largas y gruesas.
        # math.sin y math.cos trabajan en radianes, por eso usamos math.radians().
        for i in range(60):
            angulo = math.radians(i * 6)
            largo = 15 if i % 5 == 0 else 6     # % es el residuo: i % 5 == 0 -> múltiplo de 5
            grosor = 3 if i % 5 == 0 else 1
            # Cada marca es una línea que va del punto (x1, y1) más cerca del
            # centro al punto (x2, y2) pegado al borde.
            x1 = centro + (radio - largo) * math.sin(angulo)
            y1 = centro - (radio - largo) * math.cos(angulo)
            x2 = centro + (radio - 4) * math.sin(angulo)
            y2 = centro - (radio - 4) * math.cos(angulo)
            self.lienzo.create_line(x1, y1, x2, y2, fill=COLOR_FECHA, width=grosor)

        # NÚMEROS DE LAS HORAS
        # 12 números en 360°: uno cada 30°. Se colocan 35 px hacia dentro del borde.
        for hora in range(1, 13):
            angulo = math.radians(hora * 30)
            x = centro + (radio - 35) * math.sin(angulo)
            y = centro - (radio - 35) * math.cos(angulo)
            self.lienzo.create_text(x, y, text=str(hora), fill=COLOR_HORA,
                                    font=("Segoe UI", 16, "bold"))

    def dibujar_manecilla(self, angulo_grados, largo, grosor, color):
        """
        Dibuja una manecilla como una línea que sale del centro del reloj.

        Parámetros:
            angulo_grados: hacia dónde apunta (0 = las 12, 90 = las 3...).
            largo:         longitud de la manecilla en píxeles.
            grosor:        ancho de la línea en píxeles.
            color:         color de la línea.
        """
        centro = TAMANO_ANALOGICO / 2
        angulo = math.radians(angulo_grados)
        # Punta de la manecilla (misma fórmula que en dibujar_caratula)
        x = centro + largo * math.sin(angulo)
        y = centro - largo * math.cos(angulo)
        # tags="manecillas" le pone una "etiqueta" a la línea para poder
        # borrar todas las manecillas juntas en el siguiente segundo.
        # capstyle="round" redondea las puntas de la línea.
        self.lienzo.create_line(centro, centro, x, y, fill=color, width=grosor,
                                capstyle="round", tags="manecillas")

    def dibujar_manecillas(self, ahora):
        """
        Borra las manecillas anteriores y dibuja las nuevas según la hora.

        Parámetros:
            ahora: fecha y hora actual (objeto datetime).
        """
        # Borramos solo lo que tiene la etiqueta "manecillas";
        # la carátula se queda como está.
        self.lienzo.delete("manecillas")
        radio = TAMANO_ANALOGICO / 2 - 10

        # Usamos decimales para que las manecillas avancen poco a poco,
        # como en un reloj real. Ejemplo a las 3:30:00:
        #   minutos = 30 + 0/60  = 30.0
        #   horas   = 3 + 30/60  = 3.5  -> la manecilla queda entre el 3 y el 4
        # hour % 12 convierte el formato de 24 h a 12 h (15 -> 3).
        segundos = ahora.second
        minutos = ahora.minute + segundos / 60
        horas = ahora.hour % 12 + minutos / 60

        # Conversión a grados:
        #   horas:    12 horas    = 360°  -> 30° por hora
        #   minutos:  60 minutos  = 360°  ->  6° por minuto
        #   segundos: 60 segundos = 360°  ->  6° por segundo
        # Cada manecilla tiene distinto largo (fracción del radio) y grosor.
        self.dibujar_manecilla(horas * 30, radio * 0.5, 7, COLOR_HORA)
        self.dibujar_manecilla(minutos * 6, radio * 0.75, 4, COLOR_FECHA)
        self.dibujar_manecilla(segundos * 6, radio * 0.85, 2, COLOR_SEGUNDERO)

        # Círculo pequeño en el centro, encima de las manecillas
        # (en el Canvas, lo último que se dibuja queda por encima).
        centro = TAMANO_ANALOGICO / 2
        self.lienzo.create_oval(centro - 6, centro - 6, centro + 6, centro + 6,
                                fill=COLOR_SEGUNDERO, outline="", tags="manecillas")

    def cambiar_modo(self):
        """
        Muestra el reloj digital o el analógico según el botón elegido.
        Se ejecuta al iniciar y cada vez que se hace clic en el selector.
        """
        # pack() muestra un elemento y pack_forget() lo oculta
        # (el elemento no se borra, solo deja de verse).
        # pack_configure() cambia las opciones de un elemento que ya está visible.
        if self.modo.get() == "digital":
            self.lienzo.pack_forget()
            self.etiqueta_hora.pack(pady=(20, 0))
            self.boton_formato.pack(pady=(0, 25))
            self.etiqueta_fecha.pack_configure(pady=(0, 10))
        else:
            self.etiqueta_hora.pack_forget()
            self.boton_formato.pack_forget()   # El formato 12/24 h no aplica al analógico
            self.lienzo.pack(pady=(20, 10))
            self.etiqueta_fecha.pack_configure(pady=(0, 25))

    def cambiar_formato(self):
        """Alterna entre formato de 24 horas y de 12 horas (solo modo digital)."""
        # "not" invierte el valor: True -> False, False -> True
        self.formato_24h = not self.formato_24h
        # El botón muestra la opción a la que se puede cambiar, no la actual.
        # Esta forma de escribir un if en una línea se llama "expresión condicional":
        #   valor_si_verdadero if condición else valor_si_falso
        self.boton_formato.config(
            text="Cambiar a 12h" if self.formato_24h else "Cambiar a 24h")
        # Actualizamos de inmediato para no esperar al siguiente segundo.
        # reprogramar=False evita crear un segundo temporizador: si se
        # programara otro, el reloj se actualizaría dos veces por segundo.
        self.actualizar(reprogramar=False)

    def actualizar(self, reprogramar=True):
        """
        Lee la hora del sistema y actualiza el texto, la fecha y las manecillas.

        Parámetros:
            reprogramar: si es True (por defecto), vuelve a llamarse a sí misma
                         en 1 segundo, lo que mantiene el reloj en marcha.
        """
        # 1) OBTENER LA HORA ACTUAL
        ahora = datetime.now()

        # 2) DAR FORMATO A LA HORA
        # strftime convierte la fecha/hora en texto usando códigos:
        #   %H -> hora de 00 a 23      %I -> hora de 01 a 12
        #   %M -> minutos              %S -> segundos
        #   %p -> AM o PM
        if self.formato_24h:
            hora = ahora.strftime("%H:%M:%S")
        else:
            hora = ahora.strftime("%I:%M:%S %p")

        # 3) DAR FORMATO A LA FECHA
        # Las listas empiezan en 0, por eso a month (1-12) le restamos 1.
        # Una f-string (f"...") inserta el valor de las variables entre llaves {}.
        fecha = f"{DIAS[ahora.weekday()]}, {ahora.day} de {MESES[ahora.month - 1]} de {ahora.year}"

        # 4) ACTUALIZAR LA PANTALLA
        # Se actualizan los dos relojes, aunque uno esté oculto; así, al cambiar
        # de modo, el otro ya muestra la hora correcta.
        self.etiqueta_hora.config(text=hora)
        self.etiqueta_fecha.config(text=fecha)
        self.dibujar_manecillas(ahora)

        # 5) PROGRAMAR LA SIGUIENTE ACTUALIZACIÓN
        # after(milisegundos, función) le pide a Tkinter que ejecute la función
        # después de ese tiempo. 1000 ms = 1 segundo.
        # No usamos un ciclo "while True" con time.sleep(1) porque congelaría
        # la ventana: Tkinter no podría atender clics ni redibujar.
        if reprogramar:
            self.ventana.after(1000, self.actualizar)


# Este bloque solo se ejecuta cuando corremos el archivo directamente
# (python crearRelojDigital.py), no cuando otro script lo importa con "import".
if __name__ == "__main__":
    ventana = tk.Tk()        # Crea la ventana principal
    RelojDigital(ventana)    # Construye el reloj dentro de la ventana
    # mainloop() inicia el "ciclo de eventos": mantiene la ventana abierta,
    # escuchando clics y temporizadores, hasta que el usuario la cierra.
    ventana.mainloop()
