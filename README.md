# modern-py

modern-py is a [Copier](https://copier.readthedocs.io/) template for Python projects. It gives each project the same
engineering standard, and tools enforce the standard instead of trust. When the template changes, each project pulls
the change with `copier update`.

## Start a project

Install [uv](https://docs.astral.sh/uv/) and [just](https://just.systems/). Then run:

```bash
uvx copier copy --trust gh:johnny-godoy/modern-py my-project
```

The `--trust` flag lets Copier run the tasks after the copy: `git init`, `uv lock`, `uv sync` and `prek install`.

## Update a project

```bash
uvx copier update --trust
```

## Profiles and features

Each project is a library. A profile adds a kind of application, and you can choose more than one.

| Profile | Adds |
| --- | --- |
| `service` | Litestar, msgspec, Granian, anyio, aiohttp, stamina, an `api` layer with a health endpoint, a `Dockerfile`. |
| `data` | polars, duckdb, marimo, altair, and an example notebook that the docs build exports. |
| `cli` | cyclopts and a `[project.scripts]` entry point. |

| Feature | Adds |
| --- | --- |
| `db` | Piccolo on PostgreSQL, an example table, unit tests on SQLite and a CI job on PostgreSQL. |
| `ml` | A `model_store` adapter that saves models in ONNX, with skops.io as the fallback. |
| `aws` | aioboto3, with moto in server mode in the tests. |
| `text` | stringzilla. |
| `proofs` | Lean proofs and Typst papers. |
| `publish` | PyPI trusted publishing in the release workflow. |

The [documentation](docs/index.md) has the full list of tools and library choices.
