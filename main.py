import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import (
    rutas_greenhouses, rutas_sensors, rutas_sensor_readings,
    rutas_crops, rutas_crop_batches, rutas_users,
    rutas_alerts, rutas_irrigation_zones, rutas_irrigation_logs,
    rutas_actuators, rutas_actuator_controls, rutas_greenhouse_settings,
    rutas_auth
)

app = FastAPI(
    title="Invernadero Inteligente API",
    description="API REST para la gestión de invernaderos inteligentes con sensores, cultivos, riego y más.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
app.include_router(rutas_auth)

@app.get("/")
async def root():
    return {
        "mensaje": "Invernadero Inteligente API",
        "version": "1.0.0",
        "documentacion": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
