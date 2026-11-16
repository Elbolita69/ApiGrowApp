"""Asistente de consultas a la base de datos.

REGLA ABSOLUTA (S15): el asistente NUNCA muestra SQL al usuario.
- `get_schema()`: lee la estructura de la base de datos (solo uso interno).
- `run_sql_query()`: ejecuta ÚNICAMENTE consultas de lectura, validadas por una
  lista blanca y sobre una conexion de solo lectura.
- `responder_en_lenguaje_natural()`: responde solo con texto en espanol.

No hay LLM configurado: el clasificador de intencion es determinista y se basa
en palabras clave en espanol. Cada intencion tiene su consulta parametrizada
y su plantilla de respuesta.
"""

from __future__ import annotations

import logging
import re
import unicodedata
from typing import Any, Callable, Optional

from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)

SIN_DATOS = "No pude encontrar esa informacion en la base de datos."

# --------------------------------------------------------------- validacion
# Palabras que nunca pueden aparecer en una consulta de solo lectura.
PALABRAS_PROHIBIDAS = frozenset(
    {
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "create",
        "truncate",
        "grant",
        "revoke",
        "copy",
        "pg_sleep",
        "do",
        "call",
        "vacuum",
        "reindex",
        "cluster",
        "comment",
        "begin",
        "commit",
        "rollback",
        "savepoint",
        "prepare",
        "execute",
        "deallocate",
        "listen",
        "notify",
        "lock",
        "refresh",
        "attach",
        "detach",
        "security",
        "definer",
    }
)

# Tablas del sistema: no se consultan desde el asistente.
PATRONES_SISTEMA = re.compile(
    r"\b(information_schema|pg_catalog|pg_toast|pg_temp|pg_[a-z0-9_]*)\b",
    re.IGNORECASE,
)


class SqlNoPermitidoError(ValueError):
    """La consulta no cumple la lista blanca de solo lectura."""


def validar_sql(sql: str) -> tuple[bool, str]:
    """Valida una sentencia: solo consultas de lectura, una sola vez y sin
    palabras prohibidas ni tablas del sistema."""
    if not sql or not sql.strip():
        return False, "La consulta esta vacia."

    texto = sql.strip()
    if ";" in texto.rstrip(";"):
        return False, "Solo se permite una consulta a la vez."

    if not re.match(r"^\s*(select|with)\b", texto, re.IGNORECASE):
        return False, "Solo se permiten consultas de lectura."

    palabras = set(re.findall(r"[a-z_]+", texto.lower()))
    if palabras & PALABRAS_PROHIBIDAS:
        return False, "La consulta incluye operaciones que no estan permitidas."

    if PATRONES_SISTEMA.search(texto):
        return False, "No se pueden consultar las tablas internas del sistema."

    return True, ""


# ------------------------------------------------------------------ esquema
_db = None


def _get_db():
    """Una sola instancia (y un solo pool) para el asistente."""
    global _db
    if _db is None:
        from app.core.database import Database  # import local para evitar ciclos

        _db = Database()
    return _db


def get_schema() -> dict[str, list[dict]]:
    """Estructura de la base de datos: tabla -> columnas con su tipo.

    Uso interno del asistente: le sirve para entender el modelo de datos.
    """
    db = _get_db()
    with db.get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT table_name, column_name, data_type "
                "FROM information_schema.columns "
                "WHERE table_schema = 'public' "
                "ORDER BY table_name, ordinal_position;"
            )
            filas = cur.fetchall()

    esquema: dict[str, list[dict]] = {}
    for fila in filas:
        tabla = fila.get("table_name")
        if not tabla:
            continue
        esquema.setdefault(tabla, []).append(
            {"columna": fila.get("column_name"), "tipo": fila.get("data_type")}
        )
    return esquema


def run_sql_query(sql: str, params: Optional[tuple] = None) -> list[dict]:
    """Ejecuta una consulta de SOLO lectura y devuelve las filas.

    Antes de ejecutar valida la sentencia con `validar_sql()`. La conexion se
    abre en modo de solo lectura (`SET TRANSACTION READ ONLY`).
    """
    permitido, mensaje = validar_sql(sql)
    if not permitido:
        logger.warning("Consulta rechazada por el asistente: %s", mensaje)
        raise SqlNoPermitidoError(mensaje)

    db = _get_db()
    with db.get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Conexion de solo lectura para esta ruta.
            cur.execute("SET TRANSACTION READ ONLY;")
            cur.execute("SET LOCAL default_transaction_read_only = on;")
            cur.execute(sql, params)
            return [dict(fila) for fila in cur.fetchall()]


