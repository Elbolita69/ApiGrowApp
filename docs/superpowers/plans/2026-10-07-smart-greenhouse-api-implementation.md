# Smart Greenhouse API - Plan de Implementación

> **Para trabajadores agénticos:** SUBCURSOR REQUERIDO: Usar superpowers:subagent-driven-development (recomendado) o superpowers:executing-plans para implementar este plan tarea por tarea.

**Objetivo:** Implementar API principal FastAPI/PostgreSQL con JWT y API auxiliar Express/MySQL para Smart Greenhouse.

**Arquitectura:**
- FastAPI con PostgreSQL (Neon) - 12+ tablas core + 4 tablas RBAC
- Express con MySQL (PlanetScale) - 3+ tablas auxilares
- JWT para autenticación
- Despliegue en Render

**Stack Tecnológico:** FastAPI, PostgreSQL, python-jose, Express, MySQL, Render

---

## Archivo: plan.md

### Task 1: Actualizar schema.sql de PostgreSQL

**Archivos:**
- Modificar: `schema.sql`

- [ ] **Step 1: Crear backup del schema original**

```bash
cp schema.sql schema.sql.backup
```

- [ ] **Step 2: Reescribir schema.sql con campos obligatorios**

Reemplazar TODO el contenido de `schema.sql` con este schema normalizado:

