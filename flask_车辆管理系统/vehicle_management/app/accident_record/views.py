from . import accident_record_bp
from flask import request, jsonify, current_app
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from vehicle_management import db
from vehicle_management.models import AccidentRecord
import random



# 允许的图片扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 新增事故记录
@accident_record_bp.route('', methods=['POST'])
def create_accident():
    print('===============accident_record.create_accident========================')
    data = request.get_json()
    print(data)
    print('==========================================================')
    #const { id, occurrence_date, driver_name, plate_number, liability_determination, case_number, remarks } = data
    new_accident_record = AccidentRecord(

        id=random.randint(1, 1000000),
        occurrence_date=data['occurrence_date'].replace('T', ' ').replace('Z', '').split('.')[0],
        driver_name=data['driver_name'],
        plate_number=data['plate_number'],
        liability_determination=data['liability_determination'],
        case_number=data['case_number'],
        remarks=data['remarks']
    )
    db.session.add(new_accident_record)
    db.session.commit()
    return jsonify({'message': '新增成功', 'id': new_accident_record.id}), 201
    

   

    # 创建记录
    record = AccidentRecord(
        occurrence_date=occurrence_date,
        driver_name=data.get('driver_name'),
        plate_number=data.get('plate_number'),
        liability_determination=data.get('liability_determination'),
        accident_image_1=image_paths.get('accident_image_1'),
        accident_image_2=image_paths.get('accident_image_2'),
        accident_image_3=image_paths.get('accident_image_3'),
        accident_image_4=image_paths.get('accident_image_4'),
        case_number=data.get('case_number'),
        remarks=data.get('remarks')
    )
    db.session.add(record)
    db.session.commit()
    return jsonify({'message': '新增成功', 'id': record.id}), 201


# 获取事故记录列表（支持分页与搜索）
@accident_record_bp.route('', methods=['GET'])
def get_accidents():
    print('===============accident_record.get_accidents========================')
     
    accident_records = AccidentRecord.query.all()
    return jsonify([record.to_dict() for record in accident_records])


# 编辑事故记录
@accident_record_bp.route('/<int:record_id>', methods=['PUT'])
def update_accident(record_id):
    record = AccidentRecord.query.get_or_404(record_id)
    data = request.form.to_dict()
    files = request.files

    # 更新日期
    if data.get('occurrence_date'):
        record.occurrence_date = datetime.strptime(data['occurrence_date'], '%Y-%m-%d').date()

    # 更新图片
    for i in range(1, 5):
        key = f'accident_image_{i}'
        if key in files and files[key].filename != '':
            file = files[key]
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
                os.makedirs(upload_folder, exist_ok=True)
                filepath = os.path.join(upload_folder, filename)
                file.save(filepath)
                setattr(record, key, filepath)
            else:
                return jsonify({'message': f'图片{i}格式不支持'}), 400

    # 更新其他字段
    for field in ['driver_name', 'plate_number', 'liability_determination', 'case_number', 'remarks']:
        if field in data:
            setattr(record, field, data[field])

    db.session.commit()
    return jsonify({'message': '编辑成功'})


# 删除事故记录
@accident_record_bp.route('/<int:record_id>', methods=['DELETE'])
def delete_accident(record_id):
    record = AccidentRecord.query.get_or_404(record_id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': '删除成功'})
