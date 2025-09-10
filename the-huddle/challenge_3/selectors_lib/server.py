import socket

class ServidorBase:
    '''
    Un objeto servidor que se puede utilizarse para simular un sevidor en la red.
    '''

    def __init__(self, host:str, port:int) -> None:
        '''
        Inicializa el servidor en el host y puerto especificados.
        '''
        self.host:str = host
        self.port:int = port
        self._socket = None

    def crear(self) -> None:
        '''
        Crea el servidor en el host y puerto especificados.
        '''
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Servidor creado en {self.host}:{self.port}")

    def vincular(self) -> None:
        '''
        Vincula el servidor a la red.
        '''
        self._socket.bind((self.host, self.port))        
        print(f"El servidor {self.host}:{self.port} se ha vinculado a la red")

    def escuchar(self) -> None:
        '''
        Inicia el servidor y comienza a escuchar conexiones entrantes.
        '''
        self._socket.listen()
        print(f"El servidor {self.host}:{self.port} está escuchando conexiones entrantes")
        
    def aceptar(self) -> socket:
        '''
        Acepta una conexión entrante y devuelve el socket de la conexión.
        '''
        cliente_sock, cliente_addr = self._socket.accept()
        print(f"Se ha aceptado una conexión de {self._cliente_addr}")
        return cliente_sock, cliente_addr

    def recibir(self, conn:socket) -> str:
        '''
        Recibe un mensaje a través del socket especificado.
        '''
        return conn.recv(1024).decode()
    
    def enviar(self, conn:socket, mensaje:str) -> None:
        '''
        Envia un mensaje a través del socket especificado.
        '''
        conn.sendall(mensaje.encode())

    def cerrar(self) -> None:
        '''
        Cierra el servidor.
        '''
        self._socket.close()

    def __str__(self) -> str:
        return f"Servidor en {self.host}:{self.port}"

