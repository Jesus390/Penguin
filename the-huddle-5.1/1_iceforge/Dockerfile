# Etapa 1 — Compilación
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Evita que uv cree un entorno virtual (.venv) e instala globalmente en el sistema
ENV UV_PROJECT_ENVIRONMENT=/usr/local

WORKDIR /app

# Copiar archivos de configuración de dependencias
COPY pyproject.toml uv.lock ./

# Instalar dependencias (sin compilar archivos .py a .pyc para ahorrar espacio)
RUN uv sync --frozen --no-dev --no-compile

# Etapa 2 — Ejecución (Imagen final ultra ligera)
FROM python:3.12-slim

WORKDIR /app

# Copiar las dependencias instaladas en el sistema global de la etapa anterior
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar el código fuente de tu juego
COPY . .

# Asegura que los textos en la terminal se muestren en tiempo real
ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
