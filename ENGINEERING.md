# Development History

> **Why this file exists.** This repository holds two commits, and that is by
> design: it was assembled with a fresh `git init`, and the main repository's
> history was deliberately not carried over, so that internal details of the
> private environment would not travel with it. But that leaves the volume of
> real work as a claim rather than a fact. What follows are aggregate statistics
> from the private repository: figures that show the pace, without a single line
> of internal content.

---

## Period and Pace

| | |
|---|---|
| First commit | **12 February 2026** |
| Latest measurement | **24 August 2026** |
| Calendar days | **193** |
| Days with commits | **155** — 79% of all calendar days, weekends included |
| Commits on `main` | **2,280** |
| Merged pull requests | **1,198** |
| Average on an active day | **14 commits** |

Development has run continuously for six months. Not as a sprint towards a
deadline: 79% of calendar days carrying commits means the project has had
essentially no pauses longer than a couple of days.

## Commits by Month

```
2026-02   160  █████████████
2026-03    43  ████
2026-04   248  █████████████████████
2026-05   387  ████████████████████████████████
2026-06   266  ██████████████████████
2026-07   475  ████████████████████████████████████████
2026-08   482  ████████████████████████████████████████  ← in 14 days
```

The last line is the telling one. **482 commits in the first 14 days of August**
against 475 for the whole of July — roughly 34 commits a day. The project is not
levelling off and not slowing down as the submission deadline approaches; it is
accelerating.

The dip in March (43) has a simple explanation: February went into the skeleton,
and March into designing the domain model of Uzbek document flow, where little
code was written and a great deal of legislation was studied. From April onwards
the pace has only risen.

## Growth of the Codebase

Snapshots of the real tree on four dates:

| Date | `.py` files | Of which test files |
|---|---|---|
| 1 March 2026 | 175 | 12 |
| 1 May 2026 | 412 | 106 |
| 1 July 2026 | 1,575 | 586 |
| 24 August 2026 | **3,188** | **1,321** |

The number of test files grew **a hundredfold** in five months, and it grows
faster than the product code: in March tests were 7% of files, in August 41%.
This is not decoration for a report but a working necessity: the product issues
legally significant documents, and an error in an IKPU code means a penalty for
the client under Article 223 of the Tax Code of Uzbekistan.

The suite today holds **18,496** Python tests and **3,573** TypeScript tests.

## Process, Not Only Volume

- **1,198 merged pull requests** — work goes through branches and review; pushing
  directly to `main` is not practised.
- **232 Alembic migrations** — the database schema changes only through a
  revision, each with a reversible `downgrade` and a CI check.
- **Self-hosted CI across three runners** — linting, the full test run, migration
  checks up and down, secret scanning by two independent scanners, static
  analysis and CVE auditing of dependencies.
- **Automatic deployment rollback** — a failed release restores the previous
  image and database state without manual intervention.
- **A nightly run** — the entire repository history is re-examined for an
  accidentally committed secret; a red result is handled as an incident.

## How to Verify This

The private repository is closed for obvious reasons, but the volume of work is
visible from outside as well:

1. **The product works.** [app.ihisobchi.uz](https://app.ihisobchi.uz) — with
   legally significant document flow and real clients.
2. **The profile's activity graph** —
   [github.com/javoxirmarufov](https://github.com/javoxirmarufov).
3. **The code in this repository** — the selection is written in the same style
   and to the same standard as the other 555,000 lines. Every module shown comes
   with its own test.

---

## Summary

Development of iHisobchi began on **12 February 2026** and has run continuously
since:

| | |
|---|---|
| Commits on `main` | **2,280** |
| Merged pull requests | **1,198** |
| Days with commits | **155 of 193** calendar days (79%) |
| Python files | 175 → **3,188** (Mar → Aug 2026) |
| Test files | 12 → **1,321** — a hundredfold increase |
| Automated tests today | **18,496** Python · **3,573** TypeScript |
| Database migrations | **256**, each reversible and CI-verified |

Monthly commit volume: 160 · 43 · 248 · 387 · 266 · 475 · **482**. The final
figure covers only the **first 14 days of August** — roughly 34 commits per day.
The project is accelerating, not winding down toward a submission deadline.

Every change goes through a branch and a pull request. A self-hosted CI pipeline
runs linting, the full test suite, forward-and-back migration checks, two
independent secret scanners, static analysis and CVE auditing on every change,
with automatic rollback on a failed deployment.
