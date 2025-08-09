from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from dotenv import load_dotenv
import os

load_dotenv()
path = os.getenv('PENGUIN_PATH')


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
    add_log(datos.id_service, datos.name, datos.timestamp, datos.level, datos.type, datos.message)
    with open(path + 'logs.txt', 'a+', encoding='utf-8') as log_file:
        log_file.write(f"{datos.id_service} {datos.name} {datos.timestamp} {datos.level} {datos.type} {datos.message}\n")
    return {f"Id servicio: {datos.id_service}, Nombre: {datos.name}"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=12345)