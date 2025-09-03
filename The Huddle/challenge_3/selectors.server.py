import socket
import selectors

sel = selectors.DefaultSelector()

SERVER_ADDR = '127.0.0.1'
SERVER_PORT = 12345

# Crear socket del servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_ADDR, SERVER_PORT))
server.listen()
server.setblocking(False)

print(f"Iniciando servidor en {SERVER_ADDR}:{SERVER_PORT}")

sel.register(server, selectors.EVENT_READ)

# Mantener lista de clientes
clientes = set()

try:
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
