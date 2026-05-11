from dotenv import load_dotenv
from fastapi import FastAPI

import os
import uvicorn


load_dotenv()

HOST = os.getenv('HOST')
PORT = os.getenv('PORT_USERS', 23450)


app = FastAPI()

@app.get("/users")
def index():
    return {
        "status": "ok",
        "método": "GET",
        "path": "/users",
        "message": "Microservicio Usuarios",
    }

@app.post("/users/nuevo")
def nuevo():
    return {
        "status": "ok",
        "método": "POST",
        "path": f"/users/nuevo",
        "message": "Microservicio Usuarios",
    }

@app.delete("/users/eliminar/{id}")
def eliminar(id):
    return {
        "status": "ok",
        "método": "DELETE",
        "path": f"/users/eliminar/{id}",
        "message": "Microservicio Usuarios",
    }


@app.put("/users/actualizar/{id}")
def actualizar(id):
    return {
        "status": "ok",
        "método": "PUT",
        "path": f"/users/actualizar/{id}",
        "message": "Microservicio Usuarios",
    }

@app.post("/auth/validar")
def validar():
    return {
        "status": "ok",
        "método": "POST",
        "path": "/auth/validar",
        "message": "Microservicio Usuarios",
    }

if __name__=="__main__":
    uvicorn.run(app, host=HOST, port=int(PORT))