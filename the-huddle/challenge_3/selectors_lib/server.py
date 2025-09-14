from datetime import datetime

import socket
import selectors

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

    def set_blockeante(self, opcion=True):
        '''
        Configura el modo bloqueante del servidor
        '''
        self._socket.setblocking(opcion)

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
    servidor.set_blockeante()
    try:
        while True:
            # Aceptar la conección
            socket_del_cliente, direccion_del_cliente = servidor.aceptar()

            print(f"Socket: {socket_del_cliente}")
            print(f"Dirección: {direccion_del_cliente}")

            # Recibir mensaje
            mensaje = servidor.recibir(socket_del_cliente)
            print(f"{direccion_del_cliente}: {mensaje}")

            # enviar mensaje
            servidor.enviar(socket_del_cliente, mensaje)
    except KeyboardInterrupt:
        print("Interrucción por teclado.")
    finally:
        print("Cerrando servidor...")
        servidor.cerrar()
        print("Servidor cerrado correctamente.")

def server(host="127.0.0.1", port=12345):
    """
    Implementación de un servidor utilizando las librerías 'socket' y 'selectors'
    para manejar concurrencia y broadcast 

    Parámetros
    ----------
    host: dirección IP
    port: número de puerto
    """

    # Instancia del selector
    selector = selectors.DefaultSelector()

    # Captura errores
    try:
        # Intancia del socket
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Vincular la dirección IP y el Puerto al servidor
        print(f">> Vinculando el servidor en la dirección {host}:{port}")
        servidor.bind((host, port))

        # Servidor en modo de escucha
        print(">> Servidor escuchando...")
        servidor.listen()

        # Configura el servidor en modo no bloqueante
        # Se utiliza para aceptar conecciones y comunicaciones de
        # forma asincrona
        servidor.setblocking(False)

        while True:
            # Aceptar las conecciones
            # socket.accept() devuelve una tupla de 2 valores (sock, addr)
            # socket de la nueva coneccion y la dirección IP y Puerto de ese conección
            print(">> Servidor esperando conección")
            conn, addr = servidor.accept()

            # Configura la nueva conección en modo no bloquente
            conn.setblocking(False)

            # Host de la nueva conección
            host_conn = addr[0]

            # Puerto de la nueva conección
            port_conn = addr[1]

            print(f"--> Nueva coneccion desde {host_conn}:{port_conn}")

            # Maneja la nueva conección
            with conn:
                while True:        
                    # Guarda los datos enviados desde la nueva conección
                    datos = conn.recv(1024)

                    # Verifica si los datos enviados no está vacio
                    if not datos: break

                    # Imprime los datos enviados por la conección
                    mensaje = datos.decode("utf-8")
                    print(f"{addr}: {mensaje}")

                    # Reenviamos los datos a la conección
                    datos = f">> {host_conn}:{port_conn}= {mensaje}".encode("utf-8")
                    conn.send(datos)
    except KeyboardInterrupt:
        print("Interrución por teclado.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        servidor.close()

if __name__ == "__main__":
    server()
