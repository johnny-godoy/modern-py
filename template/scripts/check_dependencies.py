"""Fail when ``pyproject.toml`` declares a dependency that ``scripts/banned.toml`` bans.

The check reads the direct dependencies: ``[project].dependencies``, ``[project.optional-dependencies]`` and each group
of ``[dependency-groups]``. A dependency of a dependency is not a failure, because the rule is about what the project
chooses, not about what its dependencies pull in. Each message names the replacement.

Run it from the repo root: ``uv run python -m scripts.check_dependencies``.
"""

import re
import sys
import tomllib
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any

from scripts.sync_banned import BANNED, ROOT, Ban, load_bans

# the distribution name at the start of a requirement, before the extras, the version and the markers (PEP 508)
NAME: re.Pattern[str] = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)")


def normalize(name: str) -> str:
    """Normalize a distribution name, as PEP 503 says.

    Parameters
    ----------
    name: str
        The distribution name.

    Returns
    -------
    str
        The name in lower case, with each run of ``-``, ``_`` and ``.`` replaced by one ``-``.

    """
    return re.sub(r"[-_.]+", "-", name).lower()


def requirement_names(pyproject: Mapping[str, Any]) -> list[str]:
    """List the names of the direct dependencies of a project.

    Parameters
    ----------
    pyproject: Mapping[str, Any]
        The parsed ``pyproject.toml``.

    Returns
    -------
    list[str]
        The normalized name of each requirement, in the order of the file. An ``include-group`` entry has no name.

    """
    project = pyproject.get("project", {})
    requirements: list[str] = list(project.get("dependencies", []))
    for extra in project.get("optional-dependencies", {}).values():
        requirements.extend(extra)
    for group in pyproject.get("dependency-groups", {}).values():
        requirements.extend(entry for entry in group if isinstance(entry, str))
    return [normalize(match[1]) for requirement in requirements if (match := NAME.match(requirement))]


def dependency_problems(names: Iterable[str], bans: Iterable[Ban]) -> list[str]:
    """List the banned dependencies.

    Parameters
    ----------
    names: Iterable[str]
        The normalized names of the direct dependencies.
    bans: Iterable[Ban]
        The library choices.

    Returns
    -------
    list[str]
        One message for each banned dependency, with its replacement.

    """
    replacement = {normalize(name): ban.use for ban in bans for name in ban.dependencies}
    return [
        f"{name}: a banned dependency. Use {replacement[name]} instead (.claude/rules/libraries.md)."
        for name in names
        if name in replacement
    ]


def main(argv: Sequence[str] = ()) -> int:
    """Report every banned dependency.

    Parameters
    ----------
    argv: Sequence[str]
        The root of the project. The default is the root of this repository.

    Returns
    -------
    int
        The process exit code: 0 if no dependency is banned, 1 otherwise.

    """
    root = Path(argv[0]) if argv else ROOT
    pyproject = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    problems = dependency_problems(requirement_names(pyproject), load_bans(BANNED.read_text(encoding="utf-8")))
    for problem in problems:
        sys.stderr.write(f"{problem}\n")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
