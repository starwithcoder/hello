from .. import db
from datetime import datetime

import uuid

#汽车在库档案
class Cars(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True,unique=True,autoincrement=True)
    plate_number = db.Column(db.String(20), unique=True)
    brand = db.Column(db.String(50), nullable=False,default='无')
    brand_id = db.Column(db.String(50),default=lambda :str(uuid.uuid4()))
    vehicle_model = db.Column(db.String(50), nullable=False)
    is_annual_inspected = db.Column(db.Boolean, nullable=False, default=False)
    pickup_time = db.Column(db.DateTime,nullable=False, default=datetime.now())
    is_in_use = db.Column(db.Boolean,nullable=False, default=False)

    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'))

    driver = db.relationship('Drivers', back_populates='cars')
    def __repr__(self):
        return f'<CarInventory {self.plate_number} - {self.brand} {self.vehicle_model}>'

    def to_dict(self):
        return {
            'id': self.id,
            'plate_number': self.plate_number,
            'brand': self.brand,
            'vehicle_model': self.vehicle_model,
            'is_annual_inspected': self.is_annual_inspected,
            'pickup_time': self.pickup_time.isoformat() if self.pickup_time else None,
            'is_in_use': self.is_in_use,
        }