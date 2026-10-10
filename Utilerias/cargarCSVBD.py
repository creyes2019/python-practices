"""
cargarCSVBD.py
==============
Carga los datos de un archivo CSV a una tabla de MySQL.

¿Qué hace?
    1. Se conecta al servidor MySQL y crea la base de datos si no existe.
    2. Lee el CSV con pandas y lo convierte en un DataFrame (una "tabla en memoria").
    3. Envía el DataFrame a MySQL con to_sql(). Si la tabla no existe, pandas la
       crea solo, eligiendo el tipo de cada columna según los datos:
           enteros  -> BIGINT
           decimales -> DOUBLE
           texto    -> TEXT
           fechas   -> DATETIME
    4. Si la tabla es nueva y tiene columna "id", la convierte en llave primaria.

Librerías que usa:
    - pandas:     lee el CSV y escribe en la base de datos.
    - SQLAlchemy: administra la conexión a la base (pandas la necesita para to_sql).
    - PyMySQL:    el "driver", es decir, quien realmente habla con MySQL.
    - python-dotenv: lee el archivo .env con los datos de conexión.

Instalación:
    pip install pandas sqlalchemy pymysql python-dotenv

Configuración:
    Los datos de conexión (usuario, contraseña...) se leen del archivo .env
    que está en esta misma carpeta. Copia .env.example a .env y llena tus datos.

Uso:
    python cargarCSVBD.py                -> crea la tabla o agrega filas si ya existe
    python cargarCSVBD.py --reemplazar   -> borra la tabla y la vuelve a crear
"""
import argparse              # Para leer opciones de la línea de comandos (--reemplazar)
import os                    # Para leer variables de entorno (os.environ)
import sys                   # sys.exit() termina el programa mostrando un mensaje
from pathlib import Path     # Para manejar rutas de archivos sin importar el sistema operativo

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, inspect, text

# ---------------------------------------------------------------------------
# CARGAR EL ARCHIVO .env
# load_dotenv() lee el archivo .env y agrega cada línea CLAVE=valor a las
# variables de entorno del programa. Después las leemos con os.environ.get().
# Path(__file__).with_name(".env") apunta al .env que está junto a este
# script, así funciona aunque lo ejecutemos desde otra carpeta.
# ---------------------------------------------------------------------------
load_dotenv(Path(__file__).with_name(".env"))

# ---------------------------------------------------------------------------
# CONFIGURACIÓN
# Constantes en MAYÚSCULAS: por convención indican valores que no cambian
# durante la ejecución.
# Los datos de conexión vienen del .env, así la contraseña NO queda escrita
# en el código ni se sube al repositorio (el .env está en el .gitignore).
# os.environ.get(clave, valor_por_defecto): si la variable no existe en el .env,
# usa el valor por defecto. La contraseña no tiene valor por defecto: si falta,
# get() devuelve None y lo validamos más abajo.
# ---------------------------------------------------------------------------
USUARIO = os.environ.get("MYSQL_USER", "root")
PASSWORD = os.environ.get("MYSQL_PASSWORD")
HOST = os.environ.get("MYSQL_HOST", "localhost")         # Servidor de MySQL (localhost = esta computadora)
PUERTO = int(os.environ.get("MYSQL_PORT", "3306"))       # Puerto por defecto de MySQL; int() porque el .env guarda texto
BASE_DATOS = os.environ.get("MYSQL_DATABASE", "python_examples")

# Path(__file__).parent es la carpeta donde está este script.
# Así el CSV se encuentra aunque ejecutemos el script desde otra carpeta.
ARCHIVO_CSV = Path(__file__).parent / "clientes.csv"
TABLA = "clientes"


