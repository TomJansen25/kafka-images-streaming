import json
import time
from datetime import datetime

from kafka import KafkaConsumer
from pymongo import MongoClient


class ImageDataConsumer:
    def __init__(self, customer_id):
        self.customer_id = customer_id

        # Kafka Consumer setup
        self.consumer = KafkaConsumer(
            "data-stream",
            bootstrap_servers="localhost:9092",
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        )

        # MongoDB setup
        self.client = MongoClient(
            host="localhost", port=27017, username="root", password="example"
        )
        self.db = self.client["image_data_store"]
        self.collection = self.db["images"]

    def consume_and_store(self):
        for message in self.consumer:
            # Decode the received message
            data = message.value
            # Store the data in MongoDB
            self.store_image_data(data)

    def store_image_data(self, data):
        # Prepare document with metadata
        document = {
            "customer_id": data["customer_id"],
            "image_data": data["image_data"],  # Store image data in BSON format
            "creation_timestamp": datetime.now().isoformat(),
            "storage_timestamp": datetime.now().isoformat(),
            "additional_info": data.get("additional_info", {}),
        }
        # Insert document into MongoDB
        self.collection.insert_one(document)
        print(f"Stored image data for Customer ID: {data['customer_id']}")


if __name__ == "__main__":
    print("Starting Kafka consumer to store image data...")
    # Initialize the generator with a random Customer ID C1 and start streaming
    consumer = ImageDataConsumer(customer_id="C1")
    consumer.consume_and_store()
