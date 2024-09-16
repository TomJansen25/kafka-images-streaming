import numpy as np
from pydantic import BaseModel, Field


class ImageDataModel(BaseModel):
    customer_id: str = Field(..., min_length=1)
    message_id: int = Field(..., ge=0)
    image_data: str
    creation_timestamp: float

    # Custom validation
    @classmethod
    def validate_image_data(cls, v: str):
        try:
            # Decode hex string and ensure it can be converted to the original image shape
            image_data_bytes = bytes.fromhex(v)
            image_data_array = np.frombuffer(image_data_bytes, dtype=np.uint8).reshape(
                (1920, 1080, 3)
            )
            return image_data_array
        except Exception as e:
            raise ValueError(f"Invalid image data: {e}")
