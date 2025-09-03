import asyncio
import socket

class Servidor:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.clientes = []

    async def broadcast(self, mensaje, remitente):
        loop = asyncio.get_running_loop()
        for cliente in self.clientes:
            if cliente != remitente:
                try:
                    await loop.sock_sendall(cliente, mensaje)
                except Exception as e:
                    print(f"Error al enviar a {cliente.getpeername()}: {e}")

    async def atender_cliente(self, cliente: socket.socket):
        loop = asyncio.get_running_loop()
        self.clientes.append(cliente)

        try:
            while True:
                mensaje = await loop.sock_recv(cliente, 1024)
                if not mensaje:
                    break
                print(f"Mensaje recibido: {mensaje.decode()}")
                await self.broadcast(mensaje, cliente)
        except ConnectionResetError:
            print("Cliente desconectado abruptamente")
        finally:
            self.clientes.remove(cliente)
            cliente.close()

    async def iniciar(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((self.host, self.port))
            server.listen()
            server.setblocking(False)

            print(f"Servidor iniciado en {self.host}:{self.port}")

            loop = asyncio.get_running_loop()
            while True:
                cliente, addr = await loop.sock_accept(server)
                print(f"Conexión establecida con {addr}")
                asyncio.create_task(self.atender_cliente(cliente))

servidor = Servidor('127.0.0.1', 12345)
asyncio.run(servidor.iniciar())
