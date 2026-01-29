from flask import Flask
from vehicle_management.utils.middlewares import register_auth_middleware
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from vehicle_management.config import config
from flask_cors import CORS
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
import os




# 创建数据库实例
db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(config_name='default'):
    # 创建Flask应用实例
    app = Flask(__name__)
    # 加载flask-restx

    # 加载配置
    app.config.from_object(config[config_name])

    CORS(
        app,
        resources={r"/api/*": {"origins": "http://localhost:5173"}},  # 仅 /api/* 路径 + 仅允许 Vue 源
        supports_credentials=True  # 如果需要携带 Cookie（如 session）
    )



        # 创建 RotatingFileHandler
    file_handler = RotatingFileHandler(
            os.path.join(app.root_path, 'logs', 'app.log'),          # 日志文件路径
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,            # 保留5个旧日志文件
            encoding = 'utf-8'
        )
    file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
    file_handler.setLevel(logging.INFO)

        # 添加到 app.logger
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Application startup')
    # ====== 日志配置结束 =====





    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)

    # 注册中间件
    # register_auth_middleware(app)

    # 注册模型
    from .models import load

    # 注册蓝图
    from vehicle_management.app.user import user_bp
    from vehicle_management.app.drivers import driver_profile_bp
    from vehicle_management.app.cars import car_inventory_bp
    from vehicle_management.app.vehicle_change import vehicle_change_bp
    from vehicle_management.app.driver_return import driver_return_bp
    from vehicle_management.app.accident_record import accident_record_bp
    from vehicle_management.app.vehicle_dynamic import vehicle_dynamic_bp
    from vehicle_management.app.car_receipt_record import car_receipt_record_bp
    from vehicle_management.app.permissions import permissions
    from vehicle_management.app.roles import roles

    app.register_blueprint(user_bp)

    app.register_blueprint(driver_profile_bp)

    app.register_blueprint(car_inventory_bp)

    app.register_blueprint(vehicle_change_bp)

    app.register_blueprint(driver_return_bp)

    app.register_blueprint(accident_record_bp)

    app.register_blueprint(vehicle_dynamic_bp)

    app.register_blueprint(car_receipt_record_bp)

    app.register_blueprint(permissions)

    app.register_blueprint(roles)


    return app
