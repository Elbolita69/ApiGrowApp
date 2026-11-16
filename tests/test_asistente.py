"""Pruebas del asistente: la regla S15 (el asistente NUNCA muestra SQL)."""

from __future__ import annotations

import pytest

from app.core import asistente as modulo_asistente
from app.core.asistente import (
    SqlNoPermitidoError,
    responder_en_lenguaje_natural,
    run_sql_query,
    validar_sql,
)

CONSULTAS_PROHIBIDAS = [
    "DELETE FROM usuario",
    "DROP TABLE x",
    "SELECT 1; DELETE FROM usuario",
    "SELECT * FROM pg_user",
    "UPDATE usuario SET estado = FALSE",
    "INSERT INTO usuario (username) VALUES ('x')",
    "SELECT * FROM information_schema.tables",
    "SELECT pg_sleep(10)",
]


@pytest.mark.parametrize("sql", CONSULTAS_PROHIBIDAS)
def test_run_sql_query_rechaza_consultas_no_permitidas(sql, monkeypatch, fake_db):
    """Las consultas que no son de solo lectura se rechazan sin ejecutarse."""
    monkeypatch.setattr(modulo_asistente, "_db", fake_db)

    with pytest.raises(SqlNoPermitidoError):
        run_sql_query(sql)

    assert fake_db.consultas == [], "No se debio ejecutar ninguna sentencia"


@pytest.mark.parametrize("sql", CONSULTAS_PROHIBIDAS)
def test_validar_sql_rechaza_las_mismas_consultas(sql):
    permitido, mensaje = validar_sql(sql)
    assert permitido is False
    assert mensaje


def test_run_sql_query_acepta_un_select(monkeypatch, fake_db):
    """Una consulta de lectura normal si se ejecuta y devuelve las filas."""
    fake_db.filas = [{"total": 3}]
    monkeypatch.setattr(modulo_asistente, "_db", fake_db)

    filas = run_sql_query(
        "SELECT COUNT(*) AS total FROM greenhouses WHERE estado = TRUE;"
    )

    assert filas == [{"total": 3}]
    assert fake_db.consultas, "Se debio ejecutar la consulta"
    assert "SET TRANSACTION READ ONLY" in fake_db.consultas[0][0]


def test_la_conexion_del_asistente_es_de_solo_lectura(monkeypatch, fake_db):
    fake_db.filas = [{"total": 1}]
    monkeypatch.setattr(modulo_asistente, "_db", fake_db)

    run_sql_query("SELECT COUNT(*) AS total FROM crops WHERE estado = TRUE;")

    sqls = " ".join(fake_db.sqls).upper()
    assert "SET TRANSACTION READ ONLY" in sqls
    assert "DEFAULT_TRANSACTION_READ_ONLY" in sqls


def test_el_asistente_responde_en_lenguaje_natural_sin_sql(monkeypatch, fake_db):
    """La respuesta es texto en espanol: nunca SQL ni nombres de tabla."""
    fake_db.respuestas = {
        "count(*)": [{"total": 20}],
        "from greenhouses": [{"nombre": "Invernadero Central"}],
    }
    monkeypatch.setattr(modulo_asistente, "_db", fake_db)

    respuestas = [
        responder_en_lenguaje_natural(
            "¿Cuántos invernaderos hay?", {"rol": "lector"}
        ),
        responder_en_lenguaje_natural(
            "Muéstrame los invernaderos registrados", {"rol": "lector"}
        ),
    ]

    for respuesta in respuestas:
        assert respuesta
        for palabra in ("select", "from", "where", "insert", "delete", "update"):
            assert palabra not in respuesta.lower(), respuesta
        assert "greenhouses" not in respuesta.lower(), respuesta
        assert "20" in respuesta