```sql
-- =====================================================
-- INVERNADERO INTELIGENTE - Schema SQL (Normalizado)
-- Base de datos: PostgreSQL (Neon)
-- =====================================================

-- 1. Tabla: Invernaderos
CREATE TABLE IF NOT EXISTS greenhouses (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(200),
    area_metros_cuadrados NUMERIC(10,2),
    capacidad_maxima INTEGER,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabla: Sensores
CREATE TABLE IF NOT EXISTS sensors (
    id SERIAL PRIMARY KEY,
    greenhouse_id INTEGER REFERENCES greenhouses(id) ON DELETE CASCADE,
    tipo VARCHAR(50) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    unidad VARCHAR(20) NOT NULL,
    ubicacion VARCHAR(100),
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Tabla: Lecturas de Sensores
CREATE TABLE IF NOT EXISTS sensor_readings (
    id SERIAL PRIMARY KEY,
    sensor_id INTEGER REFERENCES sensors(id) ON DELETE CASCADE,
    valor NUMERIC(10,4) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Tabla: Cultivos (catálogo)
CREATE TABLE IF NOT EXISTS crops (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    nombre_cientifico VARCHAR(150),
    temperatura_min NUMERIC(5,2),
    temperatura_max NUMERIC(5,2),
    humedad_min NUMERIC(5,2),
    humedad_max NUMERIC(5,2),
    ph_min NUMERIC(4,2),
    ph_max NUMERIC(4,2),
    ciclo_dias INTEGER,
    descripcion TEXT,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Tabla: Lotes de Cultivos
CREATE TABLE IF NOT EXISTS crop_batches (
    id SERIAL PRIMARY KEY,
    crop_id INTEGER REFERENCES crops(id) ON DELETE SET NULL,
    greenhouse_id INTEGER REFERENCES greenhouses(id) ON DELETE CASCADE,
    fecha_siembra DATE NOT NULL,
    fecha_cosecha_estimada DATE,
    fecha_cosecha_real DATE,
    cantidad_plantas INTEGER,
    estado_lote VARCHAR(30) DEFAULT 'creciendo',
    notas TEXT,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Tabla: Roles
CREATE TABLE IF NOT EXISTS rol (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion VARCHAR(200),
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Tabla: Módulos
CREATE TABLE IF NOT EXISTS modulo (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(200),
    ruta VARCHAR(100),
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. Tabla: Matriz Permisos Rol-Módulo
CREATE TABLE IF NOT EXISTS moduloxrol (
    id SERIAL PRIMARY KEY,
    rol_id INTEGER REFERENCES rol(id) ON DELETE CASCADE,
    modulo_id INTEGER REFERENCES modulo(id) ON DELETE CASCADE,
    puede_ver BOOLEAN DEFAULT FALSE,
    puede_crear BOOLEAN DEFAULT FALSE,
    puede_editar BOOLEAN DEFAULT FALSE,
    puede_eliminar BOOLEAN DEFAULT FALSE,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(rol_id, modulo_id)
);

-- 9. Tabla: Usuarios
CREATE TABLE IF NOT EXISTS usuario (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(100),
    rol_id INTEGER REFERENCES rol(id) ON DELETE SET NULL,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 10. Tabla: Alertas
CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    greenhouse_id INTEGER REFERENCES greenhouses(id) ON DELETE CASCADE,
    sensor_id INTEGER REFERENCES sensors(id) ON DELETE SET NULL,
    tipo VARCHAR(30) NOT NULL,
    mensaje TEXT NOT NULL,
    valor_actual NUMERIC(10,4),
    umbral NUMERIC(10,4),
    prioridad VARCHAR(15) DEFAULT 'media',
    estado_alerta VARCHAR(20) DEFAULT 'activa',
    resuelta_en TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 11. Tabla: Zonas de Riego
CREATE TABLE IF NOT EXISTS irrigation_zones (
    id SERIAL PRIMARY KEY,
    greenhouse_id INTEGER REFERENCES greenhouses(id) ON DELETE CASCADE,
    nombre VARCHAR(100) NOT NULL,
    capacidad_litros_min NUMERIC(10,2),
    capacidad_litros_max NUMERIC(10,2),
    tipo VARCHAR(30) DEFAULT 'gotas',
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 12. Tabla: Historial de Riego
CREATE TABLE IF NOT EXISTS irrigation_logs (
    id SERIAL PRIMARY KEY,
    zone_id INTEGER REFERENCES irrigation_zones(id) ON DELETE CASCADE,
    duracion_minutos INTEGER NOT NULL,
    cantidad_agua_litros NUMERIC(10,2),
    modo VARCHAR(20) DEFAULT 'automatico',
    resultado VARCHAR(20) DEFAULT 'exitoso',
    notes TEXT,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 13. Tabla: Actuadores
CREATE TABLE IF NOT EXISTS actuators (
    id SERIAL PRIMARY KEY,
    greenhouse_id INTEGER REFERENCES greenhouses(id) ON DELETE CASCADE,
    tipo VARCHAR(50) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(100),
    estado_actuador VARCHAR(20) DEFAULT 'inactivo',
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 14. Tabla: Control de Actuadores
CREATE TABLE IF NOT EXISTS actuator_controls (
    id SERIAL PRIMARY KEY,
    actuator_id INTEGER REFERENCES actuators(id) ON DELETE CASCADE,
    usuario_id INTEGER REFERENCES usuario(id) ON DELETE SET NULL,
    accion VARCHAR(30) NOT NULL,
    valor_ajuste VARCHAR(50),
    resultado VARCHAR(20) DEFAULT 'exitoso',
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 15. Tabla: Configuraciones del Invernadero
CREATE TABLE IF NOT EXISTS greenhouse_settings (
    id SERIAL PRIMARY KEY,
    greenhouse_id INTEGER REFERENCES greenhouses(id) ON DELETE CASCADE UNIQUE,
    temp_min NUMERIC(5,2) DEFAULT 15.00,
    temp_max NUMERIC(5,2) DEFAULT 30.00,
    humedad_min NUMERIC(5,2) DEFAULT 40.00,
    humedad_max NUMERIC(5,2) DEFAULT 80.00,
    luz_min NUMERIC(10,2) DEFAULT 100.00,
    ph_min NUMERIC(4,2) DEFAULT 5.50,
    ph_max NUMERIC(4,2) DEFAULT 7.00,
    intervalo_lectura_minutos INTEGER DEFAULT 15,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Índices para optimizar consultas
-- =====================================================
CREATE INDEX IF NOT EXISTS idx_sensor_readings_sensor_id ON sensor_readings(sensor_id);
CREATE INDEX IF NOT EXISTS idx_sensor_readings_timestamp ON sensor_readings(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_alerts_estado ON alerts(estado_alerta);
CREATE INDEX IF NOT EXISTS idx_alerts_greenhouse_id ON alerts(greenhouse_id);
CREATE INDEX IF NOT EXISTS idx_crop_batches_estado ON crop_batches(estado_lote);
CREATE INDEX IF NOT EXISTS idx_irrigation_logs_zone_id ON irrigation_logs(zone_id);
CREATE INDEX IF NOT EXISTS idx_actuator_controls_actuator_id ON actuator_controls(actuator_id);

-- =====================================================
-- Datos iniciales (seed data)
-- =====================================================
INSERT INTO rol (nombre, descripcion) VALUES
('administrador', 'Administrador del sistema'),
('operador', 'Operador de invernaderos'),
('readonly', 'Solo lectura');

INSERT INTO modulo (nombre, descripcion, ruta) VALUES
('greenhouses', 'Gestión de invernaderos', '/greenhouses'),
('sensors', 'Gestión de sensores', '/sensors'),
('sensor_readings', 'Lecturas de sensores', '/sensor-readings'),
('crops', 'Gestión de cultivos', '/crops'),
('crop_batches', 'Lotes de cultivos', '/crop-batches'),
('alerts', 'Gestión de alertas', '/alerts'),
('irrigation_zones', 'Zonas de riego', '/irrigation-zones'),
('irrigation_logs', 'Historial de riego', '/irrigation-logs'),
('actuators', 'Actuadores', '/actuators'),
('actuator_controls', 'Control de actuadores', '/actuator-controls'),
('greenhouse_settings', 'Configuraciones', '/greenhouse-settings');

-- Permisos para administrador (todos TRUE)
INSERT INTO moduloxrol (rol_id, modulo_id, puede_ver, puede_crear, puede_editar, puede_eliminar)
SELECT 1, id, TRUE, TRUE, TRUE, TRUE FROM modulo;

-- Permisos para operador (ver, crear, editar)
INSERT INTO moduloxrol (rol_id, modulo_id, puede_ver, puede_crear, puede_editar, puede_eliminar)
SELECT 2, id, TRUE, TRUE, TRUE, FALSE FROM modulo;

-- Permisos para readonly (solo ver)
INSERT INTO moduloxrol (rol_id, modulo_id, puede_ver, puede_crear, puede_editar, puede_eliminar)
SELECT 3, id, TRUE, FALSE, FALSE, FALSE FROM modulo;
```

