from fastapi import FastAPI
from pydantic import BaseModel

class Datos(BaseModel):
    id_service: str
    name: str
    timestamp: str
    level: str
    type: str
    message: str


app = FastAPI()


@app.post("/log/")
async def create_item(datos: Datos):
    with open('log.txt', 'a+', encoding='utf-8') as log_file:
        log_file.write(f"{datos.id_service} {datos.name} {datos.timestamp} {datos.level} {datos.type} {datos.message}\n")
    return {f"Id servicio: {datos.id_service}, Nombre: {datos.name}"}