from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from src.clients.api_clients import APIClient, APIError


auth_bp = Blueprint('auth', __name__)


def _client():
    return APIClient()


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    # Si ya inició sesión, no tiene sentido mostrar nuevamente el login
    if 'usuario' in session:
        return redirect(url_for('index.index'))

    if request.method == 'POST':

        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            flash('El correo y la contraseña son obligatorios.', 'danger')
            return render_template('login.html')

        try:

            data = _client().post(
                '/auth/login',
                json={
                    'email': email,
                    'password': password
                }
            )

            # Guardamos el token que entrega el backend
            session['api_token'] = data['access_token']

            # Guardamos los datos del usuario
            session['usuario'] = data['usuario']

            # Guardamos específicamente el rol
            session['rol'] = data['usuario'].get('rol')

            return redirect(url_for('index.index'))

        except APIError as e:

            flash(e.message, 'danger')

        except Exception as e:

            print('Error en login:', e)
            flash('No fue posible conectarse con el servidor.', 'danger')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('auth.login'))