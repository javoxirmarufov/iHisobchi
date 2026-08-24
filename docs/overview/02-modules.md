# 2. Modules and Features

> Part 2 of 9. Back: [ecosystem](01-ecosystem.md). Next: [roadmap](03-roadmap.md) · [voice orchestrator](04-voice-orchestrator.md) · [security](05-security.md) · [first day](06-first-day.md) · [signing](07-signing.md) · [with us and without us](08-with-and-without.md) · [business model](09-business-model.md).
>
> Statuses: ✅ in production · 🟡 rolling out to clients · 🔵 in progress · 🎯 next step

## Map of Sections

| | Module | What it covers |
|---|---|---|
| **A** | [Document flow and digital signature](#a-document-flow-and-digital-signature) | The core: 24 Didox document types, signing, incoming mail, templates |
| **B** | [Deals](#b-deals--the-open-cycle-engine) | Contract → payment → power of attorney → e-invoice → act → closure |
| **C** | [Business Pulse](#c-business-pulse--an-x-ray-for-the-owner) | The owner sees the truth about their own company |
| **D** | [AI Lawyer](#d-ai-lawyer) | Claims, lawsuits, contracts, corporate paperwork |
| **E** | [Banking and payments](#e-banking-and-payments) | Money: statements, reconciliation, cash flow, reports |
| **F** | [Tax office — Soliq](#f-tax-office--soliq) | Letters from the tax committee, fiscal cash register, receipts |
| **G** | [Inventory, products, IKPU](#g-inventory-products-ikpu) | Catalogue, stock levels, stocktaking, Tasnif codes |
| **H** | [Counterparties](#h-counterparties) | Records, tax-committee checks, tracking of renamed companies |
| **I** | [UmagShop](#i-umagshop--a-marketplace-with-documents) | A B2B marketplace where an order turns into a deal |
| **J** | [QR-Hisob and Deal Link](#j-qr-hisob-and-deal-link) | Selling without a website: a QR code on the counter, a link in a messenger |
| **K** | [Nasiya](#k-nasiya--instalment-sales) | Accounting for instalment sales |
| **L** | [People — HR](#l-people--hr) | Hiring, orders, staffing tables, ENST filings |
| **M** | [Integrations](#m-integrations) | 1C, MoySklad, AmoCRM, Bitrix24, cash registers, e-mail |
| **N** | [AI surfaces](#n-ai-surfaces) | Assistant, voice, AI Studio, recognition |
| **O** | [Reports and analytics](#o-reports-and-analytics) | Sales, purchases, VAT, forecasting |
| **P** | [Automatic documents](#p-automatic-documents) | Documents that create themselves |
| **Q** | [Multi-business, roles, notifications](#q-multi-business-roles-notifications-audit) | Several companies, a team, events |
| **R** | [Partner channels](#r-partner-channels) | MCP, Partner API, browser extension |
| **S** | [iSMM](#s-ismm--sales-and-promotion-on-social-media) | Social media, advertising and checkout: an ad → a contract → an invoice → a payment |

---

## A. Document Flow and Digital Signature

**The core of the product.** 73,098 documents have passed through it.

### A.1. Document types ✅

Full coverage of Uzbekistan's state e-document system. The platform reads and
displays **24 Didox document codes**; **19 of them have a creation wizard of
their own**. In the table below, related codes are grouped into a single row
(006 and 062, for example, are two generations of the power of attorney):

| Code | Document | Where it is created |
|---|---|---|
| **002** | E-invoice (ESF) | Bot, Mini App, voice, API, from a contract, from an order |
| **008 / 031** | Pharma e-invoice (batch series, regulated mark-up) | Bot, Mini App |
| **021** | E-invoice (corrected / supplementary) | Incoming-mail intake |
| **023** | Hybrid e-invoice | Bot, Mini App |
| **041** | Waybill (consignment note) | Bot, Mini App, auto-generated from an e-invoice |
| **004** | Legacy waybill | Historical documents, read-only |
| **005** | Certificate of completed work | Bot, Mini App, auto-generated from an e-invoice |
| **006 / 062** | Power of attorney | Bot, Mini App, auto-generated from a deal |
| **007** | Contract on the NK template (Didox standard form) | Bot, Mini App |
| **009 / 052** | Reconciliation statement | Bot, Mini App |
| **010 / 070** | Multilateral document | Bot, Mini App |
| **013** | NK letter | Bot, Mini App, "Debt letter" |
| **014** | NK act | Incoming-mail intake |
| **054** | Handover act | Bot, Mini App |
| **075** | Minutes of a general meeting of founders | Bot, Mini App |
| **000** | Free-form document, public offer, a ready contract uploaded as a file | Bot, Mini App |

Plus our own (non-Didox) visual documents: **Contract** and **Commercial
proposal** — rendered to PDF from a template, then signed or sent as a file.

### A.2. Eight ways to create a document ✅

One document, eight ways to be born. This is what "orchestrator" means in
practice: the client picks whichever path suits them, and the result is the
same.

1. **The Mini App wizard** — a step-by-step form with hints, product lookup
   against stock, and counterparty autofill.
2. **The Telegram bot wizard** — the same flow on buttons, working on any phone
   and on a weak connection.
3. **By voice** — "create an invoice for Artel, five laptops at five million
   each" → a finished draft.
4. **Smart Paste** — copy a list of goods from anywhere, paste it in, and the
   system recognises the line items, quantities, prices and even the buyer.
5. **From a photo** — snap a delivery note or a price list and the line items
   are extracted.
6. **From another document** — an e-invoice from a contract, an act from an
   e-invoice, a waybill from an e-invoice, an invoice from a shop order.
7. **Automatically** — from a power of attorney, from a signed contract, from a
   storefront order (see [Automatic documents](#p-automatic-documents)).
8. **Through an API or an AI client** — the Partner API, the MCP server.

### A.3. Digital signature — four modes ✅

The market's central pain point: E-IMZO only works from a computer with the USB
key physically plugged in. We closed that four different ways:

| Mode | How it works | Who it is for |
|---|---|---|
| **E-IMZO Agent** | A Windows application on the client's computer holds the key; the bot sends a job over a secured WebSocket; the agent signs and returns the result | A company with an office PC |
| **Web signing** | Signing straight from the browser through the E-IMZO plug-in | People who work from a laptop |
| **24/7 signing server (managed)** | The client's key lives in an isolated environment on our side, encrypted in a sealed box; signing is available round the clock with no computer switched on | Anyone who needs automation without being present |
| **Demo mode** | The full journey without a real signature | Getting to know the product |

> **Signing has a document of its own** — [07-signing.md](07-signing.md): each
> of the four modes in detail, self-hosted installation in a single command, how
> the turnkey vault cell is built, and a direct answer to the question "could it
> sign something without me?"

**Multi-TIN support for outsourcers** ✅ — one signing agent serves several
organisations: an accounting firm holding a hundred client keys registers
another company's TIN by proving key ownership with a signed challenge.

**Signing reliability.** Every signing call carries an idempotency key; if the
network drops, the system does not blindly retry — it **verifies the document's
actual state** in Didox. That closes the classic scenario where the first POST
succeeded, the response never arrived, the user pressed the button again, and
the document ended up signed twice.

**A durable operations ledger** ✅ — a signature initiated in the Mini App
becomes a record in an operations journal with a background worker: restarting
the service mid-signature does not lose the operation.

### A.4. Incoming documents ✅

- A mirror of everything incoming from Didox — **96,217 documents** in
  production.
- Accept or reject in one tap, with a role check (who are we in this document?).
- **Bulk acceptance** — accept a batch of incoming documents in a single action.
- PDF preview without downloading.
- **Duplicate e-invoice detector** — if a supplier issues the same document
  twice, the system spots it from a canonical hash of the line items.
- **One-tap acceptance for a whitelist** ✅ — for regular suppliers the system
  recognises the document itself and sends a ready card with a preview: one
  button per document, one for the whole batch. **Silent auto-acceptance does
  not exist and will not be added** — this is a direct product requirement:
  accepting an incoming e-invoice has tax consequences, and the decision stays
  with a human.
- **The "Open documents" section** ✅ — incoming powers of attorney awaiting an
  e-invoice from us. Until we issue that invoice, the row stays on the list and
  keeps reminding.

### A.5. Drafts and rescued work ✅

There are two kinds of drafts, and the distinction matters:

- **Didox drafts** — the document already exists on the portal but is not
  signed. Editable, re-signable, deletable, printable to PDF.
- **"Unfinished"** (local drafts) — our own copy of a half-made document.
  Auto-saved at every step of the wizard.

**A rescue path on every failure path.** Didox is unavailable, the network drops,
the session expires — the wizard does not throw away what was typed. The data
lands in a local draft together with a classification of why it failed, and a
background worker **writes to the user itself** once Didox is working again,
returning them to the exact step of the wizard where they stopped.

Plus **cleaners**: abandoned unsigned Didox drafts are removed so that clutter
does not pile up in the client's portal account.

### A.6. Document templates ✅

Four levels, from "take something ready-made" to "my own letterhead, exactly":

1. **A public library** — ready-made contracts available to every user.
2. **Visual templates** — designed PDF layouts for contracts and commercial
   proposals, with versions, preview, a recycle bin and rollback.
3. **Your own DOCX/XLSX templates, 1:1** — the client uploads their file, the AI
   marks up the fields, and from then on the document prints on exactly their
   form.
4. **Didox templates (type 007)** — management of NK contract templates with
   categories.

Separately: a **letterhead** — one house header for business documents across
the whole product — and the **template wizard v2** ✅ with a field checklist and
manual mark-up correction from within the chat.

### A.7. Numbering, register, search ✅

- **Per-TIN numbering with series** — prefix, suffix, padding, a separate series
  for each document type. The number is reserved against a document plan so that
  two wizards running in parallel cannot burn the same one.
- **A single register** — every document (outgoing, incoming, draft) in one list
  with filters.
- **Full-text search** by number, counterparty, amount and content.
- **Export** to Excel, PDF download, and delivery of the signed document
  **straight into a Telegram private chat as a file** ✅.
- **Reconciliation with Didox** — a background reconciler plus a "Refresh sync"
  button, so the local picture cannot drift away from the portal.

### A.8. Getting in: from zero to the first document ✅

A piece of work that is rarely noticed and yet decides whether the client stays.
The full journey step by step, including the places where people drop out, is in
[06-first-day.md](06-first-day.md).

- **Sign-up in minutes**: phone → SMS code → Didox TIN and password → **all
  company details are pulled from the state register automatically**. No
  twenty-field questionnaires.
- **Didox registration from inside the bot** ✅ — anyone without an e-document
  account creates one without leaving iHisobchi (self-service registration
  through the Didox API), instead of going off to the portal separately. An
  assisted option is available too.
- **Demo mode** ✅ — you can walk the whole path of creating and "signing" a
  document on safe, fictional data, before registering and before connecting a
  signature key. People first see how it works, and only then hand over their
  passwords.
- **Reminders about the signature key** — if a business is set up but no key was
  ever connected, the system comes back to it tactfully instead of abandoning
  the client halfway.
- **A consent screen** and language choice — before the first byte of personal
  data is processed.

### A.9. Official mass-mailing of commercial proposals ✅

**A feature with no equivalent on the market.** With an e-document operator you
can send an arbitrary document — one at a time, by hand, to each recipient
separately. Sending a commercial proposal **to many recipients at once** is not
possible anywhere.

**What it gives you.** A supplier has a discounted batch of goods left over
until the end of the month and 300 counterparties in their database. Phoning
them all is several days of a sales manager's time. Messaging them is not
serious enough for a wholesale deal. Mailing them by e-mail is spam with no
legal standing. Here it is **one action**, and the proposal arrives as an
official document in the recipient's own e-document workspace.

| How it works | |
|---|---|
| **Recipient list** | Pasted into the chat as text, or uploaded as a file: `.txt`, `.csv`, `.tsv`, `.xlsx`, `.docx`, `.pdf`. The system finds the TINs (9 digits) and PINFLs (14 digits) itself and removes duplicates; a messy list is parsed by the AI |
| **Identification** | Every TIN is checked against the state register — the owner sees a list of **companies**, not a column of digits, and can strike out the ones that do not belong |
| **Sending** | A separate document is created for each recipient, signed with your digital signature and delivered through the e-document system |
| **Scale** | Up to **20,000** recipients per campaign |
| **Progress** | A single message updates as it goes: sent / delivered / rejected |
| **Reliability** | Each recipient's state is stored: a campaign survives a restart and **never sends duplicates** |
| **Pace** | Deliberately throttled — so as not to overload the e-document system or look like spam |
| **Safeguard** | One active campaign per organisation |

Signing runs sequentially, TIN by TIN: the signature channel is physically
singular, and trying to parallelise it would produce race conditions rather than
speed.

**There are as many uses as there are reasons to address the market:** clear
remaining stock, announce a new price list, offer a service, look for a
contractor, invite firms to a tender, notify counterparties of changed terms. A
detailed breakdown and comparison with the market is in
[08-with-and-without.md §8.6](08-with-and-without.md#86-mass-mailing-of-commercial-proposals--what-nobody-else-has).

---

## B. Deals — the Open-Cycle Engine

> ✅ In production · **85,869 deals** in the system

**This is what bookkeepers will love the product for.** The module answers a
question that ordinary accounting can only settle by reconciling three systems
by hand: **which deals are not closed, and whose move is it?**

### B.1. How it works

The system assembles the chain out of your own documents and money:

```
Contract → Payment → Power of attorney → E-invoice → Act / Waybill → Closed
```

The engine analyses everything the business has — outgoing and incoming Didox
documents, the bank statement, cash-register receipts, shop orders — and
**links them into deals on its own**. A contract for amount X dated a given day
looks for a payment of the same amount from the same TIN; a power of attorney
looks for its invoice; a waybill looks for its delivery.

Matching runs in **tiers** — from an exact match on the reference details to
probabilistic scoring; ambiguous cases are ranked by the AI, but the link is
confirmed by a human with a single tap.

### B.2. States and "whose move"

Every deal carries a computed state and a **next action**:

| State | What the owner sees |
|---|---|
| `contract_pending` | The partner has not signed the contract |
| `awaiting_payment` | Contract signed, no payment |
| `payment_partial` | Partial payment received |
| `awaiting_poa` | Payment received, no power of attorney |
| `poa_to_accept` | A power of attorney has arrived — accept it |
| `poa_received` | Time to issue the e-invoice |
| `invoice_pending` | Invoice sent, the partner has not signed it |
| `contract_to_sign` | An incoming contract is waiting for your signature |
| `poa_needed` | You signed the contract — time to send a power of attorney |
| `invoice_to_accept` | An incoming invoice is waiting for your signature |

The feed is split into **"Needs you"** and "Waiting on the partner" — and that
split lives in the state machine rather than in the interface, so a card can
never disagree with the logic behind it.

### B.3. What you can do straight from a deal card ✅

- **Sign an incoming contract** — without leaving the card.
- **Accept a power of attorney**, and from it immediately **issue an e-invoice**
  with the line items pre-filled.
- **Create a power of attorney from a contract** — one button.
- **Issue an invoice from a contract**, with line items and amounts filled in
  automatically.
- **Generate a waybill** once the invoice exists.
- **Remind the partner** — a push, a link, a letter.
- **Draft a "debt letter"** ✅ — a legally formed demand for payment (Didox type
  013) carrying the date and number of the contract, the amount and a reference
  to the relevant clauses. From here there is a direct bridge to the
  [AI Lawyer](#d-ai-lawyer) for escalation.
- **Re-check a deal** — a deep reconciliation of a single deal directly against
  Didox, when you need a guarantee that the picture is right.
- **Close it manually** — with the reason recorded.

### B.4. Why it matters

Every month the bookkeeper reconciles by hand: what was shipped, what was paid,
where the act is missing, where a power of attorney is still hanging. It eats
days and still produces errors. Here the engine does it continuously, and shows
**a list of a dozen rows that "need you", rather than a thousand rows of
"everything open"**.

---

## C. Business Pulse — an X-Ray for the Owner

> ✅ In production

**A module for people who own a business rather than run it.** The founder
presses one button, the AI scans the entire system and produces a readable
report without a single accounting term in it.

### C.1. Why it is needed

An owner sees the business through the bookkeeper's report. That report is
written so that it cannot be understood without training — tables, terminology,
references to legal articles. Problems are invisible inside it: a multi-million
error, a transaction quietly tidied away, a shortfall, a shipment that was never
paid for — all of it drowns in the wording. The owner learns the truth at the end
of the year, when the dividends come in lower than expected. By then it is too
late to investigate, and often there is nothing left to save.

The owner of several companies has neither the time nor the capacity to
re-check every payment, every document, every shipment. **Business Pulse does it
for them.**

### C.2. What it scans

One press, and the whole picture of the business:

- **Money.** How much came in, how much went out and where to, the "cash
  runway" (how many days it lasts at the current burn), net cash flow.
- **Sales.** What was sold, to whom, at what price, and the trend.
- **Deals.** What is closed, what is hanging, where goods went out and money did
  not come back.
- **Receivables.** Who owes how much, and how long they have been late.
- **Documents.** Whether every mandatory document exists behind the movement of
  money.
- **Inventory.** What is left, what moves fastest, where the count is zero.
- **Payroll and taxes.** Payment discipline and the payroll share of turnover —
  against industry norms rather than a universal number.

### C.3. "Needs attention" — the oddity detector

A separate block, and the reason the module was built. **The rules are
deterministic, with no AI involved** — falsely accusing a bookkeeper costs more
than missing a finding — and the tone throughout is "check this", not
"violation".

| What it catches | A real-world example |
|---|---|
| **Duplicate payment** | The same TIN, the same amount, twice within a few days. The operator pressed "send" twice — that is money you can get back |
| **A run of round numbers** | Several transfers of exactly one million to the same counterparty within a fortnight. Round figures rarely coincide with a real invoice line |
| **A large transfer to an individual with no stated purpose** | A large sum to a PINFL with an empty or meaningless payment reference. For a bank and for the tax committee this is a first-category red flag |
| **Possible structuring** | Many payments just below a threshold to one recipient within a week, adding up to a large transaction — this looks like an attempt to stay under a limit or to avoid documenting a deal |
| **Turnover without documents** | Money moved, no e-invoice exists. With a grace period, so that a fresh advance payment is not accused unfairly |

The Uzbek tax authority already screens businesses automatically against 59 risk
criteria. **Showing the owner those same flags before the tax committee sees
them is pure value.**

### C.4. How results are delivered

- **A mini-presentation** — an A4 PDF/PNG page of readable blocks that can be
  forwarded to a partner or shown in a meeting.
- **A full check-up** — an extended breakdown: a table of indicators against
  industry norms, "what changed since last time", non-core income, payroll and
  tax discipline.
- **An AI narrative** — a short, human explanation of the numbers. The model
  receives **only the figures we calculated ourselves** and has no way of
  inventing its own.
- **A weekly digest** in Telegram plus live event alerts (opt-in, switchable off,
  with quiet hours).

### C.5. An example

> The owner presses "Scan". A minute later:
> "In August, 340 million came in and 410 million went out. Cash runway: 22 days.
> Sales were 290 million, of which 96 million is still unpaid; 41 million is more
> than a month overdue — the largest debtor is X LLC, 28 million since 3 July.
> **Needs attention (3):** a duplicate payment of 12 million to TIN 3097… on
> 8 and 10 August; four transfers of 9.5 million to the same recipient within a
> week; 54 million of turnover with no e-invoices, older than 30 days."

Three lines that make opening the app worthwhile.

---

### C.6. Where this is heading: the same picture, facing outwards 🎯

Business Pulse looks inwards — it shows the owner the truth about their company.
The very same data can answer an outward-facing question: **what can you show a
bank, an investor or a large buyer to prove the business is dependable?**

Hence a **business-activity certificate**: how many deals were completed and for
what total, what share closed in full, how many days a payment takes on average.
Not a rating and not a solvency score — verified facts, each backed by a document
carrying a digital signature inside a state system.

It is issued **only by the owner's own decision**, every issue can be revoked,
and the certificate states honestly what share of the company's turnover we can
actually see. In detail:
[09-business-model.md §9.9](09-business-model.md#99-stream-7-the-business-activity-certificate--issued-only-by-the-business-itself).

---

## D. AI Lawyer

> ✅ In production

**A lawyer on staff is expensive; a lawyer on call arrives late.** This module
covers 80% of a small business's legal needs from inside the system.

### D.1. What it can do

**Free-form dialogue.** The user describes the situation, the AI asks for the
missing details and produces a finished document in HTML/PDF that can be edited,
downloaded and printed.

**Document types:**

| Category | Documents |
|---|---|
| **Pre-trial claims** | Formal claim, debt letter, response to a claim |
| **Litigation** | Statement of claim to the economic court, application for a court order, response to a statement of claim, debt-rescheduling agreement |
| **Contracts** | Supply, lease, services, works, promissory note, power of attorney |
| **Correspondence** | Letters, applications, acts |
| **Corporate** | 🔵 articles of association, sole-member resolution, minutes — through a separate structured process |

### D.2. The key scenario: an unpaid delivery

This is why the module is wired to [Deals](#b-deals--the-open-cycle-engine):

1. The system observes that the contract is signed, the act is completed and the
   goods have shipped — **but no payment arrived**.
2. It notifies the owner.
3. From that notification, straight into the AI Lawyer.
4. The lawyer **pulls the facts out of your own database**: the contract number
   and date, its payment clauses, the act's number and date, the amount, how
   long the payment is overdue, the parties' details.
5. It drafts a pre-trial claim citing the specific contract clauses, with the
   principal and late-payment interest calculated, and a warning that the matter
   will go to court.
6. The document can be sent to the counterparty electronically, without leaving
   the system.

If the payment still does not arrive, the same loop prepares a **statement of
claim** or an **application for a court order** with the amount already
calculated.

### D.3. The legal basis — statutes, not inventions

- **A reference base of Uzbek law** in the database, with verification of the
  citations the model writes: if the AI cites an article that does not exist, the
  citation does not pass.
- **Currency.** The corpus is topped up from official sources (lex.uz); the
  official Uzbek text is authoritative, with Russian as a convenience
  translation. A new decree enters the corpus and is used in practice.
- **Clickable links to the statutes** directly inside the bot's message.
- **A deterministic calculator** for the monetary claim: penalties, interest and
  deadlines are computed by code, not by a language model.

### D.4. The context of your business ✅

With context enabled, the lawyer sees **your** company's documents,
counterparties and deals — so it does not ask what it already knows and does not
get the reference details wrong. The feature has a switch of its own: it can be
turned off while leaving the chat, the statute reference base and attachments
working.

**Attachments** ✅ — you can upload someone else's contract or demand letter: the
system extracts the text and works with it.

### D.5. A company's operational paperwork

A separate, sizeable class of tasks that eats an owner's time:

- changing the company's name, registration details or address;
- admitting a new founder with an investment;
- changing ownership shares, increasing the charter capital;
- adopting a new version of the articles of association.

Each is a package of documents assembled by hand today. The **corporate changes**
module 🔵 (built, behind a disabled flag) does it safely: it first records the
owner-confirmed list of participants, their shares and the intent, binds the
application to a profile version and a rules version (Law ZRU-1137 of
21 April 2026), and only then prepares the documents. Free-form AI generation of
articles of association and meeting minutes is **deliberately forbidden** — the
cost of an error in a founding document is out of all proportion to the
convenience.

---

## E. Banking and Payments

> ✅ In production · **69,993 transactions** parsed

### E.1. Why a bank belongs inside an accounting system

The bank is not "one more integration" — it is the **source of truth about
money**. Without it neither Deals nor Business Pulse nor tax reconciliation can
work: the system cannot say "the payment arrived" if it cannot see the
statement.

It is also the most frequently asked question of the working day. The salesperson
rings the bookkeeper every half hour: "has the money come in?" The forwarder is
waiting to ship. Here the answer arrives **on its own, as a Telegram push**,
attached to the specific contract and invoice.

### E.2. What is built ✅

| Feature | Description |
|---|---|
| **Direct bank connection** | A Bank24.uz client: live balance and account statement, with a separate session per organisation |
| **Incoming-payment monitoring** | A Telegram push on every credit: amount, sender, reference, and the deal it belongs to |
| **Statement import from a file** | CSV, XLSX, HTML, PDF, DOCX and the 1C format — parsed in a minimum-privilege sandbox, deduplicated, matched to deals automatically |
| **A single money ledger** | One place every part of the system asks "has this been paid?". Sources: the bank, the fiscal cash register, MoySklad, shop orders |
| **Payment-to-deal scoring** | One matching core with confidence thresholds; disputed cases are confirmed by a human |
| **Payment-vs-document reconciliation** | A cross-check in both directions: money without documents, and documents without money |
| **Cash-movement report** | Income and spending by category, with a learned dictionary of payment references |
| **"Analyses" — cash flow** | A statement in, a finished Excel register out, allocated across business units, using an "account → unit" dictionary the system copies from the client's own working file |
| **Statement reports** ✅ | A long-running pipeline: upload → classification → human review → rules → version freeze → XLSX on a standard template or the client's own |
| **Data coverage** | An honest answer to "what period do we actually have money data for" — so that no conclusion is built on top of a gap |

### E.3. On open banking

Presidential decree **PP-359 of 27 November 2025** mandates the launch of an
"open banking" system **by 1 September 2026**. That changes the market: today no
bank in the country offers a public banking API, and access to an account is
only possible through a bank client.

What we have working today is a direct connection to Bank24 plus statement
import from any format — that is enough for now. An abstraction layer over
multiple banking providers has not been written yet: it is designed in our own
market study and sits in the work queue for the moment a second source appears.
In detail:
[the roadmap](03-roadmap.md#36-horizon-v--money-and-open-banking).

---

## F. Tax Office — Soliq

> ✅ In production · early audience (6 connected organisations)

The module closes two large pain points at once: **letters from the tax office**
and **fiscal cash-register receipts**.

### F.1. The tax office mailbox ✅

Today a business is obliged to log into its `my.soliq.uz` account regularly with
a digital signature and check whether a notice has arrived. Miss it, and you miss
the deadline to reply. Anyone with three companies logs in three times, with
three keys.

What the module does:

- **Checks the mailbox for you** — an hourly lightweight probe of the message
  counter (only within a working window of 08:00–21:00 Tashkent time), with a
  full sweep only once the counter has moved. Freshness of about an hour instead
  of a day, at a lower load on the portal than before.
- **Sends a Telegram notification** — a new letter from the tax committee arrives
  where the owner already is.
- **Reminds you of the deadline** — a letter requiring a reply nags before the
  due date, not after it.
- **Legally correct opening.** Until the owner explicitly confirms, the letter is
  shown as metadata only, with the contents sealed. Opening it issues exactly one
  "mark as read" call on the tax committee's side and verifies the result. This
  is not a technical nicety: the read receipt starts legal deadlines running, and
  the system has no right to set it by accident.
- **An AI explanation of the letter** ✅ — what is being asked of you, by when,
  and what happens if you do not reply. Only on an explicit request.
- **A draft reply** ✅ — a prepared document, but never automatic submission to a
  government body.
- **Secure storage** — subject, body, number and file names are encrypted and
  never reach the logs or the monitoring stack. Deduplication runs through
  cryptographic blind indexes.

**For an owner of several companies this changes the working regime.** Three
organisations, one notification feed, one tap to switch between companies, and a
reaction to an official letter on the same day instead of whenever they get
round to logging in.

### F.2. Fiscal cash registers and receipts ✅

- **Cash-register synchronisation** — terminals (points of sale) and fiscal
  receipts are pulled from the Soliq account. In production: **394 receipts**
  across pilot clients.
- **Automatic sync** ✅ — a background schedule with leasing and race protection;
  manual refresh over a chosen period.
- **Sales and refunds kept apart** — a refund is not counted as revenue (a
  separate attribute on the receipt; an error here distorts the whole set of
  reports).
- **History for earlier months** — back-filling periods the rolling window does
  not reach.
- **An evening till summary** — how much was rung up during the day, with a
  personal opt-out.
- **Receipt-to-Didox reconciliation** — what went through the till against what
  was issued as documents.
- **Card acquiring** — reconciling card revenue at the till against what the
  acquirer actually transferred.
- **An anomaly detector** — rules layered over locally cached receipts.
- **Receipts into the books** — fiscal receipts are projected into the shared
  money ledger and take part in deals and in Business Pulse.

### F.3. The Till-to-Books Bridge (Retail Bridge) 🟡

A separate loop for retail: cash-register receipts are gathered into a **daily
retail sales document** and published into the client's accounting system (1C).

The module's governing principle: **we do not ask the bookkeeper about their
accounting policy — we copy it out of their own database.** On connection the
system reads the client's most recent "Retail sales report" and offers: "We found
your document No. 0000-000156 dated 26 December — shall we take the settings from
there?" The bookkeeper presses "yes" and never answers a single question about
ledger accounts.

A side effect: the module works identically with a Russian 1C configuration, an
Uzbek one and a bespoke one, because no account number is hard-coded anywhere.

Cash-register adapters are pluggable: fiscal receipts from the Soliq account, the
yestask till, and whatever comes next — **without any code from us**.

---

## G. Inventory, Products, IKPU

> ✅ In production · **5,697 product records** in client catalogues

| Feature | Description |
|---|---|
| **Product catalogue** | A record with price, unit of measure, VAT, IKPU code, photo and barcode |
| **Warehouses** | Several warehouses per organisation, with archiving |
| **Movements** | Manual receipt, issue and transfer operations |
| **Documents affecting stock** | An accepted incoming invoice changes stock levels automatically — reliably, and guarded against being applied twice |
| **Stocktaking** | A recount session with barcode scanning straight from the phone |
| **Barcode lookup** | EAN-8 / EAN-13 |
| **Product photos** | Upload, automatic WebP derivatives, storage |
| **"Running low" alerts** | A push when an item approaches zero |
| **Price-list import** | Excel/CSV, and also from a photograph of a price list |

### Where this is heading: our own smart warehouse 🎯

Today the warehouse in the system is a **ledger**: it knows what the client has
and how much of it, but the goods sit on the client's premises.

The next step is **our own AI-run warehouse**, where a business can physically
place its stock. We take the delivery in, unpack it, reconcile it against the
documents, sort it, create product records with photographs, descriptions and
IKPU codes, label it — and from then on ship against orders anywhere in
Uzbekistan, targeting same-day delivery.

The crucial part: **you can sell anywhere**, not only through UmagShop — the
goods sit with us, and the client chooses the sales channel. A separate branch is
taking goods in **straight after customs clearance**, together with the
[broker loop](03-roadmap.md#3112--customs-and-brokers).

In detail:
[roadmap §3.11](03-roadmap.md#311-horizon-x--the-physical-loop-warehouse-customs-delivery).

### IKPU — Tasnif codes ✅

A topic of its own, because a mistake here costs money. Every product on an
e-invoice must carry a code from the state IKPU classifier; the wrong code means
a penalty under **Article 223 of the Tax Code of Uzbekistan**.

- **A five-phase code-matching pipeline**: catalogue search, matching,
  verification, substitution of the canonical name, per-business caching.
- **An iron rule: the category name always comes from Tasnif, never from the
  AI.** Every code passes through a forced substitution of the official name
  before it is sent to Didox.
- **IKPU search** is available to the user manually — inside the wizard and on a
  screen of its own.
- **An IKPU suggestion queue** ✅ — a background pipeline works through the
  catalogue and proposes codes in batches; **5,067 suggestions are already in
  production**, waiting for human confirmation. Auto-application is gated behind
  a separate flag, on the principle "the AI proposes, a human publishes".
- **Product marking (KIZ / DataMatrix)** — storage of the marking codes
  received.
- **Tax relief checks** 🔵 — contextual checking of applicable tax reliefs inside
  the invoice flows.

---

## H. Counterparties

> ✅ In production

- **A counterparty record**: registration details, bank, document history,
  turnover, favourites.
- **TIN/PINFL verification through the tax committee** — pulling the official
  company record, including via a donor token for clients who do not yet have
  their own access.
- **My clients** — the recipient list synchronised from Didox history.
- **Tracking of renamed organisations** ✅ — if a counterparty changes its name,
  the system notices it from the register and **propagates the new name through
  the books itself**, keyed on the TIN rather than an internal identifier. The
  old names stay searchable so that historical documents can still be found.
- **Reconciliation of details against the register** ✅ — account, bank code,
  address, director. A discrepancy is shown as evidence (what changed, and when)
  rather than as a flag; for the account number and bank code the system
  **reports** rather than corrects, because an organisation may hold several
  accounts.
- **Duplicate protection by TIN** ✅.

---

## I. UmagShop — a Marketplace with Documents

> ✅ In production (beta) · the infrastructure works, the marketplace is filling
> up

### I.1. The idea

**On every other marketplace an order ends in a shopping basket. Here it ends in
a closed deal with the bookkeeping done.**

UmagShop is not a separate start-up but a section of the platform. Two properties
follow from that which competing marketplaces do not have and will not have
quickly:

1. **The platform already knows how to do documents.** An order on a storefront
   becomes an ordinary iHisobchi deal and lives by the same rules: contract →
   payment → e-invoice → waybill → acceptance → closure. It is the same engine
   that tens of thousands of real deals have already passed through.
2. **The address book is not empty.** The platform's clients have around 9,800
   unique counterparties between them — a ready-made invitation list rather than
   a catalogue starting from zero.

### I.2. A double role: selling and buying at the same time

In the real data, one and the same business acts both as a supplier (17,457
roles in deals) and as a buyer (14,901). This is **one user in two modes**, so
the marketplace is designed so that a business can:

- **sell** its own goods through its own storefront;
- **buy** from others — for resale, for production, for the office — using AI to
  find a good price, good reviews and a dependable supplier;
- and in both directions receive a contract and an invoice **without leaving the
  system**.

A buyer does not then have to chase the supplier for paperwork — it is born out
of the order.

### I.3. What is built ✅

| Feature | Description |
|---|---|
| **A shop on its own subdomain** | `<shop>.umagshop.uz` plus the address `umagshop.uz/<slug>` |
| **A shared catalogue** | The marketplace: banners, 14 categories, curated collections, filters, search |
| **Three doors** | A buyer off the street · an existing iHisobchi client · a seller arriving from UmagShop advertising |
| **Cold sign-up for sellers** | The person arrives at UmagShop, not at an accounting system; iHisobchi appears at the document stage |
| **Order lifecycle** | `new → confirmed → contract → paid → shipped → closed`, plus a price request (`quote_requested → quoted`) |
| **Order → documents** | The contract and invoice are created automatically and posted into the deals engine |
| **AI moderation of listings** | Rules → LLM → photo check → verdict. Any uncertainty means "restricted", never "approved" |
| **An AI buying assistant** | "I need a pump for a country house" → product cards. The model **picks an id** from a snapshot of the catalogue instead of naming products — an invented price has nowhere to land |
| **A listing from a photo** | A photo of the packaging → a draft product listing |
| **Price-list import** | Excel/CSV, and from a photograph |
| **AI listing copy** | Descriptions offered as a suggestion; a human publishes |
| **A printed QR poster for the shop** | A4, for the point of sale |
| **A seller digest** | A weekly summary plus catch-up delivery after quiet hours |
| **Automatic payment marking** | An order's payment is found in the bank statement automatically |
| **Agent tools** | Shop statistics, listing drafts, descriptions — with publishing without a human forbidden |

### I.4. The product decision everything is built around: a product is not a listing

```
products_catalog  (PRIVATE: your stock, your purchase prices)
      │  moved across explicitly, by a human, one item at a time
      ▼
mk_listings       (PUBLIC: shop price, shop copy, shop photo)
      ▼
moderation → approved | restricted | rejected → the shared catalogue
```

A business that suspects its purchase prices might leak will not put a single
product on a storefront. So the guarantees are fixed **in the code and in the
tests**:

- a shop price is never populated from a purchase price automatically;
- a "publish everything" button **does not exist**, neither in the interface nor
  in the API — a request without an explicit list of items is rejected;
- a dedicated test walks every public route and fails if even one private field
  leaks out.

In the interface this is drawn as two columns — "In the system · only you see
this" ↔ "In the shop · buyers see this" — with a caption on the divider:
**"nothing crosses on its own"**.

### I.5. The honest state of things as of 14 August 2026

The infrastructure is ready and the marketplace is filling up: 1 shop, 5
published items, 1 order, 14 categories. There is, however, **no shortage of
supply** — 33 businesses already hold products in the system, one of them with
5,042 items; 5,067 IKPU codes have been matched by the AI and await
confirmation. The storefront is empty not because there is nothing to show, but
because almost nobody has yet walked the path from "product" to "listing".

**What does not exist today** (which matters for keeping promises honest):
carrier APIs are not connected — the delivery options (self-collection, own
courier, BTS Express, Uzbekiston Pochtasi, Yandex Delivery) are a reference list
for now and the tracking number is typed in by hand; there is no payment inside
the marketplace, only bank to bank; there is no buyer account, no chat with the
seller and no ratings yet; and **there is no video on the marketplace at all** —
neither live streaming nor short clips. All of it is on the
[roadmap](03-roadmap.md).

### I.6. What is being built next 🎯

Two sections that turn a storefront into a living trading floor. Both are in
near-term development; in detail in
[roadmap §3.5.1–3.5.2](03-roadmap.md#351--247-live-streaming--commerce-you-can-watch):

- **24/7 live streaming** — a round-the-clock broadcast of sellers' goods and
  services. The buyer asks to see an item closer, asks questions and places the
  order live on air. Hosted first by our presenter, then by our AI agent. The key
  difference from any other marketplace: what comes out of the broadcast is a
  **signed contract and an invoice**, not a shopping basket.
- **Short seller videos** — vertical clips of up to a minute in which a business
  advertises its own goods and services, with a real order card underneath.

**Pricing:** currently free — creating a shop, the storefront, orders and
documents; there is no commission on turnover. The marketplace's first real
revenue will come from **paid video promotion** — the seller pays for
impressions of their clip, not a percentage of the deal. A custom subdomain, a
custom domain and extended limits are planned on top.

---

## J. QR-Hisob and Deal Link

> ✅ In production

Two ways to sell without a website and without an integration.

### J.1. QR-Hisob — a printed QR code on the counter

The seller prints an A4 sheet with a QR code (generated by the system). A
business buyer scans it with their phone, lands on the seller's page, enters
their TIN, picks the goods and places the order — **with no registration and no
app**.

Then:
1. The seller receives a "🛒 New QR order" card in Telegram.
2. One tap, and the contract is drawn up and signed with the digital signature.
3. From the signed contract, one more button produces the e-invoice.

A separate invariant in the code: a shop will not switch on until the seller's
bank details are filled in — the account the buyer is supposed to pay into
cannot be left blank.

### J.2. Deal Link

The seller creates a link to an offer and sends it over a messenger. The buyer
opens it, fills in their details and receives a contract and an invoice. There
is a payment deadline, order statuses, a cleaner for expired orders, SMS
notifications to the buyer and pushes to the seller, automatic matching of an
incoming payment to the order, and delivery of the contract into the
counterparty's Didox account.

---

## K. Nasiya — Instalment Sales

> 🟡 Canary release

Accounting for instalment sales **for the seller** who finances the buyer
themselves. We are not a BNPL provider: the money and the credit risk stay with
the seller — we provide the bookkeeping, the documents and the discipline.

| Feature | Description |
|---|---|
| **Payment schedule** | Calculation of the schedule, the mark-up and the allocation of each payment — pure deterministic arithmetic on `Decimal` |
| **Customer by PINFL** | Recognition of an Uzbek passport or ID card from a photo, deduplication by PINFL, encryption of personal data |
| **Instalment contract** | A PDF with the schedule |
| **Taking payments** | Recording a payment with the correct split between principal and mark-up |
| **Reminders** | A −3 / 0 / +1 / +3 / +7 day cadence, with a mandatory "have they already paid?" check before every send |
| **Late fees and claims** | Accrual, a formal claim, a litigation pack |
| **Portfolio** | Analytics: buckets by days past due (DPD), collection rate |
| **Seller shifts** | Opening and closing a shift, cash reconciliation |
| **Import of existing books** | XLSX/CSV — migrating from a notebook or Excel |
| **Buyer portal** | The public link `/n/<token>`: the schedule and the outstanding balance |
| **Restructuring, cancellation, refunds** | The full lifecycle |
| **Personal-data storage** | A separate retention and deletion policy |

---

## L. People — HR

> 🔵 Built, behind a disabled flag

**The intent:** the HR department is run by the system, not by a person. From the
moment a business hires someone, everything is filed automatically — the passport
details need to be entered once.

### L.1. The principle: the source of truth is the HR event

Today an employee record is a form somebody filled in. Not a single fact in it is
backed by a document, and the orders and contracts sit in Word on somebody's
laptop.

We are building the opposite: **the employee record is derived from a stream of
events**, each formalised by an order. From which it follows that:

- "what they do" and "what they are paid" cannot be changed except through an
  order;
- the state as of any past date can be reconstructed exactly;
- documents are generated from the same data rather than retyped;
- a tax or labour inspection is answered in a minute.

### L.2. What is built

| Feature | Description |
|---|---|
| **A hiring wizard** | One action instead of four documents: contract, order, personal record and registration, in a single transaction |
| **HR events and orders** | With number series and printable forms |
| **Staffing table** | Revisions with an effective date, positions, approval by order |
| **Uzbek labour-law checks** | The minimum wage as a **calendar**, not a constant (it changes by decree, usually on 1 September), applied as at the date of the fact. The check is stricter than the Russian model: under Articles 245 and 248(2) of the Uzbek Labour Code, **the base salary itself** for a full-time position must not fall below the minimum wage — you cannot top it up with bonuses |
| **Payroll arithmetic control** | An erroneous row (0.1 FTE × 25 million = 25 million) physically cannot be written to the database |
| **Printable forms** | The order and the staffing table as PDF |
| **HR import from 1C** | Employees and their movement history |
| **ENST deadline radar** ✅ | Reads the client's HR documents in 1C and shows what has not been registered in the Unified National Labour Register on time. Read-only — behind a flag of its own, because this is employees' personal data, and having the "1C" section switched on does not by itself express that consent |
| **Employee record** ✅ | Everything 1C knows about a person: HR and payroll for a period, in a single query |
| **Timesheets / clock-in** 🎯 | A fast QR code as the primary route; geolocation agreement between two devices as the load-bearing safeguard |

**A boundary of the module, drawn deliberately:** we **do not calculate payroll**
and do not replace a payroll package. We maintain HR documents and the state of
the employee. The T-1…T-8 forms familiar from Russian practice do not exist in
Uzbekistan — this module is built on Uzbek statutes rather than on imported
templates.

---

## M. Integrations

**The philosophy:** never make a business abandon what it already uses. If the
client has 1C, MoySklad, a CRM or a cash register, we become a layer on top
rather than a replacement.

### M.1. MoySklad ✅

The most mature integration and the reference for the rest. Bidirectional.

- **Synchronisation**: products (including variants, bundles and services),
  counterparties, stock levels, price types and price lists, attachments and
  photos.
- **Webhooks** on every key document: shipment, customer order, goods receipt,
  returns (from a customer and to a supplier), retail sales and shifts, stock
  entry, write-offs, transfers, stocktaking, production and bills of material,
  incoming and outgoing invoices, incoming and outgoing payments, prepayments and
  their refunds.
- **Shipment → a Didox e-invoice**, automatically.
- **Return → a correcting invoice**.
- **Write-back**: the Didox signature status is written into the attributes of
  MoySklad entities — the bookkeeper sees the status where they work.
- **Payments** are reconciled against the bank.
- **A daily "yesterday's KPIs" summary** in Telegram.
- **Webhook self-monitoring** — if MoySklad disables a webhook on its side, the
  system notices and says so.
- The free tier works by polling, the paid tier through webhooks.

### M.2. 1C ✅

- **Reading reference data**: counterparties, products, employees.
- **Writing**: counterparties, products, outgoing e-invoices.
- **The "1C" section in the app** ✅ — accounting reports straight out of the
  client's own database: the trial balance, an account card broken down by
  analytics dimensions, mutual settlements ("who owes us / whom do we owe"), and
  cash.
- **HR**: employee import, the employee record, the ENST deadline radar.
- **A metadata map** — the system works out for itself which 1C objects a given
  client has published over OData, and does not demand an identical
  configuration.
- **The Till-to-Books bridge** — a daily retail sales document (see
  [F.3](#f3-the-till-to-books-bridge-retail-bridge-)).

### M.3. AmoCRM ✅ and Bitrix24 ✅

OAuth connection, synchronisation of companies, contacts, deals and leads,
signature-verified webhooks, write-back.

### M.4. Document intake by e-mail 🟡

A personal forwarding address: the client (or their bank, or their cash register)
forwards a message with a statement or a batch of receipts to the address they
were issued — the attachment is classified (statement / receipts / document) and
routed into the right accounting pipeline. Inside there is our own IMAP intake
with a cursor, alias management, encryption of identifiers, a confirmation window
for forwarding, and human-in-the-loop cards for messages.

### M.5. External shops ✅

Order intake from third-party online shops over an HTTP webhook, with status
callbacks in return.

---

## N. AI Surfaces

### N.1. The assistant — a universal agent ✅

It works in two places: **in the Telegram bot** (text and voice messages) and
**in the Mini App** (text chat plus live voice).

The user writes or speaks freely, and the agent carries it out with **real
system actions**, through the same capability registry the interface buttons use
(65 tools).

**What it can do:**

- **Read**: documents, statuses, incoming mail, reports, balances, deals,
  receivables, the sales trend, top counterparties, the till, tax-office letters,
  Business Pulse, IKPU search, a counterparty check by TIN.
- **Create drafts**: contract, commercial proposal, e-invoice, waybill — with a
  result card and a "Sign and send" button.
- **Ask for confirmation**: signing, sending, accepting or rejecting an incoming
  document — all published to the owner as a human-in-the-loop card. The agent
  **does not sign on its own**.
- **Find its way around the product**: a navigation manifest covering every menu
  section — the answer "there is no such feature" is impossible when the feature
  exists.
- **Remember context** — conversation history and a daily token budget per
  business.
- **Long-running errands** 🔵 — a task the agent carries to a result across
  several turns, with its state persisted and the same confirmation gates.

### N.2. The live voice orchestrator ✅ (rolling out)

Not "voice commands" but **a conversation with someone who runs your business**:
speech to speech, with the server working out for itself that your turn has
ended — you speak and you get an answer, with no second tap to "send".

This is the product's main bet and its future primary interface, so it has a
document of its own:

> **[04-voice-orchestrator.md](04-voice-orchestrator.md) — the voice AI business
> orchestrator.** What it can already do, how it reaches into every module —
> documents, deals, inventory, banking, tax, the marketplace — why it is safe,
> which devices it runs on, and how running a business by voice at 99% grows out
> of it.

Briefly, as things stand today: the speech provider is xAI Grok Voice Realtime
(Russian); the agent answers by voice while showing result cards at the same
time; the confirmation phrase for an irreversible operation is **composed by the
server, not by the model**; and there is a tap-free voice confirmation mode with
multi-layered echo protection.

### N.3. Recognition and input ✅

| Feature | What it does |
|---|---|
| **Smart Paste** | Pasted text → recognised line items, quantities and prices; the AI works out the buyer from context too |
| **Photos of source documents → a table** | A batch of photographed receipts and delivery notes → **one consolidated table** in Excel. A single vision-model request for the whole batch, under a strict honesty rule for figures: never total up what is not there, never rescale, never guess |
| **Receipt files → a register** | A batch of `.xls`/`.xlsx`/`.csv` exports → the same register; works both in a private chat and in a linked work chat |
| **Speech recognition** | Groq Whisper (ru) and Gemini (uz) for voice messages |
| **Photo OCR** | Products and company details from a photograph |
| **Document recognition** | DOCX / PDF / image → text for the AI |

### N.4. AI Studio — the spreadsheet bookkeeper ✅ (rolling out)

A general-purpose AI agent working over accounting files: the client uploads
their spreadsheets, the agent performs a task on them (consolidation,
allocation, recalculation, reformatting) and returns a finished file. There are
saved "recipes" (repeatable jobs) and templates, a run history, live progress
over SSE, and an isolated sandbox for code execution.

### N.5. Converter ✅

A separate, simple, AI-free tool: file conversion (DOCX/XLSX/PDF and others)
through an isolated LibreOffice sidecar.

### N.6. Concierge ✅

A safety net for when a message could not be parsed any other way: one fast
intent classifier, and the bot **always** answers to the point rather than
saying "I didn't understand". It never signs, sends or pays: the path from
intent to action is limited to a hard-coded list.

---

## O. Reports and Analytics

> ✅ In production

| Report | What it shows |
|---|---|
| **Sales** | Outgoing invoices by period, counterparty and amount |
| **Purchases** | Incoming invoices |
| **VAT** | Input and output VAT reconciled |
| **By client** | A breakdown per buyer: turnover, documents, debt |
| **By product** | What sells, in what volume, at what price |
| **Sales forecast** | Linear regression over the history |
| **Cash movement** | Income and spending by category |
| **Dashboard** | The home screen: the key figures for a period plus an **AI comment** in a single paragraph |
| **Export** | Excel for any report, PDF for Business Pulse |

---

## P. Automatic Documents

> ✅ In production

Pipelines that produce documents **without human involvement**, on the basis of
documents already signed.

| Pipeline | What it does |
|---|---|
| **Auto-invoice from a power of attorney** | A power of attorney arrives → the system assembles an e-invoice from its line items, shows a preview and waits for confirmation |
| **Act from an invoice** | A certificate of completed work is assembled from a signed e-invoice |
| **Waybill from an invoice** | A goods waybill (type 041) is assembled from a goods invoice, using the default transport settings |
| **One-tap invoice acceptance** | Incoming invoices from whitelisted suppliers are recognised automatically and arrive as a ready "accept" card — one document at a time or a whole batch. A human confirms the acceptance |
| **Invoice from a contract** | Line items and amounts are taken from the signed contract |
| **Invoice from an order** | An order from a storefront or a QR code becomes a contract and an invoice |
| **Default settings** | Separate "Contract settings" and "Waybill settings" profiles, so the same values are not typed twice |

**This is the approach run-up to autonomous deals** — the next step, described in
the [roadmap](03-roadmap.md#32-horizon-i--autonomous-deals).

---

## Q. Multi-business, Roles, Notifications, Audit

> ✅ In production

- **Several organisations under one person** — switching the active company in
  one tap, across every surface at once. The multi-business model was built for
  exactly this scenario: one feed, one way in, one picture.
- **Roles inside a company**: owner / admin / accountant / viewer. The role model
  and the membership table are built and the assignment interface works;
  **shared access for several employees to one organisation is being rolled out
  through a gentle migration** — until that finishes, owner access remains the
  working path. Separately and independently, there is management of employee
  roles **inside Didox itself** and a register of employee signatories — these
  are different things and are easily confused.
- **Notifications**: configurable by type, with quiet hours; a durable event feed
  that survives being offline; live updates in the Mini App over SSE.
- **Linking a work group chat** — receipt files dropped into a work group are
  processed and answered with a register in that same chat.
- **An action log** — available to the user in the interface; the AI's actions
  are written to a separate register that carries no personal data.
- **Expenses / payroll** — a simple cost register per organisation.
- **Appearance**: themes, brand families, light and dark schemes, two languages.

---

## R. Partner Channels

### R.1. MCP server ✅ (rolling out)

`mcp.ihisobchi.uz` — connects iHisobchi to external AI clients (Claude, ChatGPT
and others) over the Model Context Protocol with full OAuth 2.1 (including
dynamic client registration). The client talks to their own business from any AI
application; irreversible operations pass through the same human-in-the-loop
gate, confirmed in Telegram.

### R.2. Partner REST API 🔵

A headless surface for partners: a per-organisation key, a uniform response
envelope, two-phase rate limiting, idempotency, and a permission check on every
route.

**What is exposed over HTTP today — the exact list:** creating drafts of four
types — contract, commercial proposal, e-invoice, waybill.

**Signing and sending are deliberately not registered in the Partner API.** That
is a decision, not an omission: an external key must not be able to sign a
document on an organisation's behalf without its owner taking part. The partner
prepares a draft — a human signs it on their own surface. When a signing path for
partners does open, it will run through the same human-in-the-loop gate as
everything else.

The flag is off: the surface is enabled under a contract, after contract tests
and agreement on quotas.

### R.3. Chrome extension ✅

A browser side panel with AI workflows layered over third-party web portals:
filling in forms from saved field mappings, moving data across, looking up a
counterparty by TIN, uploading and parsing files. It pairs with the account
through a pairing code.

---

## S. iSMM — Sales and Promotion on Social Media

> 🎯 Designed, next in the build queue

**iSMM — intelligent social media management.** A business connects its social
accounts to the platform once, and they become one more workplace inside it:
posts and ad campaigns go out from here, responses come back here, and a buyer
who liked the advertisement **buys in the same minute** — contract, invoice and
payment all happen on a single page they never have to leave.

### S.1. The gap the module exists to close

Social advertising today is capable of delivering a person who **wants to buy
right now**, and there it stops. What comes next is what kills the purchase:

| The step today | Who does it | How long it lives |
|---|---|---|
| Saw the ad, wanted to buy | the buyer | seconds |
| "Leave your number in our DMs" | the buyer | minutes |
| A sales manager calls back and repeats the same thing | the seller | hours |
| Hands it to the bookkeeper | the seller | hours |
| The bookkeeper asks for details, TIN, address | the seller | hours |
| Prepares the contract and the invoice | the seller | hours |
| Sends them — by post, by messenger, through the e-document system | the seller | hours |
| The buyer opens the e-document portal, finds the contract, signs it | the buyer | a day |
| Logs into their bank client and pays against the details | the buyer | a day |
| The seller hunts for the payment in the statement | the seller | a day |

**Between "I want it" and "it is paid for" lie up to ten steps, two or three
different programs and several days.** The impulse the business paid an
advertising budget for does not survive to the till. And this is not one
seller's problem: **in B2B that path simply does not exist.** You cannot issue an
e-invoice and conclude a contract from an advertisement — not on any social
network in the world.

### S.2. The module's four layers

| Layer | What it does |
|---|---|
| **1. A single account loop** | Instagram, Telegram, Facebook, TikTok, X — and other networks on request. Connect once, and from then on they are all visible from one place |
| **2. Publishing and advertising** | Posts and campaigns from the workspace, featuring products **from your own catalogue**: current price, stock, photo, IKPU code. The copy is written by an AI that knows the range |
| **3. Checkout** | A payment page bound to a post, a campaign or a single product. The buyer enters their TIN and receives a ready contract, an invoice and online payment |
| **4. Documents and money** | Contract, payment invoice, a Didox e-invoice and a fiscal receipt — all born out of the order by themselves. The payment is found in the statement and closes the deal |

Above all four sits the same AI agent and the same
[deal](#b-deals--the-open-cycle-engine): an order from Instagram enters the
common cycle engine and lives by the common rules.

### S.3. Why this is being finished rather than started

The module rests on what **already runs in production** — what it needs is a
payment seam and a social layer, not a new platform:

| The existing brick | What iSMM takes from it |
|---|---|
| [Deal Link](#j2-deal-link) | The public page `/l/<slug>`: a cold buyer with no registration, TIN → company details, contract preview, payment deadline, status by token. Its code was **written for the in-app browser inside Instagram from the start** — right down to a 3G load budget |
| [Contract and invoice from an order](#p-automatic-documents) | Documents on the seller's template, with a number that is not burned by a preview |
| [Payment matching](#e-banking-and-payments) | A payment arriving in the account finds its own order in the statement |
| [Catalogue and storefront](#i-umagshop--a-marketplace-with-documents) | Products, prices, photos, AI moderation and the "nothing crosses on its own" rule |
| [E-documents and digital signature](#a-document-flow-and-digital-signature) | The Didox e-invoice and the signature — the loop 73,098 documents have passed through |
| [The deals engine](#b-deals--the-open-cycle-engine) | An order from social media becomes a deal with a state and an answer to "whose move is it" |

**What does not exist today and will have to be built:** online payment
acceptance (card acquiring), a fiscal receipt for a consumer buyer, connections
to the social networks and their ad workspaces, and a single feed of responses.
That is what the module consists of.

### S.4. What the module will not have

- **A percentage of the deal.** The money goes from the buyer's card or account
  straight to the seller's account — we neither hold it nor route it
  ([the principle](09-business-model.md#91-the-principle-we-do-not-take-a-percentage-of-the-deal)).
- **Auto-posting without a human.** The AI prepares the copy and picks the
  product; the owner publishes it and launches the campaign. The same
  human-in-the-loop gate as on signing.
- **A promise of "native payment inside Instagram".** Meta's built-in checkout is
  not available in Uzbekistan; we honestly open our own payment page in the
  in-app browser — which is precisely why it is engineered to open in seconds.

**The module in detail:** what the purchase looks like through the buyer's eyes,
what each network can and cannot do, how checkout works for a company and for an
individual, which documents are produced and under which law, how advertising
effectiveness is measured against the bank statement, and in what order all of it
gets built.

---

**Next:** [3. Roadmap](03-roadmap.md) — where the product is heading.
