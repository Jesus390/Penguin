import socket

class Servidor:
    def __init__(self, ip:str, puerto:int):
        self.ip = ip
        self.puerto = puerto
        self.conecciones = {}
        self.socket = None
    
    def run(self):
        # Crear un socket TCP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.puerto))
        self.socket.listen()
        print("Iniciando servidor...")
        print("Servidor iniciado en " + self.ip + ":" + str(self.puerto))
        while True:
            # Esperar a que un cliente se conecte
            cliente, direccion = self.socket.accept()
            print("Cliente conectado: " + str(direccion))
            # Manejar la conexión con el cliente
            self.conecciones[cliente] = direccion
            while cliente:
                try:
                    # Recibir datos del cliente
                    datos = cliente.recv(1024)
                    if datos:
                        print("Mensaje recibido: " + datos.decode())
                        # Enviar respuesta al cliente
                        cliente.sendall("Mensaje recibido".encode())
                    else:
                        print("No hay datos para recibir")
                except Exception as e:
                    print("Error en la conexión: " + str(e))

