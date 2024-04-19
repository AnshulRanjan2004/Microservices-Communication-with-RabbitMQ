import json
import logging
import pymongo
import pika

# Set up logging
logging.basicConfig(level=logging.INFO)

# Connect to MongoDB database
client = pymongo.MongoClient("mongodb://mongodb:27017/")
db = client["database"]
collection = db["ccdb"]

# RabbitMQ setup
credentials = pika.PlainCredentials(username='guest', password='guest')
parameters = pika.ConnectionParameters(host='rabbitmq', port=5672, credentials=credentials)
connection = pika.BlockingConnection(parameters=parameters)
channel = connection.channel()

# Declare the "insert_record" queue
channel.queue_declare(queue='insert_record', durable=True)

# Define a callback function to handle incoming messages
def callback(ch, method, properties, body):
    try:
        # Parse incoming message
        body = json.loads(body)
        logging.info(f"Received message: {body}")
        
        # Check if all required fields are present
        required_fields = ['product_id', 'name', 'price', 'seller_name']
        if all(field in body for field in required_fields):
            record = {
                "product_id": body['product_id'],
                "name": body['name'],
                "price": body['price'],
                "seller_name": body['seller_name'],
            }
            collection.insert_one(record)
            logging.info("Record inserted successfully.")
        else:
            logging.error("Message is missing required fields.")
        
        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logging.error(f"Error processing message: {e}")

# Start consuming messages from the "insert_record" queue
channel.basic_consume(queue='insert_record', on_message_callback=callback)

logging.info('Waiting for messages...')
channel.start_consuming()
