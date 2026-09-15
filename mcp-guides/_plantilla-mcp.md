# MCP: <nombre-del-servidor>

> Plantilla. Copia este archivo como `mcp-guides/<nombre-del-servidor>.md` y complétalo.

**Para qué lo uso:** (una línea)

**Tipo:** stdio local · HTTP remoto · conector de cuenta claude.ai · extensión del navegador

**Scope:** `user` (todas mis máquinas) · `project` (solo un repo)

## Requisitos previos

- (Node, Docker, una cuenta en tal servicio, la base de datos corriendo, etc.)

## Instalación

```bash
# comando exacto, tal como lo corrí
claude mcp add <nombre> --scope user -- <comando> <args>
```

Si es un conector de claude.ai o una extensión, describe los clics en vez de un comando:
no hay nada que añadir a un archivo de configuración, se reconecta solo al iniciar sesión.

## Variables de entorno

| Variable | Para qué | Dónde se obtiene |
|---|---|---|
| `EJEMPLO_API_KEY` | (autenticación contra X) | (enlace o instrucciones) |

Defínelas en el entorno antes de añadir el servidor. Nunca las escribas literales aquí.

## Verificar que quedó bien

```bash
claude mcp list          # debe aparecer como ✔ Connected
claude mcp get <nombre>  # muestra comando, args y scope
```

## Problemas conocidos

- (Errores que ya me encontré y cómo los resolví.)