- [ ] **Step 3: Commit**

```bash
git add schema.sql
git commit -m "feat: update schema with normalized tables and RBAC"
```

---

### Task 2: Implementar autenticación JWT en FastAPI

**Archivos:**
- Crear: `app/core/auth.py`
- Modificar: `app/core/database.py`, `requirements.txt`, `app/api/__init__.py`

- [ ] **Step 1: Instalar dependencias JWT**

Agregar a `requirements.txt`:
```
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.9
```

- [ ] **Step 2: Crear modulo de autenticación**

Crear `app/core/auth.py`:
```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "tu-secret-key-muy-secreta-aqui-cambiar-en-produccion"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    return {"username": username, "id": payload.get("id"), "rol": payload.get("rol")}

def verify_rol(required_rol: str):
    async def rol_checker(current_user: dict = Depends(get_current_user)):
        if current_user.get("rol") != required_rol and current_user.get("rol") != "administrador":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para esta acción"
            )
        return current_user
    return rol_checker
```

- [ ] **Step 3: Commit**

```bash
git add app/core/auth.py requirements.txt
git commit -m "feat: add JWT authentication module"
```

---

### Task 3: Crear endpoint de autenticación

**Archivos:**
- Crear: `app/api/rutas_auth.py`
- Modificar: `app/api/__init__.py`, `app/main.py`

- [ ] **Step 1: Crear rutas de autenticación**

