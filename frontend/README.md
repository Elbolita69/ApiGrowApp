# GrowApp - Frontend (SvelteKit + Svelte 5)

Interfaz web del invernadero inteligente. Es una SPA (SvelteKit con `adapter-static` y
fallback `index.html`) que consume dos APIs a traves del proxy de Vite:

| Prefijo        | API                                            | Puerto local |
| -------------- | ---------------------------------------------- | ------------ |
| `/api`         | Principal (FastAPI + PostgreSQL)               | 8000         |
| `/api-express` | Auxiliar (Express + MySQL)                      | 3000         |

El proxy **quita** el prefijo antes de reenviar: `/api/auth/login` llega al backend como
`/auth/login`. Se puede cambiar el destino sin tocar codigo con las variables de entorno
`VITE_API_TARGET` y `VITE_EXPRESS_TARGET` (ver `vite.config.js`).

## Requisitos

- Node.js 20 o superior
- La API principal encendida en `http://localhost:8000` (para leer datos reales)

## Instalacion (Windows / PowerShell o CMD)

```powershell
cd frontend
npm install
npm run dev
```

`npm install` regenera `node_modules` con los binarios de tu sistema. Si vienes de macOS,
borra `node_modules` antes de instalar: los binarios de Darwin no sirven en Windows.

## Comandos

| Comando           | Que hace                                                |
| ----------------- | ------------------------------------------------------- |
| `npm run dev`     | Servidor de desarrollo (http://localhost:5173)           |
| `npm run build`   | Compila y deja el sitio estatico en `build/`             |
| `npm run preview` | Sirve localmente el resultado de `npm run build`         |
| `npm run check`   | `svelte-check`: revisa tipos y errores de Svelte        |

## Estructura

```
src/
  lib/
    components/     Componentes reutilizables (uno por carpeta)
    config/         Catalogo de modulos: columnas y campos de cada CRUD
    services/       UNICA capa de acceso a la API (un archivo por dominio)
    stores/         Sesion y avisos (toasts)
    utils/          Formato de fechas, numeros y etiquetas
  routes/
    login/          Ingreso
    (app)/          Zona privada: menu por rol + una pagina por modulo
```

**Reglas del taller**

- Prohibido usar `fetch` fuera de `src/lib/services/`. Cada dominio tiene su archivo
  (`crops.js`, `sensors.js`, ...) y el nucleo `api.js` es el unico que hace peticiones.
- Nunca se muestran IDs: las llaves foraneas se pintan por nombre (`greenhouse_nombre`,
  `sensor_nombre`, ...) o se esconden si no se pueden resolver.
- Las tablas se construyen con el componente `DataTable` (DataTables + Bootstrap 5).
- Los formularios usan `bind:value`, `event.preventDefault()` en el envio y `onMount()`
  para la carga inicial.
