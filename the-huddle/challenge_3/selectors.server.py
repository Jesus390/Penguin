import socket
import selectors

# Dirección IP del servidor
# Para pruebas utilizando Docker
# configurar la dirección a "0.0.0.0"
# para escuchar fuera de Docker.
SERVER_ADDR = '127.0.0.1'

# Puerto para el servidor.
SERVER_PORT = 12345

# Mantener lista de clientes, guarda nuevas conecciones
# establecidas con el servidor.
clientes = set()

# Primera etapa para capturar una posible excepción
# lanzada por el teclado
try:
    
    # Se crea un socket para que trabaje como un servidor.
    # Se utiliza AF_INET para direcciones IPv4 y SOCK_STREAM
    # que se baza en un socket de flujo orientada a conección.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Vincular las direcciones IP y el Puerto al socket
    server.bind((SERVER_ADDR, SERVER_PORT))

    # Socket en escucha
    server.listen()

    # Se utiliza para que el socket funcione de forma concurrente
    server.setblocking(False)

    print(f"Iniciando servidor en {SERVER_ADDR}:{SERVER_PORT}")

    # Instancia del selectors para menejar concurrencia.
    sel = selectors.DefaultSelector()

    # Se registra el servidor al selector, esto maneja la concurrencia.
    sel.register(server, selectors.EVENT_READ)
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            sock = key.fileobj

            if sock is server:  # Nuevo cliente
                conn, addr = server.accept()
                print(f"Conexión aceptada {addr}")
                conn.setblocking(False)
                sel.register(conn, selectors.EVENT_READ)
                clientes.add(conn)

            else:  # Cliente existente
                try:
                    data = sock.recv(1024)
                    if not data:
                        raise ConnectionResetError()

                    mensaje = data.decode().strip()
                    print(f"{sock.getpeername()}: {mensaje}")

                    if mensaje.lower() == "salir":
                        print(f"Cliente {sock.getpeername()} salió")
                        sel.unregister(sock)
                        clientes.remove(sock)
                        sock.close()
                    else:
                        # Broadcast a todos los demás clientes
                        for cliente in clientes:
                            if cliente != sock:
                                try:
                                    cliente.sendall(f"{sock.getpeername()}: {mensaje}".encode())
                                except BrokenPipeError:
                                    pass  # Cliente desconectado

                except (ConnectionResetError, BrokenPipeError):
                    print(f"Cliente {sock.getpeername()} desconectado abruptamente")
                    sel.unregister(sock)
                    clientes.discard(sock)
                    sock.close()

except KeyboardInterrupt:
    print("\nServidor detenido manualmente")

finally:
    sel.close()
    server.close()
