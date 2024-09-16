# Kafka + Python Image Streaming

## Overview
- 


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


## Improvements / Next Steps
- Used a simple resize technique from OpenCV to resize + interpolate the images so they are <1MB. Other techniques such as compression with JPEG/PNG or to grayscale (if applicable) or other compression techniques could be tried and might be better. 
- Use Customer ID to only consume those messages that contain a particular Customer ID (for multi-customer setting)
- 