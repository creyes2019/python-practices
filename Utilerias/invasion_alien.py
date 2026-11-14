"""
=====================================================
  PRÁCTICA: ¡INVASIÓN ALIENÍGENA! 👽🛸
  Eres la única persona que puede salvar la Tierra.
=====================================================

Conceptos que practicas:
  - Cadenas (strings) y sus métodos
  - Diccionarios
  - Clases y objetos (POO)
  - Ciclos y condicionales
  - El módulo random
  - Manejo de errores con try / except

Cómo correrlo:
  python invasion_alien.py
"""

import random

# -------------------------------------------------
# 1. DATOS
# -------------------------------------------------
# Diccionario para traducir letras al idioma zorgiano
ALFABETO_ZORG = {
    "a": "∆", "e": "Ξ", "i": "¡", "o": "⊙", "u": "ʊ",
    "s": "§", "t": "†", "r": "Я", "n": "И", "l": "ŀ",
}
# Diccionario inverso (de zorgiano a español), creado con comprensión de diccionarios
ALFABETO_INVERSO = {zorg: letra for letra, zorg in ALFABETO_ZORG.items()}

MENSAJES_SECRETOS = [
    "venimos en paz",
    "traigan tacos",
    "su wifi es muy lento",
    "llevennos con su lider",
    "nos gusta la musica de la tierra",
]

ESPECIES = [
    {"nombre": "Zorgianos", "planeta": "Zorg-9", "peligro": 3, "come": "metal"},
    {"nombre": "Blorps", "planeta": "Gelatina Prime", "peligro": 1, "come": "chistes malos"},
    {"nombre": "Kraxxianos", "planeta": "Kraxx", "peligro": 5, "come": "satélites"},
    {"nombre": "Mininautas", "planeta": "Michi-7", "peligro": 2, "come": "atún espacial"},
]


# -------------------------------------------------
# 2. CLASES
# -------------------------------------------------
class Nave:
    """Una nave espacial con energía y un ataque."""

    def __init__(self, nombre, energia, ataque_min, ataque_max):
        self.nombre = nombre
        self.energia = energia
        self.energia_max = energia
        self.ataque_min = ataque_min
        self.ataque_max = ataque_max

    def esta_viva(self):
        return self.energia > 0

    def recibir_danio(self, cantidad):
        self.energia = max(0, self.energia - cantidad)

    def atacar(self, otra_nave):
        danio = random.randint(self.ataque_min, self.ataque_max)
        otra_nave.recibir_danio(danio)
        return danio

    def barra_energia(self):
        bloques = round(10 * self.energia / self.energia_max)
        return "█" * bloques + "░" * (10 - bloques)

    def __str__(self):
        return f"{self.nombre:<16} [{self.barra_energia()}] {self.energia}/{self.energia_max}"


# -------------------------------------------------
# 3. FUNCIONES
# -------------------------------------------------
def banner():
    print(r"""
              .     *        .        *
         *         ___         .
            .  ___/   \___  *      👽 ¡ALERTA!
         *    /___________\     Naves no identificadas
       .        \_/ \_/ \_/       sobre la Tierra
          *       |  |  |    .
                 \|/\|/\|/
    """)


def pedir_numero(mensaje, minimo, maximo):
    """Pide un entero en un rango sin que el programa truene."""
    while True:
        try:
            valor = int(input(mensaje))
            if minimo <= valor <= maximo:
                return valor
            print(f"  ⚠️  Escribe un número entre {minimo} y {maximo}.")
        except ValueError:
            print("  ⚠️  Eso no es un número, terrícola.")


def traducir_a_zorg(texto):
    """Cambia letras según ALFABETO_ZORG y voltea cada palabra."""
    letras = [ALFABETO_ZORG.get(c, c) for c in texto.lower()]
    palabras = "".join(letras).split()
    return " ".join(palabra[::-1] for palabra in palabras)


def traducir_de_zorg(texto):
    """Hace el proceso inverso de traducir_a_zorg."""
    palabras = [palabra[::-1] for palabra in texto.split()]
    return "".join(ALFABETO_INVERSO.get(c, c) for c in " ".join(palabras))


def traductor():
    print("\n📡 TRADUCTOR UNIVERSAL ESPAÑOL ⇄ ZORGIANO")
    print("  1) Español → Zorgiano\n  2) Zorgiano → Español")
    opcion = pedir_numero("Elige: ", 1, 2)
    texto = input("Escribe el mensaje: ")
    if opcion == 1:
        print(f"  👽 {traducir_a_zorg(texto)}\n")
    else:
        print(f"  🧑 {traducir_de_zorg(texto)}\n")


def cifrado_cesar(texto, desplazamiento):
    """Recorre cada letra del alfabeto 'desplazamiento' posiciones."""
    resultado = ""
    for c in texto:
        if c.isalpha():
            resultado += chr((ord(c) - ord("a") + desplazamiento) % 26 + ord("a"))
        else:
            resultado += c
    return resultado


