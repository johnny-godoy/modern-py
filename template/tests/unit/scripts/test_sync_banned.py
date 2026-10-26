"""Tests for the tables that scripts/banned.toml generates."""

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
    need="JSON",
    use="orjson",
    instead_of="json",
    reason="Speed.",
    imports=("json", "ujson"),
    dependencies=("ujson",),
)
NOTEBOOKS: Ban = Ban(
    need="Notebooks",
    use="marimo",
    instead_of="Jupyter",
    reason="Plain files.",
    files=("*.ipynb",),
    guard="A note",
)


def test_load_bans_reads_every_entry_with_defaults() -> None:
    assert sync_banned.load_bans(TOML) == [JSON, NOTEBOOKS]


def test_guards_name_every_kind_of_guard() -> None:
    assert sync_banned.guards(JSON) == "Import ban: `json`, `ujson`; Dependency ban: `ujson`"
    assert sync_banned.guards(NOTEBOOKS) == "File ban: `*.ipynb`; A note"


def test_ruff_table_bans_each_module_with_the_replacement() -> None:
    assert sync_banned.ruff_table([NOTEBOOKS, JSON]) == (
        "[tool.ruff.lint.flake8-tidy-imports.banned-api]\n"
        '"json".msg = "Use orjson. See .claude/rules/libraries.md."\n'
        '"ujson".msg = "Use orjson. See .claude/rules/libraries.md."\n'
    )


def test_rule_table_has_one_row_for_each_choice() -> None:
    assert sync_banned.rule_table([JSON, NOTEBOOKS]).splitlines() == [
        "| Need | Use | Not | Reason | Guard |",
        "| --- | --- | --- | --- | --- |",
        "| JSON | orjson | json | Speed. | Import ban: `json`, `ujson`; Dependency ban: `ujson` |",
        "| Notebooks | marimo | Jupyter | Plain files. | File ban: `*.ipynb`; A note |",
    ]


def test_replace_between_keeps_the_markers_and_the_rest() -> None:
    text = "head\nBEGIN\nold\nEND\ntail\n"
    assert sync_banned.replace_between(text, "BEGIN\n", "END\n", "new\n") == "head\nBEGIN\nnew\nEND\ntail\n"


@pytest.mark.parametrize("text", ["BEGIN\nold\n", "old\nEND\n"])
def test_replace_between_fails_without_a_marker(text: str) -> None:
    with pytest.raises(sync_banned.MarkerError, match="BEGIN"):
        sync_banned.replace_between(text, "BEGIN\n", "END\n", "new\n")


@pytest.fixture
def project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point the script at a project with stale tables in a temporary directory.

    Returns
    -------
    Path
        The root of the project.

    """
    (tmp_path / "banned.toml").write_text(TOML, encoding="utf-8")
    for name, begin, end in (
        ("pyproject.toml", sync_banned.RUFF_BEGIN, sync_banned.RUFF_END),
        ("libraries.md", sync_banned.RULE_BEGIN, sync_banned.RULE_END),
    ):
        (tmp_path / name).write_text(f"top\n{begin}stale\n{end}", encoding="utf-8")
    monkeypatch.setattr(sync_banned, "ROOT", tmp_path)
    monkeypatch.setattr(sync_banned, "BANNED", tmp_path / "banned.toml")
    monkeypatch.setattr(sync_banned, "PYPROJECT", tmp_path / "pyproject.toml")
    monkeypatch.setattr(sync_banned, "RULE", tmp_path / "libraries.md")
    return tmp_path


def test_check_fails_on_a_stale_table_and_changes_nothing(project: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert sync_banned.main(["--check"]) == 1
    assert "pyproject.toml, libraries.md" in capsys.readouterr().err
    assert "stale" in (project / "pyproject.toml").read_text(encoding="utf-8")


def test_main_writes_the_tables_and_then_the_check_passes(project: Path) -> None:
    assert sync_banned.main() == 0
    assert '"json".msg' in (project / "pyproject.toml").read_text(encoding="utf-8")
    assert "| JSON | orjson |" in (project / "libraries.md").read_text(encoding="utf-8")
    assert sync_banned.main(["--check"]) == 0


def test_the_tables_of_this_repository_are_up_to_date() -> None:
    assert sync_banned.main(["--check"]) == 0
