from flask import Blueprint


permissions = Blueprint('permissions', __name__, url_prefix='/api/permissions/')

from . import views