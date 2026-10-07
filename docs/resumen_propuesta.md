# Resumen de Propuesta: Sistema de Gestión de Invernaderos Inteligentes

## 1. Problema

Los invernaderos requieren un monitoreo constante de múltiples variables ambientales como temperatura, humedad, luz y niveles de CO2 para garantizar condiciones óptimas de cultivo. La gestión manual de estos parámetros es propensa a errores humanos, consume tiempo valioso del personal agrícola y dificulta la toma de decisiones basada en datos en tiempo real.

La ausencia de un sistema centralizado que correlacione datos de múltiples sensores limita la capacidad de los agricultores para identificar patrones, predecir problemas y optimizar el rendimiento de sus cultivos de manera científica.

## 2. Población Objetivo

Esta solución está diseñada para agricultores y operadores de invernaderos que buscan modernizar sus operaciones agrícolas mediante tecnología de monitoreo automatizado. También está orientada a empresas agrícolas de pequeño y mediano tamaño que necesitan herramientas accesibles para gestionar sus cultivos de manera más eficiente.

Cualquier persona o entidad involucrada en la agricultura de ambiente controlado puede beneficiarse de este sistema para mejorar la productividad y reducir pérdidas.

## 3. Requerimientos Generales

### 3.1 API Principal (FastAPI + PostgreSQL) - 60%

- Base de datos normalizada con 16 tablas (12 core + 4 RBAC)
- CRUD completo para todas las entidades
- Sistema de autenticación JWT
- Gestión de roles y permisos (RBAC)
- Campos de auditoría (estado, creado, actualizado)
- Despliegue en Render

### 3.2 API Auxiliar (Express + MySQL) - 30%

- Base de datos auxiliar con 3+ tablas
- CRUD para sensores externos, lecturas y alertas
- Campos de auditoría
- Despliegue en Render

### 3.3 Documentación - 10%

- Resumen de la propuesta
- Documentación de endpoints
- Guía de despliegue

## 4. Stack Tecnológico

| Componente | Tecnología |
|------------|------------|
| API Principal | FastAPI + PostgreSQL (Neon) |
| API Auxiliar | Express + MySQL |
| Auth | JWT |
| Despliegue | Render |

## 5. Autores

- Esteban Gomez Jimenez
- Victor Daniel Amaranto Garizabalo

## 6. Fecha

Octubre 2026
