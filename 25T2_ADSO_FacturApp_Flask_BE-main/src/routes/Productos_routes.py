from flask import Blueprint, request, jsonify

from src.models.Productos import Productos
from src.models import session
from src.utils.auth import token_required, rol_required

productos_bp = Blueprint('productos', __name__)


@productos_bp.route('/', methods=['GET'])
@token_required
@rol_required('admin', 'vendedor', 'cliente')
def get_productos():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=5, type=int)

    productos, total = Productos.paginate(
        page=page,
        per_page=per_page
    )

    total_pages = (total + per_page - 1) // per_page

    return jsonify({
        'data': [p.to_dict() for p in productos],
        'meta': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    })


@productos_bp.route('/<int:id>', methods=['GET'])
@token_required
@rol_required('admin', 'vendedor')
def get_producto(id):
    producto = Productos.get_by_id(id)

    if not producto:
        return jsonify({
            'message': 'Producto no encontrado'
        }), 404

    return jsonify(producto.to_dict())


@productos_bp.route('/', methods=['POST'])
@token_required
@rol_required('admin')
def create_producto():
    data = request.get_json()

    try:
        precio = float(data['precio'])
        stock = int(data['stock'])
        categoria_id = int(data['categoria_id'])
    except (KeyError, TypeError, ValueError):
        return jsonify({
            'message': 'Los datos del producto no son válidos'
        }), 400

    if not data.get('nombre'):
        return jsonify({
            'message': 'El nombre del producto es obligatorio'
        }), 400

    if not data.get('descripcion'):
        return jsonify({
            'message': 'La descripción es obligatoria'
        }), 400

    if not data.get('unidad_medida'):
        return jsonify({
            'message': 'La unidad de medida es obligatoria'
        }), 400

    if precio <= 0:
        return jsonify({
            'message': 'El precio debe ser mayor a cero'
        }), 400

    if stock < 0:
        return jsonify({
            'message': 'El stock no puede ser negativo'
        }), 400

    if categoria_id <= 0:
        return jsonify({
            'message': 'La categoría es obligatoria'
        }), 400

    producto = Productos(
        codigo=data['codigo'],
        nombre=data['nombre'],
        descripcion=data['descripcion'],
        unidad_medida=data['unidad_medida'],
        precio=precio,
        stock=stock,
        categoria_id=categoria_id
    )

    try:
        producto.save()
    except Exception as e:
        session.rollback()
        return jsonify({
            'message': 'Error al crear producto',
            'error': str(e)
        }), 500

    return jsonify({
        'message': 'Producto creado exitosamente',
        'producto': producto.to_dict()
    }), 200


@productos_bp.route('/<int:id>', methods=['PUT'])
@token_required
@rol_required('admin')
def update_producto(id):
    producto = Productos.get_by_id(id)

    if not producto:
        return jsonify({
            'message': 'Producto no encontrado'
        }), 404

    data = request.get_json()

    try:
        precio = float(data['precio'])
        stock = int(data['stock'])
        categoria_id = int(data['categoria_id'])
    except (KeyError, TypeError, ValueError):
        return jsonify({
            'message': 'Los datos del producto no son válidos'
        }), 400

    if not data.get('nombre'):
        return jsonify({
            'message': 'El nombre del producto es obligatorio'
        }), 400

    if not data.get('descripcion'):
        return jsonify({
            'message': 'La descripción es obligatoria'
        }), 400

    if not data.get('unidad_medida'):
        return jsonify({
            'message': 'La unidad de medida es obligatoria'
        }), 400

    if precio <= 0:
        return jsonify({
            'message': 'El precio debe ser mayor a cero'
        }), 400

    if stock < 0:
        return jsonify({
            'message': 'El stock no puede ser negativo'
        }), 400

    if categoria_id <= 0:
        return jsonify({
            'message': 'La categoría es obligatoria'
        }), 400

    producto.codigo = data['codigo']
    producto.nombre = data['nombre']
    producto.descripcion = data['descripcion']
    producto.unidad_medida = data['unidad_medida']
    producto.precio = precio
    producto.stock = stock
    producto.Categoria_id = categoria_id

    try:
        producto.save()
    except Exception as e:
        session.rollback()
        return jsonify({
            'message': 'Error al actualizar producto',
            'error': str(e)
        }), 500

    return jsonify({
        'message': 'Producto actualizado exitosamente',
        'producto': producto.to_dict()
    }), 200


@productos_bp.route('/<int:id>', methods=['DELETE'])
@token_required
@rol_required('admin')
def delete_producto(id):
    producto = Productos.get_by_id(id)

    if not producto:
        return jsonify({
            'message': 'Producto no encontrado'
        }), 404

    try:
        session.delete(producto)
        session.commit()
    except Exception as e:
        session.rollback()
        return jsonify({
            'message': 'Error al eliminar producto',
            'error': str(e)
        }), 500

    return jsonify({
        'message': 'Producto eliminado exitosamente'
    }), 200