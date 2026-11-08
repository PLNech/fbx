# Changelog

All notable changes to `fbx` are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning is
[SemVer](https://semver.org/).

## [0.1.0], 2026-11-08

First public release.

- Full-coverage CLI into a Freebox OS box's panel API: **15 domains,
  183 endpoint records, 292 operations**, spec-driven from the clean-room
  API notes in `docs/api/` (16 markdown files). Tagline: une CLI pour ta Freebox.
- Panel-dialect login (challenge table evaluated via a one-shot `node`
  subprocess, `HMAC-SHA1(SHA1(salt+password), challenge)`), cookie session
  stored `chmod 600`, one automatic re-login on auth errors, password read
  from 1Password or `--stdin`, never in argv.
- Generic grammar per domain (`list`/`show`/`get`/`add`/`set`/`rm`),
  auto-typed `key=value` body fields, positional path slots.
- Destructive operations (reboot/shutdown, storage format/fsck, raid member
  ops, fs rm/mv, token revocation) gated behind `--yes`.
- Global flags: `--json`, `--debug`, `--yes`; `fbx api METHOD PATH` as the
  generic escape hatch.
- Binary file transfer: `fbx fs get` / `fbx fs put` (documented multipart
  fallback).
- 259 tests: the fixture suite (formatters, path resolution, mocked auth
  flow), a surface test asserting the whole documented command tree, gate
  sweeps (every gated op refuses without `--yes` before any HTTP call), a UX
  contract test (`-h` everywhere, bare args are usage errors, no shrug
  cells, `tldr` examples executed) and a readability sweep (292-op corpus +
  fuzz, zero shrug cells).
- Generated command wiki under `docs/cmd/` (16 pages): per-command synthetic
  happy + error examples, rendered through the real CLI against a mocked
  transport; CI regenerates and diffs it.
- `fbx tldr`: ten copy-pasteable starter examples.
- Graceful degradation for multi-call commands (`fbx storage overview`
  renders what answers and warns on what does not).

[0.1.0]: https://git.nech.pl/pln/fbx/-/tags/v0.1.0
