from werkzeug.security import generate_password_hash, check_password_hash
import logging

from repository import user_repository
from models.dto.user_login_dto import UserLoginDto
from models.dto.user_updatedpassword_dto import UserUpdatePasswordDto

_logger = logging.getLogger(__name__)

class UserService:

    def get_user(self, user_id):
        user_rep = user_repository.UsersRepository()
        return user_rep.get_user(user_id)

    def create_user(self, data):
        data.password = generate_password_hash(data.password)
        user_rep = user_repository.UsersRepository()
        return user_rep.create_user(data)

    def login_user(self, email, password):
        res = UserLoginDto()
        user_rep = user_repository.UsersRepository()
        user = user_rep.get_user_by_email(email)
        if not user:
            return res
        
        is_authenticated = check_password_hash(user.password, password)
        logging.info('Check password')
        logging.info(is_authenticated)
        if is_authenticated:
            res = UserLoginDto(id=user.id, firstname=user.firstname, lastname=user.lastname, email=user.email, isauthenticated=is_authenticated)

        return res
    
    def update_password(self, user_id, password):
        res = UserLoginDto()
        user_rep = user_repository.UsersRepository()
        
        _logger.info(f'User Id during update password is {user_id}')
        user = user_rep.get_user(user_id)
        if not user:
            return res
        
        h_password = generate_password_hash(password)
        updated_user = user_rep.update_password(user_id, h_password)
        res = UserUpdatePasswordDto(id=updated_user.id, firstname=updated_user.firstname, lastname=updated_user.lastname, email=updated_user.email, issuccess=True)
        return res
        
