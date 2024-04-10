import pika, json
from sqlalchemy import create_engine, Column, Integer, String, Float

from sqlalchemy.orm import sessionmaker,declarative_base

credentials = pika.PlainCredentials('user', 'pass')
parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)

# params = pika.URLParameters('amqp://user:pass@localhost:5672/%2f')
# connection = pika.BlockingConnection(parameters)
# channel = connection.channel()
# channel.queue_declare(queue='createItem')

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@db:3306/inventory"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
class InventoryItem(Base):
    __tablename__ = "inventory_items"

    item_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    category = Column(String(50))

Base = declarative_base()

def callback(body):
    item_data = json.loads(body)
    print(item_data)
    # Create a new database session
    db = SessionLocal()

    try:
        # Create a new item object
        new_item = InventoryItem(
            name=item_data['name'],
            description=item_data['description'],
            price=item_data['price'],
            quantity=item_data['quantity'],
            category=item_data['category']
        )

        # Add the item to the session
        db.add(new_item)


        # Commit the transaction
        db.commit()
        print("item added")

    except Exception as e:
        # Rollback the transaction in case of an error
        db.rollback()
        print(f"Error: {e}")

    finally:
        # Close the session
        db.close()




item_data = {
        "name": "Sample Item2",
        "description": "This is a sample item 1",
        "price": 10,
        "quantity": 0,
        "category": "Sample Category"
    }
callback(item_data)
# print('Started Consuming Create Item')

# channel.start_consuming()

# channel.close()
