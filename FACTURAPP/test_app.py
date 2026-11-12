import pytest
from src.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_pagina_nuevo_vendedor_sin_sesion(client):
    respuesta = client.get("/vendedores/nuevo")

    assert respuesta.status_code == 302
    assert "/login" in respuesta.headers["Location"]


def test_pagina_nuevo_vendedor_con_sesion(client):
    with client.session_transaction() as session:
        session["usuario"] = {
            "id": 1,
            "nombre": "Usuario de prueba",
            "rol": "admin"
        }

    respuesta = client.get("/vendedores/nuevo")

    assert respuesta.status_code == 200