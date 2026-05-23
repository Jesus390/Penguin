# Iceforge

## Descripción
Mini arcade desde la línea de comandos implementado con Python.

## Prerrequisitos
* Python 3.10 o superior
* `uv`

### Opcionales
* Docker

## Instalación y Ejecución

```shell
# Crear el entorno virtual con 'uv'
uv venv

# Activar el entorno virtual en Windows (PowerShell)
.venv\Scripts\Activate.ps1
# O en Windows (CMD)
.venv\Scripts\activate.bat

# Activar el entorno virtual en Linux/macOS
source .venv/bin/activate

# Instalar las dependencias del proyecto
uv sync

# Ejecutar el programa
uv run main.py
```

## Ejecución con Docker (Opcional)
Si prefieres ejecutar el juego usando Docker, puedes utilizar los siguientes comandos:

```shell
# Construir la imagen
docker build -t iceforge .

# Ejecutar el contenedor de forma interactiva (necesario para juegos de terminal)
docker run -it iceforge
```
