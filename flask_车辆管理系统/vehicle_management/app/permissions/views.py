from unittest import result

from . import permissions
from flask import jsonify,request
from vehicle_management import db
from vehicle_management.models import Permission
"""查看所有的权限"""
@permissions.route('get',methods=['GET'])
def get_permissions():

    result  = []
    permissions_list = Permission.query.all()
    print(type(permissions_list))
    if permissions_list:
        for permission in permissions_list:
            result.append({
                'id': permission.id,
                'name': permission.name,
                'description': permission.description
            })

        return jsonify({'data':result,'msg':'success','code':'200'})
    return jsonify({'data':result,'msg':'success','code':'200'})
"""查单个权限"""
@permissions.route('get/<int:id>')
def get_permission(id):
    result = {}
    permission = Permission.query.filter_by(id=id).first()

    if not permission:
        return jsonify(result,{'msg':'no exsited','code':'404'})

    result ={'permission_name':permission.name}
    return jsonify(result, {'msg': 'success'})

"""增加权限"""
@permissions.route('post',methods=['POST'])
def post_permissions():
    result = {}
    data = request.get_json()
    permission_name = data.get('permission_name')
    description = data.get('description')



    result ={'permission_name':permission_name}
    if description:
        new_permission = Permission(name=permission_name,description=description)
    else:
        new_permission = Permission(name=permission_name)
    try:

        db.session.add(new_permission)

        db.session.commit()
        return jsonify(result,{'msg':'success'})
    except Exception as e:
        return jsonify(result,{'msg':str(e)})

"""修改权限"""
@permissions.route('update',methods=['PUT'])

def update_permission():

    result = {}
    data = request.get_json()

    permission_id = data.get('permission_id')
    permission_name = data.get('permission_name')
    description = data.get('description')

    print(description)


    permission = Permission.query.filter_by(id=permission_id).first()

    permission.name = permission_name
    permission.description = description

    try:
        db.session.commit()
        result['permission_name'] = permission.name
        result['description'] = description
        return jsonify(result,{'msg':'success'})
    except Exception as e:
        return jsonify(result,{'msg':str(e)})


"""删除权限"""
@permissions.route('delete',methods=['DELETE'])
def delete_permission():
    result = {}
    data = request.get_json()
    permission_id = data.get('permission_id')

    permission = Permission.query.filter_by(id=permission_id).first()

    if not permission:
        return jsonify(result,{'msg':'no exsited,success','code':'201'})

    try:
        db.session.delete(permission)
        db.session.commit()
        return jsonify(result,{'msg':'success'})
    except Exception as e:
        return jsonify(result,{'msg':str(e)})