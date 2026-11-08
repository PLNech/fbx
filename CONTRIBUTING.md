# Contributing to fbx

Thanks for wanting to improve `fbx`. The rules below keep the project
honest: everything in it is justified by the panel's own, publicly-served
code, never by anyone's live box dump.

## Dev setup

```sh
git clone https://git.nech.pl/pln/fbx && cd fbx
poetry install          # small venv: typer + rich (+ pytest, pytest-cov)
poetry run pytest       # 267 tests, all fixture-based, fully offline
poetry run python tools/gen_wiki.py   # regenerate docs/cmd/
```

### The password ladder (1Password reference)

`fbx login` reads the Freebox password with `op read`. Which 1Password item
holds it is resolved as: the `FREEBOX_OP_REF` env var, then a one-line file
at `~/.config/freebox/opref` (the whole line is the `op://` reference; keep
it `chmod 600`, fbx warns on stderr if it is too open), then the built-in
default `op://Personal/Freebox/credential`. The file rung exists so a
machine can be configured without touching anyone's shell rc.

## The clean-room rule (one paragraph, non-negotiable)

Every endpoint record in `fbx_cli/domains/` must be justified from the
markdown files in `docs/api/`, which were transcribed from the panel's
publicly-served JavaScript, not from a live box. Never reverse a record from
an HTTP dump of your own box, never paste real box payloads into issues,
PRs, fixtures or docs, and never include secrets, passwords, serials or
personal network data anywhere in the project. Synthetic fixtures only:
names look like `device-alpha`, addresses like `192.168.1.50`, and the test
suite's autouse guard fails loudly if anything tries to touch a network.

## Commit style

Tiny atomic commits, one logical change each, conventional messages
(`feat:`, `fix:`, `docs:`, `test:`, `ci:`). If a commit needs the word
"and" twice in its subject, split it.

## The CI freshness gate

Both pipelines (GitLab `.gitlab-ci.yml` and GitHub `.github/workflows/ci.yml`)
regenerate `docs/cmd/` and then run `git diff --exit-code docs/cmd`: if a
record changed without its wiki page, the build fails. Run
`python tools/gen_wiki.py` before committing a record change; the generator
is deterministic (fixed width, sorted keys, no timestamps), so an
up-to-date tree produces a zero diff.

On GitHub, the wiki job is verify-only. If you want the regenerated pages to
auto-commit on master ("wiki ships with the commands"), add a
`stefanzweifel/git-auto-commit-action@v5` step (with `permissions:
contents: write`) after the regeneration step in the `wiki` job; that
choice belongs to the repository owner, so it ships disabled.

## Adding an endpoint record, end to end

1. **Read the docs.** Find (or add) the endpoint in `docs/api/<area>.md`:
   verb set, path template, response model. If the docs don't cover it, it
   doesn't go in; `fbx api` is the escape hatch.
2. **Add the record** in `fbx_cli/domains/<domain>.py`: one `Rec(...)` with
   the documented path, op letters (`L` list, `R` show, `G` get-one, `C`
   create, `U` update, `D` delete, `A` action), render hints (`cols`,
   `units`, `name_field`) and a provenance `note`. Destructive? `gate=True`
   gates every mutating op behind `--yes`.
3. **Fixture it.** If the response model is non-trivial, add a synthetic
   payload to `tests/fixtures_models.py` (obviously fake names only).
4. **Regenerate the wiki**: `python tools/gen_wiki.py`; the new record's
   page appears in `docs/cmd/` with synthetic happy and error examples.
5. **Test**: `poetry run pytest`; the surface test verifies the record is
   registered with path and verbs; add a focused test if the record has a
   custom renderer or non-default gate.
6. **Commit** the docs, record, fixture and wiki pages (can be separate
   tiny commits, in that order).
