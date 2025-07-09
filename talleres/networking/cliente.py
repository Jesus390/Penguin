import asyncio
import websockets
import threading
from queue import Queue

cola_mensaje = Queue()

def leer_input():
    while True:
        try:
            mensaje = input()
            cola_mensaje.put(mensaje)
        except EOFError:
            break

async def enviar_mensaje(websocket):
    while True:
        try:
            if not cola_mensaje.empty():
                mensaje = cola_mensaje.get()
                await websocket.send(mensaje)
        except websockets.exceptions.ConnectionClosed:
            print(f'Coneccion cerrada, no se puede enviar mas mensajes')
            break

async def recibir_mensaje(websocket):
    while True:
        try:
            respuesta = await websocket.recv()
            print(f'Mensaje recibido: {respuesta}')
        except websockets.exceptions.ConnectionClosed:
            print(f'Coneccion cerrada por el servidor')
            break

async def chat():
    address_server = 'localhost'
    port_server = 3000
    address = f'ws://{address_server}:{port_server}'
    try:
        async with websockets.connect(address) as websocket:
            print(f'Conectado al servidor {address}')
            input_thread = threading.Thread(target=leer_input, daemon=True)
            input_thread.start()

            await asyncio.gather(
                enviar_mensaje(websocket),
                recibir_mensaje(websocket)
            )

    except websockets.exceptions.ConnectionRefused:
        print('No se pudo conectar al servidor')
    except KeyboardInterrupt:
        print('Esperando cliente')

if __name__=='__main__':
    asyncio.run(chat)




