"""
=====================================================================
  🐍  RETOS DE PYTHON PARA PRINCIPIANTES  🐍
=====================================================================

¿CÓMO FUNCIONA?
  1. Cada reto es una función. Borra la palabra `pass` y escribe tu
     código en su lugar.
  2. Usa `return` para devolver el resultado (¡no `print`!).
  3. Guarda el archivo y ejecútalo en la terminal:

         python retos.py        -> revisa TODOS los retos
         python retos.py 2      -> revisa solo el BLOQUE 2

  4. Verás:  ✅ correcto   ❌ incorrecto   ⏳ pendiente   💥 error

PLAN DE LA CLASE (3 horas aprox.)
  Bloque 1 · Variables y operaciones ........ 25 min
  Bloque 2 · Condicionales (if / elif / else)  30 min
  Bloque 3 · Bucles (for / while) ........... 35 min
  ☕ Descanso ................................ 10 min
  Bloque 4 · Listas y textos ................ 35 min
  Bloque 5 · Diccionarios ................... 25 min
  Bloque 6 · Reto final + juego bonus ....... 20 min

¡Que no te dé miedo equivocarte! Los errores también enseñan. 💪
=====================================================================
"""


# =====================================================================
#  BLOQUE 1 · VARIABLES Y OPERACIONES
# =====================================================================

def saludar(nombre):
    """
    Reto 1.1 ⭐
    Devuelve un saludo personalizado.
        saludar("Ana")  ->  "Hola, Ana!"
    Pista: puedes unir textos con +  o usar f-strings: f"Hola, {nombre}!"
    """
    pass


def area_rectangulo(base, altura):
    """
    Reto 1.2 ⭐
    Devuelve el área de un rectángulo (base por altura).
        area_rectangulo(4, 5)  ->  20
    """
    pass


def celsius_a_fahrenheit(celsius):
    """
    Reto 1.3 ⭐
    Convierte grados Celsius a Fahrenheit.
    Fórmula:  F = C * 9 / 5 + 32
        celsius_a_fahrenheit(100)  ->  212.0
    """
    pass


def convertir_segundos(segundos):
    """
    Reto 1.4 ⭐⭐
    Convierte segundos a un texto con minutos y segundos.
        convertir_segundos(125)  ->  "2 min 5 s"
    Pista: //  da la división entera y  %  da el residuo.
           125 // 60 = 2      125 % 60 = 5
    """
    pass


# =====================================================================
#  BLOQUE 2 · CONDICIONALES
# =====================================================================

def es_par(numero):
    """
    Reto 2.1 ⭐
    Devuelve True si el número es par y False si es impar.
        es_par(4)  ->  True
        es_par(7)  ->  False
    Pista: un número es par si  numero % 2 == 0
    """
    pass


def mayor_de_tres(a, b, c):
    """
    Reto 2.2 ⭐⭐
    Devuelve el mayor de tres números. ¡Sin usar max()!
        mayor_de_tres(3, 9, 5)  ->  9
    """
    pass


def calificacion(nota):
    """
    Reto 2.3 ⭐⭐
    Recibe una nota de 0 a 100 y devuelve un texto:
        90 o más   -> "Excelente"
        70 a 89    -> "Aprobado"
        menos de 70 -> "Reprobado"
    Usa if / elif / else.
    """
    pass


def es_bisiesto(anio):
    """
    Reto 2.4 ⭐⭐⭐
    Un año es bisiesto si:
      - es divisible entre 4,
      - EXCEPTO si es divisible entre 100,
      - PERO sí lo es si es divisible entre 400.
        es_bisiesto(2024) -> True
        es_bisiesto(1900) -> False
        es_bisiesto(2000) -> True
    Pista: combina condiciones con  and  /  or  /  not
    """
    pass


# =====================================================================
#  BLOQUE 3 · BUCLES
# =====================================================================

def suma_hasta(n):
    """
    Reto 3.1 ⭐
    Devuelve la suma de todos los números del 1 al n.
        suma_hasta(5)  ->  15      (1 + 2 + 3 + 4 + 5)
    Pista: for i in range(1, n + 1):
    """
    pass


def tabla_multiplicar(n):
    """
    Reto 3.2 ⭐⭐
    Devuelve una lista con la tabla de multiplicar de n, del 1 al 10.
        tabla_multiplicar(3)  ->  [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
    Pista: crea una lista vacía  resultado = []  y usa  .append()
    """
    pass


def contar_vocales(texto):
    """
    Reto 3.3 ⭐⭐
    Cuenta cuántas vocales (a, e, i, o, u) hay en el texto.
    Deben contar también las MAYÚSCULAS.
        contar_vocales("Hola Mundo")  ->  4
    Pista: puedes recorrer un texto letra por letra con un for.
           texto.lower() convierte todo a minúsculas.
    """
    pass


