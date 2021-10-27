import os
import json
from typing import Dict
from kafka import KafkaConsumer
from sqlalchemy import create_engine
from sqlalchemy.sql import text

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

TOPIC_NAME = 'locations'
KAFKA_SERVER = 'kafka-release.default.svc.cluster.local:9092'
#KAFKA_SERVER = 'localhost:9092'

consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[KAFKA_SERVER])


def save_location(location: Dict):
    person_id = int(location["person_id"])
    latitude = location["latitude"]
    longitude = location["longitude"]

    try:
        engine = create_engine(
            f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
        conn = engine.connect()
        sql = text(
            "INSERT INTO location (person_id, coordinate) VALUES (:person_id, ST_Point(:latitude,:longitude))")
        conn.execute(sql, {"person_id": person_id,
                     "latitude": latitude, "longitude": longitude})
    except:
        print('Insertion Error!')


for message in consumer:
    location_json = message.value.decode('utf-8')
    print(location_json)
    location_dict = json.loads(location_json)
    save_location(location_dict)
    print('saved')
