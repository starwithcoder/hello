from .. import db
from datetime import datetime
# 司机归还记录模型
class DriverReturn(db.Model):
    __tablename__ = 'driver_returns'
    
    id = db.Column(db.Integer, primary_key=True)
    driver_name = db.Column(db.String(50), nullable=False)
    platform = db.Column(db.String(50),default='oo')
    plate_number = db.Column(db.String(20), nullable=False)
    driver_phone = db.Column(db.String(20), nullable=False)
    registration_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    is_over_30_days = db.Column(db.Boolean, nullable=False, default=False)
    is_over_60_days = db.Column(db.Boolean, nullable=False, default=False)
    is_over_90_days = db.Column(db.Boolean, nullable=False, default=False)
    remarks = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<DriverReturn {self.driver_name} - {self.plate_number}>'

    
    def to_dict(self):
        return {
            'id': self.id,
            'driver_name': self.driver_name,
            'platform': self.platform,
            'plate_number': self.plate_number,
            'driver_phone': self.driver_phone,
            'registration_date': self.registration_date.isoformat(),
            'return_date': self.return_date.isoformat(),
            'is_over_30_days': self.is_over_30_days,
            'is_over_60_days': self.is_over_60_days,
            'is_over_90_days': self.is_over_90_days,
            'remarks': self.remarks
        }
        