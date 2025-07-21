import socket
import time

HOST = 'localhost'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Inicializando servidor...")
    s.bind((HOST, PORT))
    print(f"Servidor vinculado: {HOST}:{PORT}")
    s.listen()
    print("Esperando Conecciones...")
    s.settimeout(3)
    while True:
        try:
            conn, addr = s.accept()
            while conn:
                print(f"Conectado a {addr}")
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Recebi: {data}")
                conn.sendall(data)
        except socket.timeout:
            print("Timeout")
    