# --------------------------------------------- clasificador de intenciones
PALABRAS_CONTEO = (
    "cuantos",
    "cuantas",
    "cuanto",
    "cuanta",
    "numero de",
    "cantidad de",
    "total de",
    "hay",
)

ENTIDADES = (
    {"clave": "invernaderos", "etiqueta": "invernaderos", "tabla": "greenhouses"},
    {"clave": "cultivos", "etiqueta": "cultivos", "tabla": "crops"},
    {"clave": "sensores", "etiqueta": "sensores", "tabla": "sensors"},
    {"clave": "lecturas", "etiqueta": "lecturas", "tabla": "sensor_readings"},
    {"clave": "alertas", "etiqueta": "alertas", "tabla": "alerts"},
    {"clave": "zonas", "etiqueta": "zonas de riego", "tabla": "irrigation_zones"},
    {"clave": "riego", "etiqueta": "registros de riego", "tabla": "irrigation_logs"},
    {"clave": "actuadores", "etiqueta": "actuadores", "tabla": "actuators"},
    {"clave": "usuarios", "etiqueta": "usuarios", "tabla": "usuario"},
    {"clave": "estudiantes", "etiqueta": "estudiantes", "tabla": "estudiantes"},
)

# Palabras que identifican cada entidad (gana la que aparece antes en la frase).
PALABRAS_ENTIDAD = {
    "invernaderos": ("invernadero",),
    "cultivos": ("cultivo",),
    "sensores": ("sensor",),
    "lecturas": ("lectura",),
    "alertas": ("alerta",),
    "zonas": ("zona",),
    "riego": ("riego", "riegos", "regad"),
    "actuadores": ("actuador",),
    "usuarios": ("usuario",),
    "estudiantes": ("estudiante",),
}


def _normalizar(texto: str) -> str:
    """Minusculas y sin acentos (para comparar palabras clave)."""
    texto = (texto or "").lower()
    texto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def _detectar_entidad(texto: str) -> Optional[str]:
    """Entidad que menciona la pregunta.

    Gana la que aparece antes en la frase (asi "sensores del invernadero X" es
    una consulta de sensores y no de invernaderos).
    """
    return _mejor_entidad(texto, excepto=None)


def _mejor_entidad(texto: str, excepto: Optional[str]) -> Optional[str]:
    """Entidad mas relevante del texto (la que aparece antes y mas veces)."""
    candidatos = []
    for indice, entidad in enumerate(ENTIDADES):
        if entidad["clave"] == excepto:
            continue
        posiciones = []
        for palabra in PALABRAS_ENTIDAD[entidad["clave"]]:
            posiciones.extend(
                coincidencia.start()
                for coincidencia in re.finditer(rf"\b{palabra}\w*", texto)
            )
        if posiciones:
            candidatos.append(
                (min(posiciones), -len(posiciones), indice, entidad["clave"])
            )
    if not candidatos:
        return None
    candidatos.sort()
    return candidatos[0][3]


def _detectar_otra_entidad(texto: str, excepto: str) -> Optional[str]:
    """Primera entidad distinta de `excepto` que menciona la pregunta."""
    return _mejor_entidad(texto, excepto=excepto)


def _extraer_nombre_invernadero(pregunta: str) -> Optional[str]:
    """Nombre del invernadero mencionado en la pregunta (entre comillas o al final)."""
    entre_comillas = re.search(r"[\"“']([^\"“”']{2,80})[\"”']", pregunta or "")
    if entre_comillas:
        return entre_comillas.group(1).strip()

    texto = _normalizar(pregunta)
    coincidencia = re.search(r"invernaderos?\s+(?:llamado\s+|nombre\s+)?(.+)$", texto)
    if not coincidencia:
        return None
    resto = coincidencia.group(1).strip()
    resto = re.split(
        r"\b(tiene|tienen|hay|con|registrad|registrados|muestra|mostrar|listar|cuantos|cuantas)\b",
        resto,
    )[0]
    resto = resto.strip(" ?.!")
    return resto or None


