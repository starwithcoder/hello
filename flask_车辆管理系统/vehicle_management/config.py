class Config:
    """基础配置类"""
    SECRET_KEY = 'mmm'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:666666@localhost/mmm?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_vehicle_management.db'

class ProductionConfig(Config):
    """生产环境配置"""
    SECRET_KEY = 'your-production-secret-key-here'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///prod_vehicle_management.db'

# 配置映射
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