def descifrar_mensaje():
    """Mini-juego: hay que encontrar la clave del cifrado César."""
    original = random.choice(MENSAJES_SECRETOS)
    clave = random.randint(1, 25)
    cifrado = cifrado_cesar(original, clave)

    print("\n🔐 INTERCEPTAMOS UNA TRANSMISIÓN ALIENÍGENA:")
    print(f"   «{cifrado}»")
    print("Está cifrada con César. Prueba claves del 1 al 25 para descifrarla.")

    for intento in range(1, 6):
        prueba = pedir_numero(f"  Intento {intento}/5 - clave: ", 1, 25)
        descifrado = cifrado_cesar(cifrado, -prueba)
        print(f"   → «{descifrado}»")
        if prueba == clave:
            print("  🎉 ¡Mensaje descifrado! La humanidad te lo agradece.\n")
            return True
        pista = "mayor" if prueba < clave else "menor"
        print(f"  📡 Ruido... la clave es {pista}.")

    print(f"  💥 Se perdió la señal. La clave era {clave}: «{original}»\n")
    return False


def batalla():
    """Batalla por turnos contra la nave nodriza."""
    jugador = Nave("Halcón Terrícola", 100, 8, 18)
    enemigo = Nave("Nave Nodriza", 120, 6, 15)
    reparaciones = 2

    print("\n⚔️  ¡LA NAVE NODRIZA ATACA!\n")
    while jugador.esta_viva() and enemigo.esta_viva():
        print(jugador)
        print(enemigo)
        print(f"  1) Disparar láser  2) Reparar nave ({reparaciones} restantes)  3) Rayo arriesgado")
        accion = pedir_numero("¿Qué haces? ", 1, 3)

        if accion == 1:
            danio = jugador.atacar(enemigo)
            print(f"  🔫 Disparaste y causaste {danio} de daño.")
        elif accion == 2 and reparaciones > 0:
            jugador.energia = min(jugador.energia_max, jugador.energia + 25)
            reparaciones -= 1
            print("  🔧 Reparaste 25 de energía.")
        elif accion == 2:
            print("  🔧 ¡Ya no tienes kits de reparación! Pierdes el turno.")
        else:
            if random.random() < 0.4:
                enemigo.recibir_danio(40)
                print("  ⚡ ¡RAYO CRÍTICO! 40 de daño.")
            else:
                print("  💨 El rayo falló...")

        if enemigo.esta_viva():
            danio = enemigo.atacar(jugador)
            print(f"  👾 La nave nodriza te disparó: -{danio}.\n")

    if jugador.esta_viva():
        print("\n🌍 ¡VICTORIA! Los aliens huyen y dejan atrás su receta de tacos lunares.\n")
    else:
        print("\n🛸 Derrota... Ahora la Tierra es un parque temático zorgiano.\n")


def catalogo_especies():
    """Muestra las especies y permite filtrar por nivel de peligro."""
    print("\n📚 CATÁLOGO DE ESPECIES CONOCIDAS")
    minimo = pedir_numero("Mostrar especies con peligro mínimo (1-5): ", 1, 5)
    filtradas = [e for e in ESPECIES if e["peligro"] >= minimo]
    filtradas.sort(key=lambda e: e["peligro"], reverse=True)

    if not filtradas:
        print("  Ninguna especie es tan peligrosa. Por ahora... 👀\n")
        return
    for e in filtradas:
        calaveras = "💀" * e["peligro"]
        print(f"  {e['nombre']:<12} | {e['planeta']:<15} | {calaveras:<5} | come {e['come']}")
    print()


def menu():
    banner()
    opciones = {
        1: ("Traductor zorgiano", traductor),
        2: ("Descifrar transmisión", descifrar_mensaje),
        3: ("Batalla contra la nave nodriza", batalla),
        4: ("Catálogo de especies", catalogo_especies),
    }
    while True:
        print("=== CENTRO DE MANDO ===")
        for num, (texto, _) in opciones.items():
            print(f"  {num}) {texto}")
        print("  0) Salir")
        eleccion = pedir_numero("Elige: ", 0, len(opciones))
        if eleccion == 0:
            print("\n👽 Nanu nanu, terrícola. ¡Hasta la próxima!\n")
            break
        opciones[eleccion][1]()


# -------------------------------------------------
# 4. RETOS PARA PRACTICAR (¡modifica el código!)
# -------------------------------------------------
# 🥉 Reto 1: Agrega 2 especies nuevas al catálogo y 2 mensajes secretos más.
# 🥉 Reto 2: Agrega más letras a ALFABETO_ZORG (por ejemplo "m", "p", "d").
# 🥈 Reto 3: En el catálogo, permite buscar una especie por nombre o planeta.
# 🥈 Reto 4: Agrega un atributo "escudo" a la clase Nave que reduzca el
#            daño recibido a la mitad durante un turno.
# 🥇 Reto 5: Crea una subclase NaveNodriza(Nave) con un ataque especial que
#            se active cuando su energía baje del 30%.
# 🏆 Reto 6: Haz un "descifrador automático" que pruebe las 25 claves de César
#            y detecte cuál produce palabras en español (pista: busca palabras
#            comunes como "la", "de", "en", "su").

if __name__ == "__main__":
    menu()
