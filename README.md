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
│   └── my-toolkit/              # el plugin: skills y hooks, sin MCP
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── hooks/
│       │   ├── hooks.json       # hooks que se activan con el plugin
│       │   └── <script>.py
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
| `nestjs-project-analyzer` 🏷️ **CLEMENTE** | mía | — |
| `archify` | [tt-a1i](https://github.com/tt-a1i), basado en `Cocoon-AI/architecture-diagram-generator` | MIT |
| `vercel-react-best-practices` | [Vercel](https://github.com/vercel) | MIT |

Las dos últimas son de terceros y están copiadas dentro del repo porque no existen como
plugin en ningún marketplace — es la única forma de que viajen conmigo. Conservan sus
archivos de licencia originales; ver [Atribución](#atribución).

### Hooks incluidos en el plugin

Viajan con el plugin, así que cada máquina los recibe con el `plugin update` de siempre, sin
tocar `~/.claude/settings.json`.

| Hook | Evento | Qué hace |
|---|---|---|
| `no-claude-attribution.py` | `SessionStart` | Le indica a Claude que no añada `Co-Authored-By: Claude` en commits ni "Generated with Claude Code" en PR |
| `no-claude-attribution.py` | `PreToolUse` (Bash) | Red de seguridad: si un `git commit` o `gh pr create/edit` lleva esa atribución, bloquea el comando y Claude lo repite sin ella |
| `work-context.py` | `SessionStart` (inicio, `resume`, `clear` y **tras compactar**) | Le da a Claude el estado del trabajo: ramas de trabajo, archivos sin commitear, últimos commits y las notas de la tarea activa |

Ambos requieren `python3`. Si no está instalado, los hooks fallan sin bloquear nada.

#### `no-claude-attribution`

Bloquea en vez de reescribir el comando a propósito: para reescribirlo, el hook tendría que
aprobarlo él mismo, y eso se saltaría los permisos. Límite conocido: no ve el mensaje si el
commit se hace con `git commit -F <archivo>` o el PR con `--body-file <archivo>`, porque el
texto está en un archivo y no en el comando.

#### `work-context`

Pensado para sesiones largas, donde la compactación resume la conversación y pierde detalles.
Solo **lee**: nunca crea ni modifica archivos.

| Dónde abro Claude | Qué revisa | Dónde busca las notas |
|---|---|---|
| Carpeta con varios repos (ej. `~/Desktop/Clemente`) | Cada repo hijo; muestra solo los que están en una rama de trabajo o tienen cambios | `<carpeta>/docs/tasks/` |
| Dentro de uno de esos repos | Ese repo | La misma `<carpeta>/docs/tasks/` del padre |
| Un repo suelto o un monorepo | Ese repo y sus últimos 5 commits | `<repo>/.claude/tasks/` (avisa si no está en `.gitignore`) |

Ramas base, que no cuentan como "de trabajo": `main`, `master`, `qa`, `develop`, `dev`,
`staging`, `prod` y `production`.

Una nota de tarea es un `.md` que se asocia a una rama de dos formas: por nombre de archivo
(`feat/payment-methods` → `payment-methods.md`) o con una línea `Ramas:` cuando cubre varios
repos:

```markdown
# Métodos de pago
Ramas: mms-payments@feat/payment-methods, mms-channels@feat/payment-methods
Estado: CRUD hecho; falta validar duplicados
Decisiones: soft delete; métodos por store_id
Siguiente paso: test de PaymentMethodService.create
```

Si una rama de trabajo no tiene notas, el hook lo informa con la ruta esperada. Las notas las
escribe y actualiza Claude cuando se lo pides, o siguiendo una regla en el `CLAUDE.md`. Se
muestran como máximo 40 líneas por nota.

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