def test_el_asistente_responde_por_temas(monkeypatch, fake_db):
    """Cubre los temas minimos del taller en lenguaje natural."""
    fake_db.respuestas = {"count(*)": [{"total": 7}]}
    monkeypatch.setattr(modulo_asistente, "_db", fake_db)

    temas = [
        ("¿Cuántos cultivos hay?", "cultivos"),
        ("¿Cuántos sensores hay?", "sensores"),
        ("¿Cuántas lecturas hay?", "lecturas"),
        ("¿Cuántas alertas hay?", "alertas"),
        ("¿Cuántas zonas de riego hay?", "zonas de riego"),
        ("¿Cuántos registros de riego hay?", "registros de riego"),
        ("¿Cuántos actuadores hay?", "actuadores"),
        ("¿Cuántos usuarios hay?", "usuarios"),
        ("¿Cuántos estudiantes hay?", "estudiantes"),
    ]

    for pregunta, esperado in temas:
        respuesta = responder_en_lenguaje_natural(pregunta, {"rol": "lector"})
        assert "7" in respuesta, respuesta
        assert esperado in respuesta, respuesta
        for palabra in ("select", "from", "where"):
            assert palabra not in respuesta.lower(), respuesta


def test_pregunta_sin_respaldo_devuelve_mensaje_controlado(monkeypatch, fake_db):
    """Si no se puede resolver, responde sin filtrar informacion tecnica."""
    monkeypatch.setattr(modulo_asistente, "_db", fake_db)

    respuesta = responder_en_lenguaje_natural(
        "¿Cuál es el precio del dolar?", {"rol": "lector"}
    )

    assert respuesta == "No pude encontrar esa informacion en la base de datos."
    for palabra in ("select", "from", "where"):
        assert palabra not in respuesta.lower()


def test_los_sensores_de_un_invernadero_se_filtran_por_nombre(monkeypatch, fake_db):
    """'sensores del invernadero X' consulta por el nombre del invernadero."""
    fake_db.respuestas = {
        "count(*)": [{"total": 3}],
        "from sensors": [{"nombre": "Sensor de temperatura", "tipo": "temperatura"}],
    }
    monkeypatch.setattr(modulo_asistente, "_db", fake_db)

    respuesta = responder_en_lenguaje_natural(
        '¿Qué sensores tiene el invernadero "Invernadero Central"?',
        {"rol": "lector"},
    )

    assert "Invernadero Central" in respuesta
    assert "3" in respuesta
    for palabra in ("select", "from", "where"):
        assert palabra not in respuesta.lower()


def test_un_invernadero_numerado_se_busca_por_id_y_no_por_nombre(monkeypatch, fake_db):
    """'el invernadero 1' se resuelve por su id, no por su nombre.

    Regresion: el filtro por nombre no encontraba nada cuando el usuario
    se referia al invernadero por su numero.
    """
    fake_db.respuestas = {
        "count(*)": [{"total": 1}],
        "from sensors": [{"nombre": "Sensor Temperatura 01", "tipo": "temperatura"}],
        "from greenhouses": [{"nombre": "Invernadero Tomate Chonto Cajica"}],
    }
    monkeypatch.setattr(modulo_asistente, "_db", fake_db)

    respuesta = responder_en_lenguaje_natural(
        "Que sensores tiene el invernadero 1", {"rol": "lector"}
    )

    assert "Invernadero Tomate Chonto Cajica" in respuesta
    assert "1" in respuesta
    # La consulta debe llevar el id como parametro, no el nombre.
    consultas = [sql for sql, _ in fake_db.consultas]
    assert any("g.id = %s" in sql for sql in consultas)
    assert not any("ILIKE %s" in sql for sql in consultas)
    for palabra in ("select", "from", "where"):
        assert palabra not in respuesta.lower()


def test_el_esquema_se_arma_desde_information_schema(monkeypatch, fake_db):
    """`get_schema()` lee la estructura de la base de datos."""
    fake_db.respuestas = {
        "information_schema.columns": [
            {"table_name": "greenhouses", "column_name": "nombre", "data_type": "text"}
        ]
    }
    monkeypatch.setattr(modulo_asistente, "_db", fake_db)

    esquema = modulo_asistente.get_schema()

    assert "greenhouses" in esquema
    assert esquema["greenhouses"][0]["columna"] == "nombre"
    assert esquema["greenhouses"][0]["tipo"] == "text"
