from flask import Blueprint, request, jsonify
from src. models.Detalle_facturas import Detalle_Facturas
from src.utils.auth import token_required, rol_required

detalle_facturas_bp = Blueprint('detalle_facturas', __name__,)

@detalle_facturas_bp.route('/', methods=['GET'])
@token_required
@rol_required('admin', 'vendedor')
def get_detalle_facturas():

    page = request.args.get('page',default= 1, type=int)

    per_page = request.args.get('per_page', default=5, type=int)

    detalle_facturas, total = Detalle_Facturas.paginate(page=page, per_page=per_page)
    total_pages = (total + per_page - 1) // per_page #= 

    return jsonify({
        'data': [detalle_factura.to_dict() for detalle_factura in detalle_facturas],
        'meta': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    })


@detalle_facturas_bp.route('/<int:id>', methods=['GET'])
@token_required
@rol_required('admin', 'vendedor')
def get_detalle_factura(id):
    detalle_factura = Detalle_Facturas.get_by_id(id)
    if not detalle_factura:
        return jsonify({'message': 'Detalle de factura no encontrado'}), 404
    return jsonify({
        'id': detalle_factura.id,
        'factura_id': detalle_factura.factura_id,
        'producto_id': detalle_factura.producto_id,
        'cantidad': detalle_factura.cantidad,
        'precio_unitario': detalle_factura.precio_unitario,
        'total': detalle_factura.total
    })

@detalle_facturas_bp.route('/', methods=['POST'])
@token_required
@rol_required('admin', 'vendedor')
def create_detalle_factura(): 
    data = request.get_json()
    detalle_factura = Detalle_Facturas(
        factura_id=data['factura_id'],
        producto_id=data['producto_id'],
        cantidad=data['cantidad'],
        precio_unitario=data['precio_unitario'],
        total=data['total']
    )

    if detalle_factura.factura_id == '':
        return jsonify({'message': 'El ID de la factura es obligatorio'}), 400
    if detalle_factura.producto_id == '':
        return jsonify({'message': 'El ID del producto es obligatorio'}), 400
    if detalle_factura.cantidad == '':
        return jsonify({'message': 'La cantidad es obligatoria'}), 400
    if detalle_factura.precio_unitario == '':
        return jsonify({'message': 'El precio unitario es obligatorio'}), 400
    if detalle_factura.total == '':
        return jsonify({'message': 'El total es obligatorio'}), 400

    detalle_factura.save()
    return jsonify({'message': 'Detalle de factura creado exitosamente','detalle_factura':detalle_factura.to_dict()}), 201

@detalle_facturas_bp.route('/<int:id>', methods=['PUT'])
@token_required
@rol_required('admin')
def update_detalle_factura(id):
    detalle_factura = Detalle_Facturas.get_by_id(id)
    if not detalle_factura:
        return jsonify({'message': 'Detalle de factura no encontrado'}), 404

    data = request.get_json()
    detalle_factura.factura_id = data['factura_id']
    detalle_factura.producto_id = data['producto_id']
    detalle_factura.cantidad = data['cantidad']
    detalle_factura.precio_unitario = data['precio_unitario']
    detalle_factura.total = data['total']

    if detalle_factura.factura_id == '':
        return jsonify({'message': 'El ID de la factura es obligatorio'}), 400
    if detalle_factura.producto_id == '':
        return jsonify({'message': 'El ID del producto es obligatorio'}), 400
    if detalle_factura.cantidad == '':
        return jsonify({'message': 'La cantidad es obligatoria'}), 400
    if detalle_factura.precio_unitario == '':
        return jsonify({'message': 'El precio unitario es obligatorio'}), 400
    if detalle_factura.total == '':
        return jsonify({'message': 'El total es obligatorio'}), 400

    detalle_factura.save()
    return jsonify({'message': 'Detalle de factura actualizado exitosamente','detalle_factura':detalle_factura.to_dict()}), 200


@detalle_facturas_bp.route('/<int:id>', methods=['DELETE'])
@token_required
@rol_required('admin')
def delete_detalle_factura(id):

    detalle_factura = Detalle_Facturas.get_by_id(id)

    if not detalle_factura:
        return jsonify({
            'message': 'Detalle de factura no encontrado'
        }), 404

    detalle_factura.delete()

    return jsonify({
        'message': 'Detalle de factura eliminado exitosamente'
    }), 200