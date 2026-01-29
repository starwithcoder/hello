from flask import jsonify
from . import car_receipt_record_bp
from flask import request
from datetime import datetime
from vehicle_management import db

from vehicle_management.models import CarReceiptRecord,Drivers,Cars
from sqlalchemy.orm import selectinload

#增加
@car_receipt_record_bp.route('', methods=['POST'])
def add_car_receipt_record():
    print('======add car receipt record======')
    data  = request.get_json()
    driver_id =data.get('id')
    name = data.get('name')
    plate_number = data.get('plate_number')
    receipt_date = data.get('receipt_date')
    print(id,name,plate_number,receipt_date)

    driver = Drivers.query.options(selectinload(Drivers.cars)).filter_by(id=driver_id).first()
    print('===================================')
    if driver:

        car = [car for car in driver.cars if car.plate_number == plate_number]
        if car[0]:
            car[0].is_in_use = False
            car[0].driver_id = None

            new_car_receipt_record = CarReceiptRecord(
            name = name,
            plate_number = plate_number,
            receipt_date = receipt_date
            )
            try:
                db.session.add(new_car_receipt_record)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return jsonify({'message': 'Error adding car receipt record', 'error': str(e)}), 500
    return jsonify({'message': 'Car receipt record added successfully'}), 201



#更新
@car_receipt_record_bp.route('/<int:id>', methods=['PUT'])
def update_car_receipt_record(id):
    print(f'======update car receipt record@@@@@@@{id}======')
    car_receipt_record = CarReceiptRecord.query.get(id)
    if not car_receipt_record:
        return jsonify({'message': 'Car receipt record not found'}), 404
    data = request.get_json()
    files = request.files
    try:
        car_receipt_record.name = data['name']
        car_receipt_record.plate_number = data['plate_number']
        car_receipt_record.receipt_date = data['receipt_date'].replace('T', ' ').replace('Z', '').split('.')[0]
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating car receipt record', 'error': str(e)}), 500
    return jsonify({'message': 'Car receipt record updated successfully'}), 200

#删除
@car_receipt_record_bp.route('/<int:id>', methods=['DELETE'])
def delete_car_receipt_record(id):
   print('======delete car receipt record======')
   car_receipt_record = CarReceiptRecord.query.get(id)
   if not car_receipt_record:
       return jsonify({'message': 'Car receipt record not found'}), 404
   try:
       db.session.delete(car_receipt_record)
       db.session.commit()
   except Exception as e:
       db.session.rollback()
       return jsonify({'message': 'Error deleting car receipt record', 'error': str(e)}), 500
   return jsonify({'message': 'Car receipt record deleted successfully'}), 200
#查询
@car_receipt_record_bp.route('', methods=['GET'])
def get_car_receipt_record():
    print('======查询-car_receipt_record======')
    car_receipt_records = CarReceiptRecord.query.all()
    data = []
    for car_receipt_record in car_receipt_records:
        car_receipt_record_dict = car_receipt_record.to_dict()
        data.append(car_receipt_record_dict)
    return jsonify({'data':data,'msg':'success','code':20000}), 200