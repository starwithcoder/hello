from flask.config import T
from .. import db
from datetime import datetime
# 司机个人信息模型
class Drivers(db.Model):
    __tablename__ = 'drivers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    platform =db.Column(db.String(50))
    driver_name = db.Column(db.String(50), nullable=False)
    driver_phone = db.Column(db.String(20), nullable=False)
    remarks = db.Column(db.Text, nullable=True)
    cars = db.relationship('Cars', back_populates='driver')
    
    def __repr__(self):
        return f'<DriverProfile {self.driver_name} - {self.plate_number}>'

    def to_dict(self):
        return {
            'id': self.id,
            'platform': self.platform,
            'driver_name': self.driver_name,
            'driver_phone': self.driver_phone,
            'remarks': self.remarks

        }