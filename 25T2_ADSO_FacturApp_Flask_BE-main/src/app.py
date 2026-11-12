from flask import Flask
from flask_cors import CORS

from src.models import Base, engine
from src.models.Clientes import Clientes
from src.models.Productos import Productos
from src.models.Categorias import Categorias
from src.models.Facturas import Facturas
from src.models.Detalle_facturas import Detalle_Facturas
from src.models.Vendedores import Vendedores

from src.routes.Productos_routes import productos_bp
from src.routes.Categorias_routes import categorias_bp
from src.routes.Clientes_routes import clientes_bp
from src.routes.Facturas_routes import facturas_bp
from src.routes.Detalle_facturas_routes import detalle_facturas_bp
from src.routes.Vendedores_routes import vendedores_bp
from src.routes.auth_routes import auth_bp

app = Flask(__name__)

CORS(
    app,
    origins=['http://localhost:8100']
)

app.config['JWT_SECRET_KEY'] = (
    'mi_clave_secreta_facturapp_2026_segura'
)

app.json.compact = False

app.register_blueprint(
    productos_bp,
    url_prefix='/productos'
)

app.register_blueprint(
    categorias_bp,
    url_prefix='/categorias'
)

app.register_blueprint(
    clientes_bp,
    url_prefix='/clientes'
)

app.register_blueprint(
    facturas_bp,
    url_prefix='/facturas'
)

app.register_blueprint(
    detalle_facturas_bp,
    url_prefix='/detalle_facturas'
)

app.register_blueprint(
    vendedores_bp,
    url_prefix='/vendedores'
)

app.register_blueprint(
    auth_bp,
    url_prefix='/auth'
)

Base.metadata.create_all(engine)

if __name__ == '__main__':
    app.run(debug=True)