from sqlite3 import IntegrityError

from flask import Blueprint, request, jsonify
from vehicle_management.models import Drivers
from vehicle_management.models import Cars
from vehicle_management import db
from . import car_inventory_bp


# 查询所有车辆
@car_inventory_bp.route('', methods=['GET'])
def list_cars():
    print('===================查询所有车辆=====================')
    page = max(1,request.args.get('page', default=1, type=int))
    page_size = 10
    offset = (page - 1) * page_size
    
    query = Cars.query.order_by(Cars.id)
    cars = query.offset(offset).limit(page_size).all()
    total = query.count()  
    driver_ids =  [car.driver_id for car in cars if car.driver_id is not None]
    drivers_map = {}
    if driver_ids:
        drivers = Drivers.query.filter(Drivers.id.in_(driver_ids)).all()
        drivers_map = {d.id:d.driver_name for d in drivers }

    data = []
    for car in cars:
        car_dict = car.to_dict()
        car_dict['is_in_use'] = car.driver_id is not None
        car_dict['driver_name'] = drivers_map.get(car.driver_id)
        data.append(car_dict)

    return jsonify({'data':data,'total':total,'msg':'success','code':20000}),200

#url = '/cars/search'
# 查询单条车辆
@car_inventory_bp.route('search', methods=['GET'])
def get_car():
    print('===================查询单条车辆=====================')
    plate_number = request.args.get('plate_number')
    brand = request.args.get('brand')

    query = Cars.query

    if plate_number:
        query = query.filter_by(plate_number=plate_number)
    if brand:
        query = query.filter_by(brand=brand)
    total = query.count()
    cars = query.all()
    data = []
    for car in cars:
        car_dict = car.to_dict()
        data.append(car_dict)
    return jsonify({'data':data,'total':total,'msg':'success','code':20000}),200



#模糊查询车牌号
@car_inventory_bp.route('search/plateNumber')
def search_cars():
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify({'data': []})

    # 模糊查询（注意防 SQL 注入，SQLAlchemy 已处理）
    cars = Cars.query.filter(Cars.plate_number.like(f'%{q}%')).all()

    data = [{'plate_number': car.plate_number} for car in cars]
    return jsonify({'data': data})


# 新增车辆
@car_inventory_bp.route('', methods=['POST'])
def create_car():
    print('===================新增车辆=====================')

    data = request.get_json()

    pickup_time = data.get('pickup_time')
    plate_number = data.get('plate_number')
    brand = data.get('brand')
    vehicle_model = data.get('vehicle_model')
    is_annual_inspected = data.get('is_annual_inspected')

    new_car = Cars(
        plate_number=plate_number,
        brand=brand,
        vehicle_model=vehicle_model,
        is_annual_inspected=is_annual_inspected,
        pickup_time=pickup_time,
    )
    try:
        db.session.add(new_car)
        db.session.commit()
        return jsonify({'data':new_car.to_dict(),'msg':'success','code':20001}), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'data': '', 'msg':str(e) , 'code': 40000}), 400

# 修改车辆
@car_inventory_bp.route('<int:car_id>', methods=['PUT'])
def update_car(car_id):
    print('===================修改车辆=====================')
    car = Cars.query.filter_by(id=car_id).first()
    if car:
        data = request.get_json()
        try:
            car.brand = data.get('brand', car.brand)
            car.vehicle_model = data.get('vehicle_model', car.vehicle_model)
            car.is_annual_inspected = data.get('is_annual_inspected', car.is_annual_inspected)
            car.pickup_time = data.get('pickup_time',car.pickup_time)
            db.session.commit()
            return jsonify({'data':data,'msg':'success','code':20002}), 202
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'data': '', 'msg':str(e) , 'code': 40000}), 400

    return jsonify({'data': '', 'msg': 'not exist' , 'code': 40001}), 401

# 删除车辆
@car_inventory_bp.route('<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    car = Cars.query.filter_by(id=car_id).first()
    if car:
        try:
            db.session.delete(car)
            db.session.commit()
            return jsonify({'data':'', 'msg': 'success', 'code': 20003}), 203
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'data': '', 'msg': str(e) , 'code': 40000}), 400

    return jsonify({'data': '', 'msg': 'not exist' , 'code': 40001}), 401