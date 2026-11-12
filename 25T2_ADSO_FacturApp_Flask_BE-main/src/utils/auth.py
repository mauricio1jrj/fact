from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import current_app, request, jsonify

from src.models.Usuarios import Usuarios


def generar_token(usuario, horas=8):
    payload = {
        'sub':str(usuario.id),
        'email': usuario.email,
        'rol': usuario.rol,
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + timedelta(hours=horas)
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

def token_required(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        auth = request.headers.get('Authorization', '')

        if not auth.startswith('Bearer '):
            return jsonify({'message': 'Token faltante o mal formado'}), 401

        token = auth.split(' ', 1)[1].strip()

        try:
            payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], 
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido'}), 401

        usuario = Usuarios.get_by_id(payload['sub'])
        if not usuario:   
            return jsonify({'message': 'Usuario no encontrado'}), 401

        request.usuario = usuario
        return f(*args, **kwargs)

    return decorada

def rol_required(*roles):
    def decorador(f):
        @wraps(f)
        def decorada(*args, **kwargs):
            if request.usuario.rol not in roles:
                return jsonify({'message': 'Acceso denegado'}), 403
            return f(*args, **kwargs)
        return decorada
    return decorador
            

        
     