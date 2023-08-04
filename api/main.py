#fastapi ---- framework
#uvicorn ---- servidor webb par acomunicarnos con la api

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class  Libro(BaseModel):
    titulo: str
    autor: str
    paginas: int
    editorial: Optional[str]

@app.get("/")
async def index():
    return {"messaje" : "Hello World!"}

@app.get("/items/{id}")
async def mostrar_libro(id:int):
    return {"data": id}

@app.post("/libros/")
async def insertar_libro(libro: Libro):
    return {"message": f"Libro: {libro.titulo} insertado correctamente"}