def fizzbuzz(n):
    """
    Reto 3.4 ⭐⭐⭐  (¡un clásico de entrevistas de trabajo!)
    Devuelve una lista con los números del 1 al n, pero:
      - si el número es múltiplo de 3 y de 5 -> "FizzBuzz"
      - si solo es múltiplo de 3            -> "Fizz"
      - si solo es múltiplo de 5            -> "Buzz"
      - si no, el número tal cual
        fizzbuzz(5)  ->  [1, 2, "Fizz", 4, "Buzz"]
    Pista: ¿en qué orden conviene revisar las condiciones?
    """
    pass


# =====================================================================
#  BLOQUE 4 · LISTAS Y TEXTOS
# =====================================================================

def promedio(numeros):
    """
    Reto 4.1 ⭐
    Devuelve el promedio de una lista de números.
        promedio([8, 9, 10])  ->  9.0
    Pista: sum() y len() son tus amigos.
    """
    pass


def maximo(numeros):
    """
    Reto 4.2 ⭐⭐
    Devuelve el número más grande de la lista. ¡Sin usar max()!
        maximo([4, 17, 2, 9])  ->  17
    Pista: guarda el primero como "el mayor hasta ahora" y compara.
    """
    pass


def filtrar_pares(numeros):
    """
    Reto 4.3 ⭐⭐
    Devuelve una lista NUEVA solo con los números pares.
        filtrar_pares([1, 2, 3, 4, 5, 6])  ->  [2, 4, 6]
    Bonus: ¿puedes reutilizar tu función es_par()?
    """
    pass


def invertir_texto(texto):
    """
    Reto 4.4 ⭐⭐
    Devuelve el texto al revés.
        invertir_texto("python")  ->  "nohtyp"
    Pista: hay un truco con corchetes: texto[::-1]
           ...pero inténtalo primero con un bucle.
    """
    pass


def es_palindromo(texto):
    """
    Reto 4.5 ⭐⭐⭐
    Un palíndromo se lee igual al derecho y al revés.
    Ignora mayúsculas y espacios.
        es_palindromo("Anita lava la tina")  ->  True
        es_palindromo("Python")              ->  False
    Pista: texto.replace(" ", "") quita los espacios.
    """
    pass


# =====================================================================
#  BLOQUE 5 · DICCIONARIOS
# =====================================================================

def precio_total(carrito, precios):
    """
    Reto 5.1 ⭐⭐
    `carrito` es una lista de productos y `precios` un diccionario.
    Devuelve cuánto hay que pagar.
        carrito = ["pan", "leche", "pan"]
        precios = {"pan": 5, "leche": 20}
        precio_total(carrito, precios)  ->  30
    Pista: precios["pan"] te da 5
    """
    pass


def contar_palabras(frase):
    """
    Reto 5.2 ⭐⭐⭐
    Devuelve un diccionario con cuántas veces aparece cada palabra
    (en minúsculas).
        contar_palabras("el gato y el perro")
            ->  {"el": 2, "gato": 1, "y": 1, "perro": 1}
    Pista: frase.split() separa la frase en una lista de palabras.
           Revisa si la palabra ya existe con:  if palabra in conteo:
    """
    pass


# =====================================================================
#  BLOQUE 6 · RETO FINAL 🏆
# =====================================================================

def contrasena_segura(contrasena):
    """
    Reto 6.1 ⭐⭐⭐⭐
    Devuelve True si la contraseña es segura. Para serlo, debe:
      - tener al menos 8 caracteres
      - tener al menos una MAYÚSCULA
      - tener al menos una minúscula
      - tener al menos un número
        contrasena_segura("Python2026")  ->  True
        contrasena_segura("python")      ->  False
    Pista: letra.isupper(), letra.islower(), letra.isdigit()
    """
    pass


def adivina_el_numero():
    """
    🎮 BONUS (no se verifica automáticamente: ¡se juega!)
    Programa el juego "Adivina el número":
      1. La computadora elige un número al azar del 1 al 100.
      2. El jugador escribe un número con input().
      3. El programa responde "Más alto" o "Más bajo".
      4. Se repite hasta que adivine. Al final muestra cuántos
         intentos le tomó.
    Pistas:
      import random
      secreto = random.randint(1, 100)
      intento = int(input("Tu número: "))
    Para jugar:  python retos.py jugar
    """
    pass


# =====================================================================
#  ⚠️  VERIFICADOR AUTOMÁTICO — No hace falta modificar nada de aquí abajo
# =====================================================================

