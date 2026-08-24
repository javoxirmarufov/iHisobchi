# 3. Roadmap

> Part 3 of 9. Back: [ecosystem](01-ecosystem.md) · [modules](02-modules.md). Next: [voice orchestrator](04-voice-orchestrator.md) · [security](05-security.md) · [first day](06-first-day.md) · [signing](07-signing.md) · [with us and without us](08-with-and-without.md) · [business model](09-business-model.md).

---

## 3.1. Where We Are Going

Everything built so far is the foundation for a single idea:

> **A business should run like a Swiss watch — autonomously, without failures —
> leaving the owner to observe and to make decisions.**

Today iHisobchi removes the routine. Tomorrow it removes the need to think about
the routine at all. The difference between those two states is not a number of
features but **one step**: the system already sees the whole chain of a deal and
already knows how to create every document in it. What remains is to let it do so
by itself — where both sides have asked for that.

Below are eleven horizons. They are not sequential stages: some are already being
built in parallel, and for others the infrastructure is ready and waiting to be
switched on.

### What we are working on first

The horizons are a picture of the destination, not a work queue. The order of
work is set by today's constraint, and our constraint is not build speed: the
platform is broad, but usage is still uneven (see
[the current figures](01-ecosystem.md#19-where-we-stand-scale-and-maturity)).

| Queue | What we are doing | Why this specifically |
|---|---|---|
| **Now** | Turning what is built into regular use: the path to the first signed document, connecting the money (bank/till), closing deals, and instruments that show real usage frequency | A module nobody uses creates no value, however good it is |
| **Now** | The automatic e-invoice on payment (§3.2.1) and the voice orchestrator reaching deeper into the modules | The nearest steps that pay off without new large subsystems |
| **Next** | The accounting-firm workspace, the services exchange, autonomous deals | These need the trust and the volume that accumulate at the previous step |
| **Later** | Open banking, carriers, tax filing, mobile apps | These depend on outside parties: the regulator, partners, demand |

Risky directions carry **stop conditions**: if UmagShop does not attract live
sellers and orders by its checkpoint date, the direction is frozen and the people
go back to the core. Better to halt a hypothesis honestly than to maintain a
storefront for years for the sake of a line in a presentation.

---

## 3.2. Horizon I — Autonomous Deals

> The nearest and the most powerful step. Everything it needs is already built.

### What it is

Today the system shows **whose move it is** and produces a document in one tap.
Tomorrow it produces that document itself, once both sides of the deal have asked
for it.

**The scenario:**

1. Seller and buyer are both iHisobchi clients. Both have enabled "automatic
   deals".
2. The parties sign a contract once.
3. The buyer sends the payment to the supplier's account.
4. **From then on nobody does anything.** The system sees the payment in the
   statement, matches it to the contract, produces the power of attorney, the
   e-invoice, the waybill and the act, signs them with both parties' digital
   signatures, sends them through Didox, tracks acceptance and closes the deal.
5. The owner sees a notification: "The deal with X LLC for 45 million is closed.
   All documents signed."

**One contract — and all the paperwork that follows takes care of itself.**

### Why this is realistic

Every brick is already in production:

| What is needed | State |
|---|---|
| Seeing the whole chain of a deal and its state | ✅ [The deals engine](02-modules.md#b-deals--the-open-cycle-engine), 85,869 deals |
| Matching a payment to a contract | ✅ Payment scoring, the single money ledger |
| Creating every document programmatically | ✅ [Automatic documents](02-modules.md#p-automatic-documents): an invoice from a power of attorney, an act from an invoice, a waybill from an invoice |
| Signing without a human present | ✅ [The 24/7 signing server](02-modules.md#a3-digital-signature--four-modes-) |
| Guaranteeing that nothing extra gets signed | ✅ Idempotency, reconciliation after a timeout, the durable operations ledger |
| Stopping everything instantly | ✅ A kill switch on every pipeline |

**Exactly one thing is missing:** mutual consent from both sides, expressed
explicitly and revocable in one tap, plus a mode in which the human-in-the-loop
confirmation is replaced by advance consent to a class of operations inside a
specific contract.

### Why it matters

For a supplier with a steady flow of identical shipments to a regular customer,
this is the difference between "the bookkeeper spends a day a week on it" and
"the bookkeeper spends nothing". For the market, it is the country's first loop
in which a B2B deal runs from contract to closure with no manual paperwork at
all.

### 🎯 What we are building

- Explicit two-sided consent to automation within a specific contract, with an
  audit trail and one-tap revocation.
- Boundaries of autonomy: an amount limit, a list of counterparties, document
  types, an expiry date on the consent.
- A report after the fact instead of a confirmation before it: the owner sees a
  receipt, not a question.
- Learning from the flow: the more deals pass through, the more confident the
  matching and the wider the class of cases that can be automated.

### 3.2.1. The first step towards it — "automatic e-invoice on payment" 🎯

Full autonomy requires consent from two sides. But there is a scenario that works
**with consent from one** — the seller — and so it comes before everything else.

**A situation every supplier knows.** The contract is agreed, the goods are
shipped, the invoice for payment is issued. The e-invoice **cannot be issued
yet** — the money has not arrived, and an e-invoice issued ahead of time creates
a tax liability against payment that was never received. So you sit and wait for
the credit. And the credit arrives at 23:40 on a Friday, or while the supplier is
driving, or when they simply have no internet. Meanwhile the customer is waiting
for the document — they have their own period to close.

**How it will work.** The seller enables the mode once, on a specific deal or on a
counterparty. From then on:

```
Payment credited to the account
        │  the system recognises the payment and finds its contract
        ▼
The e-invoice is assembled from the contract's line items
        ▼
Signed with the digital signature  →  Sent to the counterparty in Didox
        ▼
A receipt for the owner: "Invoice No. 145 for 18 million sent to Artel, payment received"
```

All of it while the owner is asleep, driving or out of signal. In the morning
they see a result, not a task.

**Why this is the next step and not a dream.** Every brick already works: the
system recognises a credit in the statement and ties it to a contract (the deals
engine, payment scoring), knows how to assemble an e-invoice from a contract's
line items (the auto-invoice pipeline), knows how to sign without a human (the
24/7 signing server) and knows how to send. What is new here is the **trigger
rule** — "a payment against this contract → issue and send" — and the owner's
explicit permission for it.

**Boundaries built in from the start:** only for contracts where the seller has
enabled the mode; the invoice amount is capped by the contract value and the
actual payment; a partial payment does not trigger a full document without a
rule; on any mismatch we ask rather than issue; and revocation takes effect
immediately, including operations already queued.

---

## 3.3. Horizon II — An Exchange for Accounting and Outsourcing Services

> Supply and demand meet inside the platform.

### A problem that costs businesses dearly

A demand arrives from the tax office. Or a debt surfaces. Or a report is due
urgently and the bookkeeper has just resigned. **The owner is in a panic and does
not know three things:** how serious this is, who to turn to, and what it ought to
cost.

They walk into the first outsourcing or audit firm they find. They are quoted any
number at all — they cannot verify it. They are told about billion-som risks —
they cannot dispute it. Finding a genuinely competent bookkeeper or outsourcer in
Uzbekistan is hard, and comparing several of them is close to impossible.

### Our answer: a services marketplace

**The owner describes the problem and posts it anonymously** to the platform's
partner firms. Partners see the substance of the task — but not whose company it
is.

**Several proposals come back**: exactly how the firm proposes to solve it, in
what timeframe and for how much.

**The owner chooses.** Not because they walked into the first firm they found,
but because they compared three or four proposals from vetted partners and, from
those, understood the real size of their problem.

Then comes a contract with the chosen partner, a digital signature, and the work
itself conducted **inside the same system** that holds the documents the work is
about. Our role here is the orchestrator: we do not provide the service, we bring
demand and supply together and provide the loop of trust.

### Why this will shake up the market

- For the first time the owner gets a **market price** for an accounting service
  rather than the price of the first person they met.
- Anonymity at the request stage removes the ability to tailor a price to a
  particular company.
- Partners get a stream of clients whose documents are already digitised — they
  do not have to extract the data from the client, they can see it immediately.
- The platform gets what advertising cannot buy: a **network** in which both
  sides have an interest in bringing each other in.

### 🎯 What we are building

- A register of partner firms with a profile, a specialism and a verified track
  record.
- An anonymous request: description of the task, its type, urgency and size —
  with no identifying details.
- Proposals in response, with a price and a deadline, comparable because they
  share one form.
- Selection, contract, signing and the conduct of the work, all inside the
  system.
- Partner reputation based on tasks actually completed, not on reviews that can
  be written to order.

---

## 3.4. Horizon III — The Accounting Firm Workspace

> Multi-client mode. The strongest growth lever that is not advertising.

One outsourcing firm keeps the books of 20–50 companies. Today, to work in
iHisobchi, it has to switch between accounts.

**What we will give it:** a single workspace with all the firm's clients in one
list; batch operations across several companies at once; a shared calendar of
deadlines; separate billing; management of a hundred signature keys from one
place (the technical foundation —
[multi-TIN support for the signing agent](02-modules.md#a3-digital-signature--four-modes-) —
already works).

**The economics are obvious:** one outsourcer brings in 40 companies of its own
accord, because that is how it prefers to work. Not a som of advertising spend.

---

## 3.5. Horizon IV — Turnkey Commerce: UmagShop

> The infrastructure is built; we are finishing what turns a storefront into a
> sales channel.

### The intent

What the owner needs is for **the goods to be in stock — and nothing more**.
After that they simply watch the processes run and hand the parcel to the courier
when it arrives. The contract, the e-invoice, the power of attorney, acceptance
and closure all take care of themselves.

That is precisely what no marketplace in the country offers: there, a sale ends
at the shopping basket and the bookkeeping starts again, by hand.

### 3.5.1. 🎯 24/7 live streaming — commerce you can watch

> In near-term development. A separate section of the marketplace.

**What it is.** A round-the-clock live broadcast inside UmagShop showing the
goods and services of the marketplace's sellers. The buyer does not scroll
through cards — they **watch, ask and buy live on air**:

- **"Show me closer"** — ask to inspect the item, turn it round, show the weave
  of the fabric, the seam, the marking on the packaging, the device in
  operation;
- **ask a question in the chat** — about the batch, lead times, the minimum
  order, a volume discount;
- **place an order without leaving the broadcast** — the product card sits beside
  the video and the order is assembled in one tap.

**Who answers — in two stages.**

*First, a human.* The stream is hosted by our presenter: showing the goods,
answering questions, helping to place the order. This is not a stopgap but a way
of **learning from live conversations**: which questions get asked, where the
buyer hesitates, what decides the sale. The next stage grows out of those same
conversations.

*Then our AI agent.* It hosts the stream and talks to the buyers itself:
answering questions about a product, selecting items, calculating the batch
total, assembling the order. And this is not built from scratch: **the
marketplace's AI assistant already works** — it selects products by picking their
identifiers out of the real catalogue rather than naming them from memory, so an
invented price has physically nowhere to land. Live streaming adds voice and
video to it — and the voice loop is
[already built](04-voice-orchestrator.md).

**Why it works.** The global live-commerce market is worth $230 billion in 2026
and growing at 41% a year; live streams convert at **9–30% against 2–3% for an
ordinary product card**, and in a consultative format at up to 40–70%. The reason
is not entertainment: a live stream **compresses into one moment** what is
normally stretched across days — studying the product, judging its specification,
asking questions and deciding to buy.

**Why it fits Uzbekistan particularly well.** Trade here already lives in
Instagram and Telegram: the entrepreneur films the goods on a phone, replies in
the DMs, agrees terms by voice. Live streaming is that familiar mechanic, but
placed on a marketplace where **the transaction is formalised in law** instead of
ending in a chat thread.

**And here is what makes it ours rather than a copy.** Everyone else's live
commerce ends in a basket. Ours ends in a **signed contract and an invoice**:

> A wholesaler shows a batch of fabric. The buyer asks to unroll it and look at
> the selvedge, checks the price for 200 metres in the chat, gets an answer — and
> places the order live on air. A minute later a **contract and an invoice, both
> digitally signed**, are sitting in their Didox account, and the seller has a
> deal that will carry itself onward to the e-invoice and to closure.

A live B2B broadcast that produces a legally formed transaction exists on no
other platform in the country.

**What to show on air:** new arrivals and clearance stock, equipment in
operation, furniture being assembled, a print run coming off the press, a tool
being test-driven, a batch walked through item by item, answers to the common
questions about a product. Services work the same way: the contractor shows how
the work is done.

### 3.5.2. 🎯 Short seller videos — and the marketplace's first real revenue

> In near-term development. A separate, visually striking section of the
> marketplace.

**What it is.** A feed of short vertical clips of **up to one minute** in which
the marketplace's sellers advertise their own goods and services. Film it on a
phone, upload it, attach a link to the product card — and the clip plays in the
marketplace feed next to goods that can actually be ordered.

The format was not chosen at random: it is exactly what an Uzbek entrepreneur
already knows how to film for Instagram and Telegram. The difference is that here
**a real product card sits underneath the clip**, with a price, stock and an
order button, instead of a caption reading "price in DMs".

**How a seller uses it:**

| The occasion | The clip |
|---|---|
| A delivery has arrived | 30 seconds: boxes, unpacking, the price for the batch |
| Stock to clear | "40 left, 30% off until Friday" |
| A new service | how it works, what it costs, who it suits |
| The difference from a cheap equivalent | show it live rather than describing it |
| Manufacturing | how it is made — the strongest argument there is for a wholesaler |

**This is also where the marketplace's revenue appears.** Today UmagShop is free
and takes no commission on turnover — the marketplace works as an acquisition
channel. Paid promotion changes that: the seller pays to have **more buyers see
their clip** — a slot at the top of the feed, in curated collections, in themed
sections, on the live stream.

Why this is an honest model for us:

- **the seller pays for a result they can see** — views, taps through to the
  card, orders — rather than for an abstract "placement";
- **we take no percentage of the deal** and therefore have no interest in getting
  between the two parties' money;
- **the seller decides the budget** — from a small push behind one clip to a
  permanent presence in the feed;
- **we have something to target with honestly**: the marketplace knows what a
  business buys and sells, so a clip about packaging is shown to firms that buy
  packaging, not to everybody.

**Quality as a condition.** The video section is meant to be striking — and that
imposes an obligation: clips pass through the same
[AI moderation](02-modules.md#i-umagshop--a-marketplace-with-documents) as
product listings, under the same rule that any uncertainty means restricting
rather than approving. Cheap, blurry footage carrying somebody else's watermark
will not reach the feed: a storefront you are ashamed of sells nothing to nobody.

**The market figures we rely on** (public sources, August 2026): the size of the
global live-commerce market —
[Grand View Research](https://www.grandviewresearch.com/industry-analysis/live-commerce-market-report)
and [Straits Research](https://straitsresearch.com/report/live-commerce-platforms-market);
stream conversion against ordinary product cards —
[Getstream](https://getstream.io/blog/livestream-shopping-statistics/);
live commerce's share of e-commerce —
[eMarketer](https://www.emarketer.com/insights/livestreaming-trends-stats);
the Uzbek market and its channels —
[Daryo](https://daryo.uz/ru/2026/03/22/uzbekistan-elektronnaya-kommerciya-marketplejs/)
and [the Marketing Association of Uzbekistan](https://marketing.uz/news/association/digital-v-uzbekistane-2026-trendy-lovushki-i-tochki-rosta-dlya-biznesa.htm).
These figures are external and they move — re-check them before using them in
commercial material.

### 🎯 Integration with delivery services

Today the delivery options (self-collection, own courier, **BTS Express**,
**Uzbekiston Pochtasi**, **Yandex Delivery**, **EMU**) are a reference list: the
seller arranges the shipment the way they always have and types in the tracking
number by hand.

What we are building: **direct integrations with carriers** — a cost calculation
while the order is being placed, an automatic collection request, the tracking
number and delivery status inside the order card, notifications to the buyer. The
seller does not have to visit the carrier's website: the order goes to the
carrier by itself, and the AI picks a suitable service by route, deadline and
price.

### 🎯 The rest of the marketplace

| What | Why |
|---|---|
| **A buyer account** | Order history, reordering, favourites |
| **Buyer ↔ seller chat** | Clarify before the order rather than after it |
| **A rating based on closed deals** | B2B reputation that **cannot be gamed**: computed from deals actually closed with signed documents, not from reviews |
| **An AI buyer** | "find me 200 packages delivered to Samarkand by Friday" → a shortlist with prices, ratings and lead times |
| **Payment inside the marketplace** | Currently bank-to-bank against an invoice only |
| **Paid options** | A custom subdomain, a custom domain, extended limits |

---

## 3.6. Horizon V — Money and Open Banking

### What is changing in the market

**Presidential decree PP-359 of 27 November 2025** mandates the launch of an
**"open banking" system by 1 September 2026**: standardised data exchange between
banks, payment institutions and fintech participants with the customer's consent.
The Central Bank of Uzbekistan is the designated authority, and a $50 million
venture fund has been created with a target of 200 fintech companies by 2030.

Until that point no bank in the country offers a public banking API. What banks
call "an API for business" (acquiring, accepting card and QR payments) is **not
access to a settlement account**.

### Our position

The banking module is critical to the whole system: Deals, Business Pulse, tax
reconciliation and every report stand on it. Therefore:

1. **We already work** with a direct bank-client connection and statement import
   from any format — that gives us coverage today.
2. **The next step is a single integration through `Dibank`.** By our own market
   study this is the de facto national standard for bank-client APIs, covering
   roughly twenty of the 35 banks operating in the country. One integration →
   statements, payment orders, payroll registers and balances across almost the
   whole market. Materially: it is the same vendor as Didox, with whom we already
   have a working integration. Exact coverage and terms will be confirmed by a
   contract, not by an estimate.
3. **The provider abstraction layer is designed but not yet written.** Today the
   code holds a concrete Bank24 client; a common interface over several providers
   will be laid down together with the second source, so that the abstraction is
   not built from a single example.

### What it gives a business

- Incoming money is visible in Telegram **immediately**, tied to its contract and
  invoice — the salesperson no longer has to phone the bookkeeper.
- A payment order is sent from the same system that holds the invoice.
- Business Pulse, deals and tax reconciliation get a complete and continuous
  picture of the money.

---
## 3.7. Horizon VI — A Module for Every Type of Business

> From "a document system" to "an orchestrator of all the tools a business
> uses".

The project's full intent: every business has its own set of daily tools. Trade
means a CRM, a warehouse, bookkeeping, promotion and a bank. Services mean
requests, acts, HR and a bank. Manufacturing means bills of material, a
warehouse, logistics.

**Our job is to assemble that orchestrator for each type of business**, where
every one of its tools is either integrated (if the client already uses it) or
built by us out of the same modules. And above all of it, one AI agent that knows
this business's products, prices, customers, debts and obligations.

### 🎯 Our own CRM

Today we integrate with AmoCRM and Bitrix24. Next comes our own customer loop,
built into the same deals and documents: a pipeline, tasks, contact history,
automatic reminders. The value is that a CRM here is not a separate contact
database but **the same deal**, which already has a contract, a payment and
documents.

### 🎯 The social loop — social networks in one place

Promotion is the daily work of a trading business, and today it lives entirely
outside the accounting system. The intent: connect the business's social accounts
to the platform and publish from one place — with product cards that **already
exist in the catalogue**, prices that are **already current**, and copy written
by an AI that knows the range.

The seller does not carry photos and prices from the system into Instagram by
hand — they pick the items and press "publish".

> **This direction grew from a line in a table into a horizon of its own.**
> Publishing from the catalogue turned out to be the smaller part of it: the
> point is to carry the buyer from the advertisement to a paid invoice without
> letting them leave the social network. See
> **[iSMM — sales and promotion on social media](02-modules.md#s-ismm--sales-and-promotion-on-social-media)**.

### 🎯 The rest of the platform

| What | State |
|---|---|
| **Uzbek speech in the voice assistant** | The architecture was built in advance for a second speech provider; awaiting the Gemini Live connection |
| **Plans and billing** | The plan interface is ready; connecting the payment loop and the limits is the next step |
| **HR: timesheets and the payroll loop** | HR record-keeping is built; QR clock-in and the link to payroll calculation are the next step |
| **The counterparty replies inside our system** | Our clients already send documents to their partners through Didox. Making it possible for the partner to accept, sign and reply **here** is the cheapest growth channel that exists |

---

## 3.8. Horizon VII — Mobile Applications: iOS and Android

> An app in your pocket is not "one more platform" but a channel we physically do
> not have today.

### What a business has on its phone today

| Surface | What it gives | Where it runs out |
|---|---|---|
| **The Telegram Mini App** | A complete application inside the messenger: 117 screens, live updates | Only works for someone who uses Telegram, and only inside its WebView |
| **The web app `app.ihisobchi.uz`** | The same interface in a browser, sign-in by phone + SMS or e-mail + password, installable to the home screen (PWA manifest, standalone mode, its own icons) | No offline mode, no push notifications of our own, no access to biometrics |

In other words, **the client already has an app on their screen** — but it is a
web wrapper, and three things are fundamentally out of its reach.

### Why native apps are needed

**1. A notification channel of our own.** Today the only way to reach a client is
the Telegram bot. Anyone who does not use Telegram, or who has muted bot
notifications, will never learn that money arrived, that a letter came from the
tax office, or that an order was placed on their storefront. A native push
removes a dependency on somebody else's messenger at the product's most sensitive
point.

**2. A presence in the App Store and Google Play.** For a business choosing an
accounting system, having an app in the store is a signal of maturity. It is also
a free acquisition channel: someone searches for "hisobchi", "hisob-faktura" or
"ESF" and finds us without ever knowing about the Telegram bot.

**3. The camera and the scanner, properly.** We already lean on the camera
heavily — stocktaking with barcode scanning, adding a product by barcode,
recognising source documents and price lists from a photo, recognising a passport
for an instalment sale, voice input. Inside a WebView every one of those works
with caveats and depends on the OS version. Native camera access means scanning
speed, dependable autofocus, and a continuous "scan a whole batch in a row" mode.

**4. Offline.** Today the app simply does not open without a network — there is
no service worker. Yet the key scenarios happen where the signal is poor: a
warehouse, a stocktake, a field salesperson, a stall in a market. An offline
operations queue ("I scanned 200 items with no signal — the moment it came back
everything flew off") is exactly what makes a warehouse move to an app.

**5. Biometrics as a second factor.** Face ID or a fingerprint instead of typing
the password again to confirm a signature or the sending of a document. It is
both more convenient and stricter: confirming an operation is tied to a device
and a person.

**6. Background work.** Fetching the statement, syncing tills, refreshing deals —
while the app is closed, and with respect for quiet hours.

### Why this is a cheap step rather than a new product

The important part is already built, and built correctly:

| What a native app needs | State |
|---|---|
| A full interface for every section | ✅ An SPA with 117 routes — that is the app |
| A backend not tied to Telegram | ✅ HTTP + SSE; the web authentication mode (phone + SMS OTP, e-mail + password, JWT sessions) works outside the messenger |
| Digital signing outside Telegram | ✅ Web signing is available, managed signing runs round the clock |
| Manifest, icons, theme, standalone mode | ✅ Already there |
| File and document downloads | ✅ One-time download tickets are already implemented for native downloads |

**The product does not need rewriting** — the interface, the API and the
authentication already exist and work outside Telegram. But calling it "just a
wrapper" would be a simplification too: the offline operations queue, conflict
resolution on sync, device binding, a push-token registry and remote revocation
of access all require new server-side contracts and a security review of their
own. We regard this as **a medium-sized piece of work on an existing
foundation**, not a new product.

### Three stages

**Stage 1 — finish the PWA (cheap, no app stores).**
A service worker: an offline shell, cached reference data, an operations queue
for when the network drops. Web push where the platform supports it. That closes
offline use and part of the notification problem **without a single store
submission**, and it can be tested on real clients before any work on the stores
begins.

**Stage 2 — a hybrid shell and publication.**
The same interface code inside a native container: native push notifications, the
camera, biometrics, file handling, deep links into sections. Publication to the
App Store and Google Play with update support. One codebase for the web, Telegram
and both stores — the interface cannot drift apart between platforms, and a fix
lands everywhere at once.

**Stage 3 — native where a shell is not enough.**
A continuous barcode scanner for stocktaking, an offline warehouse with a local
database, integration with mobile digital-signature tools. Done selectively and
only for a confirmed scenario, never "because native is better".

### What we are not doing along the way

**Telegram does not stop being the first surface.** The Uzbek market lives in
Telegram, and the path of "started using it without installing anything" is a
competitive advantage, not a stopgap. A mobile app **adds** a channel for those
who need a warehouse in their hand, notifications without a messenger and a way
in without a Telegram account — but it does not take away anyone else's ability
to work where they already are.

---

## 3.9. Horizon VIII — Tax Reporting That Prepares Itself

> The closing link of full autonomy.

### What it is

The quarterly return, the VAT return and the rest of the mandatory reporting are
manual work today: gather the turnover, reconcile it against the documents,
double-check, fill in the forms in the tax portal, submit, and do not miss the
deadline.

The intent: **the system prepares the return itself, from actual data it already
holds.**

```
The filing deadline approaches
        │
        ▼
The agent gathers the basis: how much was received into the account,
how much was rung up on the till, how many e-invoices were issued and
signed, which incoming documents were accepted, what happened in the period
        ▼
It composes the return — and shows it to the owner WITH THE EVIDENCE:
every figure expands into the documents it was built from
        ▼
The owner looks → confirms, or asks for a change
(including by voice: "drop that deal, it was cancelled")
        ▼
Submission to the tax office
```

### Why this is achievable specifically here

A return cannot be assembled out of thin air — it needs source data, reconciled
and verified. That is exactly what we already have, and it is already reconciled:

- **e-invoices** — outgoing and incoming, with their signature statuses;
- **money** — the bank statement and the fiscal cash-register receipts in one
  ledger;
- **deals** — what is closed, what is not, what was paid without a document and
  the reverse;
- **reconciliation** — the mechanism that already surfaces "turnover without
  documents" in Business Pulse today.

In other words, **the basis of the return is already calculated on our side** —
as a by-product of the ordinary work. What remains is the form and the submission
channel.

### What we are waiting on from outside

An official programmatic interface from the tax authority for filing — over an
API or over the MCP protocol. The direction has been set by the state: the same
course towards open interfaces as in
[banking](#36-horizon-v--money-and-open-banking). Until an official channel
exists, we build the part that depends on us: prepare the return, show the
evidence, and let the owner confirm and export it.

**We will not submit filings to a government body by back doors.** No emulation
of a user's actions inside someone else's portal: a legally significant
submission will go only through an official channel, once one exists.

### How this completes the picture

Together with [autonomous deals](#32-horizon-i--autonomous-deals), the
[automatic invoice on payment](#321-the-first-step-towards-it--automatic-e-invoice-on-payment-)
and [banking](#36-horizon-v--money-and-open-banking), this closes the full
circle:

> Goods sold → documents filed automatically → money received and allocated
> automatically → the deal closed automatically → the return assembled and
> submitted.

The business is left with no operational work at all. Only watching, checking and
deciding — which is what it was opened for in the first place.

---
## 3.10. Horizon IX — Support That Solves Rather Than Logs

> 🔵 In development. In detail:
> [08-with-and-without.md §8.7](08-with-and-without.md#87-support-our-position).

A business entrusts us with its documents, its signatures and its money. In work
like that, support is not a department off to one side but part of the product:
"wait until Monday" can mean a missed shipment or a missed deadline to answer the
tax office.

We are building an **AI support agent** that answers on the substance and is able
to act — rather than collecting the question and passing it to a human.

- **It learns on real material.** Several years of user requests to the support
  desks of various services, and public groups describing genuine problems with
  e-documents, digital signatures, tax and bookkeeping — together with how those
  problems ended.
- **It reaches people only after evaluation.** Training, a run against difficult
  cases, a check for invention, an assessment of answer quality. A bad answer in
  support costs more than no answer at all.
- **It works round the clock and at any volume** — hundreds of thousands of
  requests, in the place where a machine has an advantage people cannot have.
- **It acts on human confirmation:** it does not only advise but changes
  settings, repairs state, lifts a block. For example: a client urgently needs to
  sign a document but access is restricted because of an unpaid invoice — the
  agent works it out and **opens a one-off passage** so the person can sign now,
  while the payment question is settled separately.

**The principle behind it:** solve the person's problem first, everything else
second. We meet the user halfway before they have paid.

---

## 3.11. Horizon X — The Physical Loop: Warehouse, Customs, Delivery

> 🎯 The next big step. Here the platform reaches beyond documents for the first
> time and takes charge of the goods themselves.

### Why we want the physical world at all

Today we know everything about an item: that it was bought, at what price, under
which document, how much of it is in stock, who it was sold to. But the item
itself sits with the client, and everything that physically happens to it —
customs clearance, storage, packing, dispatch — stays outside the system, in
somebody else's hands, with no single picture of it.

The intent of this horizon: **close the chain from the border to the buyer**.

```
Goods arrive from abroad
        ▼
Customs clearance through a broker found right here    ← 3.11.2
        ▼
Goods received into our smart warehouse                 ← 3.11.1
        ▼
Unpacking · sorting · product records · labelling
        ▼
Sale: UmagShop, your own shop, any other channel
        ▼
Delivery anywhere in Uzbekistan
        ▼
Documents and money — as usual, by themselves
```

The owner does not have to buy a warehouse, employ storekeepers, find a broker or
negotiate with carriers. What they have to do is **have the goods** — the platform
takes on the rest.

### 3.11.1. 🎯 A smart warehouse and fulfilment

**What it is.** We take a large warehouse and make it smart: stock records,
placement, picking and dispatch are run by an AI agent on the very data already
living in the system — the catalogue, IKPU codes, stock levels, orders,
documents.

The client brings the goods in (or they arrive straight from customs), and from
then on:

| Warehouse service | What we do |
|---|---|
| **Storage** | The goods sit with us; stock levels are visible in the app in real time |
| **Receiving and unpacking** | We take the delivery apart, reconcile it against the documents and find the discrepancies |
| **Sorting** | We lay it out by item, by batch, by expiry date |
| **Product records** | We create the catalogue entries: photo, description, specification, IKPU code — what usually takes weeks by hand |
| **Labelling** | We apply marking codes where the goods require them |
| **Picking and dispatch** | We assemble the order, pack it and hand it to the carrier |
| **Help with selling** | The goods appear straight away on the UmagShop storefront, in the live stream and in the short videos |

**You can sell anywhere.** This matters: the warehouse is not tied to our
marketplace. The goods sit with us and can be sold on UmagShop, in your own shop,
on Instagram or over the phone — either way we handle the dispatch, through the
integrated delivery services.

**The speed target is same-day, anywhere in Uzbekistan.** For a seller that
changes the conversation with a buyer: not "I'll send it sometime this week" but
"you'll have it tomorrow".

**Why this is a logical move for us specifically.** The warehouse is the one place
where physical goods meet documents. We already have the documents: receiving is
reconciled against the incoming invoice automatically, a dispatch immediately
produces an outgoing one, stock levels do not have to be typed in, and the IKPU
codes are already matched. An ordinary fulfilment operator sees none of that — it
works with boxes, not with deals.

### 3.11.2. 🎯 Customs and brokers

**The problem.** A business has brought goods in — and runs straight into customs
clearance. Finding a broker, working out a fair price, checking whether you are
being cheated, waiting for release, learning what is happening right now — all of
it happens over the phone, in somebody else's chat threads, and blind.

**The answer is the same mechanic as on the
[accounting services exchange](#33-horizon-ii--an-exchange-for-accounting-and-outsourcing-services):**

1. **Broker firms join the ecosystem as partners** — on the same footing as
   accounting and outsourcing firms. They work with business owners and with
   their documents, and service contracts are signed automatically.
2. **The owner posts a request anonymously**: which goods, what volume, what
   deadlines. With no company details attached.
3. **Brokers see the request and send proposals** — exactly how they will clear
   it, for how much, in what time.
4. **The owner compares and chooses.** Not the first firm they came across but
   the best of several — knowing, for the first time, the market price of their
   own task.
5. **The contract is signed right here**, and the work is conducted right here.
6. **The status is visible in real time** — what stage the consignment is at,
   what is done, what remains. The owner does not phone and ask: they look.
7. **After release the goods go wherever they say** — to our warehouse (entering
   §3.11.1 immediately), to their own warehouse, or straight to the buyer.

**What it gives a business.** An importer no longer needs to keep a customs
specialist on staff, buy a warehouse for cleared goods, or hunt for a carrier:
request → proposals → choice — and from then on everything runs in one feed that
already holds their documents and their money.

### Where the revenue comes from here

This horizon is not only convenience but **revenue for the platform**: storage,
goods handling, dispatch and a fee for the broker introduction. In detail in
[09-business-model.md](09-business-model.md).

---

## 3.13. What Does Not Change

Five rules that hold on every horizon. They are the reason a business can entrust
its money and its documents to the system at all.

1. **The AI proposes — a human confirms.** Autonomy is only ever widened through
   the owner's explicit consent, revocable and bounded by amount and duration.
   Never through "we decided it was more convenient this way".
2. **The truth of the numbers.** Bookkeeping has no right to be wrong about an
   amount, VAT, a date or a code. The name behind an IKPU code always comes from
   the state catalogue. Anomalies are found by deterministic rules, not by a
   language model. One wrong figure costs more than ten new features.
3. **Nothing crosses on its own.** Purchase prices do not leak onto a storefront,
   employees' personal data does not open up along with the accounting section, a
   tax-office letter is not marked as read without an explicit act by the owner.
4. **Everything can be killed in a second.** Every feature sits behind a switch of
   its own that works without shipping a new version.
5. **Uzbek is a first language, not a translation.** Both languages carry equal
   weight everywhere: in the interface, in documents, in PDFs, in voice.

---

## 3.14. In Summary

**What already exists:** 252 modules, 18 surfaces, 24 document types, 73,098
documents processed, 85,869 deals, full coverage of Uzbekistan's e-document
system, an AI agent, live voice, integrations with 1C, MoySklad, AmoCRM,
Bitrix24, cash registers, a bank and the tax office, a marketplace with documents
attached, and Business Pulse, which shows an owner the truth about their company.

**What lies ahead:** an e-invoice that issues itself the moment the money lands;
deals that close without a human; an exchange where a business finds an honest
bookkeeper within an hour; commerce where an order leaves with a courier without
a single click; a live broadcast that produces a signed transaction; a warehouse
that takes goods straight from customs; tax filings assembled from facts and
waiting only for the owner's nod; apps in the App Store and Google Play with a
warehouse that works without a network; and **the voice that runs all of it**.

We are not building an accounting program. We are building **an environment in
which business in Uzbekistan runs itself** — while the owner gets on with what
they started it for.

---

*Back to the beginning: [ecosystem overview](README.md)*
