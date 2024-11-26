import grpc
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from proto import bidi_pb2_grpc, bidi_pb2
from concurrent.futures import ThreadPoolExecutor


def get_session_data():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = bidi_pb2_grpc.BidiServiceStub(channel)
        for response in stub.GetSessionData(generate_session_requests()):
            if response.HasField("success"):
                print(f"Success: {response.success.code}")
            elif response.HasField("error"):
                print(f"Error: {response.error.description}, Code: {response.error.errorCode}")

def generate_session_requests():
    session_ids = ["session123"]
    for session_id in session_ids:
        yield bidi_pb2.InitialSessionRequest(sessionId=session_id)
        time.sleep(1)

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(get_session_data) for _ in range(10)]

    for future in futures:
        future.result()
