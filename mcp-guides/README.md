# Guías de MCP

Esta carpeta es **solo documentación**. Nada de lo que hay aquí se instala con el plugin:
`my-toolkit` empaqueta únicamente skills. Los servidores MCP se instalan a mano, siguiendo
la guía correspondiente.

Se hizo así a propósito. De los MCP que uso, la mayoría no son empaquetables en un
`mcp.json`: unos son conectores atados a la cuenta de claude.ai, otro viene de una extensión
de Chrome, y otros dependen de credenciales o de servicios locales (Docker, bases de datos)
que cambian de una máquina a otra. Un `mcp.json` dentro del plugin daría la falsa sensación
de que al instalar quedó todo listo.

## Un archivo por servidor

Cada MCP tiene su propio `.md` en esta carpeta. Usa [`_plantilla-mcp.md`](./_plantilla-mcp.md)
como base y nómbralo con el nombre del servidor: `playwright.md`, `gmail.md`, etc.

## Pendientes de documentar

Detectados en esta máquina al momento de armar el repo:

| Servidor | Cómo está configurado hoy | Guía |
|---|---|---|
| `playwright` | stdio scope user — `npx -y @playwright/mcp` | ☐ |
| `claude.ai Gmail` | conector de la cuenta de claude.ai | ☐ |
| `claude.ai Figma` | conector de la cuenta de claude.ai | ☐ |
| `claude-design` | HTTP first-party — `api.anthropic.com/v1/design/mcp` | ☐ |
| `claude-in-chrome` | extensión de Chrome | ☐ |
| `postgres` (investment_lab) | scope project — `docker run crystaldba/postgres-mcp` | ☐ |

## Nunca pegues credenciales aquí

Este repo es público. En las guías, las credenciales van siempre como
`${NOMBRE_DE_VARIABLE}`, nunca con el valor literal — ni siquiera las de desarrollo local.
