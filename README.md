# Kafka + Python Image Streaming

## Overview
Sample project showcasing a Python + Kafka + MongoDB setup for random image streaming. Included in setup:
- Local Kafka + MongoDB instances setup with docker-compose
- Producer written in python in `image_data_producer.py`, which takes care of generating a random image and sending it to a kafka topic
- Consumer written in python in `image_data_consumer.py`, which takes care of consuming from the kafka topic, validating the messages and images and then storing the results in MongoDB


### Instructions

1. Pull code from GitHub into a folder called `kafka-images-streaming` (important for docker container names below)

2. Install python environment with poetry (or other env tool)

```shell
poetry install
```

3. Set up the Kafka on Docker instance and create the data-stream topic

```shell
docker-compose up -d
docker exec -it kafka-images-streaming-kafka-1 kafka-topics --bootstrap-server localhost:9092 --create --topic data-stream
```

4. Open up two more shells and run the producer and the composer in two separate shells

```shell
cd kafka_images_streaming
python image_data_generator.py
```

```shell
cd kafka_images_streaming
python image_data_consumer.py
```

5. Check results in MongoDB either with Mongo Shell directly or like in the `20240916_pymongo_check.ipynb`.

## Improvements / Next Steps
- Currently only used a simple resize technique from OpenCV to resize + interpolate the images so they are <1MB. Other techniques such as compression with JPEG/PNG or to grayscale (if applicable) or other compression techniques could be tried and might be better. 
- Use Customer ID to only consume those messages that contain a particular Customer ID (for multi-customer setting)
- Don't use MongoDB for the actual storage of the images. Images could/should rather be saved in some cloud or local file storage with a structured database having a column to reference the file and all of its metadata
- Include more tests - ideally also include a mock kafka instance test to test the entire pipeline
- Extend pydantic model with more information and more validation tests
- Look at other apache/kafka images - newest images e.g. don't need zookeeper anymore (but I ran into a bunch of errors trying the latest)