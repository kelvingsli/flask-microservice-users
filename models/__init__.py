from flask import Blueprint

bp = Blueprint('models', __name__)

from models.entity import user
from models.dto import user_dto
