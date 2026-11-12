from flask import Blueprint, render_template, request
from flask import redirect, url_for, flash, session
from src.clients.api_clients import APIClient, APIError

detalles_bp = Blueprint(
    'detalles_facturas', __name__
)


def _client():
    return APIClient(session.get('api_token'))


def _datos_form():
    facturas = []
    productos = []

    f_data = _client().get(
        '/facturas/',
        params={'page': 1, 'per_page': 100}
    )
    facturas = f_data.get('data', [])

    p_data = _client().get(
        '/productos/',
        params={'page': 1, 'per_page': 100}
    )
    productos = p_data.get('data', [])

    return facturas, productos


@detalles_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    try:
        data = _client().get(
            '/detalle_facturas/',
            params={
                'page': page,
                'per_page': per_page
            }
        )

        detalles = data.get('data', [])
        meta = data.get('meta', {})

        f_data = _client().get(
            '/facturas/',
            params={'page': 1, 'per_page': 100}
        )
        facturas = f_data.get('data', [])

        p_data = _client().get(
            '/productos/',
            params={'page': 1, 'per_page': 100}
        )
        productos = p_data.get('data', [])

        v_data = _client().get(
            '/vendedores/',
            params={'page': 1, 'per_page': 100}
        )
        vendedores = v_data.get('data', [])

        c_data = _client().get(
            '/clientes/',
            params={'page': 1, 'per_page': 100}
        )
        clientes = c_data.get('data', [])

        fmap = {x['id']: x for x in facturas}
        pmap = {x['id']: x for x in productos}
        vmap = {x['id']: x for x in vendedores}
        cmap = {x['id']: x for x in clientes}

        for detalle in detalles:
            factura = fmap.get(detalle['factura_id'], {})
            producto = pmap.get(detalle['producto_id'], {})
            cliente = cmap.get(factura.get('cliente_id'), {})
            vendedor = vmap.get(factura.get('vendedor_id'), {})

            detalle['numero_factura'] = factura.get(
                'numero_factura',
                detalle['factura_id']
            )
            detalle['cliente_nombre'] = cliente.get(
                'nombre',
                detalle.get('cliente_id', '')
            )
            detalle['vendedor_nombre'] = vendedor.get(
                'nombre',
                detalle.get('vendedor_id', '')
            )
            detalle['producto_nombre'] = producto.get(
                'nombre',
                detalle['producto_id']
            )
            detalle['fecha_emision'] = factura.get(
                'fecha_emision',
                ''
            )

        total = sum(
            float(x.get('total', 0))
            for x in detalles
        )

    except APIError as e:
        flash(e.message, 'danger')
        detalles = []
        meta = {}
        total = 0

    return render_template(
        'lista_detalles_facturas.html',
        detalles=detalles,
        meta=meta,
        total=total
    )


@detalles_bp.route('/nuevo', methods=['GET', 'POST'])
def crear_detalle():
    facturas = []
    productos = []
    factura = None
    producto = None
    precio = 0
    total = 0
    cantidad = 1

    try:
        facturas, productos = _datos_form()

        if request.method == 'POST':
            factura_id = int(request.form['factura_id'])
            producto_id = int(request.form['producto_id'])
            cantidad = int(request.form['cantidad'])
            accion = request.form.get('accion')

            factura = next(
                (
                    x for x in facturas
                    if x['id'] == factura_id
                ),
                None
            )

            producto = next(
                (
                    x for x in productos
                    if x['id'] == producto_id
                ),
                None
            )

            if not producto:
                flash(
                    'Producto no encontrado.',
                    'danger'
                )
            else:
                precio = float(producto['precio'])
                total = cantidad * precio

                if accion == 'guardar':
                    datos = {
                        'factura_id': factura_id,
                        'producto_id': producto_id,
                        'cantidad': cantidad,
                        'precio_unitario': precio,
                        'total': total
                    }

                    _client().post(
                        '/detalle_facturas/',
                        json=datos
                    )

                    flash(
                        'Detalle agregado correctamente.',
                        'success'
                    )
                    return redirect(
                        url_for('detalles_facturas.index')
                    )

    except APIError as e:
        flash(e.message, 'danger')
    except Exception as e:
        flash(
            f'Error al procesar detalle: {e}',
            'danger'
        )

    return render_template(
        'nuevo_detalle_factura.html',
        facturas=facturas,
        productos=productos,
        factura=factura,
        producto=producto,
        precio=precio,
        cantidad=cantidad,
        total=total
    )


@detalles_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_detalle(id):
    if session.get('rol') != 'admin':
        flash(
            'No tienes permisos para editar detalles.',
            'danger'
        )
        return redirect(
            url_for('detalles_facturas.index')
        )

    try:
        if request.method == 'POST':
            cantidad = int(request.form['cantidad'])
            precio = float(
                request.form['precio_unitario']
            )

            datos = {
                'factura_id': int(
                    request.form['factura_id']
                ),
                'producto_id': int(
                    request.form['producto_id']
                ),
                'cantidad': cantidad,
                'precio_unitario': precio,
                'total': cantidad * precio
            }

            _client().put(
                f'/detalle_facturas/{id}',
                json=datos
            )

            flash(
                'Detalle actualizado correctamente.',
                'success'
            )
            return redirect(
                url_for('detalles_facturas.index')
            )

        detalle = _client().get(
            f'/detalle_facturas/{id}'
        )
        facturas, productos = _datos_form()

        return render_template(
            'editar_detalle_factura.html',
            detalle=detalle,
            facturas=facturas,
            productos=productos
        )

    except APIError as e:
        flash(e.message, 'danger')
    except Exception as e:
        flash(
            f'Error: {e}',
            'danger'
        )

    return redirect(
        url_for('detalles_facturas.index')
    )


@detalles_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_detalle(id):
    if session.get('rol') != 'admin':
        flash(
            'No tienes permisos para eliminar detalles.',
            'danger'
        )
        return redirect(
            url_for('detalles_facturas.index')
        )

    try:
        _client().delete(
            f'/detalle_facturas/{id}'
        )
        flash(
            'Detalle eliminado correctamente.',
            'success'
        )
    except APIError as e:
        flash(e.message, 'danger')

    return redirect(
        url_for('detalles_facturas.index')
    )