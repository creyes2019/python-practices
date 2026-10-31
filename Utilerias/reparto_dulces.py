"""
🍬 REPARTO DE DULCES DE HALLOWEEN 🍬
Ejercicio corto: input(), int(), división entera (//), módulo (%), for y if.
"""

dulces = int(input("¿Cuántos dulces juntaste? 🎃 "))
amigos = int(input("¿Entre cuántos amigos los vas a repartir? 👻 "))

if amigos <= 0:
    print("¡Necesitas al menos un amigo! 🕸️")
else:
    por_amigo = dulces // amigos   # división entera
    sobran = dulces % amigos       # lo que sobra

    print(f"\nCada amigo recibe {por_amigo} dulces:")
    for i in range(1, amigos + 1):
        print(f"  Amigo {i}: " + "🍬" * por_amigo)

    if sobran == 0:
        print("\n¡Reparto perfecto, no sobró nada! 🎉")
    else:
        print(f"\nSobran {sobran} dulce(s)... ¡se los queda el fantasma! 👻")
