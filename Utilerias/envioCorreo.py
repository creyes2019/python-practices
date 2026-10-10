"""
envioCorreo.py
==============
Envía un correo de bienvenida con credenciales de acceso usando una cuenta de Gmail.

¿Qué hace?
    1. Lee las credenciales de Gmail desde un archivo .env (no se escriben en el código).
    2. Recibe por la línea de comandos a quién enviar el correo (--para, --nombre...).
    3. Si no se indica contraseña, genera una contraseña temporal segura.
    4. Arma el correo en dos versiones: texto plano y HTML (con estilos).
    5. Se conecta al servidor SMTP de Gmail de forma cifrada (SSL) y envía el correo.

¿Qué es SMTP?
    SMTP (Simple Mail Transfer Protocol) es el protocolo estándar para ENVIAR correos.
    Gmail ofrece un servidor SMTP (smtp.gmail.com) al que nos conectamos como si
    fuéramos un cliente de correo (Outlook, Thunderbird...).

Requisitos previos en la cuenta de Gmail:
    1. Activar la verificación en 2 pasos.
    2. Crear una "Contraseña de aplicación" en https://myaccount.google.com/apppasswords
       (Gmail ya no permite iniciar sesión por SMTP con la contraseña normal).

Librerías que usa:
    - smtplib, ssl, email: vienen incluidas con Python (librería estándar).
    - python-dotenv:       lee el archivo .env y carga sus valores como variables de entorno.

Instalación:
    pip install python-dotenv

Configuración:
    Copia .env.example a .env (en esta misma carpeta) y llena tus datos.

Uso:
    python envioCorreo.py --para mayaco9358@gmail.com --nombre "Ana López"
    python envioCorreo.py --para ana@ejemplo.com --nombre "Ana" --usuario ana.lopez --password Temp123!
"""
import argparse                         # Para leer opciones de la línea de comandos (--para, --nombre...)
import os                               # Para leer variables de entorno (os.environ)
import secrets                          # Genera valores aleatorios seguros (para contraseñas)
import smtplib                          # Cliente SMTP: se conecta al servidor de correo y envía
import ssl                              # Cifrado de la conexión (para que nadie lea la contraseña en la red)
import string                           # Conjuntos de caracteres listos: letras, dígitos...
import sys                              # sys.exit() termina el programa mostrando un mensaje
from email.message import EmailMessage  # Objeto que representa un correo (asunto, remitente, cuerpo...)
from pathlib import Path                # Para manejar rutas de archivos sin importar el sistema operativo

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# CARGAR EL ARCHIVO .env
# load_dotenv() lee el archivo .env y agrega cada línea CLAVE=valor a las
# variables de entorno del programa. Después las leemos con os.environ.get().
# Path(__file__).with_name(".env") apunta al .env que está junto a este
# script, así funciona aunque lo ejecutemos desde otra carpeta.
# ¿Por qué un .env? Para no escribir contraseñas en el código: el .env está
# en el .gitignore y nunca se sube al repositorio.
# ---------------------------------------------------------------------------
load_dotenv(Path(__file__).with_name(".env"))

# ---------------------------------------------------------------------------
# CONFIGURACIÓN
# Constantes en MAYÚSCULAS: por convención indican valores que no cambian
# durante la ejecución.
# ---------------------------------------------------------------------------
SMTP_SERVIDOR = "smtp.gmail.com"  # Servidor de correo saliente de Gmail
SMTP_PUERTO = 465                 # Puerto para SMTP con SSL (cifrado desde el inicio)
# os.environ.get(clave, valor_por_defecto): si la variable no existe en el .env,
# usa el valor por defecto en lugar de fallar.
NOMBRE_EMPRESA = os.environ.get("NOMBRE_EMPRESA", "DesarrolloHouse")