# --------------------------------------------------------- consultas por tema
SQL_CONTEO = {
    "invernaderos": "SELECT COUNT(*) AS total FROM greenhouses WHERE estado = TRUE;",
    "cultivos": "SELECT COUNT(*) AS total FROM crops WHERE estado = TRUE;",
    "sensores": "SELECT COUNT(*) AS total FROM sensors WHERE estado = TRUE;",
    "lecturas": "SELECT COUNT(*) AS total FROM sensor_readings WHERE estado = TRUE;",
    "alertas": "SELECT COUNT(*) AS total FROM alerts WHERE estado = TRUE;",
    "zonas": "SELECT COUNT(*) AS total FROM irrigation_zones WHERE estado = TRUE;",
    "riego": "SELECT COUNT(*) AS total FROM irrigation_logs WHERE estado = TRUE;",
    "actuadores": "SELECT COUNT(*) AS total FROM actuators WHERE estado = TRUE;",
    "usuarios": "SELECT COUNT(*) AS total FROM usuario WHERE estado = TRUE;",
    "estudiantes": "SELECT COUNT(*) AS total FROM estudiantes WHERE estado = TRUE;",
}

SQL_LISTADO = {
    "invernaderos": (
        "SELECT nombre, ubicacion FROM greenhouses WHERE estado = TRUE "
        "ORDER BY id ASC LIMIT 20;"
    ),
    "cultivos": (
        "SELECT nombre, nombre_cientifico FROM crops WHERE estado = TRUE "
        "ORDER BY id ASC LIMIT 20;"
    ),
    "sensores": (
        "SELECT s.nombre, s.tipo, s.unidad, g.nombre AS greenhouse_nombre "
        "FROM sensors s JOIN greenhouses g ON s.greenhouse_id = g.id "
        "WHERE s.estado = TRUE ORDER BY s.id ASC LIMIT 20;"
    ),
    "lecturas": (
        "SELECT s.nombre AS sensor_nombre, sr.valor, s.unidad, sr.timestamp "
        "FROM sensor_readings sr JOIN sensors s ON sr.sensor_id = s.id "
        "WHERE sr.estado = TRUE ORDER BY sr.timestamp DESC LIMIT 10;"
    ),
    "alertas": (
        "SELECT a.mensaje, a.prioridad, a.estado_alerta, g.nombre AS greenhouse_nombre "
        "FROM alerts a LEFT JOIN greenhouses g ON a.greenhouse_id = g.id "
        "WHERE a.estado = TRUE ORDER BY a.creado DESC LIMIT 20;"
    ),
    "zonas": (
        "SELECT iz.nombre, iz.tipo, g.nombre AS greenhouse_nombre "
        "FROM irrigation_zones iz JOIN greenhouses g ON iz.greenhouse_id = g.id "
        "WHERE iz.estado = TRUE ORDER BY iz.id ASC LIMIT 20;"
    ),
    "riego": (
        "SELECT iz.nombre AS zone_nombre, il.duracion_minutos, il.cantidad_agua_litros, "
        "il.modo FROM irrigation_logs il JOIN irrigation_zones iz ON il.zone_id = iz.id "
        "WHERE il.estado = TRUE ORDER BY il.creado DESC LIMIT 20;"
    ),
    "actuadores": (
        "SELECT a.nombre, a.tipo, a.estado_actuador, g.nombre AS greenhouse_nombre "
        "FROM actuators a JOIN greenhouses g ON a.greenhouse_id = g.id "
        "WHERE a.estado = TRUE ORDER BY a.id ASC LIMIT 20;"
    ),
    "usuarios": (
        "SELECT u.username, u.nombre, r.nombre AS rol_nombre "
        "FROM usuario u LEFT JOIN rol r ON u.rol_id = r.id "
        "WHERE u.estado = TRUE ORDER BY u.id ASC LIMIT 20;"
    ),
    "estudiantes": (
        "SELECT nombre, grado, promedio FROM estudiantes WHERE estado = TRUE "
        "ORDER BY id ASC LIMIT 20;"
    ),
}

