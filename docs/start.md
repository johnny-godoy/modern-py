# Start a project

## Before you start

Install these tools:

- [uv](https://docs.astral.sh/uv/), which also runs Copier with `uvx`.
- [just](https://just.systems/), the task runner of the project.
- git, with `user.name` and `user.email` set. The first commit needs them.

## Copy the template

Run this command, and answer the questions:

```bash
uvx copier copy --trust gh:johnny-godoy/modern-py my-project
```

The `--trust` flag lets Copier run the tasks of the template after the copy:

1. `git init`, if the directory is not a repository.
2. `uv lock` and `uv sync`, which write the lockfile and install the environment.
3. `prek install`, which installs the hooks that check each commit and its message.
4. `git add --all`, because prek checks only the files that git knows.

## The questions

| Question | Default | Effect |
| --- | --- | --- |
| `project_name` | | The name in the README, the docs and the citation file. |
| `package_name` | from `project_name` | The import name. It must match `^[a-z][a-z0-9_]*$`. |
| `distribution_name` | from `package_name` | The name on PyPI and of the command line. |
| `description` | | One sentence for the README, `pyproject.toml` and the docs. |
| `author_name`, `author_email` | | The author in `pyproject.toml`, the license and the code of conduct. |
| `github_owner`, `repo_name` | | The URLs of the repository and the docs. |
| `license` | `MIT` | `MIT`, `Apache-2.0` or `Proprietary`. A proprietary project gets no `LICENSE` file and the classifier `Private :: Do Not Upload`. |
| `copyright_year` | this year | The year in the license. |
| `python_version` | `3.14` | The minimum Python version. 3.14 is the newest version that every dependency supports. |
| `profiles` | none | The kinds of application to add to the library base. |
| `features` | `publish` for a library | The opt-in features. |
| `required_approvals` | `0` | The approving reviews that a pull request needs in the ruleset. |

## Profiles

A profile adds a kind of application. You can choose more than one.

| Profile | Adds |
| --- | --- |
| `service` | Litestar, msgspec, Granian, anyio, aiohttp and stamina. An `api` layer with a health route and its test, an HTTP adapter with retries, a `Dockerfile` that hadolint lints, a nightly trivy scan of the image, Dependabot updates of the base images, and `just serve`. Mutation testing covers `core` and `domain` only, because the I/O layers make it slow. |
| `data` | polars, duckdb, pyarrow, marimo and altair. A duckdb adapter, an example notebook that the docs build exports, and the ruff ignores for marimo cells. |
| `cli` | cyclopts, a `[project.scripts]` entry point and tests that call the command line. |

## Features

| Feature | Adds |
| --- | --- |
| `db` | Piccolo on PostgreSQL, an example table and migration, unit tests on SQLite, `just migrate`, `just test-db`, and a CI job on a PostgreSQL service container. |
| `ml` | onnx, onnxruntime, skl2onnx, skops and scikit-learn, and a `model_store` adapter: ONNX first, skops.io with an allow list of types when no converter exists. |
| `aws` | aioboto3, an S3 adapter, and tests against moto in server mode. |
| `text` | stringzilla and a rule on when to use it. |
| `proofs` | A Lean 4 project with an example proof, a Typst paper, `just proofs`, the proofs rule and its workflow. |
| `publish` | A job in the release workflow that uploads the package to PyPI with trusted publishing. |

## After the copy

1. Run `just` to list the recipes. Then run `just check` and `just test`. Both pass on a new project.
2. Make the first commit, for example `git commit -m "build: start the project from modern-py"`.
3. Create the repository on GitHub and push.
4. Apply the ruleset, as `.github/rulesets/README.md` says.
5. Set the secrets that the workflows read. The release workflow needs `RELEASE_TOKEN` when the ruleset is active.
6. If the project has the `publish` feature, do the PyPI steps in the README.

The example code (`summary`, `summary_file` and the profile modules) shows each layer and each guard. Replace it with
the code of the project. Keep each module with its test, because the layout check and the coverage gate need both.
