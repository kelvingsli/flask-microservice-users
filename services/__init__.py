from flask import Blueprint

bp = Blueprint('services', __name__)

from services import user_service