SQL_CONTEO_SENSORES_INVERNADERO = (
    "SELECT COUNT(*) AS total FROM sensors s "
    "JOIN greenhouses g ON s.greenhouse_id = g.id "
    "WHERE s.estado = TRUE AND g.nombre ILIKE %s;"
)

SQL_SENSORES_INVERNADERO = (
    "SELECT s.nombre, s.tipo, s.unidad, g.nombre AS greenhouse_nombre FROM sensors s "
    "JOIN greenhouses g ON s.greenhouse_id = g.id "
    "WHERE s.estado = TRUE AND g.nombre ILIKE %s ORDER BY s.id ASC LIMIT 20;"
)

SQL_CONTEO_ALERTAS_ACTIVAS = (
    "SELECT COUNT(*) AS total FROM alerts "
    "WHERE estado = TRUE AND estado_alerta = 'activa';"
)

SQL_ALERTAS_ACTIVAS = (
    "SELECT a.mensaje, a.prioridad, a.estado_alerta, g.nombre AS greenhouse_nombre "
    "FROM alerts a LEFT JOIN greenhouses g ON a.greenhouse_id = g.id "
    "WHERE a.estado = TRUE AND a.estado_alerta = 'activa' "
    "ORDER BY a.creado DESC LIMIT 20;"
)


def _detalle_entidad(clave: str) -> Callable[[dict], str]:
    """Formato corto en espanol de un registro (sin SQL ni nombres de tabla)."""
    if clave == "lecturas":
        return lambda fila: (
            f"{fila.get('sensor_nombre') or 'sensor'}: {fila.get('valor')} "
            f"{fila.get('unidad') or ''}".strip()
        )
    if clave == "alertas":
        return lambda fila: (
            f"{fila.get('mensaje') or 'alerta'} ({fila.get('prioridad') or 'sin prioridad'})"
        )
    if clave == "riego":
        return lambda fila: (
            f"{fila.get('zone_nombre') or 'zona'}: {fila.get('duracion_minutos')} min, "
            f"{fila.get('cantidad_agua_litros')} litros"
        )
    if clave == "zonas":
        return lambda fila: (
            f"{fila.get('nombre')} ({fila.get('tipo') or 'sin tipo'}, "
            f"{fila.get('greenhouse_nombre') or 'sin invernadero'})"
        )
    if clave == "sensores":
        return lambda fila: (
            f"{fila.get('nombre')} ({fila.get('tipo') or 'sin tipo'}, "
            f"{fila.get('greenhouse_nombre') or 'sin invernadero'})"
        )
    if clave == "actuadores":
        return lambda fila: (
            f"{fila.get('nombre')} ({fila.get('estado_actuador') or 'sin estado'})"
        )
    if clave == "usuarios":
        return lambda fila: (
            f"{fila.get('username')}"
            f"{' (' + str(fila.get('rol_nombre')) + ')' if fila.get('rol_nombre') else ''}"
        )
    if clave == "estudiantes":
        return lambda fila: (
            f"{fila.get('nombre')} (grado {fila.get('grado')}, "
            f"promedio {fila.get('promedio')})"
        )
    if clave == "cultivos":
        return lambda fila: (
            f"{fila.get('nombre')}"
            f"{' (' + str(fila.get('nombre_cientifico')) + ')' if fila.get('nombre_cientifico') else ''}"
        )
    return lambda fila: str(fila.get("nombre"))


def _enumerar(filas: list[dict], detalle: Callable[[dict], str]) -> str:
    partes = [detalle(fila) for fila in filas if fila]
    if not partes:
        return ""
    if len(partes) > 10:
        restantes = len(partes) - 10
        partes = partes[:10] + [f"y {restantes} mas"]
    return ", ".join(partes)


def _responder_conteo(filas: list[dict], etiqueta: str) -> str:
    total = 0
    if filas:
        valor = filas[0].get("total")
        total = int(valor) if valor is not None else 0
    if total == 0:
        return f"No hay {etiqueta} en la base de datos."
    return f"Hay {total} {etiqueta} en la base de datos."


