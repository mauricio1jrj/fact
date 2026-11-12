from flask import Flask, session, redirect, url_for, request

def create_app(config_name='default'):
    app = Flask(__name__)
    from src.config.config import config
    app.config.from_object(config[config_name])
    @app.before_request
    def verificar_login():

        # Rutas que pueden abrirse sin iniciar sesión
        rutas_publicas = [
            'auth.login',
            'static'
        ]

        # Permitir login y archivos CSS, imágenes, etc.
        if request.endpoint in rutas_publicas:
            return

        # Si no hay usuario en sesión, mandar al login
        if 'usuario' not in session:
            return redirect(url_for('auth.login'))

    
    from src.controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)
    
    from src.controllers.index_controller import index_bp
    app.register_blueprint(index_bp)

    from src.controllers.clientes_controller import cliente_bp
    app.register_blueprint(cliente_bp, url_prefix="/clientes")

    from src.controllers.productos_controllers import producto_bp
    app.register_blueprint(producto_bp, url_prefix="/productos")

    from src.controllers.vendedores_controller import vendedor_bp
    app.register_blueprint(vendedor_bp, url_prefix="/vendedores")

    from src.controllers.categorias_controllers import categorias_bp
    app.register_blueprint(categorias_bp, url_prefix="/categorias")

    from src.controllers.facturas_controllers import facturas_bp
    app.register_blueprint(facturas_bp, url_prefix="/facturas")

    from src.controllers.Detalles_facturas_controller import detalles_bp
    app.register_blueprint(detalles_bp, url_prefix='/detalles_facturas')

    

    return app