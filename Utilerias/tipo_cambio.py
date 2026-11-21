"""
=====================================================
  TIPO DE CAMBIO DEL DÓLAR 💵 → 🇲🇽
  Precio de hoy + histórico, estadísticas y gráfica
=====================================================

Fuentes de datos:
  - Frankfurter (por defecto): gratis, sin registro. Usa datos del
    Banco Central Europeo, se publican en días hábiles.
  - Banxico (opcional): tipo de cambio FIX oficial de México (serie SF43718).
    Necesitas un token gratuito:
    https://www.banxico.org.mx/SieAPIRest/service/v1/token
    Luego guárdalo en la variable de entorno BANXICO_TOKEN
    o pásalo con --token.

Solo usa librerías estándar de Python. La gráfica en imagen (--grafica)
necesita matplotlib:  pip install matplotlib

Ejemplos:
  python tipo_cambio_dolar.py                     # hoy + últimos 30 días
  python tipo_cambio_dolar.py --dias 365          # último año
  python tipo_cambio_dolar.py --desde 2024-01-01 --hasta 2024-12-31
  python tipo_cambio_dolar.py --moneda EUR        # dólar contra euro
  python tipo_cambio_dolar.py --fuente banxico    # FIX oficial de Banxico
  python tipo_cambio_dolar.py --csv historico.csv --grafica
"""

import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta

URL_FRANKFURTER = "https://api.frankfurter.dev/v1"
URL_BANXICO = "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos"


# -------------------------------------------------
# 1. DESCARGA DE DATOS
# -------------------------------------------------
def descargar_json(url, encabezados=None):
    peticion = urllib.request.Request(url, headers={"User-Agent": "tipo-cambio-py",
                                                    **(encabezados or {})})
    try:
        with urllib.request.urlopen(peticion, timeout=20) as respuesta:
            return json.loads(respuesta.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        sys.exit(f"❌ El servidor respondió con error {e.code}. Revisa las fechas o el token.")
    except urllib.error.URLError as e:
        sys.exit(f"❌ No hay conexión con el servidor: {e.reason}")


def historico_frankfurter(desde, hasta, moneda):
    """Regresa una lista de (fecha, tipo_de_cambio) ordenada."""
    url = f"{URL_FRANKFURTER}/{desde}..{hasta}?base=USD&symbols={moneda}"
    datos = descargar_json(url)
    return sorted((datetime.strptime(f, "%Y-%m-%d").date(), tasas[moneda])
                  for f, tasas in datos.get("rates", {}).items() if moneda in tasas)


def hoy_frankfurter(moneda):
    datos = descargar_json(f"{URL_FRANKFURTER}/latest?base=USD&symbols={moneda}")
    return datetime.strptime(datos["date"], "%Y-%m-%d").date(), datos["rates"][moneda]


def historico_banxico(desde, hasta, token):
    """FIX de Banxico. Las fechas vienen como dd/mm/aaaa y el valor como texto."""
    datos = descargar_json(f"{URL_BANXICO}/{desde}/{hasta}", {"Bmx-Token": token})
    registros = datos["bmx"]["series"][0].get("datos", [])
    resultado = []
    for r in registros:
        try:   # Banxico pone "N/E" en días sin dato
            resultado.append((datetime.strptime(r["fecha"], "%d/%m/%Y").date(),
                              float(r["dato"].replace(",", ""))))
        except ValueError:
            continue
    return sorted(resultado)


def hoy_banxico(token):
    datos = descargar_json(f"{URL_BANXICO}/oportuno", {"Bmx-Token": token})
    r = datos["bmx"]["series"][0]["datos"][0]
    return datetime.strptime(r["fecha"], "%d/%m/%Y").date(), float(r["dato"].replace(",", ""))


# -------------------------------------------------
# 2. ANÁLISIS Y PRESENTACIÓN
# -------------------------------------------------
def sparkline(valores):
    """Mini gráfica de una línea:  ▁▂▄▆█▇▅"""
    barras = "▁▂▃▄▅▆▇█"
    minimo, maximo = min(valores), max(valores)
    rango = (maximo - minimo) or 1
    return "".join(barras[int((v - minimo) / rango * (len(barras) - 1))] for v in valores)


def muestrear(lista, maximo):
    """Si hay muchos puntos, toma 'maximo' repartidos de forma pareja (incluye el último)."""
    if len(lista) <= maximo:
        return lista
    paso = (len(lista) - 1) / (maximo - 1)
    return [lista[round(i * paso)] for i in range(maximo)]


def mostrar_reporte(fecha_hoy, valor_hoy, historico, moneda, fuente):
    print("\n" + "=" * 52)
    print(f"  💵 TIPO DE CAMBIO USD → {moneda}   ({fuente})")
    print("=" * 52)
    print(f"\n  HOY ({fecha_hoy:%d/%m/%Y}):  1 USD = {valor_hoy:,.4f} {moneda}")

    if len(historico) < 2:
        print("\n  (No hay suficientes datos históricos en ese rango.)\n")
        return

    valores = [v for _, v in historico]
    (f_ini, v_ini), (f_fin, v_fin) = historico[0], historico[-1]
    f_min, v_min = min(historico, key=lambda x: x[1])
    f_max, v_max = max(historico, key=lambda x: x[1])
    cambio = v_fin - v_ini
    cambio_pct = cambio / v_ini * 100
    flecha = "📈 subió" if cambio > 0 else "📉 bajó" if cambio < 0 else "➡️  se mantuvo"

    print(f"\n  HISTÓRICO {f_ini:%d/%m/%Y} → {f_fin:%d/%m/%Y}  ({len(historico)} días con dato)")
    print(f"  {sparkline([v for _, v in muestrear(historico, 50)])}")
    print(f"\n  Mínimo:    {v_min:,.4f}  ({f_min:%d/%m/%Y})")
    print(f"  Máximo:    {v_max:,.4f}  ({f_max:%d/%m/%Y})")
    print(f"  Promedio:  {sum(valores) / len(valores):,.4f}")
    print(f"  Variación: {cambio:+,.4f} ({cambio_pct:+.2f}%)  → el dólar {flecha}")

    print("\n  FECHA        TIPO DE CAMBIO")
    print("  " + "-" * 40)
    for f, v in muestrear(historico, 15):
        barra = "█" * max(1, int((v - v_min) / ((v_max - v_min) or 1) * 20))
        print(f"  {f:%d/%m/%Y}   {v:>10,.4f}  {barra}")
    print()


def guardar_csv(historico, ruta, moneda):
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["fecha", f"USD_{moneda}"])
        for f, v in historico:
            escritor.writerow([f.isoformat(), v])
    print(f"💾 Histórico guardado en {ruta}")


