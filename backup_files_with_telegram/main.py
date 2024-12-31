import os
import shutil
import zipfile
import requests

def copiar_archivos_y_carpetas_a_escritorio(ruta_origen):
    """
    Copia todos los archivos y carpetas de la ruta especificada a una carpeta en el escritorio,
    ignorando carpetas o archivos protegidos.
    """
    ruta_escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
    ruta_destino = os.path.join(ruta_escritorio, "ArchivosCopiados")

    os.makedirs(ruta_destino, exist_ok=True)

    if not os.path.exists(ruta_origen):
        print(f"La ruta de origen '{ruta_origen}' no existe.")
        return

    for elemento in os.listdir(ruta_origen):
        ruta_elemento = os.path.join(ruta_origen, elemento)
        ruta_destino_elemento = os.path.join(ruta_destino, elemento)

        try:
            if os.path.isfile(ruta_elemento):
                shutil.copy(ruta_elemento, ruta_destino)
                print(f"Archivo '{elemento}' copiado a '{ruta_destino}'.")
            elif os.path.isdir(ruta_elemento):
                # Excluir carpetas como .git
                if elemento == ".git":
                    print(f"Carpeta '{elemento}' excluida del copiado.")
                    continue
                shutil.copytree(ruta_elemento, ruta_destino_elemento, dirs_exist_ok=True)
                print(f"Carpeta '{elemento}' copiada a '{ruta_destino_elemento}'.")
        except PermissionError:
            print(f"Permiso denegado al intentar copiar: {ruta_elemento}")
        except Exception as e:
            print(f"Error al copiar '{ruta_elemento}': {e}")

    print(f"Todos los archivos y carpetas permitidos han sido copiados a la carpeta: {ruta_destino}")
    return ruta_destino


def generar_zip_en_directorio(ruta_directorio):
    """
    Crea un archivo ZIP del contenido de un directorio y lo guarda dentro del mismo directorio.
    """
    if not os.path.exists(ruta_directorio):
        print(f"La ruta '{ruta_directorio}' no existe.")
        return

    nombre_base = os.path.basename(ruta_directorio.rstrip(os.sep))
    ruta_zip = os.path.join(ruta_directorio, f"{nombre_base}.zip")

    with zipfile.ZipFile(ruta_zip, 'w', zipfile.ZIP_DEFLATED) as archivo_zip:
        for carpeta_raiz, _, archivos in os.walk(ruta_directorio):
            for archivo in archivos:
                ruta_archivo = os.path.join(carpeta_raiz, archivo)
                ruta_relativa = os.path.relpath(ruta_archivo, ruta_directorio)
                archivo_zip.write(ruta_archivo, ruta_relativa)

    print(f"Archivo ZIP generado dentro del directorio: {ruta_zip}")
    return ruta_zip

def enviar_zip_a_telegram(token, chat_id, ruta_zip):
    """
    Envía un archivo ZIP a un bot de Telegram.
    """
    if not os.path.exists(ruta_zip):
        print(f"El archivo '{ruta_zip}' no existe.")
        return

    url = f"https://api.telegram.org/bot{token}/sendDocument"

    with open(ruta_zip, "rb") as archivo:
        datos = {"chat_id": chat_id}
        archivos = {"document": archivo}

        respuesta = requests.post(url, data=datos, files=archivos)

    if respuesta.status_code == 200:
        print("Archivo enviado con éxito a Telegram.")
    else:
        print(f"Error al enviar el archivo: {respuesta.status_code}")
        print(respuesta.json())

def flujo_principal(ruta_origen, token, chat_id):
    """
    Coordina la ejecución de las funciones en el orden correcto.
    """
    print("Iniciando copia de archivos y carpetas...")
    ruta_copia = copiar_archivos_y_carpetas_a_escritorio(ruta_origen)
    
    if ruta_copia:
        print("Generando archivo ZIP...")
        ruta_zip = generar_zip_en_directorio(ruta_copia)
        
        if ruta_zip:
            print("Enviando archivo ZIP a Telegram...")
            enviar_zip_a_telegram(token, chat_id, ruta_zip)

