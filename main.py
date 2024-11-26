import grpc
from concurrent import futures
from proto import bidi_pb2_grpc
from src.bidi_server import BidiService

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=15))
    bidi_pb2_grpc.add_BidiServiceServicer_to_server(BidiService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Shutting down server...")
        server.stop(0)

if __name__ == '__main__':
    serve()
