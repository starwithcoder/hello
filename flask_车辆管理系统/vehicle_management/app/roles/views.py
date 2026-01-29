from vehicle_management.models import user_roles
from . import roles
from flask import request
from flask import jsonify


from vehicle_management import db
from vehicle_management.models import Permission,Role
from sqlalchemy.orm import selectinload
"""查询所有角色"""

@roles.route('get')
def get_roles():

    data =[]
    roles_list = Role.query.options(selectinload(Role.permissions)).all()
    for role in roles_list:
        permissions = [{'permission_name':p.name,'permission_id':p.id,'permission_description':p.description} for p in role.permissions]
        data.append({
                'role_name': role.name,
                'role_description': role.description,
                'role_permissions': permissions,
            })


    return jsonify({'data':data,'code':20000,'msg':'查询成功'})
"""查询单个角色"""



"""增加角色"""
@roles.route('post')
def post_role():
    data = request.get_json()

    role_name = data.get('role_name')
    permission_ids = data.get('permission_ids',[])
    description = data.get('description')


    existing_role = Role.query.filter_by(name=role_name).first()
    if existing_role:
        return jsonify({'data':'','code':40003,'msg':'role is existed'})



    new_role = Role(name=role_name,description=description)
    db.session.add(new_role)

    permissions = Permission.query.filter(Permission.id.in_(permission_ids)).all()

    new_role.permissions.extend(permissions)

    try:
        db.session.commit()
        return jsonify({'data':'','code':20001,'msg':'role created successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'data':'','code':50002,'msg':str(e)})

"""修改角色"""
@roles.route('put',methods=['PUT'])
def put_role():
    data = request.get_json()
    role_name = data.get('role_name')
    if not role_name:
        return jsonify({'data':'','code':40003,'msg':'role is existed'})

    role = Role.query.filter_by(name=role_name).first()
    if not role:
        return jsonify({'data':'','code':40003,'msg':'role is existed'})

    permission_ids = data.get('permission_ids', [])
    permissions = Permission.query.filter(Permission.id.in_(permission_ids)).all()

    try:
        role.permissions = permissions
        db.session.commit()
        return jsonify({'data':'','code':20002,'msg':'role updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'data':'','code':50002,'msg':str(e)})


"""删除角色"""
@roles.route('delete',methods=['DELETE'])
def delete_role():
    data = request.get_json()
    role_name = data.get('role_name')
    if not role_name:
        return jsonify({'data': '','code':40003,'msg': '参数值非法' })

    role = Role.query.filter_by(name=role_name).first()
    if not role:
        return jsonify({'data': '','code':40003,'msg': '参数值非法' })

    try:
        db.session.delete(role)
        db.session.commit()
        return jsonify({'data':'','code':20003,'msg': '删除成功' })
    except Exception as e:
        db.session.rollback()
        return jsonify({'data':str(e), 'code':50002,"msg": '数据库操作失败' })

