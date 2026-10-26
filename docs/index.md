# modern-py

modern-py is a Copier template for Python projects. Each project gets one engineering standard, and tools enforce the
standard. When the template changes, each project takes the change with `copier update`.

- [Start a project](start.md): the questions, the profiles, the features and the first steps.
- [Update a project](update.md): take the changes of the template, and resolve a conflict.
- [Library choices](libraries.md): the library for each need, the reason, and the guard that enforces it.
- [Inventory](plans/inventory.md): where each part of the standard comes from.

## What a project gets

Every project is a library at its base. The base holds the process:

| Area | Tools |
| --- | --- |
| Environment | uv with a lockfile and a 7-day cooldown on new releases. |
| Hooks | prek, with ruff (every rule), hadolint for each Dockerfile, vulture, pyrefly (strict, 100% type coverage), import-linter, semgrep, the layout check, the dependency check and the check that each workaround has a written reason. |
| Tests | pytest with hypothesis, 100% branch coverage, and cosmic-ray mutation testing with zero surviving mutants. |
| Run-time types | beartype on every function of the package. |
| Commits | conventional commits, checked by a commit-msg hook and in CI, with a size limit. |
| Releases | scriv changelog fragments, and a release workflow that sets the version, tags it and creates the GitHub release. |
| Docs | Zensical with mkdocstrings, in strict mode. |
| CI | the gates in order, a report comment on each pull request, and a GitHub ruleset that requires the gates. |
| Agents | `CLAUDE.md` and `.claude/rules/`, which give each standard with its reason. |
| Entry point | a `justfile`, which people, agents and CI all call. |

## Layers

The package follows ports and adapters. A layer imports only the layers below it.

| Layer | Job |
| --- | --- |
| `api` (service profile) | The Litestar app and its routes. |
| `cli` (cli profile) | The cyclopts commands. |
| `adapters` | Files, the network, the database, model files and the vendor SDKs. |
| `domain` | Pure logic, with attrs classes as the types. |
| `core` | Errors and types. |

Only `adapters` imports a vendor SDK. import-linter checks this rule with the list of the SDKs that the answers add.
