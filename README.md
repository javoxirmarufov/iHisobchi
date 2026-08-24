# iHisobchi — the Business Operating System of Uzbekistan

> **A project showcase for the President AI Award.** A curated public selection
> from a private codebase: the complete product overview, the architecture, and
> representative fragments of real production code.

*iHisobchi is an AI-driven business operating system for Uzbekistan —
e-invoicing with digital signature (Didox / E-IMZO), deal tracking, banking, tax
office integration, warehousing, HR and a voice-first AI orchestrator, delivered
through Telegram, a Mini App and a web app. This repository is a curated public
showcase of a private production codebase. See
[About this repository](#about-this-repository).*

---

## What This Is

An entrepreneur in Uzbekistan assembles their bookkeeping out of 7–9 disconnected
programs: the Didox portal for e-invoices, a bank client, 1C or Excel for stock,
a separate till, a separate HR package, a messenger for talking to the
bookkeeper. Between them, they are their own integration layer.

**iHisobchi replaces that assembly with a single loop.** Not one more tool in a
row of ten but an **orchestrator** in which the whole business is held at once:
documents and digital signatures, deals, money, inventory, HR, the tax office,
the till, sales. It is operated by talking to an AI agent that knows this
particular business's products, prices, counterparties, debts and obligations.

Three levels of value:

| Level | What it means |
|---|---|
| **A tool** | An e-invoice in 2 minutes instead of 40 on the portal. By voice, from a phone, digitally signed |
| **A loop** | A document is part of a deal. The system sees: contract signed → payment not received → power of attorney issued → invoice not raised — and tells the owner whose move it is |
| **An orchestrator** | An order from the storefront becomes a contract and an invoice by itself, a payment closes the deal by itself, a cash-register receipt posts itself to the books, a letter from the tax office arrives in Telegram by itself |

The product runs in production with real clients and real document flow, legally
valid under Uzbek law.

---

## The Project in Numbers

| | |
|---|---|
| Lines of application code (Python) | **580,018** |
| Lines of tests (Python) | **509,771** |
| Lines of frontend code (TypeScript/React) | **290,103** |
| Automated tests | **18,496** pytest + **3,573** vitest |
| Business-logic modules | **263** services, **105** Telegram routers |
| Database migrations | **256** (Alembic) |
| Localisation keys | **2,484** in each of two languages — Russian and Uzbek |
| Commits | **2,280** and **1,198** merged pull requests over 6 months of continuous development — [history and pace](ENGINEERING.md) |
| Points of entry for a user | **18** (Telegram, Mini App, web app, MCP, REST API, a Chrome extension, a desktop signing agent…) |

*Measured against `origin/main` on 24 August 2026.*

---

## About This Repository

The main codebase is **private**, and will stay that way: it contains a working
integration with state e-document systems, the cryptographic signing loop, and
real client data protected by Uzbek personal-data law.

The competition asks for **part of the project's code**. This repository is that
part — assembled deliberately rather than exported as a random slice:

- **The complete product overview** — nine documents in
  [`docs/overview/`](docs/overview/), written from the source code and live
  production, plus an 18-slide deck.
- **Representative code fragments** — files that show the engineering culture:
  encryption with key rotation, masking of secrets and personal data in logs, the
  codification of Uzbek labour law, background task management, migrations, the
  CI pipeline, and frontend code with its tests.
- **Tests alongside the code** — every module shown comes with its own test, so
  that coverage can be verified rather than taken on trust.

It was assembled with a fresh `git init` in a single commit: the main
repository's history was not carried over. The selection was checked with a
secret scanner (`detect-secrets`) — no findings.

That is why the commit counter here shows single digits rather than thousands.
The real volume and pace of the work is in **[ENGINEERING.md](ENGINEERING.md)**:
2,280 commits and 1,198 pull requests over six months, 155 active days out of 193,
and a test base that grew from 12 files to 1,321.

---

## What to Look At

### The product overview — [`docs/overview/`](docs/overview/)

| Document | What it covers |
|---|---|
| [01-ecosystem.md](docs/overview/01-ecosystem.md) | The problem we solve, the orchestrator idea, all 18 points of entry, the architecture, the current state in figures |
| [02-modules.md](docs/overview/02-modules.md) | Every module in detail: documents, deals, Business Pulse, the AI Lawyer, banking, tax, inventory, HR, the marketplace, integrations |
| [03-roadmap.md](docs/overview/03-roadmap.md) | Ten horizons of development |
| [04-voice-orchestrator.md](docs/overview/04-voice-orchestrator.md) | **The product's main bet** — running a business by voice |
| [05-security.md](docs/overview/05-security.md) | Encryption, zero-retention AI, the signature-key vault |
| [06-first-day.md](docs/overview/06-first-day.md) | The client's end-to-end journey: sign-up → organisation → signing → first document |
| [07-signing.md](docs/overview/07-signing.md) | Four ways to sign, and why none of them will sign anything without the owner |
| [08-with-and-without.md](docs/overview/08-with-and-without.md) | A map of the Uzbek market, and what the current assembly of 7–9 programs costs |
| [09-business-model.md](docs/overview/09-business-model.md) | Eight revenue streams |
| [pitch/deck.html](docs/overview/pitch/deck.html) | The full 47-slide deck: summary, the cost of the problem, real product screens, what clients say, every module, security, economics |

### Code fragments

| File | What it demonstrates |
|---|---|
| [`services/crypto.py`](services/crypto.py) | Fernet encryption with **key rotation**: versioned prefixes, reads with the old key under a metric, a separate loop for personal data. Access to the database does not grant access to passwords |
| [`services/logging_config.py`](services/logging_config.py) | A filter that masks secrets and **Uzbek personal data** in logs — TINs, PINFLs, +998 phone numbers. With an optimisation: a fast substring check discards ~80% of records before the expensive regular expressions |
| [`services/uz_labor.py`](services/uz_labor.py) | **Domain expertise**: Uzbek labour-law rules expressed in code. The minimum wage as a calendar rather than a constant; Articles 245 and 248(2) together mean that topping salaries up to the minimum wage with bonuses is not allowed — importing the Russian model here would be wrong |
| [`services/task_manager.py`](services/task_manager.py) | Lifecycle management for background tasks: a task is not lost when the process stops |
| [`services/error_codes.py`](services/error_codes.py) | Codification of external-system errors — the user receives a code, not a stack trace |
| [`alembic/versions/217_hr_records_foundation.py`](alembic/versions/217_hr_records_foundation.py) | The HR module migration: integrity constraints at the database level, a reversible `downgrade` |
| [`alembic/versions/224_ikpu_suggestions.py`](alembic/versions/224_ikpu_suggestions.py) | The IKPU suggestion queue: a separate table until a human confirms |
| [`miniapp/src/hooks/useDraftAutosave.ts`](miniapp/src/hooks/useDraftAutosave.ts) | Draft autosaving in the frontend — work is not lost when the connection drops |
| [`miniapp/src/components/ErrorBoundary.tsx`](miniapp/src/components/ErrorBoundary.tsx) | Isolation of interface failures |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | The CI pipeline: linting, tests, migration checks, secret scanning |
| [`ruff.toml`](ruff.toml) | The single source of truth for code style |

Tests for the modules shown are in [`tests/`](tests/).

---

## Architecture

```
Telegram Bot (aiogram)  ─┐
React Mini App          ─┤
Web app                 ─┼─→  Service layer (250 modules)  ─┬─→  PostgreSQL 16
MCP server              ─┤        business logic,           ├─→  Redis 7 (FSM, cache)
Partner REST API        ─┤        circuit breakers,         └─→  External systems:
Chrome extension        ─┤        idempotency,                   Didox, E-IMZO,
E-IMZO Agent (Windows)  ─┘        operation queues                banking, tax office,
                                                                  Grok, Whisper
```

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Bot | aiogram 3.27 |
| HTTP | aiohttp 3.11 |
| Database | PostgreSQL 16 (asyncpg), Alembic migrations |
| Cache / FSM | Redis 7 |
| Frontend | React + TypeScript, Vite |
| Documents | WeasyPrint + Jinja2 |
| Encryption | Fernet (cryptography), a sealed box for the signature vault |
| AI | Grok (xAI) — agent, lawyer, parsers; Anthropic Claude — AI Studio |
| Speech | Groq Whisper (ru), Gemini (uz), Grok Voice Realtime |
| Infrastructure | Docker Compose, nginx + Let's Encrypt |
| Observability | Sentry, Prometheus, Alertmanager, Grafana |
| CI/CD | Self-hosted GitHub Actions, automatic rollback on a failed deployment |

### Engineering principles visible in the code

- **Nothing sensitive in the clear.** Passwords, tokens, signature credentials
  and personal data are encrypted, keys are rotated, logs are masked.
- **External systems are assumed unreliable.** Every integration sits behind a
  circuit breaker; document signing is idempotent — a dropped connection cannot
  produce a double signature.
- **Failure has to be visible.** Sentry, metrics, alerts into the on-call
  engineer's messenger.
- **The database schema changes only through a migration.** 256 revisions,
  reversible and verified in CI.
- **A human confirms.** No AI agent signs or sends a document without an explicit
  action by the owner.

---

## The Product, Live

| | |
|---|---|
| Telegram | [@ihisobchi_bot](https://t.me/ihisobchi_bot) |
| Mini App / web app | [app.ihisobchi.uz](https://app.ihisobchi.uz) |

---

## Licence and Rights

© 2026 Javokhir Marufov. **All rights reserved.**

The material in this repository is published **solely so that the competition
jury can assess** the project's technical level. This is **not** open-source
software. Any use, copying, modification, distribution or creation of derivative
works without the written permission of the rights holder is prohibited.

For details, see [LICENSE](LICENSE).