def cargar_csv(archivo_csv, tabla, engine, reemplazar=False):
    """
    Lee un CSV y guarda su contenido en una tabla de MySQL.

    Parámetros:
        archivo_csv: ruta del archivo CSV a cargar.
        tabla:       nombre de la tabla destino en MySQL.
        engine:      conexión a la base de datos (creada con create_engine).
        reemplazar:  si es True, borra la tabla y la crea de nuevo;
                     si es False (por defecto), agrega las filas al final.
    """
    # 1) LEER EL CSV
    # read_csv usa la primera fila como nombres de columna y devuelve un DataFrame.
    # encoding="utf-8" para que los acentos y la ñ se lean correctamente.
    df = pd.read_csv(archivo_csv, encoding="utf-8")

    # 2) CONVERTIR FECHAS
    # pandas lee las fechas del CSV como texto. Si no las convertimos,
    # MySQL crearía la columna como TEXT en lugar de DATETIME.
    # errors="coerce" convierte los valores inválidos en NaT (fecha vacía)
    # en lugar de detener el programa con un error.
    for col in df.columns:
        if "fecha" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # 3) REVISAR SI LA TABLA YA EXISTE
    # inspect() permite consultar la estructura de la base (tablas, columnas...).
    # Lo guardamos ANTES de cargar, para saber después si la tabla es nueva.
    existia = inspect(engine).has_table(tabla)

    # 4) CARGAR LOS DATOS
    # if_exists define qué hacer si la tabla ya existe:
    #   "append"  -> agrega las filas (si no existe, la crea)
    #   "replace" -> borra la tabla y la crea de nuevo
    #   "fail"    -> lanza un error (valor por defecto de pandas)
    # index=False: no guardar el índice del DataFrame (0, 1, 2...) como columna.
    # chunksize=1000: envía los datos en bloques de 1000 filas; útil con CSV grandes.
    modo = "replace" if reemplazar else "append"
    df.to_sql(tabla, engine, if_exists=modo, index=False, chunksize=1000)

    # 5) AGREGAR LLAVE PRIMARIA
    # to_sql crea la tabla sin llave primaria, así que la agregamos nosotros.
    # Solo se hace cuando la tabla es nueva; si ya existía, ya tiene su llave
    # y volver a agregarla daría error.
    creada = reemplazar or not existia
    if creada and "id" in df.columns:
        # engine.begin() abre una conexión con transacción: al salir del bloque
        # "with" hace COMMIT automáticamente (o ROLLBACK si hubo un error).
        # text() indica a SQLAlchemy que el texto es una instrucción SQL.
        # Las comillas invertidas `...` protegen nombres de tablas/columnas en MySQL.
        with engine.begin() as conn:
            conn.execute(text(f"ALTER TABLE `{tabla}` ADD PRIMARY KEY (`id`)"))

    # 6) MOSTRAR RESULTADO
    if reemplazar:
        accion = "reemplazó la tabla y se cargaron"
    elif existia:
        accion = "agregaron"
    else:
        accion = "creó la tabla y se cargaron"
    print(f"Se {accion} {len(df)} registros en '{tabla}'.")


# Este bloque solo se ejecuta cuando corremos el archivo directamente
# (python cargarCSVBD.py), no cuando otro script lo importa con "import".
if __name__ == "__main__":
    # LEER OPCIONES DE LA LÍNEA DE COMANDOS
    # action="store_true": si se escribe --reemplazar, vale True; si no, False.
    # También genera ayuda automática: python cargarCSVBD.py --help
    parser = argparse.ArgumentParser(description="Carga un CSV a una tabla MySQL.")
    parser.add_argument("--reemplazar", action="store_true",
                        help="Borra la tabla si existe y la vuelve a crear con los datos del CSV")
    args = parser.parse_args()

    # VALIDAR LA CONFIGURACIÓN
    # Revisamos antes de conectarnos, para dar un mensaje de error claro.
    if not PASSWORD:
        sys.exit("Error: define MYSQL_PASSWORD en el archivo .env.")

    # CREAR LA BASE DE DATOS SI NO EXISTE
    # Una cadena de conexión tiene el formato:
    #   dialecto+driver://usuario:contraseña@host:puerto/base_de_datos
    # En lugar de escribirla a mano, usamos URL.create(), que arma la cadena por
    # nosotros y escapa los caracteres especiales de la contraseña (@, :, /, #...),
    # que de otra forma romperían la URL.
    # Aquí NO indicamos base de datos, porque todavía puede no existir.
    # utf8mb4 es la codificación completa de UTF-8 en MySQL (acentos, ñ, emojis).
    url_servidor = URL.create(
        "mysql+pymysql",
        username=USUARIO,
        password=PASSWORD,
        host=HOST,
        port=PUERTO,
    )
    engine_srv = create_engine(url_servidor)
    with engine_srv.begin() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{BASE_DATOS}` CHARACTER SET utf8mb4"))
    engine_srv.dispose()  # Cierra las conexiones de este engine; ya no lo necesitamos

    # CONECTARSE A LA BASE DE DATOS
    # Ahora sí incluimos el nombre de la base. url.set() crea una copia de la URL
    # anterior cambiando solo lo indicado. query agrega "?charset=utf8mb4".
    # create_engine no se conecta todavía; la conexión se abre cuando se usa.
    url_base = url_servidor.set(database=BASE_DATOS, query={"charset": "utf8mb4"})
    engine = create_engine(url_base)

    # CARGAR EL CSV
    cargar_csv(ARCHIVO_CSV, TABLA, engine, reemplazar=args.reemplazar)
