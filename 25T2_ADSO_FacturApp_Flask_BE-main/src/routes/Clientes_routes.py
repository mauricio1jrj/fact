from flask import Blueprint, request, jsonify
from src.models.Clientes import Clientes
from src.utils.auth import token_required, rol_required

clientes_bp = Blueprint('clientes', __name__,)

@clientes_bp.route('/', methods=['GET'])
@token_required
@rol_required('admin', 'vendedor')  
def get_clientes():  
    page = request.args.get('page',default= 1, type=int)

    per_page = request.args.get('per_page', default=5, type=int)

    clientes, total = Clientes.paginate(page=page, per_page=per_page)
    total_pages = (total + per_page - 1) // per_page #= 

    return jsonify({
        'data': [cliente.to_dict() for cliente in clientes],
        'meta': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    })


@clientes_bp.route('/<int:id>', methods=['GET'])
@token_required
@rol_required('admin', 'vendedor')
def get_cliente(id):
    cliente = Clientes.get_by_id(id)
    if not cliente:
        return jsonify({'message': 'Cliente no encontrado, rectificar datos'}), 404
    return jsonify({
        'id': cliente.id,
        'nombre': cliente.nombre,
        'direccion': cliente.direccion,
        'telefono': cliente.telefono,
        'cedula': cliente.cedula,
        'email': cliente.email,
        'activo': cliente.activo
    })

@clientes_bp.route('/', methods=['POST'])
@token_required
@rol_required('admin', 'vendedor')
def create_cliente(): 
    data = request.get_json()
    cliente = Clientes(
        nombre=data['nombre'],
        direccion=data['direccion'],
        telefono=data['telefono'],
        cedula=data['cedula'],
        email=data['email']
    )

    if cliente.nombre == '':
        return jsonify({'message': 'El nombre del cliente es obligatorio'}), 400
    if cliente.direccion == '':
        return jsonify({'message': 'La dirección del cliente es obligatoria'}), 400
    if cliente.telefono == '':
        return jsonify({'message': 'El teléfono del cliente es obligatorio'}), 400
    if cliente.cedula == '':
        return jsonify({'message': 'La cédula del cliente es obligatoria'}), 400
    if cliente.email == '':
        return jsonify({'message': 'El email del cliente es obligatorio'}), 400
    

    cliente.save()
    return jsonify({'message': 'Cliente creado exitosamente','cliente':cliente.to_dict()}), 201

@clientes_bp.route('/<int:id>', methods=['PUT'])
@token_required
@rol_required('admin', 'vendedor')
def update_cliente(id):   
    cliente = Clientes.get_by_id(id)
    if not cliente:
        return jsonify({'message': 'Cliente no encontrado'}), 404

    data = request.get_json()
    cliente.nombre = data['nombre']
    cliente.direccion = data['direccion']
    cliente.telefono = data['telefono']
    cliente.cedula = data['cedula']
    cliente.email = data['email']

    if cliente.nombre == '':
        return jsonify({'message': 'El nombre del cliente es obligatorio'}), 400
    if cliente.direccion == '':
        return jsonify({'message': 'La dirección del cliente es obligatoria'}), 400
    if cliente.telefono == '':
        return jsonify({'message': 'El teléfono del cliente es obligatorio'}), 400
    if cliente.cedula == '':
        return jsonify({'message': 'La cédula del cliente es obligatoria'}), 400
    if cliente.email == '':
        return jsonify({'message': 'El email del cliente es obligatorio'}), 400
    
    cliente.save()
    return jsonify({'message': 'Cliente actualizado exitosamente','cliente':cliente.to_dict()}), 200

@clientes_bp.route('/cedula/<string:cedula>', methods=['GET'])
@token_required
@rol_required('admin', 'vendedor')
def buscar_cliente_por_cedula(cedula):

    cliente = Clientes.get_by_cedula(cedula)

    if not cliente:
        return jsonify({
            "message": "Cliente no encontrado"
        }), 404

    return jsonify({
        "cliente": cliente.to_dict()
    }), 200

@clientes_bp.route('/<int:id>', methods=['DELETE'])
@token_required
@rol_required('admin')
def delete_cliente(id):

    cliente = Clientes.get_by_id(id)

    if not cliente:
        return jsonify({
            'message': 'Cliente no encontrado'
        }), 404

    cliente.delete()

    return jsonify({
        'message': 'Cliente eliminado exitosamente'
    }), 200

