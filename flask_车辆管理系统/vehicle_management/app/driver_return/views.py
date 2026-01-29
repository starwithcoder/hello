from . import driver_return_bp
from flask import jsonify, request
from vehicle_management.models import DriverReturn,Drivers,Cars
from vehicle_management import db
from datetime import datetime
from datetime import timedelta
from sqlalchemy.orm import selectinload

# 新增退车记录
@driver_return_bp.route('/add', methods=['POST'])
def create_driver_return():

    data = request.get_json()

    driver_id = data.get('id')
    driver_name = data.get('driver_name')
    plate_number = data.get('plate_number')
    return_date = datetime.strptime(data.get('return_date'), "%Y-%m-%d %H:%M:%S")

    remarks = data.get('remarks')

    is_over_30_days = False
    is_over_60_days = False
    is_over_90_days = False
    #Role.query.options(selectinload(Role.permissions)).all()
    driver = Drivers.query.options(selectinload(Drivers.cars)).filter_by(id=driver_id).first()
    print('===================================')
    if driver:
        driver_platform =driver.platform
        driver_phone = driver.driver_phone
        car = [car for car in driver.cars if car.plate_number == plate_number]
        if car[0]:
            car[0].is_in_use = False
            car[0].driver_id = None

            #计算是否超过多少天
            registration_date=car[0].pickup_time
            print('================2===================')
            if return_date-registration_date >= timedelta(days=30):
                is_over_30_days = True
            elif return_date-registration_date >= timedelta(days=60):
                is_over_60_days = True
            elif return_date-registration_date >= timedelta(days=90):
                is_over_90_days = True

            print('===============3====================')
            new_driver_return = DriverReturn(
                driver_name = driver_name,
                platform = driver_platform,
                plate_number = plate_number,
                driver_phone = driver_phone,
                registration_date = registration_date,
                return_date = return_date,
                is_over_30_days = is_over_30_days,
                is_over_60_days = is_over_60_days,
                is_over_90_days = is_over_90_days,
                remarks = remarks
            )
            try:
                db.session.add(new_driver_return)
                db.session.commit()
                return jsonify({'data':'','msg':'success','code':'20000'})
            except Exception as e:
                return jsonify({'data':'','msg': str(e),'code':'40004'}), 500
        else:
            return jsonify({'data':'','msg':'car is not exist','code':'40004'})
    else:
        return jsonify({'data':'','msg':'driver is not exist','code':'40004'})



# 获取所有退车记录
@driver_return_bp.route('search', methods=['GET'])
def get_driver_returns():
    print("=========get_driver_returns========")
    records = DriverReturn.query.all()
    return jsonify([record.to_dict() for record in records])


# 根据ID获取单条退车记录
@driver_return_bp.route('/driver_return/<int:record_id>', methods=['GET'])
def get_driver_return(record_id):
    record = DriverReturn.query.get_or_404(record_id)
    return jsonify({
        'id': record.id,
        'driver_name': record.driver_name,
        'platform': record.platform,
        'plate_number': record.plate_number,
        'driver_phone': record.driver_phone,
        'registration_date': record.registration_date.isoformat(),
        'return_date': record.return_date.isoformat(),
        'is_over_30_days': record.is_over_30_days,
        'is_over_60_days': record.is_over_60_days,
        'is_over_90_days': record.is_over_90_days,
        'remarks': record.remarks
    })


# 更新退车记录
@driver_return_bp.route('/<int:record_id>', methods=['PUT'])
def update_driver_return(record_id):
    record = DriverReturn.query.get_or_404(record_id)
    data = request.get_json()
    record.driver_name = data.get('driver_name', record.driver_name)
    record.platform = data.get('platform', record.platform)
    record.plate_number = data.get('plate_number', record.plate_number)
    record.driver_phone = data.get('driver_phone', record.driver_phone)
    if 'registration_date' in data:
        record.registration_date = data['registration_date'].replace('T', ' ').replace('Z', '').split('.')[0]
    if 'return_date' in data:
        record.return_date = data['return_date'].replace('T', ' ').replace('Z', '').split('.')[0]
    record.remarks = data.get('remarks', record.remarks)
    db.session.commit()
    return jsonify({'message': '更新成功'})


# 删除退车记录
@driver_return_bp.route('/<int:record_id>', methods=['DELETE'])
def delete_driver_return(record_id):
    record = DriverReturn.query.get_or_404(record_id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': '删除成功'})
