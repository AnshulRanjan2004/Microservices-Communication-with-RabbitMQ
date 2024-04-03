
def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='create_item')

    def createItem(ch, method, properties, body):
        print(f" [x] Received {body}")

    channel.basic_consume(queue='create_item', on_message_callback=createItem, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
