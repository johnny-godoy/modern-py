"""Write the tables that template/scripts/banned.toml generates into the template files.

A rendered project checks its tables with `scripts.sync_banned --check`, so the template must ship them up to date.
The script renders the library answer set, runs `scripts.sync_banned` there, and copies each generated table back
into the matching `.jinja` file. Run it after each change of `template/scripts/banned.toml`: `just sync-tables`.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = (
    ("pyproject.toml", "template/pyproject.toml.jinja", "RUFF_BEGIN", "RUFF_END"),
    (".claude/rules/libraries.md", "template/.claude/rules/libraries.md.jinja", "RULE_BEGIN", "RULE_END"),
)


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp) / "library"
        subprocess.run([ROOT / "scripts" / "render.sh", "library", project, "--no-checks"], check=True)
        subprocess.run(["uv", "run", "--frozen", "python", "-m", "scripts.sync_banned"], cwd=project, check=True)
        sys.path.insert(0, str(project))
        from scripts import sync_banned  # the module of the rendered project

        for rendered, template, begin_name, end_name in TARGETS:
            begin, end = getattr(sync_banned, begin_name), getattr(sync_banned, end_name)
            body = (project / rendered).read_text(encoding="utf-8").split(begin, 1)[1].split(end, 1)[0]
            path = ROOT / template
            path.write_text(sync_banned.replace_between(path.read_text(encoding="utf-8"), begin, end, body), "utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
