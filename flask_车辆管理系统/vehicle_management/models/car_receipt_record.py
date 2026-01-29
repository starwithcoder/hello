from .. import db
from datetime import datetime
# 车辆收据记录模型
class CarReceiptRecord(db.Model):
    __tablename__ = 'car_receipt_records'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    plate_number = db.Column(db.String(20), nullable=False)
    receipt_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    
    def __repr__(self):
        return f'<CarReceiptRecord {self.name} - {self.plate_number}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'plate_number': self.plate_number,
            'receipt_date': self.receipt_date.strftime('%Y-%m-%d')
        }
