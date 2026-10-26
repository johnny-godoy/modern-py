# Inventory of EBaMl

This inventory lists the files of `johnny-godoy/EBaMl` at commit `99f0954` and says what the template does with each
one. "Kept" means that the file goes into the template with only the names templated. "Generalized" means that the
template keeps the purpose of the file and changes its content. "Dropped" means that the file is domain code.

`<pkg>` is the package name from the Copier answers. `<PKG>` is the same name in upper case.

## Agent rules and settings

| File | Decision | Reason |
| --- | --- | --- |
| `CLAUDE.md` | Generalized | The structure (project, commands, architecture, layout, conventions) is process. The commands call `just` recipes. The project and architecture sections come from the profile. |
| `.claude/settings.json` | Generalized | The PostToolUse prek hook and the SessionStart `prek install` hook are process. The `~/.baml/bin` part of `PATH` is removed. |
| `.claude/rules/architecture.md` | Generalized | The layer table comes from the profile: `core`, `domain`, `adapters` and, for `service`, `api`. The rule "only the adapter layer imports vendor SDKs" stays. |
| `.claude/rules/bug-fixes.md` | Generalized | Process. The row for BAML prompt tests is removed. |
| `.claude/rules/changelog-and-versioning.md` | Generalized | Process. The public API paragraph lists Python names, CLI flags (`cli`) and HTTP routes (`service`) instead of BAML entry points and MCP tools. |
| `.claude/rules/commits-and-prs.md` | Generalized | Process. The scope list comes from the layers. |
| `.claude/rules/libraries.md` | Generalized | The table grows to the full library list of the task. It is generated from `scripts/banned.toml`. |
| `.claude/rules/prek-and-ignores.md` | Kept | Process with no domain name. |
| `.claude/rules/proofs.md` | Generalized, opt-in | Only with the `proofs` feature. The topic `LocalExplanations` becomes an example topic. |
| `.claude/rules/solid.md` | Generalized | Process. The examples (`_DESCRIPTIONS`, `descriptors.py`, `if expert:`) become generic. |
| `.claude/rules/types.md` | Generalized | Process. `ExplainableBoostingClassifier` as the example of a third-party class becomes a generic example. The semgrep rule id takes the project prefix. |
| `.claude/rules/writing-style.md` | Generalized | Process. The prompt section keeps the scope `CLAUDE.md` and `docs/plans/`, without `baml_src/`. |
| `.claude/skills/baml-core/`, `.agents/skills/baml-core/` | Dropped | A BAML skill. |
| `.claudeignore` | Generalized | The BAML lines are removed. |

## Project configuration

| File | Decision | Reason |
| --- | --- | --- |
| `pyproject.toml` | Generalized | Ruff (ALL), pyrefly strict with its error table, pytest, coverage 100%, vulture, import-linter, scriv, commitizen and the uv cooldown are process. The domain dependencies (`baml-bridge`, `interpret`, `pandas-stubs`, `scipy-stubs`, `pyarrow`) and `module-name = ["ebaml", "baml_sdk"]` are removed. The ruff `banned-api` table is generated from `scripts/banned.toml`. The marimo per-file ignores move to the `data` profile. |
| `prek.toml` | Generalized | Process. The `baml-fmt` hook and `src/baml_sdk/` exclude are removed. `check-dependencies` and `check-banned` (generated tables up to date) are added. The `semgrep` hook scans the folders that exist in the profile. |
| `cosmic-ray.toml` | Kept | `module-path` is templated. |
| `zensical.toml` | Generalized | The theme, the strict mode and mkdocstrings are process. The nav comes from the profile. |
| `.python-version` | Generalized | From the Copier answer. |
| `.gitignore` | Generalized | The BAML lines are removed. The Lean lines come only with `proofs`. |
| `.semgrepignore` | Generalized | `src/baml_sdk/` is removed. |
| `uv.lock` | Generalized | Not in the template. The Copier task `uv sync` writes it after a copy. See open question 1. |
| `baml.toml` | Dropped | BAML. |

## Scripts

