from dotenv import load_dotenv
from fastapi import FastAPI

import os
import uvicorn


load_dotenv()

HOST = os.getenv('HOST')
PORT = os.getenv('PORT_PRODUCTS', 12347)


app = FastAPI()

@app.get("/products")
def index():
    return {
        "status": "ok",
        "método": "GET",
        "path": "/products",
        "message": "Microservicio Productos",
    }

@app.post("/products/nuevo")
def nuevo():
    return {
        "status": "ok",
        "método": "POST",
        "path": f"/products/nuevo",
        "message": "Microservicio Productos",
    }

@app.delete("/products/eliminar/{id}")
def eliminar(id):
    return {
        "status": "ok",
        "método": "DELETE",
        "path": f"/products/eliminar/{id}",
        "message": "Microservicio Productos",
    }


@app.put("/products/actualizar/{id}")
def actualizar(id):
    return {
        "status": "ok",
        "método": "PUT",
        "path": f"/products/actualizar/{id}",
        "message": "Microservicio Productos",
    }

@app.post("/auth/validar")
def validar():
    return {
        "status": "ok",
        "método": "POST",
        "path": "/auth/validar",
        "message": "Microservicio Productos",
    }

if __name__=="__main__":
    uvicorn.run(app, host=HOST, port=int(PORT))