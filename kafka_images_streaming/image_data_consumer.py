import json
import time
from datetime import datetime

import numpy as np
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
        self.db_client = MongoClient(
            host="localhost", port=27017, username="root", password="example"
        )
        self.db = self.db_client["mydb"]
        self.collection = self.db["images"]

    def decode_image_data(self, image_hex_string: str) -> np.ndarray:
        """
        Decodes the hex-encoded image data back to its original NumPy array format.
        """
        # Convert hex string back to bytes
        image_data_bytes = bytes.fromhex(image_hex_string)
        # Convert bytes back to a NumPy array with the original shape (1920, 1080, 3)
        image_data_array = np.frombuffer(image_data_bytes, dtype=np.uint8).reshape(
            (1920, 1080, 3)
        )

        return image_data_array

    def store_image_data(self, data: dict):
        # Prepare document with metadata
        image_data_array = self.decode_image_data(data["image_data"])

        document = {
            "customer_id": data.get("customer_id"),
            "image_data": image_data_array.tolist(),  # Store as a list for MongoDB compatibility
            "produced_timestamp": data.get("timestamp"),
            "consumed_timestamp": datetime.now().isoformat(),
            "additional_info": data.get("additional_info", {}),
        }
        # Insert document into MongoDB
        self.collection.insert_one(document)
        print(f"Stored image data for Customer ID: {data['customer_id']}")

    def consume_and_store(self):
        for message in self.consumer:
            # Decode the received message and then call the function to test and store it
            data: dict = message.value
            self.store_image_data(data)


if __name__ == "__main__":
    print("Starting Kafka consumer to store image data...")
    # Initialize the generator with a random Customer ID C1 and start streaming
    consumer = ImageDataConsumer(customer_id="C1")
    consumer.consume_and_store()