def _responder_listado(
    filas: list[dict], total: int, etiqueta: str, detalle: Callable[[dict], str]
) -> str:
    if not filas:
        return f"No hay {etiqueta} en la base de datos."
    lista = _enumerar(filas, detalle)
    return (
        f"Hay {total} {etiqueta} en la base de datos. "
        f"Los primeros son: {lista}."
    )


def responder_en_lenguaje_natural(pregunta: str, usuario: Optional[dict] = None) -> str:
    """Responde una pregunta en espanol usando solo datos de la base.

    Devuelve SIEMPRE texto en lenguaje natural: nunca la sentencia SQL ni
    nombres de tabla crudos.
    """
    texto = _normalizar(pregunta)
    if not texto.strip():
        return SIN_DATOS

    clave = _detectar_entidad(texto)
    if clave is None:
        return SIN_DATOS

    conteo = any(palabra in texto for palabra in PALABRAS_CONTEO)
    entidad = next(e for e in ENTIDADES if e["clave"] == clave)
    etiqueta = entidad["etiqueta"]

    try:
        esquema = get_schema()
    except Exception:  # el esquema es solo contexto: no debe romper la respuesta
        logger.warning("No se pudo leer el esquema de la base de datos", exc_info=True)
        esquema = {}

    # "sensores del invernadero X": se filtra por el nombre del invernadero.
    nombre_invernadero = None
    if "invernadero" in texto:
        nombre = _extraer_nombre_invernadero(pregunta)
        if clave == "sensores" and nombre:
            nombre_invernadero = nombre
        elif clave == "invernaderos" and nombre:
            # El invernadero es el filtro, no el tema de la pregunta.
            otra = _detectar_otra_entidad(texto, "invernaderos")
            if otra:
                clave = otra
                entidad = next(e for e in ENTIDADES if e["clave"] == clave)
                etiqueta = entidad["etiqueta"]

    try:
        if esquema and entidad["tabla"] not in esquema:
            return SIN_DATOS

        if nombre_invernadero:
            if conteo:
                filas = run_sql_query(
                    SQL_CONTEO_SENSORES_INVERNADERO, (f"%{nombre_invernadero}%",)
                )
                total = int(filas[0].get("total") or 0) if filas else 0
                return (
                    f"El invernadero {nombre_invernadero} tiene {total} sensores "
                    "en la base de datos."
                )
            filas = run_sql_query(
                SQL_SENSORES_INVERNADERO, (f"%{nombre_invernadero}%",)
            )
            if not filas:
                return (
                    f"El invernadero {nombre_invernadero} no tiene sensores registrados."
                )
            total_filas = run_sql_query(
                SQL_CONTEO_SENSORES_INVERNADERO, (f"%{nombre_invernadero}%",)
            )
            total = int(total_filas[0].get("total") or 0) if total_filas else 0
            lista = _enumerar(filas, _detalle_entidad("sensores"))
            return (
                f"El invernadero {nombre_invernadero} tiene {total} sensores: {lista}."
            )

        if clave == "alertas" and "activa" in texto:
            if conteo:
                filas = run_sql_query(SQL_CONTEO_ALERTAS_ACTIVAS, ())
                return _responder_conteo(filas, "alertas activas")
            filas = run_sql_query(SQL_ALERTAS_ACTIVAS, ())
            total_filas = run_sql_query(SQL_CONTEO_ALERTAS_ACTIVAS, ())
            total = int(total_filas[0].get("total") or 0) if total_filas else 0
            return _responder_listado(
                filas, total, "alertas activas", _detalle_entidad("alertas")
            )

        if conteo:
            filas = run_sql_query(SQL_CONTEO[clave], ())
            return _responder_conteo(filas, etiqueta)

        total_filas = run_sql_query(SQL_CONTEO[clave], ())
        total = int(total_filas[0].get("total") or 0) if total_filas else 0
        filas = run_sql_query(SQL_LISTADO[clave], ())
        return _responder_listado(
            filas, total, etiqueta, _detalle_entidad(clave)
        )
    except SqlNoPermitidoError:
        logger.warning("El asistente descarto una consulta no permitida")
        return SIN_DATOS
    except Exception:
        logger.exception("Fallo la consulta del asistente")
        return SIN_DATOS
