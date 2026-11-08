# Changelog

All notable changes to `fbx` are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning is
[SemVer](https://semver.org/).

## [0.1.0] — 2026-11-08

First public release.

- Full-coverage CLI into a Freebox OS box's panel API: **15 domains,
  183 endpoint records, 292 operations**, spec-driven from the clean-room
  API notes in `docs/api/` (16 markdown files).
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
- 217 tests: 212 fixture-based tests over the formatters, path resolution and
  auth flow (mocked), plus a surface test asserting the whole documented
  command tree is registered.

[0.1.0]: https://git.nech.pl/pln/fbx/-/tags/v0.1.0
