from flask import Flask, jsonify, request, render_template, url_for
import mysql.connector
import pika
import json

mydb = mysql.connector.connect(
    host="192.168.180.2",
    user="root",
    database="student_records",
    password="password"
)
c = mydb.cursor()
def create_table():
    c.execute('CREATE TABLE STOCK_ITEMS (ProductID INT PRIMARY KEY AUTO_INCREMENT, ProductName VARCHAR(100), Quantity INT, UnitPrice VARCHAR(10));')
# create_table()

app = Flask(__name__)

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.180.2', 5672, '/', credentials))
channel = connection.channel()

channel.exchange_declare(exchange='insertion', exchange_type='direct')
channel.queue_declare(queue='insertion_queue')
channel.queue_bind(exchange='insertion', queue='insertion_queue')

channel.exchange_declare(exchange='deletion', exchange_type='direct')
channel.queue_declare(queue='deletion_queue')
channel.queue_bind(exchange='deletion', queue='deletion_queue')

channel.exchange_declare(exchange='read', exchange_type='direct')
channel.queue_declare(queue='read_queue')
channel.queue_bind(exchange='read', queue='read_queue')

channel.exchange_declare(exchange='read_response', exchange_type='direct')
channel.queue_declare(queue='read_queue_response')
channel.queue_bind(exchange='read_response', queue='read_queue_response')

channel.exchange_declare(exchange='health', exchange_type='direct')
channel.queue_declare(queue='health_check')
channel.queue_bind(exchange='health', queue='health_check')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health_check', methods=['GET'])
def health_check():
    message = request.args.get('message')
    channel.basic_publish(exchange='health', routing_key='health_check', body=message)
    return "Added to Health Check queue. Check if consumer recieved the message!"


@app.route('/insert_record', methods=['GET'])
def insert_record():
    id = request.args.get('id')
    name = request.args.get('name')
    quantity = request.args.get('quantity')
    price = request.args.get('price')
    info = {"id":str(id), "name":str(name), "quantity":str(quantity), "price":str(price)}
    channel.basic_publish(exchange='insertion', routing_key='insertion_queue', body=json.dumps(info))
    return "Added to insertion queue"


@app.route('/read_data', methods=['GET'])
def read_data():
    channel.basic_publish(exchange='read', routing_key='read_queue', body="Show records bro")
    method_frame, _, body = channel.basic_get(queue='read_queue_response', auto_ack=True)
    # channel.basic_ack(delivery_tag=method_frame.delivery_tag)
    if method_frame:
        columns = ["Product ID", "Product Name", "Product Quantity", "Product Price"]
        data = json.loads(body)
        return render_template("view_records.html", records=data, colnames=columns)
    else:
        return "No records found"

@app.route('/delete_record', methods=['GET'])
def delete_record():
    id = request.args.get('id')
    channel.basic_publish(exchange='deletion', routing_key='deletion_queue', body=id)
    return "Added to deletion queue"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
