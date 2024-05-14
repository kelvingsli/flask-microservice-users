import grpc
import pytest
from concurrent import futures

from app import app as flask_app
from grpclib import grpcserver, useraccount_pb2_grpc, useraccount_pb2
import grpclib.grpcserver


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture(autouse=True)
def grpc_server():
    server = grpc.server((futures.ThreadPoolExecutor(max_workers=10)))
    useraccount_pb2_grpc.add_UserAccountServicer_to_server(grpcserver.UserAccountService(), server)
    server.add_insecure_port(f'[::]:50051')
    server.start()
    yield server
    server.stop(grace=5)

def test_user_login():
    with grpc.insecure_channel(f'localhost:50051') as channel:
        stub = useraccount_pb2_grpc.UserAccountStub(channel)
        response = stub.LoginUser(useraccount_pb2.LoginUserRequest(Email='1@test.com', Password='12345'))
        expected_user = useraccount_pb2.User(UserId=1, FirstName='Tester1', LastName='One', Email='1@test.com')
        assert response.IsSuccess == True
        assert response.User == expected_user