| File | Decision | Reason |
| --- | --- | --- |
| `scripts/ignore_sites.py`, `check_ignores.py`, `compile_ignores.py` | Generalized | Process. Only `EXCLUDED_PREFIXES` loses `src/baml_sdk/`. EBaMl freezes these files, and the template freezes them in the same way. |
| `scripts/check_layout.py` | Generalized | Process. The package name is templated. `TOP_LEVEL_MODULES` holds `__init__.py` only (`benchmark.py` is domain). The file bans of the task are added. |
| `scripts/check_changelog.py`, `release.py` | Kept | Process with no domain name. |
| `scripts/check_fragment.py` | Generalized | `USER_VISIBLE` becomes `src/<pkg>/`. The BAML test files leave `NOT_USER_VISIBLE`. |
| `scripts/check_commits.py` | Generalized | `GENERATED` keeps `uv.lock`, `CHANGELOG.md` and `changelog.d/`. `notebooks/__marimo__/` comes with `data`. |
| `scripts/check_ruleset.py`, `check_exclusions.py` | Kept | Process. |
| `scripts/mutation.py` | Generalized | Process. The `EBAML_FIT_CACHE` directory is a cache of fitted EBMs, which is domain, so it is removed. `COPIED` loses `benchmark`. |
| `scripts/build_docs.py` | Generalized | The strict build and the griffe-warning check are process. The notebook export comes with `data`, the paper compilation with `proofs`. |
| `scripts/README.md` | Generalized | Describes the scripts that the project has. |
| `scripts/live_openrouter.py` | Dropped | A live LLM test. |
| `scripts/check_dependencies.py`, `scripts/banned.toml`, `scripts/sync_banned.py` | New | The dependency ban, the banned-library data file, and the generator of the ruff table and the `libraries.md` table. |

## Semgrep

| Rule of `semgrep/ebaml.yml` | Decision | Reason |
| --- | --- | --- |
| `ebaml-no-kwargs-bag` | Generalized | Rule id `<pkg>-no-kwargs-bag`. |
| `ebaml-no-elif-chain-on-one-value` | Generalized | Rule id with the project prefix. |
| `ebaml-no-not-implemented-stub` | Generalized | Rule id with the project prefix. |
| `ebaml-domain-does-no-io` | Generalized | Paths become `core/` and `domain/`. |
| `ebaml-preferred-libraries` | Generalized | The imports move to ruff TID251, generated from `scripts/banned.toml`. The rule is removed, because ruff runs in the editor and the data file is the single source. |
| `ebaml-no-manual-beartype` | Generalized | Rule id with the project prefix. |
| `ebaml-no-bare-value-error` | Generalized | The base error class is `<Pkg>Error` in `<pkg>.core.exceptions`. |
| `ebaml-return-attrs-not-container` | Generalized | Rule id with the project prefix. |
| `ebaml-sdk-fake-is-checked` | Dropped | BAML SDK fakes. |
| New rules | New | `datetime.now()`, `datetime.utcnow()`, `while True` with `sleep`, `asyncio.gather`, `asyncio.create_task`, `skops.io.load(..., trusted=True)`. |

`semgrep/ebaml.py` becomes `semgrep/<pkg>.py` with one `ruleid` and one `ok` case for each rule.

## GitHub

| File | Decision | Reason |
| --- | --- | --- |
| `.github/actions/setup/action.yml` | Generalized | The BAML install and `baml generate` steps are removed. The `generate` input goes. |
| `.github/actions/failure-report/action.yml` | Kept | Process. |
| `.github/scripts/ci_report.py` | Generalized | The `baml` gate and its builder are removed. A `db` gate comes with `db`. |
| `.github/workflows/ci.yml` | Generalized | The `baml` job and the `baml` path filter are removed. `OPENROUTER_API_KEY` is removed. A `db` job comes with `db`. |
| `.github/workflows/release.yml` | Generalized | The "wheel contains baml_sdk" step is removed. The `publish` job comes with `publish`. |
| `.github/workflows/docs.yml` | Generalized | The Titanic cache and the export checks of the domain notebooks are removed. |
| `.github/workflows/changelog.yml`, `commits.yml` | Kept | Process. |
| `.github/workflows/mutation-weekly.yml` | Generalized | `baml_src` and `OPENROUTER_API_KEY` are removed. |
| `.github/workflows/proofs.yml` | Generalized, opt-in | Only with `proofs`. |
| `.github/workflows/prompt-tests.yml` | Dropped | Live BAML prompt tests. |
| `.github/rulesets/main.json`, `README.md` | Generalized | The `baml check + test` check is removed. A `db` check comes with `db`. |
| `.github/dependabot.yml` | Kept | Process. |
| `.github/pull_request_template.md` | Generalized | The BAML and benchmark checks are removed. The checks call `just` recipes. |

