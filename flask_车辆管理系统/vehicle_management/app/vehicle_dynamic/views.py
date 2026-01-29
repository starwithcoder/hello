from flask import jsonify,g
from . import vehicle_dynamic_bp
from vehicle_management import db

from datetime import datetime
from flask import request
from vehicle_management.models import VehicleDynamic
from vehicle_management.utils.decorators import require_permission

# 增加
@vehicle_dynamic_bp.route('', methods=['POST'])
def add_vehicle_dynamic():
    print('======add vehicle dynamic======')
    data  = request.get_json()
    new_vehicle_dynamic = VehicleDynamic(
    plate_number = data['plate_number'],
    fault_phenomenon = data['fault_phenomenon'],
    start_date = data['start_date'].replace('T', ' ').replace('Z', '').split('.')[0],
    end_date = data['end_date'].replace('T', ' ').replace('Z', '').split('.')[0],
    related_personnel = data['related_personnel'],
    remarks = data.get('remarks', None)
    )
    db.session.add(new_vehicle_dynamic)
    db.session.commit()
    return jsonify({'message': 'Vehicle dynamic added successfully'}), 201

# 查询
@vehicle_dynamic_bp.route('', methods=['GET'])
def get_vehicle_dynamics():
    print('======get vehicle dynamics======')

    vehicle_dynamics = VehicleDynamic.query.all()
    return jsonify([vehicle_dynamic.to_dict() for vehicle_dynamic in vehicle_dynamics])
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