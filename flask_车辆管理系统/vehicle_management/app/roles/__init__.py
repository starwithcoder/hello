from flask import Blueprint


roles = Blueprint('roles', __name__, url_prefix='/api/roles/')

from . import views