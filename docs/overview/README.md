# iHisobchi — Ecosystem Overview

> **What this folder is.** A complete, current overview of the product: what
> iHisobchi is today, which surfaces and modules it consists of, how it is built
> inside, how the data is protected, and where it is heading.
>
> The overview is written from the source code and from live production, not from
> earlier documentation — which described the product as "a Telegram bot for
> documents", which is what it was in early 2026.

**Document passport**

| | |
|---|---|
| Current as of | **14 August 2026** |
| Code state | `origin/main`, Alembic head **236** |
| Production | metrics snapshot taken 14 August 2026 |
| How it was assembled | From the source code and live production: service and router docstrings, actual feature flags from Redis and the `feature_flags` table, counters from the database. Not from the documentation — parts of it are out of date |
| Drift check | `python3 scripts/overview_snapshot.py` re-measures every figure in the overview against the code and production. Figures drawn from the code are **verified automatically every night** in the nightly CI run; production counters are reviewed by hand |
| Next review | On any major product change; production figures at least quarterly |

---

## Reading Order

| # | Document | What it covers |
|---|---|---|
| 1 | **[01-ecosystem.md](01-ecosystem.md)** | What iHisobchi is, the problem it solves, the "business orchestrator" idea, all 18 platforms and points of entry, the architecture, the current state in figures |
| 2 | **[02-modules.md](02-modules.md)** | Every module and feature in detail: documents, deals, Business Pulse, the AI Lawyer, banking, tax, inventory, HR, the marketplace, instalments, integrations, AI surfaces |
| 3 | **[03-roadmap.md](03-roadmap.md)** | Eleven horizons: autonomous deals, the automatic invoice on payment, an accounting services exchange, the outsourcer workspace, turnkey commerce (live streaming and video), open banking, mobile apps, tax filing, AI support, warehousing and customs, social commerce |
| 4 | **[04-voice-orchestrator.md](04-voice-orchestrator.md)** | **The product's main bet** — the voice AI orchestrator: running an entire business by conversation, on any device |
| 5 | **[05-security.md](05-security.md)** | **Security and trust** — encryption, zero-retention AI, the signature-key vault, and what we do every night |
| 6 | **[06-first-day.md](06-first-day.md)** | **The client's first day** — the whole journey: sign-up, connecting an organisation, setting up signing, the first document, and where people drop out |
| 7 | **[07-signing.md](07-signing.md)** | **Document signing** — four methods from the classic to the fully autonomous, plus enterprise delivery, and why none of them will sign anything without you |
| 8 | **[08-with-and-without.md](08-with-and-without.md)** | **With us and without us** — a map of the Uzbek market, what the current assembly of 7–9 programs costs, what nobody else has, official mass-mailing of proposals, and our position on support |
| 9 | **[09-business-model.md](09-business-model.md)** | **How we make money** — eight revenue streams: subscriptions with prices, marketplace promotion, the corporate environment, warehousing and fulfilment, service exchanges, the accounting firm workspace, the business-activity certificate, implementation and partners |

**Separately:** [pitch/investor-deck.html](pitch/investor-deck.html) — an
18-slide investor deck assembled from these documents.

---

## The Product on One Page

**iHisobchi is a business operating system for Uzbekistan.**
Not an eleventh tool alongside ten others but an **orchestrator** in which an
entrepreneur keeps their whole business at once: documents and digital
signatures, deals, money, inventory, HR, the tax office, the till, sales — and
runs all of it by talking to an AI agent that knows their products, prices,
counterparties, debts and obligations.

Three levels of value, in ascending order:

1. **The tool level.** An e-invoice in 2 minutes instead of 40 on the Didox
   portal. By voice, from a phone, with a digital signature.
2. **The loop level.** A document does not live on its own — it is part of a
   deal. The system sees: contract signed → payment not received → power of
   attorney issued → invoice not raised → and tells the owner whose move it is.
3. **The orchestrator level.** The business runs like a Swiss watch: an order
   from the storefront becomes a contract and an invoice by itself, a payment
   closes the deal by itself, a cash-register receipt posts itself to the books,
   a letter from the tax office arrives in Telegram by itself, and the AI-driven
   Business Pulse shows the owner, unprompted, where money is leaking out of the
   company.

**And above all of it — [the voice](04-voice-orchestrator.md).** The owner
talks; the business works.

## What Already Works — in Live Production Figures

**The size of the platform:**

| Indicator | Value |
|---|---|
| Business-logic modules | **252** |
| Telegram routers | **103** |
| Mini App screens | **126** routes |
| Capabilities available to the AI | **67** |
| Database migrations | Alembic head **236** (195 tables in production) |
| Lines of code | ~**562,000** Python (excluding tests) + ~**262,000** TypeScript/React |
| Tests | ~**439,000** lines of test code |

**Accumulated over all time** (part of it mirrors what businesses were doing in
Didox anyway; this is the system's throughput, not solely value we created):

| Indicator | Value |
|---|---|
| Documents processed | **73,098** |
| Deals in the cycle engine | **85,869**, of which **62,802 (73%)** are closed |
| Incoming documents mirrored | **96,217** |
| Bank transactions parsed | **70,094** |
| Product records in catalogues | **5,699** |
| Active signature keys | **25** |

**What is being used right now — over 30 days:**

| Indicator | Value |
|---|---|
| Organisations in total | **80** |
| Organisations that created documents | **57** |
| Users who signed in (30 days / 7 days) | **76 / 19** |
| Documents created | **4,095** |
| AI agent actions | **313** (across 9 organisations) |

> **How to read this.** The platform is broadly built and technically mature; the
> audience is early and depth of use is uneven. The constraint today is not how
> fast new modules can be built but getting what is already built into regular
> use. That directly determines the [order of work](03-roadmap.md#what-we-are-working-on-first).

## Status Legend

Every feature in these documents carries an honest marker. The full picture
includes what works, what is rolling out, and what has been designed and is next
in the queue. Without that marking, an overview turns either into a promise or
into an omission.

| Marker | What it means |
|---|---|
| ✅ **In production** | Working for clients right now, with the switch on globally |
| 🟡 **Rolling out** | Built and tested, enabled client by client (canary release or a dedicated flag) |
| 🔵 **In progress** | The code is in production behind a disabled flag, or is being built now |
| 🎯 **Next step** | Decided, designed, and near the front of the queue |

Where an enabled feature has an **early audience**, that is stated alongside the
marker: "in production" means "available and working", not "everyone is already
using it".

---

*The overview is maintained by hand. On major product changes, update it together
with `docs/feature-history.md`. Production figures are marked with the date they
were taken.*