## Documents

| File | Decision | Reason |
| --- | --- | --- |
| `README.md` | Generalized | A short project README with the `--8<--` markers that `docs/index.md` uses. |
| `CONTRIBUTING.md` | Generalized | Process. The BAML steps and `fake_sdk` are removed. The steps call `just` recipes. |
| `SECURITY.md` | Generalized | The reporting section is process. The section about data sent to the LLM provider is domain. |
| `CODE_OF_CONDUCT.md` | Kept | Process. |
| `LICENSE` | Generalized | From the Copier answer. |
| `CHANGELOG.md` | Generalized | The header and the scriv marker only, with no entries. |
| `changelog.d/README.md` | Kept | Process. |
| `ROADMAP.md` | Generalized | A table with one first milestone, because `release.py` and the changelog rule read it. |
| `docs/plans/` | Generalized | An empty folder with a README that says what a plan is. The plans of EBaMl are domain. |
| `docs/index.md`, `docs/api.md`, `docs/changelog.md` | Generalized | A home page, an API page from mkdocstrings and the changelog page. |
| `docs/setup.md`, `usage.md`, `providers.md`, `local-explanations*.md`, `benchmark.md`, `notebook.md`, `local-notebook.md` | Dropped | Domain documentation. |
| `NOTICE`, `CITATION.cff` | Dropped | They describe EBaMl and TalkToEBM. See open question 2. |

## Source, tests and other folders

| Path | Decision | Reason |
| --- | --- | --- |
| `src/ebaml/__init__.py` | Generalized | The `beartype_this_package` call and its comments are process. The exports are the error classes. |
| `src/ebaml/core/exceptions.py` | Generalized | `<Pkg>Error` and one `InvalidOptionError(<Pkg>Error, ValueError)` as the example. |
| `src/ebaml/core/custom_types.py`, `graphs/`, `local/`, `llm/`, `benchmark.py` | Dropped | Domain code. |
| `src/ebaml/py.typed` | Kept | Process. |
| `tests/unit/conftest.py` | Kept | The Hypothesis `ci` profile and the `MUTATION_FIRST` order are process. |
| `tests/unit/scripts/` | Generalized | The test of every kept script. |
| `tests/unit/ebaml/` | Generalized | Tests of the example modules only. `conftest.py` with `fake_sdk` and the EBM fits is dropped. |
| `baml_src/`, `benchmark/` | Dropped | Domain. |
| `notebooks/` | Generalized | One example marimo notebook with `data`. |
| `proofs/` | Generalized, opt-in | With `proofs`: the Lake project, the shared Typst style and one small example topic. The `LocalExplanations` topic is domain. |

## Open questions

These are the points where I cannot tell process from domain. Each one has my proposed answer.

1. **`uv.lock` in the template.** A committed lock in the template goes stale, and its hash fails `uv lock --check`
   after a change of the answers. Proposal: do not ship it. The Copier task `uv sync` writes it, and the project
   commits it. The CI of the template checks that a fresh lock passes every gate.
2. **`NOTICE` and `CITATION.cff`.** `NOTICE` is about TalkToEBM. A citation file is useful for a research library and
   noise for a service. Proposal: drop `NOTICE`, and ship `CITATION.cff` only for the `library` profile with the
   author from the answers.
3. **The `ci_report.py` PR comment and the `progress` job.** They are process, but 700 lines of code that every project
   must keep at 100% coverage. Proposal: keep them, because they make CI failures readable for an agent.
4. **`ROADMAP.md` and milestone versions.** `release.py` takes a version from `pyproject.toml` when a milestone PR sets
   it. A project with no roadmap can still use this. Proposal: keep `ROADMAP.md` with one row.
5. **The ruleset bypass actor and `required_approving_review_count: 0`.** EBaMl has one maintainer. Proposal: keep
   both as defaults, and make the review count a Copier question.
6. **`semgrep p/default` in CI and trufflehog and trivy.** They are process. Proposal: keep them as they are.
