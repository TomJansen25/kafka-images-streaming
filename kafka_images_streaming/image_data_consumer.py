import json
import time

import numpy as np
from kafka import KafkaConsumer
from loguru import logger
from pydantic import ValidationError
from pymongo import MongoClient

from kafka_images_streaming.image_data_model import ImageDataModel


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
            host="localhost", port=27017, username="root", password="pass"
        )
        self.db = self.db_client["mydb"]
        self.collection = self.db["images"]

    def decode_image_data(self, image_data: str) -> np.ndarray:
        """
        Decodes the hex-encoded image data back to its original NumPy array format.
        """
        # Convert hex string back to bytes
        image_data_bytes = bytes.fromhex(image_data)
        # Convert bytes back to a NumPy array with the compressed shape (480, 270, 3)
        image_data_array = np.frombuffer(image_data_bytes, dtype=np.uint8).reshape(
            (480, 270, 3)
        )
        return image_data_array

    def store_image_data(self, data: dict):
        try:
            # Validate consumed data with Pydantic Model
            validated_consumed_data = ImageDataModel(**data)
            decoded_image = self.decode_image_data(validated_consumed_data.image)

            # Prepare and insert document to MongoDB
            document = {
                "customer_id": validated_consumed_data.customer_id,
                "message_id": validated_consumed_data.message_id,
                "image_data": decoded_image.tolist(),
                "produced_timestamp": validated_consumed_data.timestamp,
                "consumed_timestamp": time.time(),
            }
            self.collection.insert_one(document)
            logger.info(
                f"Stored image data of Message ID {validated_consumed_data.message_id} for Customer ID: {validated_consumed_data.customer_id}"
            )

        except ValidationError as e:
            logger.error(f"Validation error: {e}")

        except Exception as e:
            logger.error(f"Failed to store image data: {e}")

    def consume_and_store(self):
        for message in self.consumer:
            # Decode the received message and then call the function to validate and store it
            data: dict = message.value
            self.store_image_data(data)


if __name__ == "__main__":
    print("Starting Kafka consumer to store image data...")
    # Initialize the generator with a random Customer ID C1 and start consuming
    consumer = ImageDataConsumer(customer_id="C1")
    consumer.consume_and_store()
