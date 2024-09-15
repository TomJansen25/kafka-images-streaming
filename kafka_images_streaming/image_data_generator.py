import time

import numpy as np


class ImageDataGenerator:
    """
    Class to generate image-like data for a given customer ID and stream it to Kafka
    """

    def __init__(self, customer_id):
        self.customer_id = customer_id

    def generate_image_data(self):
        # Generate a random image-like array of shape (1920, 1080, 3)
        image_data = np.random.randint(0, 256, (1920, 1080, 3), dtype=np.uint8)
        return image_data

    def update_customer_id(self, new_customer_id):
        self.customer_id = new_customer_id

    def stream_images(self):
        while True:
            # Generate image data
            image_data = self.generate_image_data()
            print(f"Generated new image for Customer ID: {self.customer_id}")

            # Print image shape and data type for debugging / checking
            print(f"Image shape: {image_data.shape}, Data type: {image_data.dtype}")

            # Wait for 1 second to generate an image every second
            time.sleep(1)


# Example usage
if __name__ == "__main__":
    # Initialize the generator with a random Customer ID C1 and start streaming
    generator = ImageDataGenerator(customer_id="C1")
    generator.stream_images()
