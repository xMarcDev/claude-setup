# claude-setup

Mi configuración personal de [Claude Code](https://code.claude.com): las **skills** que uso
a diario, empaquetadas como un *plugin marketplace* instalable, más una carpeta con guías
para instalar a mano mis servidores MCP.

La idea: en una máquina nueva, dos comandos y tengo todas mis skills. Y al ser público,
cualquiera puede ver (y copiar) lo que uso.

## Estructura

```
claude-setup/
├── .claude-plugin/
│   └── marketplace.json         # catálogo del marketplace + dependencias del plugin
├── plugins/
│   └── my-toolkit/              # el plugin: SOLO skills, sin MCP
│       ├── .claude-plugin/
│       │   └── plugin.json
│       └── skills/
│           └── <cada-skill>/SKILL.md
└── mcp-guides/                  # documentación manual, NO se instala
    ├── README.md
    └── <servidor>.md            # una guía por servidor MCP
```

## Qué instala

### Skills incluidas en el plugin

| Skill | Origen | Licencia |
|---|---|---|
| `optimizador-prompts` | mía | — |
| `superpowers` | mía | — |
| `mms-nest-structure` 🏷️ **CLEMENTE** | mía | — |
| `archify` | [tt-a1i](https://github.com/tt-a1i), basado en `Cocoon-AI/architecture-diagram-generator` | MIT |
| `vercel-react-best-practices` | [Vercel](https://github.com/vercel) | MIT |

Las dos últimas son de terceros y están copiadas dentro del repo porque no existen como
plugin en ningún marketplace — es la única forma de que viajen conmigo. Conservan sus
archivos de licencia originales; ver [Atribución](#atribución).

### Skills que llegan como dependencia

Estas **no** están copiadas. El marketplace las declara como dependencia y Claude Code las
instala solo, así que siempre quedo con la versión actual de su autor:

- [`mattpocock-skills@claude-plugins-official`](https://github.com/mattpocock/skills) — 25 skills de ingeniería (tdd, grilling, code-review, domain-modeling…)
- `code-review@claude-plugins-official` — revisión de código de Anthropic

Esto funciona gracias a dos campos en `marketplace.json`:

```jsonc
{
  // sin esto, una dependencia hacia otro marketplace se bloquea
  "allowCrossMarketplaceDependenciesOn": ["claude-plugins-official"],
  "plugins": [{
    "name": "my-toolkit",
    "dependencies": ["mattpocock-skills@claude-plugins-official", "..."]
  }]
}
```

> **Ojo:** `dependencies` tiene que ir en la **entrada del marketplace**, no en `plugin.json`.
> Si se pone en `plugin.json` la validación pasa igual pero el campo se ignora en silencio y
> las dependencias no se instalan nunca.

### MCP: no van en el plugin

El plugin no trae ningún servidor MCP, a propósito. Ver [`mcp-guides/README.md`](./mcp-guides/README.md)
para el motivo y para las guías de instalación manual.

## Instalar en una máquina nueva

Dentro de una sesión de Claude Code:

```
/plugin marketplace add xMarcDev/claude-setup
/plugin install my-toolkit@xMarcDev-claude-setup
```

O sin interactivo:

```bash
claude plugin marketplace add xMarcDev/claude-setup
claude plugin install my-toolkit@xMarcDev-claude-setup --scope user
```

La salida debería terminar en `(+ 2 dependencies: mattpocock-skills, code-review)` la primera
vez. Para comprobarlo:

```bash
claude plugin details my-toolkit   # inventario de componentes y coste en tokens
claude plugin list                 # las dependencias aparecen también como instaladas
```

## Cómo lo mantengo actualizado

Ver [`COMO-ACTUALIZAR.md`](./COMO-ACTUALIZAR.md).

## Atribución

`archify` y `vercel-react-best-practices` son MIT y se redistribuyen aquí sin modificar.

- `plugins/my-toolkit/skills/archify/` incluye su `LICENSE` y `THIRD_PARTY_NOTICES.md`.
- `plugins/my-toolkit/skills/vercel-react-best-practices/` declara `license: MIT` en el
  frontmatter de su `SKILL.md`, pero **no trae archivo `LICENSE`**. Pendiente: copiar el
  texto MIT desde el repo original para cumplir con la condición de atribución.

## Seguridad: nunca subas credenciales

- Nada de API keys ni tokens en los `SKILL.md` ni en las guías de `mcp-guides/`. Usa
  `${NOMBRE_DE_VARIABLE}`.
- Revisa el diff antes de cada commit. Si alguna vez subes un secreto, **rótalo** — borrarlo
  del historial de git no basta si ya llegó a GitHub.

## Pendientes

- [ ] Añadir el `LICENSE` de `vercel-react-best-practices`.
- [ ] Escribir las guías de `mcp-guides/` (una por servidor).
- [ ] Publicar el repo en GitHub y probar la instalación desde cero.
