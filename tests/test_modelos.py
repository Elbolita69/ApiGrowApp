from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

import app.models as modelos
from app.models.crop import Crop, CropCreate, CropUpdate
from app.models.estudiante import Estudiante, EstudianteResponse
from app.models.user import User, UserCreate, UserUpdate


def test_crop_create_no_acepta_id():
    with pytest.raises(ValidationError):
        CropCreate(nombre="Tomate", id=1)


def test_crop_update_no_acepta_id():
    with pytest.raises(ValidationError):
        CropUpdate(nombre="Tomate", id=1)


def test_user_update_no_acepta_id():
    with pytest.raises(ValidationError):
        UserUpdate(nombre="Ana", id=1)


def test_estudiante_no_acepta_id():
    with pytest.raises(ValidationError):
        Estudiante(nombre="Ana", grado=3, promedio=4.5, id=7)


@pytest.mark.parametrize("promedio", [-1, -0.5, 5.5, 6, 10])
def test_estudiante_rechaza_promedio_fuera_de_rango(promedio):
    with pytest.raises(ValidationError):
        Estudiante(nombre="Ana", grado=3, promedio=promedio)


@pytest.mark.parametrize("promedio", [0, 2.5, 4.5, 5])
def test_estudiante_acepta_promedio_valido(promedio):
    estudiante = Estudiante(nombre="Ana", grado=3, promedio=promedio)
    assert estudiante.promedio == promedio
    assert estudiante.grado == 3


def test_los_modelos_de_escritura_rechazan_campos_desconocidos():
    with pytest.raises(ValidationError):
        CropCreate(nombre="Tomate", campo_inventado="x")
    with pytest.raises(ValidationError):
        UserUpdate(campo_inventado="x")


def test_user_create_no_expone_el_hash_de_la_contrasena():
    assert "password_hash" not in UserCreate.model_fields
    assert "password" in UserCreate.model_fields
    assert "password_hash" not in User.model_fields


def test_los_modelos_de_lectura_incluyen_la_auditoria():
    for campo in ("id", "creado", "actualizado", "estado"):
        assert campo in Crop.model_fields
        assert campo in User.model_fields
        assert campo in EstudianteResponse.model_fields


def test_los_modelos_usan_pydantic_v2():
    for nombre in dir(modelos):
        objeto = getattr(modelos, nombre)
        if isinstance(objeto, type) and issubclass(objeto, BaseModel):
            assert "Config" not in vars(objeto), f"{nombre} usa la Config de Pydantic v1"
            assert "from_attributes" in objeto.model_config


def test_el_estudiante_expone_el_promedio_validado():
    estudiante = Estudiante(nombre="Ana", grado=3, promedio=4.5)
    assert estudiante.model_dump()["promedio"] == 4.5
    assert estudiante.model_dump()["grado"] == 3
