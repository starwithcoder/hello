

from flask import Blueprint

driver_profile_bp = Blueprint('drivers', __name__, url_prefix='/api/drivers/')

from . import views