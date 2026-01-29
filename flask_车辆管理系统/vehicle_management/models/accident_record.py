from .. import db
from datetime import datetime
# 事故记录模型
class AccidentRecord(db.Model):
    __tablename__ = 'accident_records'
    
    id = db.Column(db.Integer, primary_key=True)
    occurrence_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    driver_name = db.Column(db.String(50), nullable=False)
    plate_number = db.Column(db.String(20), nullable=False)
    liability_determination = db.Column(db.String(100), nullable=False)
    accident_image_1 = db.Column(db.String(255), nullable=True)
    accident_image_2 = db.Column(db.String(255), nullable=True)
    accident_image_3 = db.Column(db.String(255), nullable=True)
    accident_image_4 = db.Column(db.String(255), nullable=True)
    case_number = db.Column(db.String(50), nullable=True)
    remarks = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<AccidentRecord {self.case_number} - {self.plate_number}>'
    def to_dict(self):
        return {
            'id': self.id,
            'occurrence_date': self.occurrence_date.strftime('%Y-%m-%d'),
            'driver_name': self.driver_name,
            'plate_number': self.plate_number,
            'liability_determination': self.liability_determination,
            'accident_image_1': self.accident_image_1,
            'accident_image_2': self.accident_image_2,
            'accident_image_3': self.accident_image_3,
            'accident_image_4': self.accident_image_4,
            'case_number': self.case_number,
            'remarks': self.remarks
        }