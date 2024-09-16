import unittest

from pydantic import ValidationError

from kafka_images_streaming.image_data_consumer import ImageDataModel


class TestImageDataModel(unittest.TestCase):

    def test_valid_image_data(self):
        # Example of valid input data
        valid_data = {
            "customer_id": "CUST123",
            "message_id": 1,
            "image_data": "00ff..." * (1920 * 1080 * 3 // 2),  # Mock hex data
            "creation_timestamp": 1630611212.123,
        }
        try:
            # Should not raise a validation error
            validated_model = ImageDataModel(**valid_data)
            self.assertTrue(isinstance(validated_model, ImageDataModel))
        except ValidationError as e:
            self.fail(f"Validation failed unexpectedly: {e}")

    def test_invalid_customer_id(self):
        # Example of invalid input data with empty customer_id
        invalid_data = {
            "customer_id": "",
            "array_id": 1,
            "image_data": "00ff..." * (1920 * 1080 * 3 // 2),
            "creation_timestamp": 1630611212.123,
        }
        with self.assertRaises(ValidationError):
            ImageDataModel(**invalid_data)

    def test_invalid_image_data(self):
        # Example of invalid input data with malformed image data
        invalid_data = {
            "customer_id": "CUST123",
            "array_id": 1,
            "image_data": "zzzz",  # Invalid hex data
            "creation_timestamp": 1630611212.123,
        }
        with self.assertRaises(ValidationError):
            ImageDataModel(**invalid_data)


if __name__ == "__main__":
    unittest.main()