Crear `app/api/rutas_auth.py`:
```python
from datetime import timedelta
from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.core.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_HOURS
)
from app.core.database import get_connection

router = APIRouter(prefix="/auth", tags=["Autenticación"])

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    nombre: str
    rol_id: int = 2

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    nombre: str
    rol_id: int

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = None):
    if form_data is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Missing form data"
        )
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, password_hash, rol_id FROM usuario WHERE username = %s AND estado = TRUE", (form_data.username,))
    user = cur.fetchone()
    conn.close()
    
    if not user or not verify_password(form_data.password, user[2]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user[1], "id": user[0], "rol": user[3]},
        expires_delta=timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    conn = get_connection()
    cur = conn.cursor()
    
    # Verificar si existe
    cur.execute("SELECT id FROM usuario WHERE username = %s OR email = %s", (user.username, user.email))
    if cur.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Usuario o email ya existe")
    
    password_hash = get_password_hash(user.password)
    cur.execute(
        """INSERT INTO usuario (username, email, password_hash, nombre, rol_id) 
           VALUES (%s, %s, %s, %s, %s) RETURNING id, username, email, nombre, rol_id""",
        (user.username, user.email, password_hash, user.nombre, user.rol_id)
    )
    result = cur.fetchone()
    conn.commit()
    conn.close()
    
    return UserResponse(id=result[0], username=result[1], email=result[2], nombre=result[3], rol_id=result[4])

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user_from_token)):
    return current_user
```

Necesitaremos una función `get_current_user_from_token`. Agregar a `app/core/auth.py`:
```python
# Ya existe get_current_user, solo hay que exportarla correctamente
```

- [ ] **Step 2: Actualizar imports en main.py**

Modificar `app/main.py` para incluir el router de auth.

- [ ] **Step 3: Commit**

```bash
git add app/api/rutas_auth.py app/main.py
git commit -m "feat: add auth endpoints (login, register, me)"
```

---

### Task 4: Actualizar modelos para usar campos normalizados

**Archivos:**
- Modificar: `app/models/greenhouse.py`, `app/models/user.py`, `app/models/sensor.py`, etc.

- [ ] **Step 1: Actualizar GreenhouseModel**

Modificar `app/models/greenhouse.py` para agregar `estado`, `creado`, `actualizado`

- [ ] **Step 2: Commit**

```bash
git add app/models/
git commit -m "feat: update models with estado, creado, actualizado fields"
```

---

### Task 5: Crear API Express + MySQL

**Archivos:**
- Crear: `express-api/` (todo el proyecto)

- [ ] **Step 1: Inicializar proyecto Express**

```bash
mkdir -p express-api/src
cd express-api
npm init -y
npm install express mysql2 cors dotenv
npm install --save-dev nodemon
```

- [ ] **Step 2: Crear estructura del proyecto**

```
express-api/
├── src/
│   ├── index.js
│   ├── config/
│   │   └── database.js
│   ├── routes/
│   │   ├── sensores.js
│   │   ├── lecturas.js
│   │   └── alertas.js
│   └── middleware/
│       └── errorHandler.js
├── .env.example
├── package.json
└── README.md
```

- [ ] **Step 3: Crear config/database.js**

```javascript
const mysql = require('mysql2/promise');

const pool = mysql.createPool({
    host: process.env.DB_HOST || 'localhost',
    user: process.env.DB_USER || 'root',
    password: process.env.DB_PASSWORD || '',
    database: process.env.DB_NAME || 'greenhouse_aux',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
});

module.exports = pool;
```

- [ ] **Step 4: Crear schema MySQL**

Crear `express-api/schema.sql`:
```sql
-- Base de datos auxiliar MySQL
CREATE DATABASE IF NOT EXISTS greenhouse_aux;
USE greenhouse_aux;

-- Tabla: Sensores Externos
CREATE TABLE IF NOT EXISTS sensores_externos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,
    valor_actual DECIMAL(10,4),
    ubicacion VARCHAR(100),
    estado BOOLEAN DEFAULT TRUE,
    creado DATETIME DEFAULT CURRENT_TIMESTAMP,
    actualizado DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla: Lecturas Externas
CREATE TABLE IF NOT EXISTS lecturas_externas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sensor_id INT,
    valor DECIMAL(10,4) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    creado DATETIME DEFAULT CURRENT_TIMESTAMP,
    actualizado DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (sensor_id) REFERENCES sensores_externos(id) ON DELETE SET NULL
);

-- Tabla: Alertas Externas
CREATE TABLE IF NOT EXISTS alertas_externas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mensaje TEXT NOT NULL,
    prioridad VARCHAR(20) DEFAULT 'media',
    estado BOOLEAN DEFAULT TRUE,
    creado DATETIME DEFAULT CURRENT_TIMESTAMP,
    actualizado DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Seed data
INSERT INTO sensores_externos (tipo, valor_actual, ubicacion) VALUES
('temperatura', 25.5, 'Externo Norte'),
('humedad', 65.0, 'Externo Sur');

INSERT INTO alertas_externas (mensaje, prioridad) VALUES
('Sensor externo desconectado', 'alta');
```

