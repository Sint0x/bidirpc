import grpc
import time
import sys
import os
from multiprocessing import Process, Lock
from concurrent.futures import ThreadPoolExecutor

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from proto import bidi_pb2_grpc, bidi_pb2


lock = Lock()


def get_session_data():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = bidi_pb2_grpc.BidiServiceStub(channel)
        with lock:
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
    processes = []
    for _ in range(3):
        process = Process(target=get_session_data)
        process.start()
        processes.append(process)

    for process in processes:
        process.join()
