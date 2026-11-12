from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.clients.api_clients import APIClient, APIError

categorias_bp = Blueprint('categorias', __name__)


def _client():
    return APIClient(session.get('api_token'))


@categorias_bp.route('/')
def index():
    q = request.args.get('q', '').strip()

    try:
        data = _client().get('/categorias/')
        print(data)

        categorias = data.get('data', [])

    except APIError as e:
        flash(str(e), 'danger')
        categorias = []

    return render_template(
        'lista_categorias.html',
        categorias=categorias,
        q=q
    )





@categorias_bp.route('/nuevo', methods=['GET', 'POST'])
def crear_categoria():

    if request.method == 'POST':

        datos = {
            "nombre": request.form["nombre"],
            "descripcion": request.form["descripcion"]
        }

        _client().post("/categorias/", json=datos)

        flash("Categoría creada correctamente", "success")

        return redirect(url_for("categorias.index"))

    return render_template("nueva_categoria.html")


