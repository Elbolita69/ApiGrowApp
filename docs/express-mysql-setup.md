# Guia de Despliegue: API Express con MySQL (Railway)

Este documento describe paso a paso como se configuro la API Auxiliar Express con MySQL en Railway.

---

## 1. Resumen de la Solucion

| Componente | Tecnologia |
|------------|------------|
| API | Express.js (Node.js) |
| Base de datos | MySQL (Railway) |
| Despliegue API | Render.com |
| Despliegue DB | Railway.app |

---

## 2. Cambios en el Codigo

### 2.1 Dependencies (package.json)

Se remplazo la libreria `pg` (PostgreSQL) por `mysql2` (MySQL):

```json
{
  "name": "express-api",
  "version": "1.0.0",
  "main": "src/index.js",
  "scripts": {
    "start": "node src/index.js",
    "dev": "nodemon src/index.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "mysql2": "^3.6.0",
    "cors": "^2.8.5",
    "dotenv": "^16.3.1"
  },
  "devDependencies": {
    "nodemon": "^3.0.1"
  }
}
```

### 2.2 Configuracion de Base de Datos (src/config/database.js)

Se modifico para usar `mysql2/promise` con conexion via URI:

```javascript
const mysql = require('mysql2/promise');

const pool = mysql.createPool({
    uri: process.env.MYSQL_URL,
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0,
    timezone: 'local'
});

module.exports = pool;
```

### 2.3 Rutas Actualizadas (src/routes/*.js)

Todas las rutas fueron actualizadas para usar el API de `mysql2` que retorna arrays en lugar de objetos con `rows`:

```javascript
// ANTES (PostgreSQL con pg)
const result = await pool.query('SELECT * FROM tabla');
res.json(result.rows);

// AHORA (MySQL con mysql2)
const [rows] = await pool.query('SELECT * FROM tabla');
res.json(rows);
```

Estructura de respuesta MySQL vs PostgreSQL:

| Operacion | PostgreSQL (pg) | MySQL (mysql2) |
|-----------|-----------------|----------------|
| SELECT | `result.rows` | `const [rows] = await` |
| INSERT | `result.rows[0]` | `const [result] = await` luego `result.insertId` |
| UPDATE/DELETE | `result.rowCount` | `result.affectedRows` |

---

## 3. Creacion de Base de Datos en Railway

### 3.1 Pasos para crear el servicio MySQL

1. Ir a **railway.app**
2. Crear un nuevo proyecto
3. Agregar plugin **MySQL**
4. Railway genera automaticamente las variables de entorno

### 3.2 Habilitar Conexion Externa (Public Networking)

Por defecto Railway bloquea conexiones externas. Para habilitarlas:

1. Ir al servicio MySQL en Railway
2. Buscar la seccion **Networking** o **Settings**
3. Activar **Public Networking**
4. Se genera una URL publica tipo: `mysql://root:password@turntable.proxy.rlwy.net:59812/railway`

### 3.3 Variables de Entorno Proporcionadas por Railway

```
MYSQL_DATABASE=railway
MYSQL_PUBLIC_URL=mysql://root:password@turntable.proxy.rlwy.net:59812/railway
MYSQL_ROOT_PASSWORD=password_generado
MYSQL_URL=mysql://root:password@mysql.railway.internal:3306/railway
MYSQLHOST=mysql.railway.internal
MYSQLPORT=3306
MYSQLUSER=root
```

---

## 4. Variables de Entorno en Render

En el servicio **ApiGrowExpress** en Render.com, se configuro:

| Variable | Valor |
|----------|-------|
| `MYSQL_URL` | `mysql://root:password@turntable.proxy.rlwy.net:59812/railway` |

---

## 5. Esquema de Base de Datos (express-api/schema.sql)

Las 3 tablas creadas con sus campos obligatorios:

### 5.1 Tabla: sensores_externos

```sql
CREATE TABLE sensores_externos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(100) NOT NULL,
    valor_actual DECIMAL(10, 2),
    ubicacion VARCHAR(255),
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 5.2 Tabla: lecturas_externas

```sql
CREATE TABLE lecturas_externas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sensor_id INT,
    valor DECIMAL(10, 2) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (sensor_id) REFERENCES sensores_externos(id) ON DELETE CASCADE
);
```

### 5.3 Tabla: alertas_externas

```sql
CREATE TABLE alertas_externas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mensaje TEXT NOT NULL,
    prioridad VARCHAR(20) DEFAULT 'media',
    estado BOOLEAN DEFAULT TRUE,
    creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 5.4 Datos de Prueba

```sql
INSERT INTO sensores_externos (tipo, valor_actual, ubicacion) VALUES ('temperatura', 25.50, 'Externo Norte');
INSERT INTO sensores_externos (tipo, valor_actual, ubicacion) VALUES ('humedad', 65.00, 'Externo Sur');
INSERT INTO alertas_externas (mensaje, prioridad) VALUES ('Sensor externo desconectado', 'alta');
```

---

## 6. Endpoints de la API Express

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | `/` | Raiz de la API |
| GET | `/health` | Estado de salud |
| GET | `/sensores-externos` | Listar todos los sensores |
| GET | `/sensores-externos/:id` | Obtener un sensor por ID |
| POST | `/sensores-externos` | Crear nuevo sensor |
| PUT | `/sensores-externos/:id` | Actualizar sensor |
| DELETE | `/sensores-externos/:id` | Eliminar sensor (soft delete) |
| GET | `/lecturas-externas` | Listar lecturas |
| POST | `/lecturas-externas` | Crear lectura |
| GET | `/alertas-externas` | Listar alertas |
| POST | `/alertas-externas` | Crear alerta |
| PUT | `/alertas-externas/:id` | Actualizar alerta |
| DELETE | `/alertas-externas/:id` | Eliminar alerta (soft delete) |

---

## 7. Notas Importantes

### 7.1 Conexion Externa de Railway

- `mysql.railway.internal` solo funciona dentro de Railway
- Para conectar desde Render se debe usar `turntable.proxy.rlwy.net` (public proxy)
- El puerto externo (59812) es diferente al puerto interno (3306)

### 7.2 Limitaciones de Railway MySQL

- No permite multiples sentencias SQL en una sola ejecucion
- Cada CREATE TABLE debe ejecutarse por separado
- La base de datos `railway` es la base de datos por defecto

### 7.3 Soft Delete

Todas las tablas implementan eliminacion logica (soft delete):
- `DELETE` cambia `estado` a `FALSE` en lugar de borrar el registro
- Las consultas solo retornan registros con `estado = TRUE`

---

## 8. Commits Realizados

| Hash | Descripcion |
|------|-------------|
| 6404efe | feat(express-api): switch from PostgreSQL to MySQL |
| c23e85b | fix(express): add root route / to fix Cannot GET / |
| c480306 | fix(express): remove USE statement from schema for Railway compatibility |
| c6dadd0 | fix(express): remove all comments from schema for easy copy |
| fa1508e | fix(express): use MYSQL_URL directly instead of individual params |

---

## 9. URLs de Despliegue

| Servicio | URL |
|----------|-----|
| API FastAPI (Principal) | https://apigrowapp.onrender.com |
| Web Dashboard | https://webpage-56vp.onrender.com |
| API Express (Auxiliar) | https://apigrowexpress.onrender.com |
