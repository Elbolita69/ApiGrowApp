"""Utilidades compartidas para UPDATE dinamico y eliminacion logica."""

TABLAS_PERMITIDAS = {
    "sensor_readings", "irrigation_logs", "actuator_controls", "alerts",
}


async def actualizar_generico(db, tabla: str, datos: dict, registro_id: int) -> bool:
    """UPDATE de los campos recibidos (no nulos). Siempre refresca 'actualizado'."""
    assert tabla in TABLAS_PERMITIDAS
    campos = {k: v for k, v in datos.items() if v is not None}
    if not campos:
        return False
    sets = [f"{col} = ${i}" for i, col in enumerate(campos, start=1)]
    valores = list(campos.values()) + [registro_id]
    query = (
        f"UPDATE {tabla} SET {', '.join(sets)}, actualizado = CURRENT_TIMESTAMP "
        f"WHERE id = ${len(valores)} RETURNING id;"
    )
    conn = await db.get_connection()
    try:
        row = await conn.fetchrow(query, *valores)
        return row is not None
    finally:
        await db.release_connection(conn)


async def eliminar_logico(db, tabla: str, registro_id: int) -> bool:
    """Eliminacion logica: estado = FALSE (el registro no se borra)."""
    assert tabla in TABLAS_PERMITIDAS
    conn = await db.get_connection()
    try:
        row = await conn.fetchrow(
            f"UPDATE {tabla} SET estado = FALSE, actualizado = CURRENT_TIMESTAMP "
            "WHERE id = $1 AND estado = TRUE RETURNING id;",
            registro_id,
        )
        return row is not None
    finally:
        await db.release_connection(conn)
