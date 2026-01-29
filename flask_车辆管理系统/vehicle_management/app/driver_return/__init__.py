from flask import Blueprint

driver_return_bp = Blueprint('driver_return', __name__, url_prefix='/api/driver_return/')

from . import views