def generar_password_temporal(longitud=12):
    """
    Genera una contraseña temporal aleatoria y segura.

    Parámetros:
        longitud: número de caracteres de la contraseña (12 por defecto).

    Devuelve:
        Un texto (str) con la contraseña generada, por ejemplo "aT9#kP2!xQ7m".
    """
    # Juntamos todos los caracteres permitidos en un solo texto:
    # letras (a-z, A-Z) + dígitos (0-9) + algunos símbolos.
    alfabeto = string.ascii_letters + string.digits + "!@#$%&*?"

    # secrets.choice() elige un carácter al azar. Usamos "secrets" y NO "random"
    # porque random es predecible y no debe usarse para contraseñas.
    # "".join(...) une los caracteres elegidos en un solo texto.
    # El "_" en el for indica que no nos importa el número de vuelta.
    return "".join(secrets.choice(alfabeto) for _ in range(longitud))


def construir_mensaje(remitente, destinatario, nombre, usuario, password):
    """
    Arma el correo de bienvenida (encabezados + cuerpo).

    Parámetros:
        remitente:    correo de Gmail desde el que se envía.
        destinatario: correo de la persona que recibe la bienvenida.
        nombre:       nombre de la persona, para personalizar el saludo.
        usuario:      usuario de acceso que se le asigna.
        password:     contraseña temporal que se le asigna.

    Devuelve:
        Un objeto EmailMessage listo para enviarse.
    """
    # 1) ENCABEZADOS
    # Un EmailMessage funciona como un diccionario: cada clave es un encabezado.
    mensaje = EmailMessage()
    mensaje["Subject"] = f"¡Bienvenido(a) a {NOMBRE_EMPRESA}, {nombre}!"  # Asunto
    mensaje["From"] = f"{NOMBRE_EMPRESA} <{remitente}>"  # "Nombre <correo>" muestra un nombre bonito
    mensaje["To"] = destinatario

    # 2) CUERPO EN TEXTO PLANO
    # Los f-strings (f"...") reemplazan cada {variable} por su valor.
    # Las triples comillas permiten escribir texto de varias líneas.
    # Esta versión se muestra en clientes de correo que no soportan HTML.
    texto_plano = f"""Hola {nombre},

¡Te damos la bienvenida a {NOMBRE_EMPRESA}!

Estas son tus credenciales de acceso:
  Usuario: {usuario}
  Contraseña temporal: {password}

Por seguridad, te pedimos cambiar tu contraseña al iniciar sesión por primera vez.

Saludos,
El equipo de {NOMBRE_EMPRESA}
"""

    # 3) CUERPO EN HTML
    # Es la versión "bonita" que verá la mayoría de la gente.
    # Los estilos van en línea (style="...") porque muchos clientes de correo,
    # como Gmail, ignoran las hojas de estilo <style> o los archivos .css.
    # La "\" después de las comillas evita que el texto empiece con un salto de línea.
    html = f"""\
<html>
  <body style="font-family: Arial, sans-serif; color: #333;">
    <div style="max-width: 600px; margin: auto; border: 1px solid #ddd; border-radius: 8px; overflow: hidden;">
      <div style="background: #1a73e8; color: #fff; padding: 20px; text-align: center;">
        <h1 style="margin: 0;">¡Bienvenido(a), {nombre}!</h1>
      </div>
      <div style="padding: 20px;">
        <p>Nos alegra que formes parte de <strong>{NOMBRE_EMPRESA}</strong>.</p>
        <p>Estas son tus credenciales de acceso:</p>
        <table style="background: #f5f5f5; padding: 12px; border-radius: 6px;">
          <tr><td><strong>Usuario:</strong></td><td>{usuario}</td></tr>
          <tr><td><strong>Contraseña temporal:</strong></td><td><code>{password}</code></td></tr>
        </table>
        <p style="color: #c62828;">Por seguridad, cambia tu contraseña al iniciar sesión por primera vez.</p>
        <p>Saludos,<br>El equipo de {NOMBRE_EMPRESA}</p>
      </div>
    </div>
  </body>
</html>
"""

    # 4) AGREGAR AMBAS VERSIONES AL CORREO
    # set_content() pone el texto plano como cuerpo principal.
    # add_alternative() agrega el HTML como "versión alternativa" del mismo
    # contenido. El cliente de correo elige cuál mostrar (normalmente el HTML).
    mensaje.set_content(texto_plano)
    mensaje.add_alternative(html, subtype="html")
    return mensaje


