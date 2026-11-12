from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from src.clients.api_clients import APIClient, APIError


vendedor_bp = Blueprint('vendedores', __name__)


def _client():
    return APIClient(session.get('api_token'))


@vendedor_bp.route('/')
def index():

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    try:

        data = _client().get(
            '/vendedores/',
            params={
                'page': page,
                'per_page': per_page
            }
        )

        print(data)

        vendedores = data.get('data', [])
        meta = data.get('meta', {})

    except APIError as e:

        flash(str(e), 'danger')
        vendedores = []
        meta = {}

    return render_template(
        'lista_vendedores.html',
        vendedores=vendedores,
        meta=meta
    )


@vendedor_bp.route('/nuevo', methods=['GET', 'POST'])
def crear_vendedor():

    if request.method == 'POST':

        datos = {
            "nombre": request.form["nombre"],
            "direccion": request.form["direccion"],
            "telefono": request.form["telefono"],
            "cedula": request.form["cedula"],
            "email": request.form["email"],
            "activo": True
        }

        _client().post("/vendedores/", json=datos)

        flash("Vendedor creado correctamente", "success")

        return redirect(url_for("vendedores.index"))

    return render_template("Nuevo_vendedor.html")

@vendedor_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_vendedor(id):

    if session.get('rol') != 'admin':
        flash('No tienes permisos para editar vendedores.', 'danger')
        return redirect(url_for('vendedores.index'))

    try:

        # Obtener vendedor
        vendedor = _client().get(f'/vendedores/{id}')

        if request.method == 'POST':

            datos = {
                "nombre": request.form["nombre"],
                "cedula": request.form["cedula"],
                "telefono": request.form["telefono"],
                "direccion": request.form["direccion"],
                "email": request.form["email"],
                "activo": True
            }

            _client().put(
                f'/vendedores/{id}',
                json=datos
            )

            flash('Vendedor actualizado correctamente.', 'success')

            return redirect(url_for('vendedores.index'))

        return render_template(
            'Editar_vendedor.html',
            vendedor=vendedor
        )

    except APIError as e:

        flash(e.message, 'danger')

        return redirect(url_for('vendedores.index'))

    except Exception as e:

        print('Error al editar vendedor:', e)

        flash('No fue posible editar el vendedor.', 'danger')

        return redirect(url_for('vendedores.index'))