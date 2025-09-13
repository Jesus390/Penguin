import socket

class ClienteChat():
    '''
    Chat cliente para envios de mensajes
    '''

    def __init__(self, host:str, port:int) -> None:
        '''
        Inicializa el cliente de chat
        '''
        self.host = host
        self.port = port
        self._client_socket = self._crear()

    def _crear(self) -> None:
        '''
        Crea el socket cliente
        '''
        try:
            return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            self._client_socket = None
            raise Exception(f"No se pudo crear el socket.\nError: {e}")

    def conectar(self) -> None:
        '''
        Conecta el cliente al servidor
        '''
        self._client_socket.connect((self.host, self.port))

    def cerrar(self) -> None:
        '''
        Cierra la conexión del cliente
        '''
        if self._client_socket:
            self._client_socket.close()
            self._client_socket = None

    def enviar(self, mensaje:str) -> None:
        '''
        Envia un mensaje al servidor
        '''
        if self._client_socket:
            mensaje_bytes = mensaje.encode('utf-8')
            self._client_socket.send(mensaje_bytes)
            print(f"Mensaje enviado: {mensaje}")
        else:
            print("No hay conexión establecida")

    def recibir(self) -> str:
        '''
        Recibe un mensaje del servidor
        '''
        if self._client_socket:
            mensaje_bytes = self._client_socket.recv(1024)
            mensaje = mensaje_bytes.decode('utf-8')
            print(f"Mensaje recibido: {mensaje}")
            # return mensaje
        else:
            print("No hay conexión establecida")

    def __str__(self) -> str:
        '''
        Retorna una cadena con la información del cliente
        '''
        return f'Cliente Chat - Host: {self.host} - Puerto: {self.port}'


def main():
    import time

    HOST = "127.0.0.1"
    PORT = 12345

    # Instancia del Cliente
    cliente = ClienteChat(HOST, PORT)
    

    intentos = 0

    # Reintentos para conectar
    while intentos < 3:
        try:
            # Conectar cliente
            cliente.conectar()
            while True:
                
                    try:
                        intentos = 0
                        mensaje = input(">> ")
                        # Enviar mensaje
                        cliente.enviar(mensaje)

                        # Recibir mensaje
                        cliente.recibir()
                    except KeyboardInterrupt:
                        print("Interrucción por teclado.")
                        intentos = 3
                        break
        except Exception as e:
            print(f"No se pudo conectar con el servidor: {e}")
            intentos += 1
            print(f"Intentos: {intentos}")
            time.sleep(5)
        except KeyboardInterrupt:
            print("Interrucción por teclado.")
        finally:
            if intentos == 3:
                cliente.cerrar()
                print("Socket cerrado con exitó.")

if __name__=="__main__":
    main()