import socket

REMOTE_ADDR = "127.0.0.1"
REMOTE_PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    print("Iniciando cliente...")
    cliente.connect((REMOTE_ADDR, REMOTE_PORT))
    print(f"Cliente conectado al {REMOTE_ADDR}:{REMOTE_PORT}")
    mensaje = b"Echo..."
    cliente.sendall(mensaje)
    data = cliente.recv(1024)
    if data:
        print(f"--- {data}")
    