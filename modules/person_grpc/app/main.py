import time
import os
from concurrent import futures

import grpc
import person_pb2
import person_pb2_grpc
from sqlalchemy import create_engine
from sqlalchemy.sql import text

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]


class PersonServicer(person_pb2_grpc.PersonServiceServicer):
    def Get(self, request, context):

        try:
            engine = create_engine(
                f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
            conn = engine.connect()
            sql = text("SELECT * FROM PERSON")
            persons = conn.execute(sql).fetchall()
        except:
            print('Connection Error!')

        result = person_pb2.PersonMessageList()

        for person in persons:
            person_message = person_pb2.PersonMessage(
                id=person.id,
                first_name=person.first_name,
                last_name=person.last_name,
                company_name=person.company_name
            )
            result.persons.extend([person_message])

        return result


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
person_pb2_grpc.add_PersonServiceServicer_to_server(PersonServicer(), server)


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
