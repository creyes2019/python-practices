"""
🎃 NOCHE DE BRUJAS EN PYTHON 🎃
Script de ejemplo para clase.

Conceptos que se practican:
  - Variables y tipos de datos
  - Listas y diccionarios
  - Funciones con parámetros y return
  - Condicionales (if / elif / else)
  - Ciclos (for / while)
  - Módulo random
  - Entrada del usuario con input()
"""

import random
import time

# ---------------------------------------------------------------
# 1. DATOS: listas y diccionarios
# ---------------------------------------------------------------
DULCES = ["chocolate 🍫", "paleta 🍭", "caramelo 🍬", "gomitas 🐛", "mazapán 🥜"]
TRUCOS = [
    "¡Un fantasma te jaló los calcetines! 👻",
    "¡Una araña cayó en tu cabeza! 🕷️",
    "¡Tu sombra se fue a pasear sin ti! 🌑",
    "¡Te convertiste en sapo por 5 segundos! 🐸",
]

# Diccionario: cada letra inicial tiene un monstruo
MONSTRUOS = {
    "A": "Araña", "B": "Bruja", "C": "Calavera", "D": "Drácula",
    "E": "Espectro", "F": "Fantasma", "G": "Gárgola", "H": "Hombre Lobo",
    "J": "Jinete Sin Cabeza", "L": "Llorona", "M": "Momia", "N": "Nahual",
    "Z": "Zombi",
}
ADJETIVOS = ["Tenebroso", "Pegajoso", "Dormilón", "Hambriento", "Bailarín", "Chimuelo"]


# ---------------------------------------------------------------
# 2. FUNCIONES
# ---------------------------------------------------------------
def escribir_lento(texto, pausa=0.03):
    """Imprime el texto letra por letra para dar suspenso."""
    for letra in texto:
        print(letra, end="", flush=True)
        time.sleep(pausa)
    print()


def dibujar_calabaza(ojos="^", boca="w"):
    """Dibuja una calabaza ASCII con los ojos y la boca que elija el usuario."""
    print(f"""
          ,
       .-'|'-.
     .'   |   '.
    /  {ojos}     {ojos}  \\
   |             |
   |    {boca}{boca}{boca}{boca}{boca}    |
    \\           /
     '._______.'
    """)


def dulce_o_truco():
    """Devuelve un dulce o un truco al azar (50% de probabilidad)."""
    if random.random() < 0.5:
        return "DULCE", random.choice(DULCES)
    else:
        return "TRUCO", random.choice(TRUCOS)


def nombre_de_monstruo(nombre):
    """Genera un nombre de monstruo usando la primera letra del nombre."""
    inicial = nombre.strip().upper()[0]
    monstruo = MONSTRUOS.get(inicial, "Criatura Misteriosa")  # valor por defecto
    adjetivo = random.choice(ADJETIVOS)
    return f"{monstruo} {adjetivo}"


def adivina_el_numero():
    """La bruja piensa un número del 1 al 20; tienes 5 intentos."""
    secreto = random.randint(1, 20)
    intentos = 5
    escribir_lento("🧙 La bruja pensó un número del 1 al 20... ¡Adivínalo!")

    while intentos > 0:
        respuesta = input(f"   Intentos restantes: {intentos}. Tu número: ")
        if not respuesta.isdigit():
            print("   ⚠️  Escribe solo números.")
            continue

        numero = int(respuesta)
        intentos -= 1

        if numero == secreto:
            escribir_lento("   🎉 ¡Correcto! La bruja te regala una escoba voladora 🧹")
            return True
        elif numero < secreto:
            print("   🔼 Más alto...")
        else:
            print("   🔽 Más bajo...")

    escribir_lento(f"   💀 ¡Se acabaron los intentos! Era el {secreto}. Ahora eres un sapo 🐸")
    return False


# ---------------------------------------------------------------
# 3. PROGRAMA PRINCIPAL (menú con while)
# ---------------------------------------------------------------
def main():
    bolsa = []  # aquí se guardan los dulces ganados

    escribir_lento("🦇🦇🦇  BIENVENIDO A LA NOCHE DE BRUJAS EN PYTHON  🦇🦇🦇")

    while True:
        print("\n========== MENÚ ==========")
        print("1. Dibujar mi calabaza 🎃")
        print("2. Tocar una puerta (¿dulce o truco?) 🚪")
        print("3. Descubrir mi nombre de monstruo 👹")
        print("4. Jugar con la bruja 🧙")
        print("5. Ver mi bolsa de dulces 🛍️")
        print("6. Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            ojos = input("¿Qué símbolo quieres para los ojos? (ej. ^, O, X): ") or "^"
            boca = input("¿Y para la boca? (ej. w, -, V): ") or "w"
            dibujar_calabaza(ojos[0], boca[0])

        elif opcion == "2":
            escribir_lento("Toc, toc... 🚪", 0.1)
            tipo, resultado = dulce_o_truco()
            if tipo == "DULCE":
                bolsa.append(resultado)
                print(f"🍬 ¡Dulce! Te dieron: {resultado}")
            else:
                print(f"😱 ¡Truco! {resultado}")

        elif opcion == "3":
            nombre = input("¿Cómo te llamas? ")
            if nombre.strip():
                escribir_lento(f"🌕 Esta noche serás... ¡{nombre_de_monstruo(nombre)}!")
            else:
                print("Necesito un nombre 👀")

        elif opcion == "4":
            if adivina_el_numero():
                bolsa.append("escoba voladora 🧹")

        elif opcion == "5":
            if len(bolsa) == 0:
                print("Tu bolsa está vacía... 🕸️")
            else:
                print(f"Tienes {len(bolsa)} premio(s):")
                for i, dulce in enumerate(bolsa, start=1):
                    print(f"  {i}. {dulce}")

        elif opcion == "6":
            escribir_lento(f"👻 ¡Feliz Halloween! Te llevas {len(bolsa)} premio(s). Buuuu...")
            break

        else:
            print("Opción no válida, intenta de nuevo.")


# Solo se ejecuta si corres este archivo directamente
if __name__ == "__main__":
    main()
