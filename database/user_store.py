from app import db
from models.entity.user import User
from models.dto.user_dto import UserDto

class UserStore:

    def get_user(self, user_id):
        user = User()
        user = db.one_or_404(db.select(User).filter_by(id=user_id))
        return UserDto(id=user.id, firstname=user.first_name, lastname=user.last_name, email=user.email)

    def create_user(self, data):
        user = User()
        user.first_name = data.firstname
        user.last_name = data.lastname
        user.email = data.email
        user.passwordhash = data.password
        db.session.add(user)
        db.session.commit()
        return UserDto(id=user.id, firstname=user.first_name, lastname=user.last_name, email=user.email)
    
    def get_user_by_email(self, email):
        res = UserDto()
            
        user = db.one_or_404(db.select(User).filter_by(email=email))
        if user:
            res = UserDto(id=user.id, firstname=user.first_name, lastname=user.last_name, email=user.email, password=user.passwordhash)
        return res
    
    def update_password(self, user_id, password):
        user = db.one_or_404(db.select(User).filter_by(id=user_id))
        user.passwordhash = password
        db.session.add(user)
        db.session.commit()
        return UserDto(id=user.id, firstname=user.first_name, lastname=user.last_name, email=user.email)
