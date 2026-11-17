from __future__ import annotations

import pytest
from fastapi import HTTPException

from app.core import auth as modulo_auth
from app.core.auth import (
    create_access_token,
    decode_token,
    get_current_user_id,
    require_permission,
)

USUARIO = {"sub": "7", "username": "ana", "rol": "supervisor"}


def test_require_permission_consulta_moduloxrol_con_el_nombre_del_rol(
    monkeypatch, fake_db
):
    fake_db.fila = {"permitido": True}
    monkeypatch.setattr(modulo_auth, "_db", fake_db)

    checker = require_permission("greenhouses", "ver")
    assert checker(USUARIO) == USUARIO

    sql, params = fake_db.consultas[-1]
    sql_minusculas = sql.lower()
    assert "moduloxrol" in sql_minusculas
    assert "join rol r on r.id = mr.rol_id" in sql_minusculas
    assert "join modulo m on m.id = mr.modulo_id" in sql_minusculas
    assert "r.nombre = %s" in sql_minusculas
    assert "m.nombre = %s" in sql_minusculas
    assert "puede_ver" in sql_minusculas
    assert "mr.estado = true" in sql_minusculas
    assert "r.estado = true" in sql_minusculas
    assert "m.estado = true" in sql_minusculas
    assert params == ("supervisor", "greenhouses")


def test_rol_sin_permiso_recibe_403(monkeypatch, fake_db):
    fake_db.fila = {"permitido": False}
    monkeypatch.setattr(modulo_auth, "_db", fake_db)

    checker = require_permission("greenhouses", "eliminar")
    with pytest.raises(HTTPException) as error:
        checker({"sub": "1", "username": "lector", "rol": "lector"})

    assert error.value.status_code == 403
    assert "lector" in error.value.detail


def test_sin_registro_de_permiso_recibe_403(monkeypatch, fake_db):
    fake_db.fila = None
    monkeypatch.setattr(modulo_auth, "_db", fake_db)

    checker = require_permission("crops", "crear")
    with pytest.raises(HTTPException) as error:
        checker({"sub": "1", "rol": "tecnico"})

    assert error.value.status_code == 403


def test_la_accion_usa_la_columna_correspondiente(monkeypatch, fake_db):
    fake_db.fila = {"permitido": True}
    monkeypatch.setattr(modulo_auth, "_db", fake_db)

    for accion, columna in (
        ("ver", "puede_ver"),
        ("crear", "puede_crear"),
        ("editar", "puede_editar"),
        ("eliminar", "puede_eliminar"),
    ):
        checker = require_permission("crops", accion)
        checker(USUARIO)
        sql = fake_db.consultas[-1][0]
        assert columna in sql.lower()


def test_get_current_user_id_devuelve_el_id_numerico():
    assert get_current_user_id({"sub": "42"}) == 42


def test_el_token_lleva_el_nombre_del_rol():
    token = create_access_token({"sub": "3", "username": "ana", "rol": "agronomo"})
    payload = decode_token(token)
    assert payload is not None
    assert payload["sub"] == "3"
    assert payload["username"] == "ana"
    assert payload["rol"] == "agronomo"
    assert "exp" in payload
