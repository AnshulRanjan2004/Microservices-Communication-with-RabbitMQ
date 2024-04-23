import pika
import mysql.connector
import json
import os

source_ip = os.getenv('SOURCE_IP')

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(source_ip, 5672, '/', credentials))

channel = connection.channel()
channel.exchange_declare(exchange='insertion', exchange_type='direct')
channel.queue_declare(queue='insertion_queue')
channel.queue_bind(exchange='insertion', queue='insertion_queue')

mydb = mysql.connector.connect(
    host="mysql_container",
    user="root",
    database="student_project",
    password="2002"
)
c = mydb.cursor()

def callback(ch, method, properties, body):
    data = json.loads(body)
    print("Received message for inserting record: {}".format(data))
    # insert the record into the database
    c.execute("INSERT INTO INVENTORY_MANAGEMENT (name, item_id, qty) VALUES (%s, %s, %s)", (data["name"], data["item_id"], data["qty"]))
    mydb.commit()
    # acknowledge that the message has been received
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='insertion_queue', on_message_callback=callback)
channel.start_consuming()



