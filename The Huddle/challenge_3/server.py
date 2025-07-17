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
    while True:
        try:
            conn, addr = s.accept()
            conn.setblocking(False)
            with conn:
                print(f"Cliente conectado: {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break 
                    print(f"{addr}-{time.ctime(time.time())}: {data.decode()}")
                    conn.sendall(data)
        except ConnectionResetError:
            print(f"Conexión con {addr} cerrada")
        except OSError as e:
            print(f"Error de socket: {e}")
