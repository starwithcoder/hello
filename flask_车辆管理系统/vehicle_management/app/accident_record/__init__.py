from flask import Blueprint

# 创建事故记录管理蓝图
accident_record_bp = Blueprint('accident_record', __name__, url_prefix='/api/accident_record/')

from . import views
