import pytest

from pydantic import ValidationError
from kafka_images_streaming.image_data_consumer import ImageDataModel


def test_valid_image_data():
    # Example of valid input data
    valid_data = {
        "customer_id": "CUST123",
        "message_id": 1,
        "image": "00ff..." * (480 * 270 * 3 // 2),  # Mock hex data
        "timestamp": 1630611212.123,
    }
    # Should not raise a validation error
    validated_model = ImageDataModel(**valid_data)
    assert isinstance(validated_model, ImageDataModel)

def test_invalid_customer_id():
    # Example of invalid input data with empty customer_id
    invalid_data = {
        "customer_id": "",
        "array_id": 1,
        "image": "00ff..." * (480 * 270 * 3 // 2),
        "timestamp": 1630611212.123,
    }
    with pytest.raises(ValidationError):
        ImageDataModel(**invalid_data)

def test_invalid_image_data():
    # Example of invalid input data with malformed image data
    invalid_data = {
        "customer_id": "CUST123",
        "array_id": 1,
        "image": "zzzz",  # Invalid hex data
        "timestamp": 1630611212.123,
    }
    with pytest.raises(ValidationError):
        ImageDataModel(**invalid_data)
