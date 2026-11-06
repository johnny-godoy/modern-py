# Library choices

The template uses one library for each need, chosen for this stack, not for its popularity. Each rendered project
gets a rule file, `.claude/rules/libraries.md`. It points a coding agent at the ruff `banned-api` table in
`pyproject.toml`, which is the single source of the banned imports, so the rule holds no copy of the list. The guards
are:

- An import ban is a ruff `banned-api` entry (TID251). It fails in the editor, with the replacement in the message.
- A file ban is `BANNED_FILES` in `scripts/check_layout.py`.
- A semgrep rule guards a choice that is not an import, for example `datetime.now()` or `while True` with a sleep.
- "Rule only" means that no tool checks the choice. The rule file lists these choices.

To change a choice, edit the table of `template/pyproject.toml.jinja` or `template/scripts/check_layout.py`, the rule
file `template/.claude/rules/libraries.md.jinja`, and the table below.

| Need | Use | Not | Reason | Guard |
| --- | --- | --- | --- | --- |
| Packaging, environments | uv | pip, poetry, pipenv | One fast tool, a lockfile and the 7-day cooldown. | File ban: `requirements*.txt`, `setup.py`, `setup.cfg`, `poetry.lock`, `Pipfile`, `Pipfile.lock` |
| Git hooks | prek | pre-commit | Faster, a TOML config and hook priorities. | File ban: `.pre-commit-config.yaml` |
| Lint and format | ruff (select ALL) | black, isort, flake8, pylint | One tool and one config. | Rule only |
| Static types | pyrefly (strict) | mypy | Speed and a check of the type coverage. | Rule only |
| Run-time types | beartype | typeguard | Near-zero overhead and a hook that covers the whole package. | Import ban: `typeguard` |
| Logging | structlog | logging, loguru, `print` | Structured events that tests read with `capture_logs`. | Import ban: `logging`, `loguru`; ruff `print` rule (T201) |
| JSON | orjson | json, ujson, simplejson | Speed and correct types. | Import ban: `json`, `ujson`, `simplejson` |
| Domain data classes | attrs | dataclasses | Validators, slots and frozen classes. | Import ban: `dataclasses` |
| Wire schemas (API bodies, config files, messages) | msgspec | pydantic | Litestar supports it natively, it is much faster, and it keeps validation at the edge. attrs stays the domain type. | Import ban: `pydantic`, `pydantic_settings` |
| Serialization of objects | msgspec, orjson | pickle, shelve, dill | pickle runs code when it loads a file. | Import ban: `pickle`, `shelve`, `dill`, `cloudpickle`, `joblib`; File ban: `*.pkl`, `*.pickle`, `*.joblib` |
| Saved ML models | ONNX (skl2onnx, onnxmltools, `torch.onnx`), and skops.io when no ONNX converter exists for the model | pickle, joblib, cloudpickle, dill | ONNX is portable, runs in onnxruntime without the training stack and holds no code. skops.io loads only the types that you trust. | The pickle bans above; semgrep rule `skops-load-trusted-true` |
| Database ORM | Piccolo | SQLAlchemy, SQLModel, Django ORM, Tortoise | Async-native, a typed query builder, migrations and an admin in one package, and it works with Litestar. Convert rows to msgspec Structs in the adapter, because the pydantic ban also covers `create_pydantic_model`. | Import ban: `sqlalchemy`, `sqlmodel`, `tortoise`, `peewee` |
| Date and time | whenever | datetime arithmetic, arrow, pendulum, pytz | Distinct types for instants and local times, so a naive datetime cannot happen. | Import ban: `arrow`, `pendulum`, `pytz`; semgrep rule `no-naive-now` (`datetime.now()`, `datetime.utcnow()` in `src/`) |
| Web framework | Litestar | FastAPI, Django, Flask | Faster, msgspec-native, a real dependency injection system and an active team. | Import ban: `fastapi`, `django`, `flask`, `starlette` |
| ASGI server | Granian | uvicorn, daphne, hypercorn | Rust I/O, and one binary for HTTP/1, HTTP/2 and WebSockets. | Rule only |
| HTTP client | aiohttp | requests, httpx, urllib3 | A mature, fast asyncio client with connection pooling. httpx stays allowed as a dependency of the Litestar test client. | Import ban: `requests`, `httpx`, `urllib3` |
| HTTP servers in tests | the aiohttp test server (`aiohttp.test_utils.TestServer`) | responses, respx, aioresponses | It serves real HTTP on localhost, so a test runs the real client code. aioresponses 0.7.9 fails with aiohttp 3.14. | Rule only |
| AWS | aioboto3 | boto3 | It does not block the event loop. botocore stays allowed as a dependency of aioboto3. | Import ban: `boto3` |
| AWS mocks in tests | moto in server mode | hand-written fakes | It speaks the real AWS protocol to aioboto3. | Rule only |
| Retries | stamina | tenacity, backoff, hand-written loops | Safe defaults, jitter, a test mode and structlog integration. | Import ban: `tenacity`, `backoff`; semgrep rule `no-sleep-loop` (`while True` with `sleep` in `src/`) |
| Concurrency | anyio task groups | bare `asyncio.gather`, `create_task` | Structured concurrency and cancel scopes. Litestar runs on anyio. | semgrep rule `structured-concurrency` (`asyncio.gather`, `asyncio.create_task` in `src/`) |
| Async tests | the anyio pytest plugin | pytest-asyncio | One event-loop model across the code and the tests. | Rule only |
| CLI | cyclopts | click, typer, argparse | Type hints are the interface, with good help text and no decorator for each option. | Import ban: `click`, `typer`, `argparse` |
| Data frames | polars | pandas | Speed, a lazy API, strict types and no index surprises. If a third-party library needs pandas, convert in one module, `adapters/pandas_interop.py`, with an inline `# ruff: ignore[banned-api]` and its reason. | Import ban: `pandas` |
| Code that accepts a frame of any library (pandas, polars, pyarrow) | narwhals | `isinstance` branches on `pd.DataFrame` and `pl.DataFrame` | One API over every frame library, so the caller keeps its own library and the code imports none of them. Use polars where the frame is yours. | semgrep rule `no-frame-type-branches` (`isinstance` of a pandas or polars frame in `src/`) |
| SQL over files | duckdb | pandas SQL, sqlite for analytics | It queries Parquet files and polars frames in place. | Rule only |
| File format for tables | Parquet | CSV | Types and compression. | Rule only |
| Charts in notebooks | altair | matplotlib, seaborn | Declarative, and interactive inside marimo (`mo.ui.altair_chart`). | Rule only |
| Notebooks | marimo | Jupyter | Plain `.py` files, reactive, with diffs that a reviewer can read and that ruff can lint. | File ban: `*.ipynb` |
| String-heavy work | stringzilla | `str`, `re` loops | SIMD search, split and hashing on large text. | Rule only, and only when the project processes large text |
| Docs | Zensical with mkdocstrings | Sphinx, MkDocs | Fast builds, a TOML config and a modern theme. | File ban: `mkdocs.yml`, `docs/conf.py` |
| Task runner | just | make, invoke, tox, nox | Plain recipes with arguments, and no tab or `.PHONY` traps. | File ban: `Makefile`, `tox.ini`, `noxfile.py`, `tasks.py` |
| Changelog | scriv fragments | a hand-edited `CHANGELOG.md`, towncrier | No merge conflicts, and the release workflow collects the fragments. | The check-changelog hook and the fragment workflow |
| Project template | Copier | cookiecutter | `copier update` brings the template changes into each project. | Rule only |
| Mutation testing | cosmic-ray | mutmut | Parallel shards over a session database, and a filter for equivalent mutants. | Rule only |

## Notes

- aioresponses 0.7.9 fails with aiohttp 3.14, so the tests of the HTTP adapter use the aiohttp test server.
- The beartype hook skips the `api` package of a service, because a Litestar route decorator returns a handler
  object. Litestar checks each request and response against its msgspec schema.
- duckdb needs pyarrow to return a polars frame, so the data profile adds pyarrow.
