import asyncio
import socket


class Cliente():
    def __init__(self, host:str, puerto:int) -> None:
        self.host = host
        self.puerto = puerto
        # # Resolver siempre a IPv4
        # info = socket.getaddrinfo(host, puerto, family=socket.AF_INET, type=socket.SOCK_STREAM)
        # self.direccion = info[0][4]  # Tupla (host, puerto)

    async def nuevo_mensaje(self, s):
        loop = asyncio.get_event_loop()
        while True:
            try:
                data = await loop.sock_recv(s, 1024)
                if not data:
                    break
                print(f"Recibido: {data.decode()}")
            except:
                break
    
    async def ejecutar(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setblocking(False)

            loop = asyncio.get_running_loop()

            try:
                await loop.sock_connect(s, (self.host, self.puerto))
                print("Conectado al servidor.")
            except Exception as e:
                print("No se pudo conectar:", e)
                return

            asyncio.create_task(self.nuevo_mensaje(s))

            while True:
                try:
                    print(">> ", end='')
                    # mensaje = input()
                    mensaje = await loop.run_in_executor(None, input, '')
                    if mensaje=='salir': break
                    await loop.sock_sendall(s, mensaje.encode())

                except ConnectionResetError:
                    print("Conexión cerrada")
                    break

cliente = Cliente('127.0.0.1', 12345)
asyncio.run(cliente.ejecutar())