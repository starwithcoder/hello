from flask import Blueprint, render_template, request, redirect, url_for, flash
from vehicle_management.models import CarChangeRecord as VehicleChangeRecord
from vehicle_management import db
from . import vehicle_change_bp
import random
from flask import jsonify
from vehicle_management.models import Drivers,Cars
from sqlalchemy.orm import selectinload
# 查询所有变更记录
@vehicle_change_bp.route('/')
def index():
    print('===============vehicle_change.index========================')
    records = VehicleChangeRecord.query.all()
    return jsonify([record.to_dict() for record in records]), 200

# 新增变更记录
@vehicle_change_bp.route('/add', methods=['GET', 'POST'])
def add():
    print('===============vehicle_change.add========================')
    data = request.get_json()
    driver_id = data['id']
    driver_name = data['driver_name']
    change_time = data['change_time']
    original_plate = data['original_plate']
    new_plate = data['new_plate']

    driver = Drivers.query.options(selectinload(Drivers.cars)).filter_by(id=driver_id).first()
    print('===================================')
    if driver:
        driver_platform = driver.platform
        driver_phone = driver.driver_phone
        #如果纯在原车
        if original_plate:
            car = [car for car in driver.cars if car.plate_number == original_plate]
            if car[0]:
                car[0].is_in_use = False
                car[0].driver_id = None
        car = Cars.query.filter_by(plate_number=new_plate).first()
        car.driver_id = driver_id
        vehicleChangeRecord = VehicleChangeRecord(
            id=driver_id,
            driver_name=driver_name,
            change_time=change_time,
            original_plate=original_plate,
            new_plate=new_plate,
            
        )
       
        db.session.add(vehicleChangeRecord)
        db.session.commit()
        flash('新增成功')
        return jsonify(vehicleChangeRecord.to_dict()), 201
    else:
        return jsonify({'data':'','msg':'driver is not exist'})
   


 # id = random.randint(1000, 9999)
        # driver_name = request.form.get('driver_name')
        # change_time = request.form.get('change_time')
        # original_plate = request.form.get('original_plate')
        # new_plate = request.form.get('new_plate')
# 修改变更记录
@vehicle_change_bp.route('/edit/<int:record_id>', methods=['PUT'])
def edit(record_id):
    record = VehicleChangeRecord.query.get_or_404(record_id)
    if request.method == 'PUT':
        data = request.get_json()
        record.driver_name = data['driver_name']
        record.change_time = data['change_time']
        record.original_plate = data['original_plate']
        record.new_plate = data['new_plate']
        db.session.commit()
        flash('修改成功')
        return jsonify(record.to_dict()), 200
    return render_template('vehicle_change/edit.html', record=record)

# 删除变更记录
@vehicle_change_bp.route('/delete/<int:record_id>', methods=['DELETE'])
def delete(record_id):
    print(f'===============vehicle_change.delete{record_id}========================')
    record = VehicleChangeRecord.query.get_or_404(record_id)
    db.session.delete(record)
    db.session.commit()
    flash('删除成功')
    return jsonify({'code': 200, 'msg': 'success'}), 200
