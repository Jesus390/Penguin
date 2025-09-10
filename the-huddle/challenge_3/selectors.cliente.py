import socket

REMOTE_ADDR = "127.0.0.1"
REMOTE_PORT = 12345

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        print("Iniciando cliente...")
        cliente.connect((REMOTE_ADDR, REMOTE_PORT))
        print(f"Cliente conectado al {REMOTE_ADDR}:{REMOTE_PORT}")

        while True:
            try:
                mensaje = input("Escribe un mensaje ('salir' para terminar): ")

                if mensaje.lower() == "salir":
                    print("Cerrando cliente...")
                    break

                # Enviar al servidor
                cliente.sendall(mensaje.encode())

                # Recibir respuesta del servidor
                data = cliente.recv(1024)
                if not data:
                    print("Servidor cerró la conexión")
                    break

                print(f"--- Respuesta: {data.decode()}")

            except (ConnectionResetError, BrokenPipeError):
                print("Conexión perdida con el servidor")
                break

except KeyboardInterrupt:
    print("\nCliente detenido manualmente")

except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")
