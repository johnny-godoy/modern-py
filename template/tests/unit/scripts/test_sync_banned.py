"""Tests for the ruff table that scripts/banned.toml generates."""

from pathlib import Path

import pytest
from scripts import sync_banned
from scripts.sync_banned import Ban

TOML = """
[[ban]]
need = "JSON"
use = "orjson"
instead_of = "json"
reason = "Speed."
imports = ["json", "ujson"]
dependencies = ["ujson"]

[[ban]]
need = "Notebooks"
use = "marimo"
instead_of = "Jupyter"
reason = "Plain files."
files = ["*.ipynb"]
guard = "A note"
"""
JSON: Ban = Ban(
    use="orjson",
    imports=("json", "ujson"),
    dependencies=("ujson",),
)
NOTEBOOKS: Ban = Ban(
    use="marimo",
    files=("*.ipynb",),
)


def test_load_bans_reads_every_entry_with_defaults() -> None:
    assert sync_banned.load_bans(TOML) == [JSON, NOTEBOOKS]


def test_ruff_table_bans_each_module_with_the_replacement() -> None:
    assert sync_banned.ruff_table([NOTEBOOKS, JSON]) == (
        "[tool.ruff.lint.flake8-tidy-imports.banned-api]\n"
        '"json".msg = "Use orjson. See .claude/rules/libraries.md."\n'
        '"ujson".msg = "Use orjson. See .claude/rules/libraries.md."\n'
    )


def test_replace_between_keeps_the_markers_and_the_rest() -> None:
    text = "head\nBEGIN\nold\nEND\ntail\n"
    assert sync_banned.replace_between(text, "BEGIN\n", "END\n", "new\n") == "head\nBEGIN\nnew\nEND\ntail\n"


@pytest.mark.parametrize("text", ["BEGIN\nold\n", "old\nEND\n"])
def test_replace_between_fails_without_a_marker(text: str) -> None:
    with pytest.raises(sync_banned.MarkerError, match="BEGIN"):
        sync_banned.replace_between(text, "BEGIN\n", "END\n", "new\n")


@pytest.fixture
def project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point the script at a project with a stale table in a temporary directory.

    Returns
    -------
    Path
        The root of the project.

    """
    (tmp_path / "banned.toml").write_text(TOML, encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text(
        f"top\n{sync_banned.RUFF_BEGIN}stale\n{sync_banned.RUFF_END}",
        encoding="utf-8",
    )
    monkeypatch.setattr(sync_banned, "ROOT", tmp_path)
    monkeypatch.setattr(sync_banned, "BANNED", tmp_path / "banned.toml")
    monkeypatch.setattr(sync_banned, "PYPROJECT", tmp_path / "pyproject.toml")
    return tmp_path


def test_check_fails_on_a_stale_table_and_changes_nothing(project: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert sync_banned.main(["--check"]) == 1
    assert "pyproject.toml" in capsys.readouterr().err
    assert "stale" in (project / "pyproject.toml").read_text(encoding="utf-8")


def test_main_writes_the_table_and_then_the_check_passes(project: Path) -> None:
    assert sync_banned.main() == 0
    assert '"json".msg' in (project / "pyproject.toml").read_text(encoding="utf-8")
    assert sync_banned.main(["--check"]) == 0


def test_the_table_of_this_repository_is_up_to_date() -> None:
    assert sync_banned.main(["--check"]) == 0
