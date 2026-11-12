from flask import Blueprint, render_template, session, redirect, url_for

index_bp = Blueprint('index', __name__)


@index_bp.route('/')
def index():

    if 'usuario' not in session:
        return redirect(url_for('auth.login'))

    return render_template('index.html')