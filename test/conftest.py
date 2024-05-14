import pytest
from concurrent import futures
import grpc

from app import app as flask_app
from grpclib import grpcserver, useraccount_pb2_grpc

@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def grpc_server():
    server = grpc.server((futures.ThreadPoolExecutor(max_workers=10)))
    useraccount_pb2_grpc.add_UserAccountServicer_to_server(grpcserver.UserAccountService(), server)
    server.add_insecure_port(f'[::]:50051')
    print('gRPC server starting...')
    server.start()
    yield server
    print('gRPC server stopping...')
    server.stop(grace=5)
