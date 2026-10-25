# Checklists por fase

Todos los comandos son de solo lectura. Excluye siempre `node_modules/`, `dist/` y `coverage/`. Si existe `rg`, úsalo en lugar de `grep -rn`.

## Inventario inicial

```bash
git -C <repo> log --oneline -10 && git -C <repo> status --short   # contexto, sin cambiar nada
find <repo>/src -type f -name '*.ts' | sed 's|/[^/]*$||' | sort | uniq -c | sort -rn | head -40
grep -rn --include='*.ts' -E '@Controller\(' <repo>/src
grep -rn --include='*.ts' -E '@(Get|Post|Put|Patch|Delete)\(' <repo>/src | wc -l
grep -rln --include='*.ts' -E '@Module\(' <repo>/src
find <repo>/src -name '*.test.ts' -o -name '*.spec.ts' | wc -l
```

## 1. Reconocimiento

- [ ] `package.json`: nombre, versión, `engines`, scripts, dependencias clave y su versión (`@nestjs/core`, `typescript`, ORM/ODM, colas, validación, logger, tests).
- [ ] Gestor de paquetes por el lockfile (`pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`) y `packageManager`.
- [ ] Node: `.nvmrc`, `engines`, la imagen base de los `Dockerfile`.
- [ ] `tsconfig*.json`: `strict`, `strictNullChecks`, `noImplicitAny`, alias de paths (`@/`).
- [ ] Herramientas: ESLint, Prettier, Husky, lint-staged, `nest-cli.json`.
- [ ] Árbol de `src/` a 2 niveles y una línea de descripción por carpeta.
- [ ] `README.md` y `docs/`: qué dicen y si están al día con el código.

## 2. Arquitectura

- [ ] Bootstrap (`main.ts`, `app.ts`): pipes, interceptores y filtros globales, versioning, prefijo global, CORS, Swagger, `bufferLogs`, shutdown hooks.
- [ ] `app.module.ts`: módulos importados, módulos `@Global()`, `ConfigModule`.
- [ ] Patrón real (modular por feature, capas, hexagonal...). Justifícalo con la estructura de carpetas, no con el README.
- [ ] Separación de capas: controller → service → repository/provider. Busca violaciones (un controller que llama al repositorio, un service que importa un SDK).
- [ ] Componentes transversales: guards, pipes, interceptors, filters, decorators propios.

## 3. Mapa de módulos

- [ ] Una fila por módulo: nombre, responsabilidad, controllers, providers, imports, exports.
- [ ] Dependencias entre módulos y ciclos (`forwardRef` es señal de ciclo).
- [ ] Estado verificable: **Completo** (endpoints, service y tests), **Parcial** (le falta alguna pieza o tiene TODOs) o **Vacío/Stub**.
- [ ] Código muerto: módulos no registrados en `app.module.ts`, archivos que nadie importa.

## 4. Endpoints y API

Tabla con: método, ruta completa (prefijo + versión + path), handler (`archivo:línea`), guard(s), DTO de entrada, validación (zod, class-validator, ninguna), respuesta y Swagger (sí/no).

- [ ] Endpoints **sin guard** (excepto health) → candidatos a P0.
- [ ] Rutas estáticas declaradas después de rutas con parámetro (`':id'` antes de `'bulk'`).
- [ ] Versionado consistente (`version: '1'` frente a un prefijo global).
- [ ] Respuestas uniformes (envelope, interceptor) y códigos HTTP correctos.
- [ ] Paginación, filtros y límites en los listados.

## 5. Lógica de negocio

- [ ] Los 3–5 flujos más importantes del dominio (pagos, autenticación, pedidos...), descritos paso a paso con `archivo:línea`.
- [ ] Transacciones: operaciones de varios pasos sin sesión ni transacción y sin compensación.
- [ ] Idempotencia en operaciones que se pueden repetir (webhooks, reintentos de cola, pagos).
- [ ] Validaciones de negocio frente a validaciones de forma.
- [ ] Acoplamiento: services enormes (más de 400 líneas), dependencias circulares, lógica duplicada entre módulos.
- [ ] Puntos de fallo: llamadas externas en el camino crítico, `await` en bucles, errores tragados (`catch {}` vacío).

## 6. Base de datos y persistencia

- [ ] ORM/ODM y forma de conexión (URI desde la config, pool, opciones).
- [ ] Inventario de colecciones o entidades: campos clave, `timestamps`, índices y relaciones o referencias.
- [ ] Índices que faltan para las queries reales (compara los `find` con los `index()`).
- [ ] Queries de riesgo: sin filtro por tenant/`store_id`, sin límite, regex sin anclar, `$where`, N+1.
- [ ] Concurrencia: read-modify-write sin operadores atómicos (`$inc`, `findOneAndUpdate`), contadores, stock.
- [ ] Migraciones o seeds: si existen y cómo se aplican.
- [ ] Mapeo de documento a DTO: si el documento crudo sale fuera de la capa de datos.

## 7. Autenticación, autorización y seguridad

