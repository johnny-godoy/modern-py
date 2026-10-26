"""Write the tables that template/scripts/banned.toml generates into the template files and the docs.

A rendered project checks its tables with `scripts.sync_banned --check`, so the template must ship them up to date.
The script renders the library answer set, runs `scripts.sync_banned` there, and copies each generated table back
into the matching `.jinja` file and into `docs/libraries.md`. Run it after each change of
`template/scripts/banned.toml`: `just sync-tables`. With `--check`, it changes nothing and fails on a stale table.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = (
    ("pyproject.toml", "template/pyproject.toml.jinja", "RUFF_BEGIN", "RUFF_END"),
    (".claude/rules/libraries.md", "template/.claude/rules/libraries.md.jinja", "RULE_BEGIN", "RULE_END"),
    (".claude/rules/libraries.md", "docs/libraries.md", "RULE_BEGIN", "RULE_END"),
)


def main() -> int:
    check = "--check" in sys.argv[1:]
    stale = []
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
            text = path.read_text(encoding="utf-8")
            new = sync_banned.replace_between(text, begin, end, body)
            if new != text:
                stale.append(template)
                if not check:
                    path.write_text(new, "utf-8")
    if check and stale:
        sys.stderr.write(f"out of date: {', '.join(stale)}. Run `just sync-tables`.\n")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
