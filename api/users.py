from api import bp as api_bp
from services import user_service
from models import user_dto

@api_bp.route('/', methods=['GET'])
def get_default():
    return 'Server running...'

@api_bp.route('/users/add', methods=['GET'])
def create_user():

    data = user_dto.UserDto()
    data.firstname = 'Tester3'
    data.lastname = 'Three'
    data.email = '3@test.com'
    data.password = '123456'

    svc = user_service.UserService()
    user = svc.create_user(data=data)
    
    return f'{user.id}'

