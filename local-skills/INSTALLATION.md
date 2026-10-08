# Local academic skill installation

Installed for the `E:\AgentBackdoorAttack` workspace on 2026-09-28.

| Source | Skills | Extracted source |
| --- | ---: | --- |
| [Academic Research Skills](https://github.com/Imbad0202/academic-research-skills) | 4 | `local-skills/_sources/academic-research-skills-main/` |
| [Supervisor-Skills](https://github.com/HKUSTDial/Supervisor-Skills) | 12 | `local-skills/_sources/Supervisor-Skills-main/` |

Codex project discovery uses junctions in `.agents/skills/`. The actual skill files remain on E:. `academic-deep-research` and `supervisor-deep-research` are different folder links, but both upstream `SKILL.md` files declare `name: deep-research`; mention the package name when selecting one.

Source ZIP SHA-256:

- Academic Research Skills: `8D77F4C5B9E50FAD88C18686A409C07B790642D05F76F579858E56EE9359EE87`
- Supervisor-Skills: `8B09079E67ACDC8DB7521DD42FB3ACEDD345785C7A9763217AA3B263C6DDCB45`

These are Codex project skills, available when working in this workspace. Upstream Claude-specific plugin commands and hooks are not installed by this setup. New skill payloads for this workspace should continue to use the E: drive.
