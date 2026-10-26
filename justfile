# Recipes for the work on the template. The rendered projects have their own justfile.
set shell := ["bash", "-euo", "pipefail", "-c"]

# List the recipes.
default:
    @just --list

# Render one answer file of tests/answers/ into a directory and run its checks.
render name dir="/tmp/modern-py-render":
    scripts/render.sh {{name}} {{dir}}/{{name}}

# Render every answer file and run its checks, as the CI matrix does.
render-all dir="/tmp/modern-py-render":
    for f in tests/answers/*.yml; do scripts/render.sh "$(basename "$f" .yml)" "{{dir}}/$(basename "$f" .yml)"; done

# Run copier update from the previous tag to the working tree on a rendered project.
update-check dir="/tmp/modern-py-update":
    scripts/update_check.sh {{dir}}

# Write the tables that template/scripts/banned.toml generates into the template files.
sync-tables:
    python3 scripts/sync_tables.py

# Fail when a table that template/scripts/banned.toml generates is out of date.
check-tables:
    python3 scripts/sync_tables.py --check
