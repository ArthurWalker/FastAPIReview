from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    text:str
    is_done:bool = False

items = []

@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.post("/items")
def create_item(item:Item):
    items.append(item)
    return {"message": "Item created successfully", "item": items}

@app.get("/items/{item_id}", response_model= Item)
def get_item(item_id:int):
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code = 404, detail = "Item not found")
    
@app.get("/items",response_model = list[Item])
def list_items(limit:int=3):
    return items[:limit]