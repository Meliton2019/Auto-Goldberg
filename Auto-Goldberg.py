import os
import shutil
import zipfile
import urllib.request
import tkinter as tk
from tkinter import filedialog
import requests

# ── CFG ──────────────────────────────────────────────
REPO_URL = "https://github.com/Meliton2019/goldberg/releases/download/Latest/goldberg.zip"
ZIP_NAME = "goldberg.zip"
EXTRACT_DIR = "goldberg"
# ───────────────────────────────────────────────────────────────


def descargar_zip(url: str, destino: str) -> None:
    print("Downloading goldberg...")
    urllib.request.urlretrieve(url, destino)


def extraer_zip(zip_path: str, carpeta_destino: str) -> list[str]:
    print("Extracting...")
    with zipfile.ZipFile(zip_path, "r") as zf:
        nombres = zf.namelist()
        zf.extractall(carpeta_destino)
    return nombres


def seleccionar_dll() -> str | None:
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    archivo = filedialog.askopenfilename(
        title="Selecciona steam_api(64).dll",
        filetypes=[("Archivos DLL", "*.dll")]
    )
    root.destroy()
    return archivo if archivo else None


def reemplazar_dll(ruta_dll: str) -> None:
    nombre_dll = os.path.basename(ruta_dll)

    origen = None
    for raiz, _, archivos in os.walk(EXTRACT_DIR):
        if nombre_dll in archivos:
            origen = os.path.join(raiz, nombre_dll)
            break

    if origen:
        shutil.copy2(origen, ruta_dll)
        print(f"{nombre_dll} reemplazado.")
    else:
        print(f"'{nombre_dll}' no encontrado en '{EXTRACT_DIR}'.")


def crear_carpeta_settings(ruta_dll: str) -> str:
    directorio = os.path.dirname(ruta_dll)
    carpeta_settings = os.path.join(directorio, "steam_settings")
    os.makedirs(carpeta_settings, exist_ok=True)
    return carpeta_settings


def pedir_numero() -> str:
    while True:
        valor = input("Introduce el AppID de Steam: ").strip()
        if valor.isdigit():
            return valor
        print("Invalido.")


def obtener_nombre_juego(appid: str) -> str | None:
    try:
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
        response = requests.get(url, timeout=10)
        data = response.json()
        if data[appid]["success"]:
            return data[appid]["data"]["name"]
        return None
    except Exception:
        return None


def obtener_dlcs(appid: str) -> list:
    try:
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
        response = requests.get(url, timeout=10)
        data = response.json()
        if data[appid]["success"]:
            return data[appid]["data"].get("dlc", [])
        return []
    except Exception:
        return []


def obtener_nombre_dlc(dlc_id: int) -> str | None:
    try:
        url = f"https://store.steampowered.com/api/appdetails?appids={dlc_id}"
        response = requests.get(url, timeout=10)
        data = response.json()
        key = str(dlc_id)
        if data[key]["success"]:
            return data[key]["data"]["name"]
        return None
    except Exception:
        return None


def guardar_numero(carpeta_settings: str, numero: str) -> None:
    ruta_txt = os.path.join(carpeta_settings, "steam_appid.txt")
    with open(ruta_txt, "w", encoding="utf-8") as f:
        f.write(numero)


def guardar_dlcs(carpeta_settings: str, appid: str) -> None:
    dlc_ids = obtener_dlcs(appid)
    if not dlc_ids:
        print("No se encontraron DLCs.")
        return

    ruta_txt = os.path.join(carpeta_settings, "dlc.txt")
    with open(ruta_txt, "w", encoding="utf-8") as f:
        for dlc_id in dlc_ids:
            nombre = obtener_nombre_dlc(dlc_id)
            if nombre:
                f.write(f"{dlc_id}={nombre}\n")
                print(f"{dlc_id}={nombre}")

    print("dlc.txt guardado.")


def guardar_account_name(carpeta_settings: str) -> None:
    ruta_txt = os.path.join(carpeta_settings, "account_name.txt")
    with open(ruta_txt, "w", encoding="utf-8") as f:
        f.write("player")


def guardar_language(carpeta_settings: str) -> None:
    ruta_txt = os.path.join(carpeta_settings, "language.txt")
    with open(ruta_txt, "w", encoding="utf-8") as f:
        f.write("english")

def guardar_force_account_name(carpeta_settings: str) -> None:
    ruta_txt = os.path.join(carpeta_settings, "force_account_name.txt")
    with open(ruta_txt, "w", encoding="utf-8") as f:
        f.write("Player")


def preparar_goldberg() -> None:
    if os.path.isdir(EXTRACT_DIR):
        return

    if os.path.isfile(ZIP_NAME):
        extraer_zip(ZIP_NAME, EXTRACT_DIR)
        return

    descargar_zip(REPO_URL, ZIP_NAME)
    extraer_zip(ZIP_NAME, EXTRACT_DIR)


if __name__ == "__main__":
    preparar_goldberg()
    ruta_dll = seleccionar_dll()
    if ruta_dll:
        reemplazar_dll(ruta_dll)
        carpeta_settings = crear_carpeta_settings(ruta_dll)

    numero = pedir_numero()
    nombre = obtener_nombre_juego(numero)
    if nombre:
        print(f"{nombre}")
    else:
        print("AppID no encontrado.")

    guardar_numero(carpeta_settings, numero)

    guardar_dlcs(carpeta_settings, numero)

    guardar_account_name(carpeta_settings)
    

    guardar_language(carpeta_settings)
    
    guardar_force_account_name(carpeta_settings)
