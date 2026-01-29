
from flask import Blueprint

vehicle_change_bp = Blueprint('vehicle_change', __name__, url_prefix='/api/vehicle_change/')

from . import views


