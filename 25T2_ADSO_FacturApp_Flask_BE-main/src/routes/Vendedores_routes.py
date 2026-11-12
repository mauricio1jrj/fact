from flask import Blueprint, request, jsonify
from src.models.Vendedores import Vendedores
from src.utils.auth import token_required, rol_required

vendedores_bp = Blueprint('vendedores', __name__,)

@vendedores_bp.route('/', methods=['GET'])
@token_required
@rol_required('admin', 'vendedor')
def get_vendedores():
    page = request.args.get('page',default= 1, type=int)

    per_page = request.args.get('per_page', default=5, type=int)

    vendedores, total = Vendedores.paginate(page=page, per_page=per_page)
    total_pages = (total + per_page - 1) // per_page #= 

    return jsonify({
        'data': [vendedor.to_dict() for vendedor in vendedores],
        'meta': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    })


@vendedores_bp.route('/<int:id>', methods=['GET'])
@token_required
@rol_required('admin')
def get_vendedor_by_id(id):
    vendedor = Vendedores.get_by_id(id)
    if not vendedor:
        return jsonify({'message': 'Vendedor no encontrado'}), 404
    return jsonify({
        'id': vendedor.id,
        'nombre': vendedor.nombre,
        'direccion': vendedor.direccion,
        'telefono': vendedor.telefono,
        'cedula': vendedor.cedula,
        'email': vendedor.email,
        'activo': vendedor.activo
    })

@vendedores_bp.route('/', methods=['POST'])
@token_required
@rol_required('admin')
def create_vendedor(): 
    data = request.get_json()
    vendedor = Vendedores(
        nombre=data['nombre'],
        direccion=data['direccion'],
        telefono=data['telefono'],
        cedula=data['cedula'],
        email=data['email'],
        activo=data.get('activo', True)
    )

    if vendedor.nombre == '':
        return jsonify({'message': 'El nombre del vendedor es obligatorio'}), 400
    if vendedor.direccion == '':
        return jsonify({'message': 'La dirección del vendedor es obligatoria'}), 400
    if vendedor.telefono == '':
        return jsonify({'message': 'El teléfono del vendedor es obligatorio'}), 400
    if vendedor.cedula == '':
        return jsonify({'message': 'La cédula del vendedor es obligatoria'}), 400
    if vendedor.email == '':
        return jsonify({'message': 'El email del vendedor es obligatorio'}), 400
    if Vendedores.get_by_id(vendedor.id):
        return jsonify({'message': 'El vendedor ya existe'}), 400
    

    vendedor.save()
    return jsonify({'message': 'Vendedor creado exitosamente','vendedor':vendedor.to_dict()}), 201

@vendedores_bp.route('/<int:id>', methods=['PUT'])
@token_required
@rol_required('admin')
def update_vendedor(id):   
    vendedor = Vendedores.get_by_id(id)
    if not vendedor:
        return jsonify({'message': 'Vendedor no encontrado'}), 404

    data = request.get_json()
    vendedor.nombre = data['nombre']
    vendedor.direccion = data['direccion']
    vendedor.telefono = data['telefono']
    vendedor.cedula = data['cedula']
    vendedor.email = data['email']
    vendedor.activo = data.get('activo', True)

    if vendedor.nombre == '':
        return jsonify({'message': 'El nombre del vendedor es obligatorio'}), 400
    if vendedor.direccion == '':
        return jsonify({'message': 'La dirección del vendedor es obligatoria'}), 400
    if vendedor.telefono == '':
        return jsonify({'message': 'El teléfono del vendedor es obligatorio'}), 400
    if vendedor.cedula == '':
        return jsonify({'message': 'La cédula del vendedor es obligatoria'}), 400
    if vendedor.email == '':
        return jsonify({'message': 'El email del vendedor es obligatorio'}), 400
    if Vendedores.get_by_id(vendedor.id) and Vendedores.get_by_id(vendedor.id).id != id:
        return jsonify({'message': 'El vendedor ya existe'}), 400

    vendedor.save()
    return jsonify({'message': 'Vendedor actualizado exitosamente','vendedor':vendedor.to_dict()}), 200


