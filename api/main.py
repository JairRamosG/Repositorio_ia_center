#fastapi ---- framework
#uvicorn ---- servidor webb par acomunicarnos con la api
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def raiz():
    return {"Hello" : "World"}

@app.get("/items/{item_id}/{m}")
def read_item(item_id:int, m: str = None):
    return {"item_del_id": item_id, "mensaje":m}
