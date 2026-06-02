# Auto-Goldberg

Automatiza la preparación de archivos de configuración para aplicaciones basadas en Steam.

## Características

* Descarga automáticamente los archivos necesarios.
* Extrae el contenido del paquete descargado.
* Permite seleccionar un archivo DLL mediante una interfaz gráfica.
* Crea automáticamente la carpeta `steam_settings`.
* Solicita un Steam AppID al usuario.
* Obtiene el nombre del juego utilizando la API pública de Steam.
* Obtiene la lista de DLCs asociados al AppID.
* Genera automáticamente los siguientes archivos:

  * `steam_appid.txt`
  * `dlc.txt`
  * `account_name.txt`
  * `force_account_name.txt`
  * `language.txt`

## Requisitos

* Python 3.10 o superior
* Dependencias:

```bash
pip install requests
```

## Uso

Ejecuta el script:

```bash
python Auto-Goldberg.py
```

### Proceso

1. El programa descargará y preparará los archivos necesarios.
2. Se abrirá un selector para elegir el archivo DLL correspondiente.
3. Introduce el Steam AppID cuando se solicite.
4. El programa obtendrá la información del juego y sus DLCs.
5. Se generarán automáticamente los archivos de configuración dentro de la carpeta `steam_settings`.

## Archivos generados

### steam_appid.txt

Contiene el AppID especificado por el usuario.

### dlc.txt

Contiene la lista de DLCs detectados para el AppID.

### account_name.txt

Nombre de usuario predeterminado:

```text
player
```

### force_account_name.txt

Nombre de usuario forzado:

```text
Player
```

### language.txt

Idioma predeterminado:

```text
english
```

## Dependencias utilizadas

* requests
* tkinter
* urllib
* zipfile
* shutil
* os

## Licencia

Este proyecto se distribuye únicamente con fines educativos y de automatización. El usuario es responsable de cumplir con los términos de uso y licencias del software que utilice.