- [ ] Mecanismo de autenticación (JWT propio, validación delegada a otro servicio, API keys, passport) y dónde se valida.
- [ ] Autorización: roles y permisos, y si cada recurso se filtra por su dueño (tienda, usuario). Su ausencia es un **IDOR**.
- [ ] Hashing de contraseñas (algoritmo y coste) si aplica.
- [ ] CORS, Helmet, límite de tamaño del body, rate limiting.
- [ ] Inyección: queries construidas con input del usuario, operadores Mongo sin sanear (`{ $gt: '' }`), SSRF en URLs que vienen del cliente.
- [ ] Datos sensibles en respuestas o en logs (tokens, contraseñas, datos personales completos).
- [ ] Secretos en el código: `grep -rnE "(api[_-]?key|secret|password|token)\s*[:=]\s*['\"][^'\"]{8,}" src` → informa con el valor enmascarado.
- [ ] Dependencias con vulnerabilidades conocidas: solo si el usuario autoriza `pnpm audit` (no cambia nada, pero necesita red).

## 8. Errores y observabilidad

- [ ] Filtro global de excepciones y forma del error de salida.
- [ ] Exceptions propias frente a `throw new Error` o exceptions genéricas de Nest.
- [ ] Logging: librería, transporte (Loki, CloudWatch...), uso de `console.*`, niveles, contexto (`Logger(Clase.name)`), correlación (request id).
- [ ] Health checks: qué comprueban (solo "vivo" o también Mongo y Redis).
- [ ] Métricas y trazas (Prometheus, OpenTelemetry), si existen.

## 9. Integraciones externas

- [ ] Inventario: otros microservicios, APIs de terceros, AWS (S3, SNS, SQS), Redis, colas. Para cada una: archivo cliente, autenticación y config.
- [ ] Resiliencia: timeouts, reintentos con backoff, circuit breaker, qué pasa si el otro servicio cae.
- [ ] Colas (BullMQ...): colas, jobs, `attempts`/`backoff`, `removeOnFail`, idempotencia del consumer, dead-letter.
- [ ] Webhooks entrantes: verificación de firma y deduplicación.
- [ ] Cache: qué se cachea, TTLs, invalidación, si se acopla a un proveedor concreto.
- [ ] Crons: qué hacen, frecuencia y si es seguro ejecutarlos con varias instancias en paralelo.

## 10. Pruebas y calidad del código

- [ ] Framework (Vitest, Jest) y configuración (`vitest.workspace.mts`, `jest.config`).
- [ ] Recuento de tests por capa (controllers, services, repositories, consumers) frente al número de archivos de cada capa.
- [ ] Flujos críticos de la fase 5 **sin** tests.
- [ ] Calidad de los tests: si comprueban comportamiento o solo que "se llamó al mock", tests vacíos, `skip`.
- [ ] TypeScript: número de `any` (`grep -rn ': any\|as any' src | wc -l`), `@ts-ignore`, `eslint-disable`.
- [ ] Archivos más grandes (`find src -name '*.ts' -exec wc -l {} + | sort -rn | head`) y duplicación evidente.

## 11. Configuración, infraestructura y despliegue

- [ ] Variables de entorno requeridas: tabla con nombre, uso y si tiene default. Salen de `.env.example` y `settings/`, **nunca** de `.env*`.
- [ ] Validación de la config al arrancar (zod, Joi) o ausencia de ella.
- [ ] `Dockerfile`/`Dockerfile-prod`: imagen base, multi-stage, usuario no root, `HEALTHCHECK`, tamaño.
- [ ] `docker-compose.yml`: servicios locales que levanta.
- [ ] CI/CD (`.github/workflows/`): qué corre en cada evento, si los tests bloquean el deploy, entornos (qa, prod), cómo se inyectan los secretos.
- [ ] Cómo arrancar en local según los scripts y el README.

## 12. Deuda técnica

Consolida todos los hallazgos de las fases anteriores en una matriz única (ver la plantilla). Cada hallazgo lleva:
prioridad (P0–P3), área, descripción, evidencia (`archivo:línea`), impacto, recomendación y esfuerzo (S/M/L).

Ordena por prioridad y después por esfuerzo, para que los quick wins (P0/P1 con esfuerzo S) queden arriba.

## 13. Diagramas (Mermaid)

Como mínimo:
1. **Arquitectura**: `flowchart` con el cliente, el servicio, sus módulos, la base de datos, Redis/colas y los servicios externos.
2. **Dependencias entre módulos**: `flowchart LR` a partir de los `imports` reales.
3. **Ciclo de vida de una petición**: `sequenceDiagram` desde el cliente, pasando por guard, pipe, controller, service, repository y DB, hasta el interceptor de respuesta.
4. **Un flujo de negocio clave** de la fase 5, incluyendo colas si las hay.

Si la skill `archify` está disponible y el usuario quiere diagramas visuales, ofrécelos como HTML después de los Mermaid.

## 14. Documentación final y onboarding

- [ ] Resumen ejecutivo: 5–8 líneas para alguien no técnico, con el estado general y los 3 riesgos principales.
- [ ] Ficha técnica en una tabla.
- [ ] Guía de onboarding: requisitos, clonar, variables necesarias (nombres, sin valores), levantar las dependencias, arrancar, correr los tests, dónde está cada cosa y cómo añadir un endpoint siguiendo las convenciones del repo.
