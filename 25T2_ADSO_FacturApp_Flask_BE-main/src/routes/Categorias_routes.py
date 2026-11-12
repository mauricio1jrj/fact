from flask import Blueprint, request, jsonify
from src.models.Categorias import Categorias

categorias_bp = Blueprint('categorias', __name__,)

@categorias_bp.route('/', methods=['GET'])
def get_categorias():
    page = request.args.get('page',default= 1, type=int)

    per_page = request.args.get('per_page', default=5, type=int)

    categorias, total = Categorias.paginate(page=page, per_page=per_page)
    total_pages = (total + per_page - 1) // per_page #= 

    return jsonify({
        'data': [categoria.to_dict() for categoria in categorias],
        'meta': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    })


@categorias_bp.route('/<int:id>', methods=['GET'])
def get_categoria(id):
    categoria = Categorias.get_by_id(id)
    if not categoria:
        return jsonify({'message': 'Categoría no encontrada'}), 404
    return jsonify({
        'id': categoria.id,
        'nombre': categoria.nombre,
        
    })


@categorias_bp.route('/', methods=['POST'])
def create_categoria(): 
    data = request.get_json()
    categoria = Categorias(
        nombre=data['nombre'],

    )

    if categoria.nombre == '':
        return jsonify({'message': 'El nombre de la categoría es obligatorio'}), 400

    categoria.save()
    return jsonify({'message': 'Categoría creada exitosamente','categoria':categoria.to_dict()}), 201 
   

@categorias_bp.route('/<int:id>', methods=['PUT'])
def update_categoria(id):   
    categoria = Categorias.get_by_id(id)
    if not categoria:
        return jsonify({'message': 'Categoría no encontrada'}), 404

    data = request.get_json()
    categoria.nombre = data['nombre']

    if categoria.nombre == '':
        return jsonify({'message': 'El nombre de la categoría es obligatorio'}), 400


    categoria.save()
    return jsonify({'message': 'Categoría actualizada exitosamente','categoria':categoria.to_dict()}), 200