def guardar_grafica(historico, moneda, fuente, ruta="tipo_cambio.png"):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("⚠️  Para la gráfica instala matplotlib:  pip install matplotlib")
        return
    fechas, valores = zip(*historico)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(fechas, valores, color="#1a7f37", linewidth=2)
    ax.fill_between(fechas, valores, min(valores), alpha=0.15, color="#1a7f37")
    ax.set_title(f"Tipo de cambio USD → {moneda} ({fuente})")
    ax.set_ylabel(f"{moneda} por 1 USD")
    ax.grid(alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(ruta, dpi=120)
    print(f"🖼️  Gráfica guardada en {ruta}")


# -------------------------------------------------
# 3. PROGRAMA PRINCIPAL
# -------------------------------------------------
def main():
    p = argparse.ArgumentParser(description="Tipo de cambio del dólar: hoy e histórico.")
    p.add_argument("--dias", type=int, default=30, help="Días hacia atrás (default 30)")
    p.add_argument("--desde", help="Fecha inicial AAAA-MM-DD")
    p.add_argument("--hasta", help="Fecha final AAAA-MM-DD (default hoy)")
    p.add_argument("--moneda", default="MXN", help="Moneda destino (default MXN). Solo Frankfurter")
    p.add_argument("--fuente", choices=["frankfurter", "banxico"], default="frankfurter")
    p.add_argument("--token", default=os.environ.get("BANXICO_TOKEN"), help="Token de Banxico")
    p.add_argument("--csv", help="Guardar histórico en un archivo CSV")
    p.add_argument("--grafica", action="store_true", help="Guardar gráfica PNG (requiere matplotlib)")
    args = p.parse_args()

    try:
        hasta = date.fromisoformat(args.hasta) if args.hasta else date.today()
        desde = date.fromisoformat(args.desde) if args.desde else hasta - timedelta(days=args.dias)
    except ValueError:
        sys.exit("❌ Usa fechas con formato AAAA-MM-DD, por ejemplo 2024-03-15")
    if desde > hasta:
        sys.exit("❌ La fecha --desde debe ser anterior a --hasta")

    moneda = args.moneda.upper()
    print("⏳ Consultando...")

    if args.fuente == "banxico":
        if not args.token:
            sys.exit("❌ Banxico requiere token: usa --token o la variable BANXICO_TOKEN.\n"
                     "   Pídelo gratis en https://www.banxico.org.mx/SieAPIRest/service/v1/token")
        moneda, nombre_fuente = "MXN", "Banxico FIX"
        fecha_hoy, valor_hoy = hoy_banxico(args.token)
        historico = historico_banxico(desde, hasta, args.token)
    else:
        nombre_fuente = "Frankfurter / BCE"
        fecha_hoy, valor_hoy = hoy_frankfurter(moneda)
        historico = historico_frankfurter(desde, hasta, moneda)

    mostrar_reporte(fecha_hoy, valor_hoy, historico, moneda, nombre_fuente)

    if args.csv and historico:
        guardar_csv(historico, args.csv, moneda)
    if args.grafica and len(historico) >= 2:
        guardar_grafica(historico, moneda, nombre_fuente)


if __name__ == "__main__":
    main()
