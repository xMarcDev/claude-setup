---
name: nestjs-project-analyzer
description: >
  Análisis técnico integral, por fases y en modo solo lectura de un proyecto backend en NestJS (por ejemplo los servicios mms-* de CLEMENTE: mms-payments, mms-authentication, mms-data, mms-channels, mms-restaurants). Úsala cuando el usuario pida auditar, analizar, revisar, documentar o "entender" un backend NestJS existente: arquitectura, módulos, endpoints, lógica de negocio, base de datos, seguridad, errores y observabilidad, integraciones, tests, infraestructura, deuda técnica, diagramas o guía de onboarding. También para comparar varios servicios NestJS entre sí. No la uses para implementar, refactorizar ni arreglar código.
metadata:
  project: CLEMENTE
  tags: [clemente, nestjs, audit, read-only]
---

# NestJS Project Analyzer

Auditoría técnica de un backend NestJS en 14 fases. El resultado es un informe basado en evidencias del repositorio. El proyecto no se toca.

## Reglas estrictas

1. **Solo lectura.** No crees, edites, muevas ni borres archivos del proyecto. Tampoco hagas commits, cambies de rama ni hagas `git stash`.
2. **No ejecutes nada que cambie el estado.** Nada de `install`, migraciones, seeds, `build` (escribe `dist/`), `test:cov` (escribe `coverage/`), `lint:fix` ni `format`. Solo puedes correr `lint` o `test` si el usuario lo autoriza explícitamente, y avisando de que pueden conectarse a servicios reales.
3. **Secretos.** Nunca abras `.env`, `.env.dev`, `.env.qa`, `.env.prod` ni `.env.test`: las variables se obtienen de `.env.example`, `settings/` y los `Dockerfile`/workflows. Si encuentras un secreto en el código, informa del archivo, la línea y el tipo, con el valor enmascarado (`sk_live_****`).
4. **Evidencia o nada.** Cada afirmación lleva su `ruta:línea`. Si algo no se puede verificar, márcalo como **No verificado** o **Inferido** y nunca lo presentes como hecho.
5. **No implementes.** Si ves un problema, lo describes y propones la solución en el informe. No la aplicas.

## Flujo

1. **Alcance.** Confirma la ruta (o rutas) y la profundidad: **rápida** (fases 1, 2, 3, 4, 12 y 14) o **completa** (las 14). Si el usuario no lo dice, haz la completa.
2. **Inventario primero.** Antes de leer en detalle, saca el mapa con búsquedas (ver los comandos en [phases.md](references/phases.md)). Lee archivos completos solo donde haya lógica relevante.
3. **Ejecuta las fases en orden.** Cada fase tiene su checklist en [phases.md](references/phases.md). Si una fase no aplica (por ejemplo, no hay crons), dilo en una línea y sigue.
4. **Informe.** Usa la estructura de [report-template.md](references/report-template.md). En un repo grande, entrega una fase o un bloque de fases cada vez y pregunta si seguir.
5. **Dónde guardarlo.** Por defecto el informe va en la conversación. Si el usuario quiere un archivo, se escribe **fuera** del repo analizado (pregunta la ruta). Nunca dentro del proyecto.

## Las 14 fases

| # | Fase | Qué responde |
|---|---|---|
| 1 | Reconocimiento | Stack, versiones (Node, Nest, TS), gestor de paquetes, scripts, estructura de `src/` |
| 2 | Arquitectura | Patrón (modular, capas, hexagonal...), bootstrap (`main.ts`/`app.ts`), componentes globales |
| 3 | Mapa de módulos | Inventario de módulos, dependencias entre ellos y estado real (completo, parcial, vacío) |
| 4 | Endpoints y API | Tabla de rutas: método, path, versión, guard, DTO, validación, Swagger |
| 5 | Lógica de negocio | Flujos clave, transacciones, validaciones de negocio, acoplamiento, puntos de fallo |
| 6 | Base de datos | ORM/ODM, colecciones o entidades, índices, relaciones, consultas de riesgo, concurrencia |
| 7 | Seguridad | Autenticación, autorización, CORS, rate limiting, IDOR, inyección, exposición de datos |
| 8 | Errores y observabilidad | Filtros/interceptores globales, exceptions, logging, health checks, trazabilidad |
| 9 | Integraciones | Otros servicios, APIs de terceros, colas, cache, storage, timeouts y reintentos |
| 10 | Tests y calidad | Tipos de tests, cobertura estimada, calidad de TypeScript, lint, mantenibilidad |
| 11 | Infraestructura | Dockerfiles, compose, variables de entorno, CI/CD, entornos |
| 12 | Deuda técnica | Matriz de hallazgos P0–P3 con esfuerzo estimado |
| 13 | Diagramas | Mermaid: arquitectura, dependencias entre módulos, flujos HTTP y de colas |
| 14 | Documentación final | Resumen ejecutivo, ficha técnica y guía de onboarding |

## Prioridades

| Nivel | Significado | Ejemplos |
|---|---|---|
| **P0** | Crítico: riesgo de seguridad, pérdida de datos o caída en producción | Endpoint sin guard que expone datos, secreto en el código, IDOR |
| **P1** | Alto: bug probable o riesgo operativo serio | Sin reintentos en una llamada de pago, condición de carrera, consumer sin manejo de errores |
| **P2** | Medio: mantenibilidad o consistencia | Lógica en controllers, módulos acoplados, tests ausentes en flujos clave |
| **P3** | Bajo: estilo o mejoras menores | Nombres inconsistentes, imports sin alias, comentarios de más |

Esfuerzo: **S** (< 1 día), **M** (1–3 días), **L** (> 3 días).

## Servicios mms-* de CLEMENTE

Si el proyecto es un servicio mms-* y la skill `mms-nest-structure` está disponible, úsala como **estándar de referencia**: en las fases 2, 3, 4, 7, 8 y 12, señala cada desviación de sus reglas obligatorias (versioning, guards, infraestructura agnóstica, Logger, `AppException`, zod, `@ResponseMessage`). Sin esa skill, evalúa contra las buenas prácticas generales de NestJS.

Stack habitual de estos servicios, útil para no perder tiempo en el reconocimiento: NestJS + Mongoose, BullMQ sobre Redis, `nestjs-zod`, `nestjs-pino` con Loki, Vitest, pnpm, Docker (`Dockerfile` y `Dockerfile-prod`) y GitHub Actions (`deploy-qa`, `deploy-prod`, `unit-test`). Que sea el habitual no significa que se cumpla: verifícalo igual.

## Varios proyectos a la vez

Si el usuario pasa varias rutas:
1. Haz primero la fase 1 de todos, para tener la foto general.
2. Analiza cada servicio por separado, al nivel de profundidad acordado.
3. Termina con una **matriz comparativa**: una fila por criterio (versiones, guards, validación, logging, tests, CI...) y una columna por servicio. Así se ven las inconsistencias entre servicios.
4. Añade un diagrama Mermaid con las llamadas **entre** servicios (providers HTTP, colas y eventos compartidos).
