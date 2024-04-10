import pika, json
from flask import Flask
#amqp://rabbit:rabbit@localhost:5672/%2f
credentials = pika.PlainCredentials('user', 'pass')
parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
# params = pika.URLParameters('amqp://user:pass@localhost:5672/%2f')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='createItem')
def publish(body):
    
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body))

app = Flask(__name__)

@app.post("/createitem")
def createItem(): 
    item_data = {
        "name": "Sample Item2",
        "description": "This is a sample item 1",
        "price": 10,
        "quantity": 0,
        "category": "Sample Category"
    }
    publish(item_data)
    return {"message":"item created"}

@app.route('/')
def index():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True,port=8001)
