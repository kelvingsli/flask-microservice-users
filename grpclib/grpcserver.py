from concurrent import futures
import grpc
import logging

import app
import grpclib.useraccount_pb2_grpc as useraccount_pb2_grpc
import grpclib.useraccount_pb2 as useraccount_pb2
from services import user_service
from models import user_dto

_logger = logging.getLogger(__name__)

class UserAccountService(useraccount_pb2_grpc.UserAccountServicer):

    def flask_appctx(f):
        '''
        Decorator to inject app context into all grpc method calls
        '''
        def inner(*args, **kwargs):
            with app.app.app_context():
                return f(*args, **kwargs)
        return inner

    @flask_appctx
    def GetUser(self, request, context):
        svc = user_service.UserService()
        personData = svc.get_user(request.UserId)
        response = useraccount_pb2.User(UserId=personData.id, FirstName=personData.firstname, LastName=personData.lastname, Email=personData.email)
        return response
    
    @flask_appctx
    def CreateUser(self, request, context):
        response = None
        try:
            _logger.info('Getting grpc request...')
            _logger.info(request)
            svc = user_service.UserService()
            data = user_dto.UserDto()
            data.firstname = request.FirstName
            data.lastname = request.LastName
            data.email = request.Email
            data.password = request.Password

            personData = svc.create_user(data)

            _logger.info('After adding into database...')
            _logger.info(personData.id)
            response = useraccount_pb2.User(UserId=personData.id, FirstName=personData.firstname, LastName=personData.lastname, Email=personData.email)
        except Exception as err:
            _logger.error(err)
        return response
    
    @flask_appctx
    def LoginUser(self, request, context):  
        isAuthenticated = False
        res_User = useraccount_pb2.User()
        try:
            svc = user_service.UserService()
            data = svc.login_user(email=request.Email, password=request.Password)
            if data.isauthenticated:
                isAuthenticated = data.isauthenticated
                res_User = useraccount_pb2.User(UserId=data.id, FirstName=data.firstname, LastName=data.lastname, Email=data.email)
        except Exception as err:
            _logger.error(err)
        return useraccount_pb2.LoginUserResponse(IsSuccess=isAuthenticated, User=res_User)

    
def serve(port=50051):
    try:
        server = grpc.server((futures.ThreadPoolExecutor(max_workers=10)))
        useraccount_pb2_grpc.add_UserAccountServicer_to_server(UserAccountService(), server)
        server.add_insecure_port(f'[::]:{port}')
        logging.info(f'server started running on port [::]:{port}')
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        logging.info('Shutting down gRPC server...')
    except Exception as err:
        _logger.error(err)
        raise err

if __name__ == '__main__':
    serve()
