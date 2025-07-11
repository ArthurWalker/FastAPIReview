from enum import Enum
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app = FastAPI()

class Category(Enum):
    TOOLS = "tools"
    CONSUMABLES = "consumables"

class Item(BaseModel):
    name: str
    price: str
    count: int
    id: int
    category: Category


items = {
    0: Item(name="Hammer", price="10.99", count=5, id=0, category=Category.TOOLS),
    1: Item(name="Screwdriver", price="5.49", count=10, id=1, category=Category.TOOLS),
    2: Item(name="Nails", price="2.99", count=100, id=2, category=Category.CONSUMABLES),
    3: Item(name="Glue", price="3.49", count=20, id=3, category=Category.CONSUMABLES),
}

Selection = dict[
    str, str | int | float | Category | None | Item
] 

@app.get("/")
def index() -> dict[str,dict[int,Item]]:
    return {"items": items}

@app.get("/items/{item_id}")
def get_item(item_id:int) -> Item:
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

@app.get("/items")
def query_items_params(name:str | None = None,
                       price:float | None = None,
                       count:int | None = None,
                       category:Category | None = None,
                       ) -> dict[str, Selection]:
    
    def check_item(item:Item) -> bool:
        return all((name is None or item.name == name,
                    price is None or item.price == price,
                    count is None or item.count != count,
                    category is None or item.category is category))
    
    selection =  [item for item in items.values() if check_item(item)]

    return {"query": {
        "name": name,
        "price": price,
        "count": count,
        "category": category,
        "items": selection
    }}

@app.post("/items")
def add_item(item: Item) -> dict[str,Selection]:
    if item.id in items:
        raise HTTPException(status_code=400, detail="Item with this ID already exists")
    items[item.id] = item
    return {"message": "Item added successfully", "item": item}

@app.put("/update_items/{item_id}")
def update_item(item_id: int, 
                name:str | None = None,
                price:float | None = None,
                count:int | None = None) -> Selection:

    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
  
    if name is None and price is None and count is None:
        raise HTTPException(status_code=400, detail="No fields to update provided")
    if all(info is None for info in (name,price,count)):
        raise HTTPException(status_code=400, detail="At least one field must be provided for update")
    
    if name is not None:
        items[item_id].name = name
    if price is not None:
        items[item_id].price = price
    if count is not None:
        items[item_id].count = count
    
    return {"message": "Item updated successfully", "item": items[item_id]}

@app.delete("/items/{item_id}")
def delete_item(item_id: int) -> dict[str, str]:
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    
    del items[item_id]
    return {"message": "Item deleted successfully"}