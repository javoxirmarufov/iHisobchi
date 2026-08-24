# 1. The iHisobchi Ecosystem

> Part 1 of 9. Next: [modules](02-modules.md) · [roadmap](03-roadmap.md) · [voice orchestrator](04-voice-orchestrator.md) · [security](05-security.md) · [first day](06-first-day.md) · [signing](07-signing.md) · [with us and without us](08-with-and-without.md) · [business model](09-business-model.md).

---

## 1.1. In One Sentence

**iHisobchi is a business operating system: a single environment in which an
Uzbek entrepreneur keeps documents, deals, money, inventory, payroll, tax
affairs and sales — and runs all of it by talking to an AI agent that knows
their business.**

The key word is **orchestrator**. We are not building an eleventh tool to sit
beside the ten a company already owns. We are building the layer that **connects
and drives** those ten: integrating with what the client already uses (1C,
MoySklad, AmoCRM, Bitrix24, their cash register, their bank) where that makes
sense, replacing it with a module of our own where it does not — but always so
that the business ends up with **one way in and one picture of reality**.

---

## 1.2. The Problem We Solve

### What a typical Uzbek business goes through today

Take an ordinary trading company. To get through a single working day, its staff
log into:

| System | What for | What it costs them |
|---|---|---|
| **Didox** (state e-document portal) | issue an e-invoice, waybill, contract, acceptance act | 30–60 minutes of manual data entry per document, plus hunting for the right IKPU product code in the Tasnif catalogue |
| **E-IMZO** | sign it | requires a desktop computer, a USB key, installed software — office only |
| **my.soliq.uz** | collect letters from the tax office, export fiscal cash-register receipts | manual login with a digital signature, downloading files one at a time |
| **Bank client** | check whether the money has arrived | a separate login, a separate statement export |
| **1C / MoySklad** | post it to the books | the same figures typed in by hand for the third time |
| **Excel** | work out what is actually going on | assembled by hand, out of date the moment it is saved |
| **Telegram / phone** | "Hey, did the payment from Artel come through?" | dozens of calls a day |

None of these systems knows the others exist. **A human moves the data — by
hand, three times over, with mistakes.**

### What that really costs

The problem is not the lost hours. It is the three holes through which money
leaves the company:

**1. Deals that never close.** The contract is signed, the goods are shipped,
the act is completed — and the payment never comes. Nobody notices, because
nobody reconciles contracts against the bank statement. A year later it is a
receivable that can no longer be collected.

**2. An owner who cannot see.** The founder looks at the business once a
quarter, through a report written in terms they were never required to
understand. By the time the dividends come in lower than expected, it is too
late to investigate.

**3. Panic at the moment of risk.** A demand arrives from the tax office. The
owner has no idea how serious it is, who to turn to, what it should cost, or
whether they are being taken for a ride. The first outsourcing firm they call
can name any number it likes.

### Our answer

**One loop. One AI that sees everything. Automation where a human adds nothing,
and an explicit confirmation where a human is essential.**

A document is born in two minutes — but what matters more is that it
**immediately becomes part of a deal**, that the deal reconciles itself against
the bank and the tax office, and that Business Pulse translates the result into
plain language for the owner.

---

## 1.3. Who It Is For

| Segment | Size in Uzbekistan | What they get |
|---|---|---|
| **Sole traders and micro-businesses** | ~600,000 | An accountant in your pocket: documents dictated from a phone, no PC and no bookkeeper required |
| **Small businesses (LLCs up to 50 staff)** | ~200,000 | The bookkeeper freed from routine: automatic documents, automatic reconciliation, automatic intake |
| **Multi-business owners** | tens of thousands | Several companies in one app, one tap to switch, a single event feed across all of them |
| **Founders and investors** | — | Business Pulse: a clear picture without accounting jargon, plus a detector for unusual transactions |
| **Wholesalers and manufacturers** | ~50,000 | Dozens of e-invoices a day, waybills, inventory, a storefront on the marketplace |
| **Retail with a fiscal cash register** | ~15,000 | Cash-register receipts posted to the books automatically, an evening summary of the till |
| **Pharmaceuticals** | ~15,000 | Pharma e-invoices (types 008/031) with batch series and regulated mark-up |
| **Logistics** | ~10,000 | Waybills with driver, route and weight — every single day |
| **Accounting and outsourcing firms** | thousands | 🎯 a multi-client workspace: one firm running the books of 40 companies |

