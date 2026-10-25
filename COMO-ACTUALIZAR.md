# Cómo actualizar este repo con lo que tengo instalado

Correr en la máquina donde tengo todo (la personal) y volcar el resultado en los archivos
de este repo.

## 1. Skills sueltas (las que vivo en `~/.claude/skills/`)

No hay un `claude skills list`. Lo comprobé: `claude plugin list` solo muestra plugins, y
`claude plugin validate <dir>` valida pero no enumera. Así que se listan a mano:

```bash
ls ~/.claude/skills/                      # Linux / macOS
dir "$env:USERPROFILE\.claude\skills"     # Windows PowerShell
```

Por cada skill que quiera conservar, copiar la carpeta **completa** (con su `SKILL.md` y
todos sus archivos auxiliares) a `plugins/my-toolkit/skills/<nombre>/`:

```bash
cp -r ~/.claude/skills/<nombre> plugins/my-toolkit/skills/<nombre>
```

Si la skill es de otra persona, conservar su `LICENSE` y añadirla a la tabla de
**Atribución** del README.

## 2. Skills que vienen de un plugin

```bash
claude plugin list
```

Estas **no se copian**. Se declaran como dependencia en `.claude-plugin/marketplace.json`,
dentro de la entrada de `my-toolkit`:

```jsonc
"dependencies": ["nombre-del-plugin@nombre-del-marketplace"]
```

Y si el marketplace de origen es distinto al mío, añadirlo al allowlist de la raíz:

```jsonc
"allowCrossMarketplaceDependenciesOn": ["nombre-del-marketplace"]
```

Sin el allowlist, la instalación **falla** con
`cross-marketplace dependencies are blocked by default`.

## 3. Ver qué quedó dentro del plugin

```bash
claude plugin details my-toolkit
```

Muestra el inventario de componentes (skills, agents, hooks, MCP) y el coste en tokens,
separado en *always-on* (se paga en cada sesión) y *on-invoke* (solo al dispararse).
Útil para no inflar el arranque de cada sesión sin darme cuenta.

## 4. Servidores MCP

No van en el plugin. Ver `mcp-guides/README.md`. Para revisar qué tengo configurado:

```bash
claude mcp list              # todos, con estado de conexión
claude mcp get <nombre>      # comando, args, env y scope de uno
```

Los de scope `user` y `project` salen de un archivo de configuración y se pueden documentar
con comandos. Los conectores de claude.ai y la extensión de Chrome no: esos se describen
con pasos manuales.

## 5. Validar antes de subir

```bash
claude plugin validate .                      # el marketplace
claude plugin validate ./plugins/my-toolkit   # el plugin
```

Y la prueba de verdad, instalándolo desde el repo local sin pasar por GitHub:

```bash
claude plugin marketplace add /ruta/a/claude-setup
claude plugin install my-toolkit@xMarcDev-claude-setup --scope user
claude plugin details my-toolkit
```

Para deshacer la prueba:

```bash
claude plugin uninstall my-toolkit@xMarcDev-claude-setup
claude plugin prune                # quita las dependencias que quedaron huérfanas
claude plugin marketplace remove xMarcDev-claude-setup
```

## 6. Subir la versión

**Obligatorio en cada cambio del plugin.** `claude plugin update` solo descarga algo nuevo si la
`version` subió. Con la misma versión responde *"already at the latest version"* y las skills
nuevas no llegan nunca.

Cambiarla en los dos archivos, con el mismo valor:

- `plugins/my-toolkit/.claude-plugin/plugin.json` → `"version"`
- `.claude-plugin/marketplace.json` → `"version"`

Criterio: skill nueva o eliminada → sube el minor (`0.2.0` → `0.3.0`); ajuste dentro de una
skill → sube el patch (`0.2.0` → `0.2.1`).

## 7. Subir los cambios

```bash
git add -A
git commit -m "Actualizo skills con lo que tengo instalado"
git push
```

## 8. Actualizar en las otras máquinas

```bash
claude plugin marketplace update xMarcDev-claude-setup   # refresca el catálogo
claude plugin update my-toolkit@xMarcDev-claude-setup     # baja la nueva versión
```

Reiniciar Claude Code para que cargue las skills. Comprobar con `claude plugin details my-toolkit`.

Si `update` dice *"already at the latest version"* pero faltan skills, alguien se olvidó del
paso 6. Arreglo inmediato: reinstalar.

```bash
claude plugin uninstall my-toolkit@xMarcDev-claude-setup --scope user
claude plugin install my-toolkit@xMarcDev-claude-setup --scope user
```

No correr `claude plugin prune` entre medias: borraría las dependencias (`code-review`) que la
reinstalación vuelve a necesitar.
