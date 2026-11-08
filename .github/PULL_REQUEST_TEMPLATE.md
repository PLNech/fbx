<!--
  Reminder: no live box data and no secrets in this PR — synthetic fixtures
  only. See CONTRIBUTING.md ("The clean-room rule").
-->

## What changed

<!-- Domain/records touched, and why: which docs/api file justifies it -->

## Checklist

- [ ] Endpoint record(s) justified from `docs/api/` (never from a live box)
- [ ] Fixtures are synthetic; no live data, no secrets, no personal network info
- [ ] `python tools/gen_wiki.py` run — `docs/cmd/` regenerated (CI diffs it)
- [ ] `pytest` green (surface test included)

## Test evidence

<!-- paste the pytest tail and, for render changes, a before/after snippet -->
