# Echo client program
import socket

HOST = 'localhost'    # The remote host
PORT = 12345          # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(10)
    try:
        s.connect((HOST, PORT))
        print(">> ", end='')
        msg = input()
        s.sendall(msg.encode('utf-8'))
        data = s.recv(1024)
        print('Received', repr(data))
        print('Cerrando cliente')
    except socket.timeout:
        print("Timeout")
    except ConnectionRefusedError:
        print("❌ Error: El servidor rechazó la conexión o no está disponible.")
    except ConnectionAbortedError:
        print("❌ Error: La conexión con el servidor se ha cerrado.")