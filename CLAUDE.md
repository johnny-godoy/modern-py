# CLAUDE.md

<project>
modern-py is a Copier template. It starts Python projects with one engineering standard: uv, prek, ruff with every
rule, pyrefly strict, beartype, import-linter layers, semgrep design rules, 100% branch coverage, cosmic-ray mutation
testing, conventional commits, scriv changelog fragments and a release workflow. Projects pull template changes with
`copier update`, so a standard stays the same in every project.
</project>

<layout>
- `copier.yml` holds the questions, the tasks that run after a copy, and the Jinja settings.
- `template/` is the project that Copier renders. A file with the suffix `.jinja` is rendered; every other file is
  copied as it is. A path part that renders to an empty string is skipped, which is how a profile adds files.
- `tests/answers/` holds one answer file per CI matrix entry. `tests/forbidden-names.txt` lists the names that no
  rendered project may contain.
- `scripts/render.sh` renders an answer file into a directory and runs the checks of the rendered project.
- `docs/` is the documentation of the template.
</layout>

<commands>
```bash
just render library /tmp/out        # render tests/answers/library.yml into /tmp/out and run just check, test, docs
just render-all                      # every answer file, as the CI matrix does
just update-check                    # copier update from the previous tag on a rendered project
just sync-tables                     # write the tables of template/scripts/banned.toml into the template and docs/
just check-tables                    # fail when one of those tables is out of date
```

`scripts/render.sh <name> <dir> --no-checks` renders without the checks, which is fast for a look at the output. Each
check of a rendered project takes one to two minutes, so render one answer set while you work, and all of them before
you commit.
</commands>

<conventions>
- Test each change in a rendered project, because the template files are not valid Python before rendering. A change
  is done when `just render-all` passes: the CI matrix runs the same command.
- Keep the rendered project free of EBaMl names. The reason: the template serves every domain.
  `tests/forbidden-names.txt` is checked in CI.
- Follow the rules in `template/.claude/rules/` for the template too: conventional, atomic commits, and the writing
  style of `writing-style.md` for the docs.
- Put a profile file under a path part that renders empty when the profile is off, for example
  `{% if 'service' in profiles %}api{% endif %}`. The reason: vulture, coverage and mutation testing fail on code that
  a project does not use, so no answer may add unused code.
- Change the answer files when you add a question, so that the CI matrix covers each answer. The matrix is the list
  of files in `tests/answers/`.
- Make a rendered file pass the formatters as it comes out of Copier: `just check` must pass on the first run. Put
  each Jinja block tag on its own line, and split a call whose length depends on an answer over several lines.
- After a fix in a rendered project, copy the fix back to the template file. A file without `.jinja` is copied as it
  is, so you can copy it back whole.
</conventions>
