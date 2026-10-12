# Resumen de Propuesta: Sistema de Gestion de Jardines y Cultivos Inteligentes

## 1. Problema

Los jardines y areas de cultivo requieren un monitoreo constante de multiples variables ambientales como temperatura, humedad, luz y niveles de CO2 para garantizar condiciones optimas de cultivo. La gestion manual de estos parametros es propensa a errores humanos, consume tiempo valioso del personal agricola y dificulta la toma de decisiones basada en datos en tiempo real.

La ausencia de un sistema centralizado que correlacione datos de multiples sensores limita la capacidad de los agricultores para identificar patrones, predecir problemas y optimizar el rendimiento de sus cultivos de manera cientifica.

## 2. Poblacion Objetivo

Esta solucion esta disenada para agricultores y operadores de jardines y areas de cultivo que buscan modernizar sus operaciones agricolas mediante tecnologia de monitoreo automatizado. Tambien esta orientada a empresas agricolas de pequeno y mediano tamano que necesitan herramientas accesibles para gestionar sus cultivos de manera mas eficiente.

Cualquier persona o entidad involucrada en la agricultura de ambiente controlado puede beneficiarse de este sistema para mejorar la productividad y reducir perdidas.

## 3. Requerimientos Generales

### 3.1 API Principal (FastAPI + PostgreSQL) - 60%

- Base de datos normalizada con 16 tablas (12 core + 4 RBAC)
- CRUD completo para todas las entidades
- Sistema de autenticacion JWT
- Gestion de roles y permisos (RBAC)
- Campos de auditoria (estado, creado, actualizado)
- Despliegue en Render

### 3.2 API Auxiliar (Express + MySQL) - 30%

- Base de datos auxiliar con 3+ tablas
- CRUD para sensores externos, lecturas y alertas
- Campos de auditoria (estado, creado, actualizado)
- Despliegue en Render

### 3.3 Documentacion - 10%

- Resumen de la propuesta
- Documentacion de endpoints
- Guia de despliegue

## 4. Stack Tecnologico

| Componente | Tecnologia |
|------------|------------|
| API Principal | FastAPI + PostgreSQL (Neon) |
| API Auxiliar | Express + MySQL (Railway) |
| Auth | JWT |
| Despliegue | Render |

## 5. Autores

- Esteban Gomez Jimenez
- Victor Daniel Amaranto Garizabalo

## 6. Fecha

Octubre 2026
