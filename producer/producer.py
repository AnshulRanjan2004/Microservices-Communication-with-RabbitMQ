import pika, json
from flask import Flask

# connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
# channel = connection.channel()
# def publish(method, body):
#     properties = pika.BasicProperties(method)
#     channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)

app = Flask(__name__)

@app.post("/createitem")
def createItem():
    item_data = {
        "name": "Sample Item",
        "description": "This is a sample item",
        "price": 9.99,
        "quantity": 100,
        "category": "Sample Category"
    }
    channel.basic_publish(exchange='', routing_key='items_queue', body=message_body)
    return {"message":"item created"}

@app.route('/')
def index():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True,port=8001)
