import pytest
import grpc

from app import app as flask_app
from grpclib import grpcserver, useraccount_pb2_grpc
import grpclib.useraccount_pb2 as up

@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def grpc_server():
    grpcserver.serve()

# @pytest.fixture
# def grpc_client():
#     with grpc.insecure_channel(f'localhost:50051') as channel:
#         stub = useraccount_pb2_grpc.UserAccountStub(channel)
#         response = stub.LoginUser(up.User(name='Jack'))