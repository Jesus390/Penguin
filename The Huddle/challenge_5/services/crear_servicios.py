import json
import random
import requests
import threading
import time

HOST = '127.0.0.1'
PORT = 12345

def crear_servicio(id_serv:str, data:dict, tipo_log:dict, cantidad:int=10) -> None:
    '''
    @function, crear_servicio, recibe una lista de servicios y los ejecuta en segundo plano.
    @param, id_serv, id del servicio
    @param, data, datos del servicio
    @param, tipo_log, tipo de log
    @param, cantidad, cantidad de veces que se ejecuta el servicio
    @return, None
    '''
    name = data['name']

    cantidad = cantidad
    while cantidad:
        level = random.choice(list(tipo_log['level'].keys()))
        type = random.choice([k for k, _ in tipo_log['Type'].items() if tipo_log['Type'][k]['level']==level])
        message = random.choice(tipo_log['Type'][type]['messages'])

        # formato de envio de log
        log = {
            'id_service': id_serv,
            'name': name,
            'timestamp': time.ctime(time.time()),
            'level': level,
            'type': type,
            'message': message
        }

        # envio de log
        try:
            requests.post(f'http://{HOST}:{PORT}/log', data=json.dumps(log))
        except Exception as e:
            print(f"[{id_serv}] Error al enviar log: {e}")

        # tiempo de espera antes de volver a generar un log
        time.sleep(random.choice(range(1, 10)))
        
        # decrementar la cantidad de logs a generar
        cantidad -= 1

def iniciar_servicios() -> None:
    with open('config_servicios.json', 'r', encoding='utf-8') as file:
        config = json.load(file)

    servicios = config['services']
    tipo_log = config['severity']

    for id_servicio, data in servicios.items():
        thread = threading.Thread(target=crear_servicio, args=(id_servicio, data, tipo_log), daemon=False)
        thread.start()

if __name__=="__main__":
    iniciar_servicios()

