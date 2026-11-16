"""Pruebas de la capa de datos con la base de datos simulada."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

from app.repositories.actuator_control_repo import ActuatorControlRepository
from app.repositories.actuator_repo import ActuatorRepository
from app.repositories.alert_repo import AlertRepository
from app.repositories.crop_batch_repo import CropBatchRepository
from app.repositories.crop_repo import CropRepository
from app.repositories.estudiante_repo import EstudianteRepository
from app.repositories.greenhouse_repo import GreenhouseRepository
from app.repositories.greenhouse_setting_repo import GreenhouseSettingRepository
from app.repositories.irrigation_log_repo import IrrigationLogRepository
from app.repositories.irrigation_zone_repo import IrrigationZoneRepository
from app.repositories.rol_repo import RolRepository
from app.repositories.sensor_reading_repo import SensorReadingRepository
from app.repositories.sensor_repo import SensorRepository
from app.repositories.user_repo import UserRepository

RAIZ_APP = Path(__file__).resolve().parents[1] / "app"

# (clase del repositorio, tabla en la base de datos)
REPOSITORIOS = [
    (GreenhouseRepository, "greenhouses"),
    (SensorRepository, "sensors"),
    (SensorReadingRepository, "sensor_readings"),
    (CropRepository, "crops"),
    (CropBatchRepository, "crop_batches"),
    (AlertRepository, "alerts"),
    (IrrigationZoneRepository, "irrigation_zones"),
    (IrrigationLogRepository, "irrigation_logs"),
    (ActuatorRepository, "actuators"),
    (ActuatorControlRepository, "actuator_controls"),
    (GreenhouseSettingRepository, "greenhouse_settings"),
    (UserRepository, "usuario"),
    (EstudianteRepository, "estudiantes"),
    (RolRepository, "rol"),
]

RE_SOLO_ESTADO_ACTIVO = re.compile(
    r"where\s+(\w+\.)?estado\s*=\s*true", re.IGNORECASE
)


def _modulo_de(clase):
    return sys.modules[clase.__module__]


@pytest.mark.parametrize("clase,tabla", REPOSITORIOS)
def test_crud_completo(clase, tabla):
    """Cada repositorio de entidad expone el CRUD completo."""
    for metodo in ("obtener_todos", "obtener_por_id", "crear", "actualizar", "eliminar"):
        assert callable(getattr(clase, metodo, None)), f"{clase.__name__}.{metodo}"


@pytest.mark.parametrize("clase,tabla", REPOSITORIOS)
def test_listado_filtra_por_estado_activo(clase, tabla, patch_db):
    """El listado solo trae registros con `estado = TRUE`."""
    fake = patch_db(_modulo_de(clase))
    repo = clase()

    repo.obtener_todos()

    sql = fake.consultas[-1][0]
    assert RE_SOLO_ESTADO_ACTIVO.search(sql), sql
    assert tabla in sql.lower()


@pytest.mark.parametrize("clase,tabla", REPOSITORIOS)
def test_eliminar_es_borrado_logico(clase, tabla, patch_db):
    """El borrado es `UPDATE ... SET estado = FALSE` (nunca borra la fila)."""
    fake = patch_db(_modulo_de(clase))
    repo = clase()

    repo.eliminar(1)

    sql = fake.consultas[-1][0]
    assert "DELETE" not in sql.upper(), sql
    assert re.match(
        rf"update\s+{tabla}\s+set\s+estado\s*=\s*false", sql, re.IGNORECASE
    ), sql
    assert "actualizado = CURRENT_TIMESTAMP" in sql, sql
    assert "estado = TRUE" in sql, sql


@pytest.mark.parametrize("clase,tabla", REPOSITORIOS)
def test_listado_devuelve_lista_de_diccionarios(clase, tabla, patch_db):
    fake = patch_db(_modulo_de(clase))
    fake.filas = [{"id": 1, "nombre": "Registro 1"}]

    repo = clase()
    resultado = repo.obtener_todos()

    assert isinstance(resultado, list)
    assert resultado == [{"id": 1, "nombre": "Registro 1"}]


def test_no_existe_borrado_fisico_en_el_codigo():
    """Ningun archivo de `app/` puede contener un borrado fisico."""
    ofensores = []
    for ruta in sorted(RAIZ_APP.rglob("*.py")):
        contenido = ruta.read_text(encoding="utf-8")
        for numero, linea in enumerate(contenido.splitlines(), start=1):
            if "DELETE FROM" in linea.upper():
                ofensores.append(f"{ruta.relative_to(RAIZ_APP.parent)}:{numero}")
    assert not ofensores, f"Borrado fisico en: {', '.join(ofensores)}"


def test_no_existe_manejo_asincrono_en_el_codigo():
    """La capa de la aplicacion es sincrona (driver psycopg2)."""
    ofensores = []
    for ruta in sorted(RAIZ_APP.rglob("*.py")):
        contenido = ruta.read_text(encoding="utf-8")
        for numero, linea in enumerate(contenido.splitlines(), start=1):
            if "asyncpg" in linea or "async def" in linea:
                ofensores.append(f"{ruta.relative_to(RAIZ_APP.parent)}:{numero}")
    assert not ofensores, f"Async sin migrar en: {', '.join(ofensores)}"


def test_el_borrado_logico_actualiza_el_timestamp():
    """`eliminar_logico` siempre refresca `actualizado`."""
    from app.repositories.crud_utils import eliminar_logico

    class _Cursor:
        def __init__(self):
            self.sql = ""
            self.params = ()

        def execute(self, sql, params=None):
            self.sql = sql
            self.params = params

        def fetchone(self):
            return {"id": 1}

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    class _Conn:
        def __init__(self):
            self.cursor_ = _Cursor()

        def cursor(self, cursor_factory=None):
            return self.cursor_

    conn = _Conn()
    assert eliminar_logico(conn, "greenhouses", 7) is True
    assert "SET estado = FALSE" in conn.cursor_.sql
    assert "actualizado = CURRENT_TIMESTAMP" in conn.cursor_.sql
    assert conn.cursor_.params == (7,)
