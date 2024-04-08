import pika, json
from fastapi import FastAPI, HTTPException
params = pika.URLParameters('')

connection = pika.BlockingConnection(params)

channel = connection.channel()
def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)

app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/createitem")
def createItem():
    item_data = {
        "name": "Sample Item",
        "description": "This is a sample item",
        "price": 9.99,
        "quantity": 100,
        "category": "Sample Category"
    }
    return {"message":"item created"}


