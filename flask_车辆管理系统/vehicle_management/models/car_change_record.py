from .. import db
from datetime import datetime
# 车辆变更记录模型
class CarChangeRecord(db.Model):
    __tablename__ = 'car_change_records'
    
    id = db.Column(db.Integer, primary_key=True)
    driver_name = db.Column(db.String(50), nullable=False)
    change_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    original_plate = db.Column(db.String(20), nullable=False)
    new_plate = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        return f'<CarChangeRecord {self.driver_name} - {self.original_plate} → {self.new_plate}>'

    def to_dict(self):
        return {
            'id': self.id,
            'driver_name': self.driver_name,
            'change_time': self.change_time.isoformat(),
            'original_plate': self.original_plate,
            'new_plate': self.new_plate
        }