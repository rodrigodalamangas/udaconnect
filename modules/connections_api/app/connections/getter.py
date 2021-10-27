import grpc
import app.connections.person_pb2 as person_pb2
import app.connections.person_pb2_grpc as person_pb2_grpc

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:30005")
stub = person_pb2_grpc.PersonServiceStub(channel)

response = stub.Get(person_pb2.Empty())

print(type(response))

for resp in response.persons:
    print(type(resp))
    print(resp)

print(response)
