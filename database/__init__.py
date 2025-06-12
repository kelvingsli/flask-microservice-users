from flask import Blueprint

bp = Blueprint('repository', __name__)

from database import user_store