---

## 1.4. Platforms and Points of Entry

This is not "a bot with an app attached". It is **eighteen surfaces on one
core** — for different roles, different devices and different degrees of
involvement.

### For the business owner

| # | Surface | Address | What it is |
|---|---|---|---|
| 1 | **Telegram bot (Free)** | container `bot` | The free tier: documents, signing, incoming mail, reports. The way in for the whole market |
| 2 | **Telegram bot — iHisobchi Pro** | container `bot-pro` | The full product: integrations, automatic documents, the AI agent, banking, deals |
| 3 | **Telegram Mini App** | `app.ihisobchi.uz` inside Telegram | A complete application: 126 screens, authentication via Telegram's signed initData (HMAC-SHA256), live updates over SSE |
| 4 | **Web app in the browser** | `app.ihisobchi.uz` | The same SPA outside Telegram: sign in with phone + SMS OTP, or e-mail + password. Installs as an app (PWA manifest, standalone mode, icons, its own splash screen) — on a phone it is indistinguishable from a native one |
| 5 | **Voice assistant** | the "Assistant" section | A live speech-to-speech conversation: you talk, it acts. Not "command recognition" — an actual conversation |
| 6 | **Landing page** | `ihisobchi.uz` | The public product page and sign-up |

### For counterparties and buyers — no sign-up required

| # | Surface | Address | What it is |
|---|---|---|---|
| 7 | **UmagShop — the marketplace** | `umagshop.uz` | A shared B2B catalogue: banners, categories, curated collections, search, an AI shopping assistant |
| 8 | **UmagShop — seller storefront** | `<shop>.umagshop.uz` and `umagshop.uz/<slug>` | A business's own shop on its own subdomain |
| 9 | **UmagShop — seller entry point** | `seller.umagshop.uz` | A landing page and sign-up for sellers arriving cold, with no mention of iHisobchi until an organisation is linked |
| 10 | **QR-Hisob** | `shop.ihisobchi.uz`, public `/shop/<TIN>` | A printed QR code on the counter: the buyer scans it, places an order and receives a contract and an invoice. No app, no registration |
| 11 | **Deal Link** | `/l/<slug>` | The seller sends a link over a messenger → the buyer fills in their details → the contract and invoice are ready |
| 12 | **Instalment buyer portal** | `/n/<token>` | The customer sees their payment schedule and outstanding balance from a link |

### Technical and partner surfaces

