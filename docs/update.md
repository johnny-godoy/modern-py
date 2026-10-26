# Update a project

A standard that each project changes on its own drifts apart. So the project takes each change of the template with
`copier update`. `.copier-answers.yml` holds the answers and the template version of the last copy or update.

## Take the template changes

1. Commit or stash every change of the project. Copier updates only a clean working tree.
2. Run the update:

   ```bash
   uvx copier update --trust
   ```

3. Read the diff. Run `just check` and `just test`.
4. Commit the update as one commit, for example `build: update from modern-py v0.2.0`.

Copier compares three versions of each file: the template at the last version, the template at the new version, and
the project. It applies the change of the template to the project.

## Change an answer

Run the update with the new answer, for example to add a profile or to raise the approvals of the ruleset:

```bash
uvx copier update --trust --data 'profiles=["service"]'
uvx copier update --trust --data required_approvals=1
```

## Resolve a conflict

A conflict occurs when the project and the template change the same lines. Copier writes both versions with the
markers `<<<<<<<` and `>>>>>>>`.

1. Find the files: `git diff --name-only --diff-filter=U`, or search for `<<<<<<<`.
2. Keep the change of the template in the shared files: the scripts, the hooks, the workflows and the rules. The
   project gets the same standard as the other projects only then.
3. Keep the change of the project in its own files: the code, the tests, the docs and the README.
4. Remove the markers, run `just check` and `just test`, and commit.

To keep conflicts rare, change a shared file in the template, not in the project. Copier copies `CHANGELOG.md` and
`ROADMAP.md` only on the first copy, so the release workflow and the project own them.

## How the template checks updates

The `update` job of the template CI renders a project from the previous tag, commits it, and runs
`copier update` to the new commit. The job fails on a conflict, and then it runs `just check` and `just test` on the
updated project. So an untouched project takes each release of the template with no conflict.
