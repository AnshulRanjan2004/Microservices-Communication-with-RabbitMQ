from typing import Union
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@db:3306/inventory"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database models
class InventoryItem(Base):
    __tablename__ = "inventory_items"

    item_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    category = Column(String(50))


Base.metadata.create_all(bind=engine)

# FastAPI endpoints
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    db = SessionLocal()
    item = db.query(InventoryItem).filter(InventoryItem.item_id == item_id).first()
    db.close()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item.item_id, "name": item.name, "description": item.description, "price": item.price, "quantity": item.quantity, "category": item.category}


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    db = SessionLocal()
    item = db.query(InventoryItem).filter(InventoryItem.item_id == item_id).first()
    if item is None:
        db.close()
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    db.close()
    return {"message": "Item deleted successfully"}


@app.post("/items/{item_id}/add")
def add_item_quantity(item_id: int, quantity: int):
    db = SessionLocal()
    item = db.query(InventoryItem).filter(InventoryItem.item_id == item_id).first()
    if item is None:
        db.close()
        raise HTTPException(status_code=404, detail="Item not found")
    item.quantity += quantity
    db.commit()
    db.close()
    return {"message": "Quantity added successfully", "new_quantity": item.quantity}