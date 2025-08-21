from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel

import datetime
import jwt
import os
import uvicorn

load_dotenv()
path = os.getenv('PENGUIN_PATH')

# clave secreta para firmar los tokens
SECRET_KEY = "secret_key"
ALGORITHM = "HS256"

# guarda los tokens generados para los servicios
tokens = {}

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Logs(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    id_service = Column(String(255))
    name = Column(String(255))
    timestamp = Column(String(255))
    level = Column(String(255))
    type = Column(String(255))
    message = Column(String(255))


engine = create_engine(f'sqlite:///{path}logs.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def add_log(id_service, name, timestamp, level, type, message):
    new_log = Logs(id_service=id_service, name=name, timestamp=timestamp, level=level, type=type, message=message)
    session.add(new_log)
    session.commit()
    session.close()

def generate_token(service_id):
    payload = {
        "service_id": service_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    tokens[service_id] = {"payload": payload, "token": token}
    return token

# modelos
class Datos(BaseModel):
    id_service: str
    name: str
    timestamp: str
    level: str
    type: str
    message: str

class ServiceId(BaseModel):
    service_id: str

app = FastAPI()

# Función para validar token
def verify_token(authorization: str = Header(...)):
    print(authorization)
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Header de autorización inválido")

    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # contiene service_id, exp
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

@app.post("/log/")
async def create_item(datos: Datos, payload: dict = Depends(verify_token)):
    """
    Se requiere header: Authorization: Bearer <token>
    """
    # validación de que el id_service del log coincide con el del token
    if datos.id_service != payload.get("service_id"):
        raise HTTPException(status_code=403, detail="Servicio no autorizado")

    add_log(datos.id_service, datos.name, datos.timestamp, datos.level, datos.type, datos.message)

    with open(path + "logs.txt", "a+", encoding="utf-8") as log_file:
        log_file.write(f"{datos.id_service} {datos.name} {datos.timestamp} {datos.level} {datos.type} {datos.message}\n")

    return {"status": "ok", "service_id": datos.id_service}

@app.post("/token")
def token(datos: ServiceId):
    token = generate_token(datos.service_id)
    return {"token": token}  # <- más estándar

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=12345)