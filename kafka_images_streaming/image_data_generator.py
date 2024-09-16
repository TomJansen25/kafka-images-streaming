import cv2
import json
import time

import numpy as np
from kafka import KafkaProducer
from loguru import logger


class ImageDataGenerator:
    """
    Class to generate image-like data for a given customer ID and stream it to Kafka
    """

    def __init__(self, customer_id: str, use_kafka_producer: bool = True):
        """
        """
        self.customer_id = customer_id
        self.use_kafka_producer = use_kafka_producer
        if use_kafka_producer:
            self.producer = KafkaProducer(
                bootstrap_servers="localhost:9092",
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )

    def generate_random_image(self, resize: bool = False) -> np.ndarray:
        # Generate a random image-like array of shape (1920, 1080, 3)
        image_data = np.random.randint(
            low=0, high=256, size=(1920, 1080, 3), dtype=np.uint8
        )
        if resize:
            # Resize + interpolate image to 1/4 of the size to make it fit in a Kafka message
            image_data = cv2.resize(image_data, (480, 270), interpolation=cv2.INTER_AREA)
        return image_data

    def update_customer_id(self, new_customer_id):
        self.customer_id = new_customer_id

    def stream_images(self):
        msg_index = 1
        while True:
            # Generate image data
            image_data = self.generate_random_image(resize=True)
            logger.info(
                f"Generated random image with shape: {image_data.shape}, data type: {image_data.dtype}, and Message ID: {msg_index}"
            )

            # Create a message to send to Kafka, convert image to bytes and hex to make it serializible
            message = {
                "customer_id": self.customer_id,
                "message_id": msg_index,
                "image": image_data.tobytes().hex(),
                "timestamp": time.time(),
            }
            # Send the message to Kafka topic 'data-stream'
            if self.use_kafka_producer:
                self.producer.send("data-stream", value=message)
                logger.info(
                    f"Sent message with Customer ID {self.customer_id} and Message ID {msg_index} to Kafka."
                )

            msg_index += 1
            # Wait for 1 second to generate an image every second
            time.sleep(1)


# Example usage
if __name__ == "__main__":
    # Initialize the generator with a random Customer ID C1 and start streaming
    generator = ImageDataGenerator(customer_id="C1")
    generator.stream_images()
