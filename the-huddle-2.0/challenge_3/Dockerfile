# Usa una imagen base de Python
FROM python:3.9.23-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia tu script de Python al contenedor
COPY selectros.server.py .

# Expone el puerto que tu servidor escuchará
# El puerto es 12345, pero tu código usa '127.0.0.1' que solo funciona dentro del contenedor
# Para que sea accesible desde fuera, el host debe ser '0.0.0.0'
EXPOSE 12345

# Comando para ejecutar el servidor cuando el contenedor se inicie
CMD ["python", "selectors.server.py"]