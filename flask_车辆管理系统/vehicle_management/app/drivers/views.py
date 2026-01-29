from flask import  request, jsonify
from vehicle_management import db
from vehicle_management.models import Drivers,Cars
from . import driver_profile_bp
import random
from sqlalchemy.orm import joinedload


# 查询所有司机档案
@driver_profile_bp.route('', methods=['GET'])
def list_drivers():

    drivers = Drivers.query.options(joinedload(Drivers.cars)).limit(10).all()

    data =[]

    for driver in drivers:
        plate_numbers = [c.plate_number for c in driver.cars]
        driver_dict = driver.to_dict()
        driver_dict['plate_numbers'] = plate_numbers
        data.append(driver_dict)


    return jsonify({'data': data,'msg':'success','code':20000}),200

# 根据ID查询单个司机档案
@driver_profile_bp.route('search', methods=['GET'])
def get_driver():
    data = request.get_json()
    driver_name = data['driver_name']
    driver_phone = data['driver_phone']
    if  driver_name and  driver_phone:
        drivers = Drivers.query.filter_by(driver_name=driver_name, driver_phone=driver_phone).all()
        return jsonify([driver.to_dict() for driver in drivers])

    if  driver_name:
        drivers = Drivers.query.filter_by(driver_name=driver_name).all()
        print([driver.to_dict() for driver in drivers])
        return jsonify([driver.to_dict() for driver in drivers])

    if  driver_phone:
        drivers = Drivers.query.filter_by(driver_phone=driver_phone).all()
        return jsonify([driver.to_dict() for driver in drivers])

# 新增司机档案
@driver_profile_bp.route('', methods=['POST'])
def create_driver():
    print('====新增====')
    data = request.get_json()
    driver_name = data['driver_name']
    driver_phone = data['driver_phone']
    remarks = data['remarks']

    print(data)
    driver = Drivers(
        driver_name = driver_name,# 司机姓名
        driver_phone = driver_phone,# 司机手机号
        remarks = remarks
    )
    try:
        db.session.add(driver)
        db.session.commit()
    except Exception as e:
        return jsonify({'data':'','message': str(e),'code':40000}), 400
    return jsonify({'data':driver.to_dict(),'msg':'success','code':'20001'}), 201


# 更新司机档案
@driver_profile_bp.route('<int:driver_id>', methods=['PUT'])
def update_driver(driver_id):
    print('===============================更新========================')
    data = request.get_json()
    plate_number = data.get('plate_number')
    driver = Drivers.query.filter_by(id=driver_id).first()

    if plate_number:
        car = Cars.query.filter_by(plate_number=plate_number).first()

        if car:
            print(car.driver_id)
            if  car.driver_id is None:
                print(car.driver_id)
                car.driver_id = driver.id
                print(car.driver_id)
            else:
                return jsonify({'data':'','message':'car is used','code':'40004'}), 404
        else:
            return jsonify({'data':'','message':'not exist car','code':'40004'}), 404

    if driver:
        driver.driver_name = data.get('driver_name',driver.driver_name)
        driver.driver_phone = data.get('driver_phone',driver.driver_phone)
        driver.remarks = data.get('remarks',driver.remarks)

        try:
            db.session.commit()
            return jsonify({'data':driver.to_dict(),'msg':'success','code':'20001'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'data':'','message': str(e),'code':40000}), 400
    return jsonify({'data':'','message':'not exist','code':40004}), 404


# 删除司机档案
@driver_profile_bp.route('<int:driver_id>', methods=['DELETE'])
def delete_driver(driver_id):
    print(driver_id)
    driver = Drivers.query.filter_by(id=driver_id).first()
    if driver:
        try:
            db.session.delete(driver)
            db.session.commit()
            return jsonify({'data':'','msg':'success','code':20003}), 203
        except Exception as e:
            return jsonify({'data':'','message': str(e),'code':40000}), 400

    return jsonify({'data':'','message':'not exist','code':40001}), 401

