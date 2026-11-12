from flask import Blueprint, render_template, request
from flask import redirect, url_for, flash, session
from src.clients.api_clients import APIClient, APIError

facturas_bp = Blueprint('facturas', __name__)


def _client():
    return APIClient(session.get('api_token'))


@facturas_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    try:
        data = _client().get(
            '/facturas/',
            params={'page': page, 'per_page': per_page}
        )
        return render_template(
            'lista_facturas.html',
            facturas=data.get('data', []),
            meta=data.get('meta', {})
        )
    except APIError as e:
        flash(e.message, 'danger')
    return render_template(
        'lista_facturas.html', facturas=[], meta={}
    )


@facturas_bp.route('/nuevo', methods=['GET', 'POST'])
def crear_factura():
    cedula = request.args.get('cedula', '')
    cliente = None
    vendedores = []
    productos = []

    if cedula:
        try:
            respuesta = _client().get(
                f'/clientes/cedula/{cedula}'
            )
            cliente = respuesta.get('cliente', respuesta)
        except APIError as e:
            flash(e.message, 'danger')

    if request.method == 'POST':
        print(request.form.to_dict())
        try:
            datos = {
                'numero_factura': request.form['numero_factura'],
                'fecha_emision': request.form['fecha_emision'],
                'cliente_id': int(request.form['cliente_id']),
                'vendedor_id': int(request.form['vendedor_id'])
            }
            respuesta = _client().post('/facturas/', json=datos)
            factura_id = respuesta.get('factura', {}).get('id')
            producto_id = int(request.form['producto_id'])
            cantidad = int(request.form['cantidad'])
            producto = _client().get(f'/productos/{producto_id}')
            precio = float(producto['precio'])
            detalle = {
                'factura_id': factura_id,
                'producto_id': producto_id,
                'cantidad': cantidad,
                'precio_unitario': precio,
                'total': precio * cantidad
            }
            _client().post('/detalle_facturas/', json=detalle)
            flash('Factura creada correctamente.', 'success')
            return redirect(url_for('facturas.index'))
        except APIError as e:
            flash(e.message, 'danger')

        except Exception as e:
            print('ERROR:', e)
            flash(f'Error: {e}', 'danger')

    try:
        data = _client().get(
            '/vendedores/',
            params={'page': 1, 'per_page': 100}
        )
        vendedores = data.get('data', [])
    except Exception:
        vendedores = []

    try:
        data = _client().get(
            '/productos/',
            params={'page': 1, 'per_page': 100}
        )
        productos = data.get('data', [])
    except Exception:
        productos = []

    return render_template(
        'nueva_factura.html',
        cliente=cliente,
        cedula=cedula,
        vendedores=vendedores,
        productos=productos
    )


@facturas_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_factura(id):
    if session.get('rol') != 'admin':
        flash('No tienes permisos para editar facturas.', 'danger')
        return redirect(url_for('facturas.index'))
    try:
        factura = _client().get(f'/facturas/{id}')
        if request.method == 'POST':
            datos = {
                'numero_factura': request.form['numero_factura'],
                'fecha_emision': request.form['fecha_emision'],
                'cliente_id': int(request.form['cliente_id']),
                'vendedor_id': int(request.form['vendedor_id'])
            }
            _client().put(f'/facturas/{id}', json=datos)
            flash('Factura actualizada correctamente.', 'success')
            return redirect(url_for('facturas.index'))
        
        return render_template(
            'Editar_factura.html', factura=factura
        )
    except APIError as e:

        flash(e.message, 'danger')

    except Exception:
        flash('No fue posible editar la factura.', 'danger')
    return redirect(url_for('facturas.index'))


@facturas_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_factura(id):
    if session.get('rol') != 'admin':
        flash('No tienes permisos para eliminar facturas.', 'danger')
        return redirect(url_for('facturas.index'))
    try:
        _client().delete(f'/facturas/{id}')
        flash('Factura eliminada correctamente.', 'success')

    except APIError as e:
        flash(e.message, 'danger')

    except Exception:
        flash('No fue posible eliminar la factura.', 'danger')
    return redirect(url_for('facturas.index'))