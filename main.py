import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import (
    rutas_actuator_controls,
    rutas_actuators,
    rutas_alerts,
    rutas_asistente,
    rutas_auth,
    rutas_crop_batches,
    rutas_crops,
    rutas_estudiantes,
    rutas_greenhouse_settings,
    rutas_greenhouses,
    rutas_irrigation_logs,
    rutas_irrigation_zones,
    rutas_roles,
    rutas_sensor_readings,
    rutas_sensors,
    rutas_users,
)

app = FastAPI(
    title="Invernadero Inteligente API",
    description="API REST para la gestión de invernaderos inteligentes con sensores, cultivos, riego y más.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://webpage-56vp.onrender.com",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:4173",
        "http://127.0.0.1:5173",
    ]
    + [o for o in os.getenv("CORS_ORIGINS", "").split(",") if o],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rutas_greenhouses)
app.include_router(rutas_sensors)
app.include_router(rutas_sensor_readings)
app.include_router(rutas_crops)
app.include_router(rutas_crop_batches)
app.include_router(rutas_users)
app.include_router(rutas_alerts)
app.include_router(rutas_irrigation_zones)
app.include_router(rutas_irrigation_logs)
app.include_router(rutas_actuators)
app.include_router(rutas_actuator_controls)
app.include_router(rutas_greenhouse_settings)
app.include_router(rutas_estudiantes)
app.include_router(rutas_roles)
app.include_router(rutas_auth)
app.include_router(rutas_asistente)


@app.get("/")
def root():
    return {
        "mensaje": "Invernadero Inteligente API",
        "version": "1.0.0",
        "documentacion": "/docs",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
