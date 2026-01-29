from flask import Blueprint

# 创建车辆库存管理蓝图
car_inventory_bp = Blueprint('cars', __name__, url_prefix='/api/cars/')



# 导入视图模块以注册路由
from . import views
