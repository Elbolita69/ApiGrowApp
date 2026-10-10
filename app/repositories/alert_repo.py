from app.core.database import Database
from app.models.alert import Alert, AlertCreate, AlertUpdate
from typing import Optional, List

class AlertRepository:
    def __init__(self):
        self.db = Database()

    async def obtener_todos(self) -> List:
        conn = await self.db.get_connection()
        try:
            query = (
                "SELECT a.*, g.nombre as greenhouse_nombre, s.nombre as sensor_nombre "
                "FROM alerts a "
                "LEFT JOIN greenhouses g ON a.greenhouse_id = g.id "
                "LEFT JOIN sensors s ON a.sensor_id = s.id "
                "ORDER BY a.timestamp DESC LIMIT 100;"
            )
            rows = await conn.fetch(query)
            return rows
        finally:
            await self.db.release_connection(conn)

    async def obtener_por_id(self, alert_id: int):
        conn = await self.db.get_connection()
        try:
            query = (
                "SELECT a.*, g.nombre as greenhouse_nombre, s.nombre as sensor_nombre "
                "FROM alerts a "
                "LEFT JOIN greenhouses g ON a.greenhouse_id = g.id "
                "LEFT JOIN sensors s ON a.sensor_id = s.id "
                "WHERE a.id = $1;"
            )
            row = await conn.fetchrow(query, alert_id)
            return row
        finally:
            await self.db.release_connection(conn)

    async def obtener_activas(self) -> List:
        conn = await self.db.get_connection()
        try:
            query = (
                "SELECT a.*, g.nombre as greenhouse_nombre, s.nombre as sensor_nombre "
                "FROM alerts a "
                "LEFT JOIN greenhouses g ON a.greenhouse_id = g.id "
                "LEFT JOIN sensors s ON a.sensor_id = s.id "
                "WHERE a.estado_alerta = 'activa' "
                "ORDER BY a.timestamp DESC;"
            )
            rows = await conn.fetch(query)
            return rows
        finally:
            await self.db.release_connection(conn)

    async def crear(self, alert: AlertCreate) -> int:
        conn = await self.db.get_connection()
        try:
            query = (
                "INSERT INTO alerts (greenhouse_id, sensor_id, tipo, mensaje, valor_actual, umbral, prioridad, estado) "
                "VALUES ($1, $2, $3, $4, $5, $6, $7, $8) RETURNING id;"
            )
            row = await conn.fetchrow(
                query,
                alert.greenhouse_id, alert.sensor_id, alert.tipo, alert.mensaje,
                alert.valor_actual, alert.umbral, alert.prioridad, alert.estado
            )
            await conn.execute("COMMIT;")
            return row['id']
        finally:
            await self.db.release_connection(conn)

    async def actualizar_estado(self, alert_id: int, estado: str) -> bool:
        conn = await self.db.get_connection()
        try:
            if estado == "resuelta":
                query = "UPDATE alerts SET estado = $1, resuelta_en = CURRENT_TIMESTAMP WHERE id = $2 RETURNING id;"
            else:
                query = "UPDATE alerts SET estado = $1 WHERE id = $2 RETURNING id;"
            result = await conn.fetchrow(query, estado, alert_id)
            await conn.execute("COMMIT;")
            return result is not None
        finally:
            await self.db.release_connection(conn)
