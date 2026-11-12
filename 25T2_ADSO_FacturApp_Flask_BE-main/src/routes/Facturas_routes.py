from flask import Blueprint, request, jsonify
from src.models.Productos import Productos
from src.models.Facturas import Facturas
from src.utils.auth import token_required, rol_required

facturas_bp = Blueprint('facturas', __name__,)

@facturas_bp.route('/', methods=['GET'])
@token_required
@rol_required('admin', 'vendedor')

def get_facturas():
    page = request.args.get('page',default= 1, type=int)

    per_page = request.args.get('per_page', default=5, type=int)

    facturas, total = Facturas.paginate(page=page, per_page=per_page)
    total_pages = (total + per_page - 1) // per_page #= 

    return jsonify({
        'data': [factura.to_dict() for factura in facturas],
        'meta': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    })


@facturas_bp.route('/<int:id>', methods=['GET'])
@token_required
@rol_required('admin', 'vendedor')
def get_factura_by_id(id):
    factura = Facturas.get_by_id(id)
    if not factura:
        return jsonify({'message': 'Factura no encontrada'}), 404
    return jsonify({
        'id': factura.id,
        'numero_factura': factura.numero_factura,
        'fecha_emision': factura.fecha_emision,
        'cliente_id': factura.Cliente_id,
        'vendedor_id': factura.Vendedor_id
    })


@facturas_bp.route('/', methods=['POST'])
@token_required
@rol_required('admin', 'vendedor')
def create_factura(): 
    data = request.get_json()
    factura = Facturas(
        numero_factura=data['numero_factura'],
        fecha_emision=data['fecha_emision'],
        cliente_id=data['cliente_id'],
        vendedor_id=data['vendedor_id']
    )

    if factura.numero_factura == '':
        return jsonify({'message': 'El número de factura es obligatorio'}), 400
    if factura.fecha_emision == '':
        return jsonify({'message': 'La fecha de emisión es obligatoria'}), 400
    if factura.Cliente_id == '':
        return jsonify({'message': 'El ID del cliente es obligatorio'}), 400
    if factura.Vendedor_id == '':
        return jsonify({'message': 'El ID del vendedor es obligatorio'}), 400

    factura.save()
    return jsonify({'message': 'Factura creada exitosamente','factura':factura.to_dict()}), 201

@facturas_bp.route('/<int:id>', methods=['PUT'])
@token_required
@rol_required('admin')
def update_factura(id):   
    factura = Facturas.get_by_id(id)
    if not factura:
        return jsonify({'message': 'Factura no encontrada'}), 404

    data = request.get_json()
    factura.numero_factura = data['numero_factura']
    factura.fecha_emision = data['fecha_emision']
    factura.Cliente_id = data['cliente_id']
    factura.Vendedor_id = data['vendedor_id']

    if factura.numero_factura == '':
        return jsonify({'message': 'El número de factura es obligatorio'}), 400
    if factura.fecha_emision == '':
        return jsonify({'message': 'La fecha de emisión es obligatoria'}), 400
    if factura.Cliente_id == '':
        return jsonify({'message': 'El ID del cliente es obligatorio'}), 400
    if factura.Vendedor_id == '':
        return jsonify({'message': 'El ID del vendedor es obligatorio'}), 400

    factura.save()
    return jsonify({'message': 'Factura actualizada exitosamente','factura':factura.to_dict()}), 200  
  
@facturas_bp.route('/<int:id>', methods=['DELETE'])
@token_required
@rol_required('admin')
def delete_factura(id):

    factura = Facturas.get_by_id(id)

    if not factura:
        return jsonify({
            'message': 'Factura no encontrada'
        }), 404

    factura.delete()

    return jsonify({
        'message': 'Factura eliminada exitosamente'
    }), 200