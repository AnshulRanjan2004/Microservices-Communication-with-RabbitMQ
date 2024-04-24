import pika
import mysql.connector
import json

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.0.104', 5672, '/', credentials))

channel = connection.channel()
channel.exchange_declare(exchange='deletion', exchange_type='direct')
channel.queue_declare(queue='deletion_queue')
channel.queue_bind(exchange='deletion', queue='deletion_queue')

mydb = mysql.connector.connect(
    host="192.168.0.104",
    user="root",
    database="student_records",
    password="password"
)
c = mydb.cursor()

def callback(ch, method, properties, body):
    print("Received message for deleting record: {}".format(body))
    id = body.decode()
    # delete the record from the database
    c.execute("DELETE FROM STOCK_ITEMS WHERE ProductID = %s", (id,))
    mydb.commit()
    # acknowledge that the message has been received
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='deletion_queue', on_message_callback=callback)
channel.start_consuming()