| # | Surface | Address / form | What it is |
|---|---|---|---|
| 13 | **E-IMZO Agent** | Windows application | A desktop signing agent: it holds the USB key or `.pfx` file and signs documents on command from Telegram. The owner is travelling — the documents still get signed |
| 14 | **"24/7 Signing Server"** | managed environment | The signature key inside an isolated environment: signing works round the clock without the client's computer being switched on. Requires separate, explicit consent; storage is a sealed box that the ordinary production backend cannot decrypt (the exact model is in [05-security.md](05-security.md#54-the-247-signing-server--what-exactly-we-store)) |
| 15 | **Chrome extension** | browser | AI workflows layered over third-party web portals: filling in forms, moving data across, looking things up |
| 16 | **MCP server** | `mcp.ihisobchi.uz` | Connects iHisobchi to external AI clients (Claude, ChatGPT and others) over the MCP protocol with OAuth 2.1. The client talks to their own business from any AI application |
| 17 | **Partner REST API** | HTTP | A headless surface for partners: creating document drafts with a per-organisation key (signing and submission are not yet open on this surface — see [02-modules.md §R.2](02-modules.md#r2-partner-rest-api-)) |
| 18 | **Internal admin console** | internal network | The team's own panel: users, feature flags, billing, access tokens |

> **On mobile apps.** The phone is covered today in two ways: the Telegram Mini
> App, and a web app that installs onto the home screen and behaves like an
> ordinary application. Native iOS and Android apps are a separate horizon on
> the roadmap, with their own reasoning and stages:
> [3.8. Mobile applications](03-roadmap.md#38-horizon-vii--mobile-applications-ios-and-android).

**Every surface is a window onto the same core, not a product of its own.** A
document dictated in the Mini App is visible in the bot, reachable over the
Partner API, folded into a deal, rolled into a report, and delivered to the
counterparty through Didox.

---

## 1.5. How It Works Inside: One Brain, Many Windows

This is the architectural decision everything else follows from:

```
                    ┌─────────────────────────────────┐
                    │   CAPABILITY REGISTRY           │
                    │   services/capabilities/        │
                    │   65 tools:                     │
                    │   read · calculate · create a   │
                    │   draft · request a signature   │
                    └───────────────┬─────────────────┘
                                    │
        ┌───────────────┬───────────┼───────────┬────────────────┐
        ▼               ▼           ▼           ▼                ▼
  AI agent in      Voice        MCP server   Partner        Buttons and
  the Telegram     assistant    (external    REST API       screens in
  bot              (Mini App)   AI clients)                 the Mini App
```

Add one capability and it **appears at once on every AI surface**. The agent has
no private set of "agent functions": it calls exactly the same audited operations
a button in the interface calls. Two consequences follow:

- **the AI cannot do anything the interface cannot** — there is no separate,
  less scrutinised path around the business rules;
- **every registered capability works on all AI surfaces at once** — it does not
  have to be written three times, for chat, for voice and for MCP.

**An important boundary, so we do not promise more than exists.** The registry
does not yet cover 100% of the interface: today it holds 65 capabilities. Where a
function has no capability yet, the agent neither invents one nor refuses — it
looks the function up in a navigation manifest and **walks the human to the right
screen**. A dedicated CI gate prevents a section from shipping that the agent can
neither perform nor navigate to. Extending the registry towards full coverage is
continuous work, and it is precisely what makes the voice orchestrator
progressively more self-sufficient
([04-voice-orchestrator.md](04-voice-orchestrator.md)).

### The rule that is never broken: the AI proposes, the human confirms

Every irreversible operation — signing, submitting, accepting an incoming
document, making a payment — passes through a **human-in-the-loop gate**: a
confirmation card shown to the owner. The AI prepares, calculates, fills in and
explains, but **does not sign on its own**. The owner's tap is the border between
"proposed" and "done", and that border lives in the code, not in a policy
document.

This is not caution for caution's sake. A wrong IKPU code on an e-invoice is a
penalty under Article 223 of the Tax Code of Uzbekistan. So:

- a product name attached to an IKPU code is **always** taken from the state
  Tasnif catalogue, never composed by the model;
- the marketplace assistant does not name products, it **selects an id** from a
  list our code has read — an invented price has physically nowhere to land;
- Business Pulse looks for anomalies using **deterministic rules**, without AI:
  wrongly accusing a bookkeeper costs more than missing a finding.

---

## 1.6. The Technology Foundation

| Layer | Technology |
|---|---|
| Language / runtime | Python 3.12, asyncio |
| Telegram | aiogram 3.27 (long polling, two independent bots) |
| HTTP / WebSocket | aiohttp 3.11 |
| Database | PostgreSQL 16 (asyncpg), 194 tables, Alembic head 236 (232 revision files — the numbering has gaps) |
| Containers | 16 services under Docker Compose |
| Cache, queues, FSM, rate limits | Redis 7 |
| Frontend | React + TypeScript, Vite (rolldown), TanStack Router, Zustand, Tailwind |
| Documents | Jinja2 → WeasyPrint (PDF), DOCX/XLSX templates, a LibreOffice sidecar for conversion |
| Encryption | Fernet (cryptography) with key rotation, a sealed box for the signature-key vault |
| LLM | Grok (xAI) — agent, lawyer, parsers, moderation; Anthropic Claude — AI Studio |
| Speech | Groq Whisper (ru) and Gemini (uz) for recognition; xAI Grok Voice Realtime for live conversation |
| SMS | Eskiz.uz |
| Infrastructure | Docker Compose, 16 services, nginx + Let's Encrypt, Hetzner |
| Observability | Sentry, Prometheus, Alertmanager → Telegram, Grafana, cAdvisor, blackbox probes |
| CI/CD | Self-hosted GitHub Actions, 6 runners in rotation (2 in production + 4 on the development machine), automatic rollback on a failed deployment |

### Engineering principles you can see in the code

- **A circuit breaker on every external API.** Verified file by file: Didox,
  Bank24, Tasnif, Grok, Groq STT, E-IMZO, Soliq, MoySklad and 1C each have their
  own breaker (the 1C breaker is keyed by the client's database address, so one
  client's outage does not affect the others). A provider's failure does not take
  the system down with it.
- **Idempotent mutations.** Document signing always carries an idempotency key
  plus a reconciliation pass after a timeout: if the network drops, a retry
  cannot produce a second signature.
- **Kill switches on risky and optional features.** 108 feature flags, some
  stored in the database so that an emergency shutdown survives the loss of
  Redis: such a feature can be killed in a second without a deployment. Core
  paths — authentication, document creation — are deliberately not gated: a
  switch belongs where there is something to switch off, not everywhere.
- **Durable state, with a precise boundary.** In PostgreSQL, and therefore
  surviving anything: drafts, signing jobs, document plans, the operations
  ledger, the notification queue. In Redis, and therefore living exactly as long
  as Redis does: wizard FSM steps, locks, caches, some flags. We call only the
  first group durable.
- **A rescue path on every failure path.** Didox goes down mid-wizard — the
  document is not lost, it lands in "Unfinished", and when Didox comes back the
  system writes to the client on its own.

---

## 1.7. Security and Trust

The security of client data is not a closing section of a document; it is the
condition on which the product exists at all. Businesses trust us with passwords
to government systems, with digital signature keys, with bank statements, with
their employees' personal data and with the commercial secret of their purchase
prices. One incident is enough for nobody to extend that trust again.

That is why security has a document of its own here, rather than a line in a
table:

> **[05-security.md](05-security.md) — how we protect a business's data.**
> What is encrypted and with what, where the data physically sits, what exactly
> goes to the AI and what happens to it afterwards (zero-retention mode), how the
> signature-key vault is built, where the boundaries of access run, what we do
> daily so that the protection does not go stale, and which questions remain
> open.

---

## 1.8. Two Languages

Russian and Uzbek carry equal weight wherever the product meets a client or the
law: 2,484 interface strings in each language, both languages in the bot and the
Mini App, on the UmagShop storefronts, in printed PDFs and in the wording of
legal documents. Uzbek appears in Latin script in the interface and in Cyrillic
inside the body of legal documents, as Uzbek judicial and business practice
requires.

**Where parity does not yet exist — stated plainly:** live voice conversation
currently works in Russian. Uzbek speech requires a second recognition provider,
and the seam for it is already in place in the architecture — this is the
[next step](03-roadmap.md), not a property of today. Voice *messages* in the bot
are already transcribed in both languages.

---

## 1.9. Where We Stand: Scale and Maturity

An honest picture requires three different numbers, and they must not be mixed
up.

**What has been built** — the size of the platform:

252 business-logic modules, 103 Telegram routers, 126 Mini App screens, Alembic
head 236, ~562,000 lines of Python and ~262,000 lines of TypeScript, ~439,000
lines of tests. This is the surface area a team of 40–60 engineers would usually
build in a couple of years.

**What has passed through the system** — cumulative throughput to date:

73,057 documents, 85,869 deals (of which **62,802 are closed — 73%**), 96,217
incoming documents, 70,094 bank transactions, 25 active signature keys. Some of
these rows mirror what the business was doing in Didox anyway; they cannot be
credited wholesale as value we created.

**What is actually being used right now** — over the last 30 days:

| Metric | Value |
|---|---|
| Organisations in total | 80 |
| Organisations that created documents | 57 |
| Users who signed in (30 days / 7 days) | 76 / 19 |
| Documents created | 4,044 |
| AI agent actions | 313 (across 9 organisations) |

**The conclusion that follows.** The product is technically mature and
functionally broad, but the audience is early and depth of use is uneven:
documents flow steadily, while the AI agent is used by one organisation in nine.
The constraint today is not how fast we can build new modules — it is
**turning what is already built into regular use**. That feeds directly into the
priorities in the [roadmap](03-roadmap.md).

---

**Next:** [2. Modules and features](02-modules.md) — a detailed walk through
every part of the product.
