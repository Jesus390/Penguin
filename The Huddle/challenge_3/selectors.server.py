import socket
import selectors

sel = selectors.DefaultSelector()

SERVER_ADDR = '127.0.0.1'
SERVER_PORT = 12345

# Crear socket del servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    print(f"Iniciando servidor...")
    server.bind((SERVER_ADDR, SERVER_PORT))
    server.listen()
    server.setblocking(False)

    print(f"Escuchando en {SERVER_ADDR}:{SERVER_PORT}")

    # Registrar el servidor en el selector
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
            else:  # Cliente existente
                data = sock.recv(1024)
                if data:
                    print(f"{sock.getpeername()}: {data.decode()}")
                    sock.sendall(data)  # eco
                else:  # Cliente cerró
                    print(f"Conexión cerrada {sock.getpeername()}")
                    sel.unregister(sock)
                    sock.close()
