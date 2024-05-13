from sqlalchemy import Column, ForeignKey, Integer, String

from app import db

class User(db.Model):
   
   __tablename__ = 'hrb_users'
   id = Column(Integer, primary_key=True)
   first_name = Column(String(250), nullable=False)
   last_name = Column(String(250), nullable=False)
   email = Column(String(250), nullable=False, unique=True)
   passwordhash = Column(String(250))

