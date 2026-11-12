from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from src.clients.api_clients import APIClient, APIError


cliente_bp = Blueprint('clientes', __name__)


def _client():
    return APIClient(session.get('api_token'))


@cliente_bp.route('/')
def index():

    q = request.args.get('q', '').strip()

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    try:

        data = _client().get(
            '/clientes/',
            params={
                'page': page,
                'per_page': per_page
            }
        )

        print(data)

        clientes = data.get('data', [])
        meta = data.get('meta', {})

    except APIError as e:

        flash(str(e), 'danger')
        clientes = []
        meta = {}

    return render_template(
        'lista_clientes.html',
        clientes=clientes,
        meta=meta,
        q=q
    )


@cliente_bp.route('/nuevo', methods=['GET', 'POST'])
def crear_cliente():

    if request.method == 'POST':

        datos = {
            "nombre": request.form["nombre"],
            "cedula": request.form["cedula"],
            "telefono": request.form["telefono"],
            "direccion": request.form["direccion"],
            "email": request.form["email"]
        }

        try:

            _client().post(
                "/clientes/",
                json=datos
            )

            flash(
                "Cliente creado correctamente",
                "success"
            )

            return redirect(
                url_for("clientes.index")
            )

        except APIError as e:

            flash(
                str(e),
                "danger"
            )

    return render_template(
        "Nuevo_Cliente.html"
    )


@cliente_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):

    if request.method == 'POST':

        datos = {
            "nombre": request.form["nombre"],
            "cedula": request.form["cedula"],
            "telefono": request.form["telefono"],
            "direccion": request.form["direccion"],
            "email": request.form["email"]
        }

        try:

            _client().put(
                f'/clientes/{id}',
                json=datos
            )

            flash(
                "Cliente actualizado correctamente",
                "success"
            )

            return redirect(
                url_for("clientes.index")
            )

        except APIError as e:

            flash(
                str(e),
                "danger"
            )


    try:

        cliente = _client().get(
            f'/clientes/{id}'
        )

    except APIError as e:

        flash(
            str(e),
            "danger"
        )

        return redirect(
            url_for("clientes.index")
        )


    return render_template(
        "editar_cliente.html",
        cliente=cliente
    )


@cliente_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_cliente(id):

    if session.get('rol') != 'admin':

        flash(
            "No tienes permisos para eliminar clientes.",
            "danger"
        )

        return redirect(
            url_for("clientes.index")
        )

    try:

        _client().delete(
            f'/clientes/{id}'
        )

        flash(
            "Cliente eliminado correctamente",
            "success"
        )

    except APIError as e:

        flash(
            str(e),
            "danger"
        )

    return redirect(
        url_for("clientes.index")
    )