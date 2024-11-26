import sys
import os
import grpc
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from proto import bidi_pb2_grpc, bidi_pb2
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime
import time


def send_stream_messages():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = bidi_pb2_grpc.BidiServiceStub(channel)
        for response in stub.GetStreamMessages(generate_messages()):
            if response.HasField("success"):
                print(f"Success: {response.success.code}")
            elif response.HasField("error"):
                print(f"Error: {response.error.description}")

def generate_messages():
    for i in range(5):
        timestamp = Timestamp()
        timestamp.FromDatetime(datetime.utcnow())
        yield bidi_pb2.InitialRequest(
            sourceSystem="SystemA",
            publicationTime=timestamp,
            sessionId="session123",
            messageId=f"msg{i}",
            messageText=f"Hello, World {i}!",
            messageWithContext="Some context"
        )
        time.sleep(1)

if __name__ == '__main__':
    send_stream_messages()
