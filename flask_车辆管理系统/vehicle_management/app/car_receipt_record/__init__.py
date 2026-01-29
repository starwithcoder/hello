
from flask import Blueprint

# 创建用户模块蓝图
car_receipt_record_bp = Blueprint('car_receipt_record', __name__, url_prefix='/api/carReceiptRecord/')
from . import views
