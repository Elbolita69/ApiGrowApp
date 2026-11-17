from app.api.rutas_greenhouse import router as rutas_greenhouses
from app.api.rutas_sensor import router as rutas_sensors
from app.api.rutas_sensor_reading import router as rutas_sensor_readings
from app.api.rutas_crop import router as rutas_crops
from app.api.rutas_crop_batch import router as rutas_crop_batches
from app.api.rutas_user import router as rutas_users
from app.api.rutas_alert import router as rutas_alerts
from app.api.rutas_irrigation_zone import router as rutas_irrigation_zones
from app.api.rutas_irrigation_log import router as rutas_irrigation_logs
from app.api.rutas_actuator import router as rutas_actuators
from app.api.rutas_actuator_control import router as rutas_actuator_controls
from app.api.rutas_greenhouse_setting import router as rutas_greenhouse_settings
from app.api.rutas_estudiante import router as rutas_estudiantes
from app.api.rutas_rol import router as rutas_roles
from app.api.rutas_auth import router as rutas_auth
from app.api.rutas_asistente import router as rutas_asistente

__all__ = [
    "rutas_greenhouses",
    "rutas_sensors",
    "rutas_sensor_readings",
    "rutas_crops",
    "rutas_crop_batches",
    "rutas_users",
    "rutas_alerts",
    "rutas_irrigation_zones",
    "rutas_irrigation_logs",
    "rutas_actuators",
    "rutas_actuator_controls",
    "rutas_greenhouse_settings",
    "rutas_estudiantes",
    "rutas_roles",
    "rutas_auth",
    "rutas_asistente",
]
