import pika
import mysql.connector
import json
import os

source_ip = os.getenv('SOURCE_IP')

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(source_ip, 5672, '/', credentials))

channel = connection.channel()
channel.exchange_declare(exchange='deletion', exchange_type='direct')
channel.queue_declare(queue='deletion_queue')
channel.queue_bind(exchange='deletion', queue='deletion_queue')

mydb = mysql.connector.connect(
    host="mysql_container",
    user="root",
    database="student_project",
    password="2002"
)
c = mydb.cursor()

def callback(ch, method, properties, body):
    print("Received message for deleting record: {}".format(body))
    item_id = body.decode()
    # delete the record from the database
    c.execute("DELETE FROM INVENTORY_MANAGEMENT WHERE item_id=%s", (item_id,))
    mydb.commit()
    # acknowledge that the message has been received
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='deletion_queue', on_message_callback=callback)
channel.start_consuming()



