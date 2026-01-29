
from flask import Blueprint

# 创建用户模块蓝图
vehicle_dynamic_bp = Blueprint('vehicle_dynamic', __name__, url_prefix='/api/vehicle_dynamic/')

from . import views