PRUEBAS = {
    1: ("Variables y operaciones", [
        ("saludar", ("Ana",), "Hola, Ana!"),
        ("saludar", ("Luis",), "Hola, Luis!"),
        ("area_rectangulo", (4, 5), 20),
        ("area_rectangulo", (3, 3), 9),
        ("celsius_a_fahrenheit", (100,), 212),
        ("celsius_a_fahrenheit", (0,), 32),
        ("convertir_segundos", (125,), "2 min 5 s"),
        ("convertir_segundos", (60,), "1 min 0 s"),
    ]),
    2: ("Condicionales", [
        ("es_par", (4,), True),
        ("es_par", (7,), False),
        ("mayor_de_tres", (3, 9, 5), 9),
        ("mayor_de_tres", (10, 2, 8), 10),
        ("mayor_de_tres", (1, 2, 30), 30),
        ("calificacion", (95,), "Excelente"),
        ("calificacion", (70,), "Aprobado"),
        ("calificacion", (69,), "Reprobado"),
        ("es_bisiesto", (2024,), True),
        ("es_bisiesto", (1900,), False),
        ("es_bisiesto", (2000,), True),
        ("es_bisiesto", (2023,), False),
    ]),
    3: ("Bucles", [
        ("suma_hasta", (5,), 15),
        ("suma_hasta", (100,), 5050),
        ("tabla_multiplicar", (3,), [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]),
        ("contar_vocales", ("Hola Mundo",), 4),
        ("contar_vocales", ("AEIOU xyz",), 5),
        ("fizzbuzz", (5,), [1, 2, "Fizz", 4, "Buzz"]),
        ("fizzbuzz", (15,), [1, 2, "Fizz", 4, "Buzz", "Fizz", 7, 8, "Fizz",
                             "Buzz", 11, "Fizz", 13, 14, "FizzBuzz"]),
    ]),
    4: ("Listas y textos", [
        ("promedio", ([8, 9, 10],), 9),
        ("promedio", ([5, 6],), 5.5),
        ("maximo", ([4, 17, 2, 9],), 17),
        ("maximo", ([-5, -2, -9],), -2),
        ("filtrar_pares", ([1, 2, 3, 4, 5, 6],), [2, 4, 6]),
        ("filtrar_pares", ([1, 3, 5],), []),
        ("invertir_texto", ("python",), "nohtyp"),
        ("es_palindromo", ("Anita lava la tina",), True),
        ("es_palindromo", ("Python",), False),
    ]),
    5: ("Diccionarios", [
        ("precio_total", (["pan", "leche", "pan"], {"pan": 5, "leche": 20}), 30),
        ("precio_total", ([], {"pan": 5}), 0),
        ("contar_palabras", ("el gato y el perro",),
         {"el": 2, "gato": 1, "y": 1, "perro": 1}),
        ("contar_palabras", ("Hola hola HOLA",), {"hola": 3}),
    ]),
    6: ("Reto final", [
        ("contrasena_segura", ("Python2026",), True),
        ("contrasena_segura", ("python",), False),
        ("contrasena_segura", ("PYTHON2026",), False),
        ("contrasena_segura", ("Python",), False),
        ("contrasena_segura", ("Pyt2",), False),
    ]),
}


def _iguales(obtenido, esperado):
    # Permite 212 == 212.0 y pequeñas diferencias de decimales
    if isinstance(esperado, (int, float)) and not isinstance(esperado, bool):
        if isinstance(obtenido, bool) or not isinstance(obtenido, (int, float)):
            return False
        return abs(obtenido - esperado) < 1e-9
    return obtenido == esperado


def verificar(funciones, bloque=None):
    bloques = [bloque] if bloque else sorted(PRUEBAS)
    total = correctas = 0
    estado_por_reto = {}

    for b in bloques:
        titulo, pruebas = PRUEBAS[b]
        print(f"\n━━━ BLOQUE {b} · {titulo} ━━━")
        for nombre, args, esperado in pruebas:
            total += 1
            funcion = funciones.get(nombre)
            llamada = f"{nombre}({', '.join(repr(a) for a in args)})"
            try:
                obtenido = funcion(*args)
            except Exception as e:
                print(f"  💥 {llamada}  ->  error: {type(e).__name__}: {e}")
                estado_por_reto[nombre] = False
                continue
            if obtenido is None and esperado is not None:
                print(f"  ⏳ {llamada}  ->  pendiente (¿olvidaste el return?)")
                estado_por_reto.setdefault(nombre, False)
            elif _iguales(obtenido, esperado):
                print(f"  ✅ {llamada}  ->  {obtenido!r}")
                correctas += 1
                estado_por_reto.setdefault(nombre, True)
            else:
                print(f"  ❌ {llamada}  ->  obtuve {obtenido!r}, esperaba {esperado!r}")
                estado_por_reto[nombre] = False

    retos_ok = sum(estado_por_reto.values())
    print("\n" + "═" * 55)
    print(f"  Pruebas superadas: {correctas}/{total}")
    print(f"  Retos completados: {retos_ok}/{len(estado_por_reto)}")
    barra = int(20 * correctas / total) if total else 0
    print(f"  [{'█' * barra}{'░' * (20 - barra)}] {100 * correctas // total}%")
    if correctas == total:
        print("  🏆 ¡INCREÍBLE! Completaste todos los retos. 🎉")
    print("═" * 55)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "jugar":
        adivina_el_numero()
    elif len(sys.argv) > 1 and sys.argv[1].isdigit() and int(sys.argv[1]) in PRUEBAS:
        verificar(globals(), int(sys.argv[1]))
    else:
        verificar(globals())