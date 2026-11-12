from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.clients.api_clients import APIClient, APIError

producto_bp = Blueprint('productos', __name__)

def _client():
    return APIClient(session.get('api_token'))

@producto_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    try:
        data = _client().get('/productos/', params={'page': page, 'per_page': per_page})
        return render_template('lista_productos.html',
                               productos=data.get('data', []),
                               meta=data.get('meta', {}))
    except APIError as e:
        flash(e.message, 'danger')
        return render_template('lista_productos.html', productos=[], meta={})

@producto_bp.route('/tienda')
def tienda():

    try:

        data = _client().get(
            '/productos/',
            params={
                'page': 1,
                'per_page': 100
            }
        )

        return render_template(
            'productos.html',
            productos=data.get('data', []),
            meta=data.get('meta', {})
        )

    except APIError as e:

        flash(e.message, 'danger')

        return render_template(
            'productos.html',
            productos=[],
            meta={}
        )

@producto_bp.route('/nuevo', methods=['GET', 'POST'])
def crear_producto():
    if request.method == 'POST':
        try:
            datos = {
                'codigo': request.form['codigo'],
                'nombre': request.form['nombre'],
                'descripcion': request.form['descripcion'],
                'unidad_medida': request.form['unidad_medida'],
                'precio': float(request.form['precio']),
                'stock': int(request.form['stock']),
                'categoria_id': int(request.form['categoria_id'])
            }
            _client().post('/productos/', json=datos)
            flash('Producto creado correctamente.', 'success')
            return redirect(url_for('productos.index'))
        except APIError as e:
            flash(e.message, 'danger')

    try:
        data = _client().get('/categorias/', params={'page': 1, 'per_page': 100})
        categorias = data.get('data', [])
    except Exception:
        categorias = []

    return render_template('Nuevo_producto.html', categorias=categorias)

@producto_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    if session.get('rol') != 'admin':
        flash('No tienes permisos para editar productos.', 'danger')
        return redirect(url_for('productos.index'))

    try:
        producto = _client().get(f'/productos/{id}')

        if request.method == 'POST':
            datos = {
                'codigo': request.form['codigo'],
                'nombre': request.form['nombre'],
                'descripcion': request.form['descripcion'],
                'unidad_medida': request.form['unidad_medida'],
                'precio': float(request.form['precio']),
                'stock': int(request.form['stock']),
                'categoria_id': int(request.form['categoria_id'])
            }
            _client().put(f'/productos/{id}', json=datos)
            flash('Producto actualizado correctamente.', 'success')
            return redirect(url_for('productos.index'))

        data = _client().get('/categorias/', params={'page': 1, 'per_page': 100})
        return render_template('Editar_producto.html',
                               producto=producto,
                               categorias=data.get('data', []))

    except APIError as e:
        flash(e.message, 'danger')
    except Exception:
        flash('No fue posible editar el producto.', 'danger')

    return redirect(url_for('productos.index'))

@producto_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    if session.get('rol') != 'admin':
        flash('No tienes permisos para eliminar productos.', 'danger')
        return redirect(url_for('productos.index'))

    try:
        _client().delete(f'/productos/{id}')
        flash('Producto eliminado correctamente.', 'success')
    except APIError as e:
        flash(e.message, 'danger')
    except Exception:
        flash('No fue posible eliminar el producto.', 'danger')

    return redirect(url_for('productos.index'))