- [ ] **Step 5: Crear routes/sensores.js**

```javascript
const express = require('express');
const router = express.Router();
const pool = require('../config/database');

// GET /sensores-externos
router.get('/', async (req, res) => {
    try {
        const [rows] = await pool.query('SELECT * FROM sensores_externos WHERE estado = TRUE');
        res.json(rows);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// POST /sensores-externos
router.post('/', async (req, res) => {
    try {
        const { tipo, valor_actual, ubicacion } = req.body;
        const [result] = await pool.query(
            'INSERT INTO sensores_externos (tipo, valor_actual, ubicacion) VALUES (?, ?, ?)',
            [tipo, valor_actual, ubicacion]
        );
        res.json({ id: result.insertId, tipo, valor_actual, ubicacion });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

module.exports = router;
```

- [ ] **Step 6: Crear index.js principal**

```javascript
const express = require('express');
const cors = require('cors');
const sensoresRouter = require('./routes/sensores');
const lecturasRouter = require('./routes/lecturas');
const alertasRouter = require('./routes/alertas');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Routes
app.get('/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date() });
});

app.use('/sensores-externos', sensoresRouter);
app.use('/lecturas-externas', lecturasRouter);
app.use('/alertas-externas', alertasRouter);

// Error handler
app.use((err, req, res, next) => {
    res.status(500).json({ error: err.message });
});

app.listen(PORT, () => {
    console.log(`Express API running on port ${PORT}`);
});
```

- [ ] **Step 7: Commit**

```bash
git add express-api/
git commit -m "feat: add Express + MySQL auxiliary API"
```

---

### Task 6: Crear documento de resumen de propuesta

**Archivos:**
- Crear: `docs/resumen_propuesta.md`

- [ ] **Step 1: Escribir el resumen**

Crear `docs/resumen_propuesta.md`:
```markdown
# Resumen de Propuesta: Sistema de Gestión de Invernaderos Inteligentes

## Problema

Los invernaderos modernos requieren monitoreo constante de múltiples variables ambientales como temperatura, humedad, pH, CO2 y luz. La gestión manual de estos datos es propensa a errores, consume tiempo excesivo y dificulta la toma de decisiones basada en datos en tiempo real.

## Población Objetivo

Agricultores y operadores de invernaderos que necesitan:
- Monitoreo automatizado de condiciones ambientales
- Control de sistemas de riego y actuadores
- Alertas tempranas ante condiciones adversas
- Registro histórico de lecturas para análisis

## Requerimientos Generales

### API Principal (FastAPI + PostgreSQL)
- CRUD completo para 12+ entidades (invernaderos, sensores, cultivos, etc.)
- Sistema de autenticación JWT
- Gestión de roles y permisos (RBAC)
- Campos de auditoría (creado, actualizado, estado)
- Despliegue en Render

### API Auxiliar (Express + MySQL)
- Gestión de sensores externos
- Registro de lecturas externas
- Sistema de alertas auxiliar
- Minimo 3 tablas normalizadas

### Documentación
- Resumen de la propuesta
- Documentación de endpoints
- Guia de despliegue

## Autores

- Esteban Gomez Jimenez
- Victor Daniel Amaranto Garizabalo

## Fecha

Octubre 2026
```

- [ ] **Step 2: Commit**

```bash
git add docs/resumen_propuesta.md
git commit -m "docs: add project proposal summary"
```

---

## Resumen de Tasks

| Task | Descripción | Archivos |
|------|-------------|----------|
| 1 | Schema PostgreSQL normalizado | `schema.sql` |
| 2 | Módulo JWT auth | `app/core/auth.py` |
| 3 | Endpoints auth (login/register) | `app/api/rutas_auth.py` |
| 4 | Modelos actualizados | `app/models/*.py` |
| 5 | API Express + MySQL | `express-api/` |
| 6 | Resumen propuesta | `docs/resumen_propuesta.md` |
