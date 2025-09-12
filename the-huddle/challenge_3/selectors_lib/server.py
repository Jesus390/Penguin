from datetime import datetime

import socket

class Cliente:
    '''
    Registra la información de un nuevo cliente.
    '''

    def __init__(self, cliente):
        '''
        Inicializa los valores del cliente.
        '''

        # Socket que permite la conección cliente/servidor
        self.sock = cliente["sock"]

        # Nombre de usuario
        self.nombre = cliente["nombre"]

        # Tiempo de conección inicial con el servidor
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f"""
- Socket: {self.sock}
- Nombre: {self.nombre}
- Inicio de la conección: {self.timestamp}
        """

class ListaDeClientes():
    '''
    Contiene una lista de clientes nuevos.
    '''

    # Guarda las conecciones registradas
    conecciones = set()

    def agregar(self, nueva_coneccion):
        '''
        Agrega una nueva conección a la lista
        '''
        self.conecciones.add(nueva_coneccion)

    def eliminar(self, coneccion):
        '''
        Elimina la coneccion de la lista
        '''
        self.conecciones.discard(coneccion)

    def get_cliente(self, socket):
        '''
        Devuelve el cliente
        '''
        for cliente in self.conecciones:
            if socket == cliente.sock:
                return cliente
        return None

class Servidor:
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
        print(f"Se ha aceptado una conexión de {cliente_addr}")
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


def main():
    '''
    Implementación del servidor
    '''
    HOST = "127.0.0.1"
    PORT = 12345
    
    # Instancia de la clase servidor
    servidor = Servidor(HOST, PORT)

    # Crear el servidor, vincular y que este en modo de escucha
    servidor.crear()
    servidor.vincular()
    servidor.escuchar()

    # Aceptar la conección
    socket_del_cliente, direccion_del_cliente = servidor.aceptar()

    print(f"Socket: {socket_del_cliente}")
    print(f"Dirección: {direccion_del_cliente}")

    # Recibir mensaje
    print(f"Mensaje: {servidor.recibir(socket_del_cliente)}")



if __name__ == "__main__":
    main()

    # cliente_0 = {
    #     "sock": "Socket 0",
    #     "nombre": "Cliente 0"
    # }
    # cli_0 = Cliente(cliente_0)

    # cliente_1 = {
    #     "sock": "Socket 1",
    #     "nombre": "Cliente 1"
    # }
    # cli_1 = Cliente(cliente_1)

    # cliente_3 = {
    #     "sock": "Socket 3",
    #     "nombre": "Cliente 3"
    # }
    # cli_3 = Cliente(cliente_3)

    # lista_de_conecciones = ListaDeClientes()
    # print("Conecciones print 0:", lista_de_conecciones.conecciones)
    # lista_de_conecciones.agregar(cli_0)
    # lista_de_conecciones.agregar(cli_1)
    # print("Conecciones print 1:", lista_de_conecciones.conecciones)
    # lista_de_conecciones.eliminar(cli_0)
    # lista_de_conecciones.agregar(cli_3)
    # lista_de_conecciones.eliminar(cli_0)
    # print("Coneccion print 2", lista_de_conecciones.conecciones)
    # cliente_0_ = lista_de_conecciones.get_cliente(cli_3.sock)
    # print("Cliente:", cliente_0_)
