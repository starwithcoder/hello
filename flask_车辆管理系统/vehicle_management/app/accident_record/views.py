from . import accident_record_bp
from flask import request, jsonify, current_app
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from vehicle_management import db
from vehicle_management.models import AccidentRecord, Drivers,Cars
import random
from sqlalchemy.orm import joinedload


# 允许的图片扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

#获取基础路径
def get_baseurl():
    return current_app.root_path
#保存文件
def save_file(file_fields,driver_name):
    path = []
    base_dir = get_baseurl()
    upload_folder = os.path.join(base_dir, f'uploads/{driver_name}')
    os.makedirs(upload_folder, exist_ok=True)


    for field in file_fields:
        if field:
            filename = secure_filename(field.filename)
            filepath = os.path.join(upload_folder, filename)
            field.save(filepath)
            path.append(filepath)
    return path

# 新增事故记录
@accident_record_bp.route('', methods=['POST'])
async def create_accident():
    print('===============accident_record.create_accident========================')

    occurrence_date = request.form.get("occurrence_date")
    driver_name = request.form.get("driver_name")
    plate_number = request.form.get("plate_number")
    liability_determination = request.form.get("liability_determination")
    #案件号
    case_number = request.form.get("case_number")
    remarks = request.form.get("remark")

    file_fields = [
        request.files.get('accident_images_1'),
        request.files.get('accident_images_2'),
        request.files.get('accident_images_3'),
        request.files.get('accident_images_4')
    ]

    driver = Drivers.query.options(joinedload(Drivers.cars)).filter_by(driver_name=driver_name).first()

    if driver:
        car = next((c for c in driver.cars if c.plate_number == plate_number), None)
        if car:
            paths = save_file(file_fields,driver_name)

            new_accident_record = AccidentRecord(
               occurrence_date = occurrence_date,
               driver_name = driver_name,
               plate_number = plate_number,
               liability_determination = liability_determination,
               accident_image_1 = next(iter(paths[0:1]), None),
               accident_image_2 = next(iter(paths[1:2]), None),
               accident_image_3 = next(iter(paths[2:3]), None),
               accident_image_4 = next(iter(paths[3:]), None),
               case_number = case_number,
               remarks = remarks
               )
            try:
                db.session.add(new_accident_record)
                db.session.commit()
            except Exception as e:
                print(str(e))
                return jsonify({'message': str(e)}), 500
            return jsonify({'msg':'success'})
        else:
            return jsonify({'msg':'车辆错误'})
    else:
        return jsonify({'msg':'司机错误'})



    return jsonify({'message': '新增成功'}), 201
    

   

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
