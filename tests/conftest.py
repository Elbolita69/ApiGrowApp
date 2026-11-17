from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Optional

import pytest

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))


class FakeCursor:
    def __init__(self, db: "FakeDatabase") -> None:
        self._db = db
        self._filas: list[Any] = []
        self._fila: Any = None

    def execute(self, sql: str, params: Optional[tuple] = None):
        self._db.registrar(sql, params)
        self._filas = self._db.filas_para(sql)
        self._fila = self._db.fila_para(sql)
        return self

    def fetchone(self):
        return self._fila

    def fetchall(self):
        return list(self._filas)

    def close(self) -> None:
        pass

    def __enter__(self) -> "FakeCursor":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        self.close()
        return False


class FakeConnection:
    def __init__(self, db: "FakeDatabase") -> None:
        self._db = db

    def cursor(self, cursor_factory=None) -> FakeCursor:
        return FakeCursor(self._db)

    def commit(self) -> None:
        self._db.commits += 1

    def rollback(self) -> None:
        self._db.rollbacks += 1

    def close(self) -> None:
        self._db.cierres += 1


class FakeConexionContext:
    def __init__(self, db: "FakeDatabase") -> None:
        self._db = db

    def __enter__(self) -> FakeConnection:
        return FakeConnection(self._db)

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False


class FakeDatabase:
    def __init__(
        self,
        filas: Optional[list] = None,
        fila: Any = None,
        respuestas: Optional[dict] = None,
    ) -> None:
        self.consultas: list[tuple[str, Any]] = []
        self.filas = list(filas or [])
        self.fila = fila
        self.respuestas = dict(respuestas or {})
        self.commits = 0
        self.rollbacks = 0
        self.cierres = 0

    def registrar(self, sql: str, params: Any = None) -> None:
        self.consultas.append((sql, params))

    @property
    def sqls(self) -> list[str]:
        return [sql for sql, _ in self.consultas]

    def filas_para(self, sql: str) -> list:
        for fragmento, filas in self.respuestas.items():
            if fragmento.lower() in sql.lower():
                return list(filas)
        return list(self.filas)

    def fila_para(self, sql: str) -> Any:
        for fragmento, fila in self.respuestas.items():
            if fragmento.lower() in sql.lower():
                return fila
        return self.fila

    def get_connection(self) -> FakeConexionContext:
        return FakeConexionContext(self)

    def release_connection(self, conn: Any) -> None:
        pass

    def close_pool(self) -> None:
        pass

    def consultar(self, sql: str, params: Optional[tuple] = None) -> list[dict]:
        self.registrar(sql, params)
        return [dict(fila) for fila in self.filas_para(sql)]

    def consultar_uno(self, sql: str, params: Optional[tuple] = None) -> Optional[dict]:
        self.registrar(sql, params)
        fila = self.fila_para(sql)
        return dict(fila) if fila else None


@pytest.fixture
def fake_db() -> FakeDatabase:
    return FakeDatabase()


@pytest.fixture
def patch_db(monkeypatch):
    def _patch(*modulos) -> FakeDatabase:
        fake = FakeDatabase()
        for modulo in modulos:
            monkeypatch.setattr(modulo, "Database", lambda: fake)
        return fake

    return _patch
