from .. import db
from datetime import datetime

# 车辆动态模型
class VehicleDynamic(db.Model):
    __tablename__ = 'vehicle_dynamics'
    
    id = db.Column(db.Integer, primary_key=True)
    plate_number = db.Column(db.String(20), nullable=False)
    fault_phenomenon = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    end_date = db.Column(db.Date, nullable=True)
    related_personnel = db.Column(db.String(100), nullable=False)
    remarks = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<VehicleDynamic {self.plate_number} - {self.fault_phenomenon[:20]}...>'

    def to_dict(self):
        return {
            'id': self.id,
            'plate_number': self.plate_number,
            'fault_phenomenon': self.fault_phenomenon,
            'start_date': self.start_date.strftime('%Y-%m-%d'),
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'related_personnel': self.related_personnel,
            'remarks': self.remarks
        }
