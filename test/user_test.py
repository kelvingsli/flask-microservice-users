import grpc
import pytest

from app import app as flask_app
from grpclib import useraccount_pb2_grpc, useraccount_pb2


@pytest.fixture
def app():
    yield flask_app


def test_user_login(grpc_server):
    with grpc.insecure_channel(f'localhost:50051') as channel:
        stub = useraccount_pb2_grpc.UserAccountStub(channel)
        response = stub.LoginUser(useraccount_pb2.LoginUserRequest(Email='1@test.com', Password='12345'))
        expected_user = useraccount_pb2.User(UserId=1, FirstName='Tester1', LastName='One', Email='1@test.com')
        print('Testing...')
        assert response.IsSuccess == True
        assert response.User == expected_user
