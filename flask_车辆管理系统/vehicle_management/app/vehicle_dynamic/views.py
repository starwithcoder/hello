from flask import jsonify,g
from . import vehicle_dynamic_bp
from vehicle_management import db

from datetime import datetime
from flask import request
from vehicle_management.models import VehicleDynamic,Cars
from vehicle_management.utils.decorators import require_permission

# 增加
@vehicle_dynamic_bp.route('', methods=['POST'])
def add_vehicle_dynamic():
    print('======add vehicle dynamic======')
    data  = request.get_json()

    plate_number = data.get('plate_number')
    fault_phenomenon = data.get('fault_phenomenon')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    related_personnel = data.get('related_personnel')
    remarks = data.get('remarks', None)

    car = Cars.query.filter_by(plate_number=plate_number).first()
    if car:
        new_vehicle_dynamic = VehicleDynamic(
        plate_number = plate_number,
        fault_phenomenon = fault_phenomenon,
        start_date = start_date,
        end_date = end_date,
        related_personnel = related_personnel,
        remarks = remarks
        )
        try:
            db.session.add(new_vehicle_dynamic)
            db.session.commit()
        except Exception as e:
            return jsonify({'message': 'Vehicle dynamic add failed', 'error': str(e)}), 500
        return jsonify({'message': 'Vehicle dynamic added successfully'}), 201
    else:
        return jsonify({'message': 'Vehicle dynamic not found'}), 404

# 查询
@vehicle_dynamic_bp.route('', methods=['GET'])
def get_vehicle_dynamics():
    print('======get vehicle dynamics======')
    data = []
    vehicle_dynamics = VehicleDynamic.query.order_by(VehicleDynamic.id).limit(10).all()
    for vehicle_dynamic in vehicle_dynamics:
        vehicle_dynamic_dict = vehicle_dynamic.to_dict()
        data.append(vehicle_dynamic_dict)

    return jsonify({'message': 'Vehicle dynamics retrieved successfully', 'data': data}), 200
# 更新
@vehicle_dynamic_bp.route('/<int:id>', methods=['PUT'])
def update_vehicle_dynamic(id):
    print(f'======update vehicle dynamic@@@@@@@{id}======')
    vehicle_dynamic = VehicleDynamic.query.get(id)
    if not vehicle_dynamic:
        return jsonify({'message': 'Vehicle dynamic not found'}),
    data = request.get_json()
    try:
        vehicle_dynamic.plate_number = data['plate_number']
        vehicle_dynamic.fault_phenomenon = data['fault_phenomenon']
        vehicle_dynamic.start_date = data['start_date'].replace('T', ' ').replace('Z', '').split('.')[0]
        vehicle_dynamic.end_date = data.get('end_date', None)
        vehicle_dynamic.related_personnel = data['related_personnel']
        vehicle_dynamic.remarks = data.get('remarks', None)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Vehicle dynamic update failed', 'error': str(e)}), 500
    return jsonify({'message': 'Vehicle dynamic updated successfully'})


# 删除
@vehicle_dynamic_bp.route('/<int:id>', methods=['DELETE'])
def delete_vehicle_dynamic(id):
    print(f'======delete vehicle dynamic@@@@@@@{id}======')
    vehicle_dynamic = VehicleDynamic.query.get(id)
    if not vehicle_dynamic:
        return jsonify({'message': 'Vehicle dynamic not found'}),
    try:
        db.session.delete(vehicle_dynamic)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Vehicle dynamic delete failed', 'error': str(e)}), 500
    return jsonify({'message': 'Vehicle dynamic deleted successfully'})