def enviar_correo(mensaje, remitente, app_password):
    """
    Se conecta al servidor SMTP de Gmail y envía el correo.

    Parámetros:
        mensaje:      el EmailMessage creado con construir_mensaje().
        remitente:    correo de Gmail con el que se inicia sesión.
        app_password: contraseña de aplicación de Google (16 caracteres).
    """
    # Contexto SSL con la configuración segura recomendada: verifica que de
    # verdad estemos hablando con el servidor de Google y cifra la conexión.
    contexto = ssl.create_default_context()

    # SMTP_SSL abre una conexión cifrada desde el primer momento (puerto 465).
    # El bloque "with" cierra la conexión automáticamente al terminar,
    # incluso si ocurre un error dentro del bloque.
    with smtplib.SMTP_SSL(SMTP_SERVIDOR, SMTP_PUERTO, context=contexto) as servidor:
        servidor.login(remitente, app_password)  # Iniciar sesión en Gmail
        servidor.send_message(mensaje)           # Enviar el correo


def main():
    """Punto de entrada: lee los argumentos, prepara el correo y lo envía."""
    # 1) LEER LOS ARGUMENTOS DE LA LÍNEA DE COMANDOS
    # argparse convierte lo que escribimos en la terminal en variables.
    # required=True: el programa no corre si falta ese argumento.
    # Sin required: el argumento es opcional y vale None si no se escribe.
    # Además, argparse genera la ayuda automáticamente: python envioCorreo.py --help
    parser = argparse.ArgumentParser(description="Envía un correo de bienvenida vía Gmail.")
    parser.add_argument("--para", required=True, help="Correo del destinatario")
    parser.add_argument("--nombre", required=True, help="Nombre del destinatario")
    parser.add_argument("--usuario", help="Usuario de acceso (por defecto, el correo del destinatario)")
    parser.add_argument("--password", help="Contraseña temporal (si se omite, se genera una)")
    args = parser.parse_args()  # Ahora args.para, args.nombre, etc. tienen los valores

    # 2) LEER LAS CREDENCIALES DE GMAIL (cargadas desde el .env)
    # os.environ.get() devuelve None si la variable no existe.
    remitente = os.environ.get("GMAIL_USER")
    app_password = os.environ.get("GMAIL_APP_PASSWORD")
    # Validamos antes de intentar conectarnos, para dar un mensaje de error claro.
    if not remitente or not app_password:
        sys.exit("Error: define GMAIL_USER y GMAIL_APP_PASSWORD en el archivo .env.")

    # 3) VALORES POR DEFECTO
    # "a or b" devuelve a si tiene valor; si a es None (o vacío), devuelve b.
    usuario = args.usuario or args.para                        # Si no hay usuario, se usa el correo
    password = args.password or generar_password_temporal()    # Si no hay contraseña, se genera una

    # 4) ARMAR EL CORREO
    mensaje = construir_mensaje(remitente, args.para, args.nombre, usuario, password)

    # 5) ENVIARLO, MANEJANDO LOS POSIBLES ERRORES
    # try/except evita que el programa termine con un error largo y confuso.
    # Los except se revisan en orden, del error más específico al más general.
    try:
        enviar_correo(mensaje, remitente, app_password)
    except smtplib.SMTPAuthenticationError:
        # Gmail rechazó el usuario o la contraseña.
        sys.exit("Error de autenticación: verifica GMAIL_USER y que uses una contraseña de aplicación.")
    except (smtplib.SMTPException, OSError) as e:
        # Cualquier otro problema de SMTP o de red (sin internet, puerto bloqueado...).
        sys.exit(f"No se pudo enviar el correo: {e}")

    print(f"Correo de bienvenida enviado a {args.para}")


# Este bloque solo se ejecuta si corremos el archivo directamente
# (python envioCorreo.py), NO si otro script lo importa con "import envioCorreo".
# Así sus funciones se pueden reutilizar desde otros programas.
if __name__ == "__main__":
    main()
