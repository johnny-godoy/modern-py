"""Tests for the check of the banned dependencies."""

from pathlib import Path

import pytest
from scripts import check_dependencies
from scripts.sync_banned import Ban

BANS = [Ban(need="Lint", use="ruff", instead_of="black", reason="One tool.", dependencies=("black", "Pre_Commit"))]


@pytest.mark.parametrize(("name", "normal"), [("Pre_Commit", "pre-commit"), ("zope.interface", "zope-interface")])
def test_normalize_follows_pep_503(name: str, normal: str) -> None:
    assert check_dependencies.normalize(name) == normal


def test_requirement_names_read_every_kind_of_dependency() -> None:
    pyproject = {
        "project": {"dependencies": ["attrs>=26"], "optional-dependencies": {"x": ["Black[d] ; python_version>'3'"]}},
        "dependency-groups": {"dev": ["pytest", {"include-group": "docs"}], "docs": ["zensical"]},
    }
    assert check_dependencies.requirement_names(pyproject) == ["attrs", "black", "pytest", "zensical"]


def test_requirement_names_of_an_empty_project() -> None:
    assert check_dependencies.requirement_names({}) == []


def test_a_banned_dependency_fails_with_its_replacement() -> None:
    [problem] = check_dependencies.dependency_problems(["attrs", "pre-commit"], BANS)
    assert problem == "pre-commit: a banned dependency. Use ruff instead (.claude/rules/libraries.md)."


def test_allowed_dependencies_pass() -> None:
    assert check_dependencies.dependency_problems(["attrs", "ruff"], BANS) == []


@pytest.mark.parametrize(("dependency", "code"), [("attrs", 0), ("black", 1)])
def test_main(tmp_path: Path, dependency: str, code: int, capsys: pytest.CaptureFixture[str]) -> None:
    (tmp_path / "pyproject.toml").write_text(f'[project]\ndependencies = ["{dependency}"]\n', encoding="utf-8")
    assert check_dependencies.main([str(tmp_path)]) == code
    assert bool(capsys.readouterr().err) == bool(code)


def test_main_checks_this_repository() -> None:
    assert check_dependencies.main() == 0
