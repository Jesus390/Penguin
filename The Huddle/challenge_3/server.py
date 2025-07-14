import socket

HOST = 'localhost'
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Inicializando servidor...")
    print(f"Host: {HOST}")
    print(f"Porta: {PORT}")
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Conectado a', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)

        print("Cerrando servidor.")
