from flask import Blueprint

# 创建用户模块蓝图
user_bp = Blueprint('user', __name__,url_prefix='/api/')

# 导入视图函数，确保路由注册
from . import views
