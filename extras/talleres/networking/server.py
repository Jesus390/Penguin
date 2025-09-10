import asyncio
import websockets

clientes_conectados = set()

async def manejar_cliente(websocket):
    direccion = websocket.remote_address
    clientes_conectados.add(websocket)
    print(
        f'Cliente conectado desde {direccion}. Total conectados: {len(clientes_conectados)}'
    )
    try:
        async for mensaje in websocket:
            print(f'Mensaje recibido de {direccion}:{mensaje}')
            for cliente in clientes_conectados:
                try:
                    await cliente.send(mensaje)    
                    print(f'Mensaje enviado a {cliente.remote_address}')
                except websockets.exceptions.ConnectionClosed():
                    print(f'Cliente desconectado {cliente.remote_address}')
                    clientes_conectados.discard(cliente)
    except websockets.exceptions.ConnectionClosed():
       print(f'Cliente desconectado {cliente.remote_address}')
       clientes_conectados.discard(cliente)

async def main():
    address_server = 'localhost'
    port_server = 3000
    servidor = await websockets.serve(manejar_cliente, address_server, port_server)
    print(f'Servidor iniciado en ws://{address_server}:{port_server}')
    await servidor.wait_closed()

if __name__=='__main__':
    asyncio.run(main())