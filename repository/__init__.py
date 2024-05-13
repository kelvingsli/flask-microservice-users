from flask import Blueprint

bp = Blueprint('repository', __name__)

from repository import user_repository
