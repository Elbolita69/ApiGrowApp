from __future__ import annotations

from typing import Any, Mapping, Optional

from psycopg2.extras import RealDictCursor

TABLAS_PERMITIDAS = frozenset(
    {
        "greenhouses",
        "sensors",
        "sensor_readings",
        "crops",
        "crop_batches",
        "alerts",
        "irrigation_zones",
        "irrigation_logs",
        "actuators",
        "actuator_controls",
        "greenhouse_settings",
        "usuario",
        "estudiantes",
        "rol",
    }
)

COLUMNAS_PERMITIDAS: Mapping[str, frozenset[str]] = {
    "greenhouses": frozenset(
        {"nombre", "ubicacion", "area_metros_cuadrados", "capacidad_maxima", "estado"}
    ),
    "sensors": frozenset(
        {"greenhouse_id", "tipo", "nombre", "unidad", "ubicacion", "estado"}
    ),
    "sensor_readings": frozenset({"sensor_id", "valor", "estado"}),
    "crops": frozenset(
        {
            "nombre",
            "nombre_cientifico",
            "temperatura_min",
            "temperatura_max",
            "humedad_min",
            "humedad_max",
            "ph_min",
            "ph_max",
            "ciclo_dias",
            "descripcion",
            "estado",
        }
    ),
    "crop_batches": frozenset(
        {
            "crop_id",
            "greenhouse_id",
            "fecha_siembra",
            "fecha_cosecha_estimada",
            "fecha_cosecha_real",
            "cantidad_plantas",
            "estado_cultivo",
            "notas",
            "estado",
        }
    ),
    "alerts": frozenset(
        {
            "greenhouse_id",
            "sensor_id",
            "tipo",
            "mensaje",
            "valor_actual",
            "umbral",
            "prioridad",
            "estado_alerta",
            "resuelta_en",
            "estado",
        }
    ),
    "irrigation_zones": frozenset(
        {
            "greenhouse_id",
            "nombre",
            "capacidad_litros_min",
            "capacidad_litros_max",
            "tipo",
            "estado",
        }
    ),
    "irrigation_logs": frozenset(
        {
            "zone_id",
            "duracion_minutos",
            "cantidad_agua_litros",
            "modo",
            "resultado",
            "notas",
            "estado",
        }
    ),
    "actuators": frozenset(
        {"greenhouse_id", "tipo", "nombre", "ubicacion", "estado_actuador", "estado"}
    ),
    "actuator_controls": frozenset(
        {"actuator_id", "usuario_id", "accion", "valor_ajuste", "resultado", "estado"}
    ),
    "greenhouse_settings": frozenset(
        {
            "greenhouse_id",
            "temp_min",
            "temp_max",
            "humedad_min",
            "humedad_max",
            "luz_min",
            "ph_min",
            "ph_max",
            "intervalo_lectura_minutos",
            "estado",
        }
    ),
    "usuario": frozenset(
        {"username", "email", "password_hash", "nombre", "rol_id", "estado"}
    ),
    "estudiantes": frozenset({"nombre", "grado", "promedio", "estado"}),
    "rol": frozenset({"nombre", "descripcion", "estado"}),
}


class TablaNoPermitida(ValueError):
    pass


def _validar_tabla(tabla: str) -> None:
    if tabla not in TABLAS_PERMITIDAS:
        raise TablaNoPermitida(f"La tabla '{tabla}' no esta permitida en esta operacion")


def actualizar_generico(
    conn: Any, tabla: str, datos: Mapping[str, Any], registro_id: int
) -> bool:
    _validar_tabla(tabla)
    permitidas = COLUMNAS_PERMITIDAS[tabla]
    campos = {
        columna: valor
        for columna, valor in (datos or {}).items()
        if columna in permitidas and valor is not None
    }
    if not campos:
        return False
    asignaciones = ", ".join(f"{columna} = %s" for columna in campos)
    valores = list(campos.values()) + [registro_id]
    sql = (
        f"UPDATE {tabla} SET {asignaciones}, actualizado = CURRENT_TIMESTAMP "
        f"WHERE id = %s AND estado = TRUE RETURNING id;"
    )
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, tuple(valores))
        fila = cur.fetchone()
    return fila is not None


def actualizar_generico_por_campo(
    conn: Any,
    tabla: str,
    campo: str,
    valor: Any,
    datos: Mapping[str, Any],
) -> bool:
    _validar_tabla(tabla)
    permitidas = COLUMNAS_PERMITIDAS[tabla]
    if campo not in permitidas:
        raise TablaNoPermitida(
            f"El campo '{campo}' no se puede actualizar en la tabla '{tabla}'"
        )
    campos = {
        columna: valor_campo
        for columna, valor_campo in (datos or {}).items()
        if columna in permitidas and valor_campo is not None
    }
    if not campos:
        return False
    asignaciones = ", ".join(f"{columna} = %s" for columna in campos)
    valores = list(campos.values()) + [valor]
    sql = (
        f"UPDATE {tabla} SET {asignaciones}, actualizado = CURRENT_TIMESTAMP "
        f"WHERE {campo} = %s AND estado = TRUE RETURNING id;"
    )
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, tuple(valores))
        fila = cur.fetchone()
    return fila is not None


def eliminar_logico(conn: Any, tabla: str, registro_id: int) -> bool:
    _validar_tabla(tabla)
    sql = (
        f"UPDATE {tabla} SET estado = FALSE, actualizado = CURRENT_TIMESTAMP "
        "WHERE id = %s AND estado = TRUE RETURNING id;"
    )
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, (registro_id,))
        fila = cur.fetchone()
    return fila is not None


def eliminar_logico_por_campo(
    conn: Any, tabla: str, campo: str, valor: Any
) -> bool:
    _validar_tabla(tabla)
    if campo not in COLUMNAS_PERMITIDAS[tabla]:
        raise TablaNoPermitida(
            f"El campo '{campo}' no se puede actualizar en la tabla '{tabla}'"
        )
    sql = (
        f"UPDATE {tabla} SET estado = FALSE, actualizado = CURRENT_TIMESTAMP "
        f"WHERE {campo} = %s AND estado = TRUE RETURNING id;"
    )
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, (valor,))
        fila = cur.fetchone()
    return fila is not None
