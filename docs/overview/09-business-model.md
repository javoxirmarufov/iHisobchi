# 9. How We Make Money

> Part 9 of 9. Back: [ecosystem](01-ecosystem.md) · [modules](02-modules.md) · [roadmap](03-roadmap.md) · [voice orchestrator](04-voice-orchestrator.md) · [security](05-security.md) · [first day](06-first-day.md) · [signing](07-signing.md) · [with us and without us](08-with-and-without.md).

---

## 9.1. The Principle: We Do Not Take a Percentage of the Deal

The first thing to say about our economics is what is **absent** from it.

**We take no commission on a client's turnover.** Not on a deal, not on a
payment, not on a marketplace order. This is not generosity but a design
decision, and three things follow from it:

1. **We have no reason to get between the two parties' money.** Funds go directly
   from the buyer's settlement account to the seller's — we do not hold them, do
   not route them and do not delay them. We work with the documents about money,
   not with the money.
2. **Our revenue does not rise because a client sold at a higher price.** So there
   is no conflict of interest: we have no incentive to push, to hurry or to
   conceal.
3. **The client understands what they are paying for.** A subscription for the
   system's work, a payment for a service, a payment for promotion. No "where did
   that 2% go?"

We earn from what **we ourselves do for the client**: we provide a tool, we
provide infrastructure, we provide a service, we provide buyers' attention.

---

## 9.2. Eight Revenue Streams

| # | Stream | What we sell | State |
|---|---|---|---|
| 1 | **Subscription** | Access to the platform on a plan | 🔵 Plans defined, billing under construction |
| 2 | **Promotion in UmagShop** | Impressions of products and videos to buyers | 🎯 Together with the [video section](03-roadmap.md#352--short-seller-videos--and-the-marketplaces-first-real-revenue) |
| 3 | **Corporate environment** | A dedicated hosted server or an on-premise install | 🎯 In preparation |
| 4 | **Warehouse and fulfilment** | Storage, goods handling, dispatch | 🎯 [Horizon X](03-roadmap.md#311-horizon-x--the-physical-loop-warehouse-customs-delivery) |
| 5 | **Service exchanges** | Introducing businesses to bookkeepers and brokers | 🎯 Horizons II and X |
| 6 | **The accounting firm workspace** | A fee per client served | 🎯 [Horizon III](03-roadmap.md#34-horizon-iii--the-accounting-firm-workspace) |
| 7 | **Business-activity certificate** | A company's verified history — issued at its own decision | 🎯 An idea; needs legal work |
| 8 | **Implementation and a partner network** | Turnkey rollout, training, integrator certification | 🎯 Can begin now |

Different streams for different clients, and that is deliberate. A micro-business
pays only the subscription; a trading company adds promotion and the warehouse; a
corporation buys an environment; an importer buys customs clearance and goods
handling; an accounting firm pays for its clients; someone who needs credit pays
for a certificate. The platform grows with the client rather than squeezing
everything out of one plan.

**Three of the eight need no new large subsystems** — the accounting firm
workspace, the certificate and implementation all rest on what is already built
and already in the database.

---

## 9.3. Stream 1: Subscription

The foundation. A business pays for the system working on its behalf every day.

| Plan | Price per month | Who it is for |
|---|---|---|
| **Light** | **250,000 UZS** | Sole traders, micro-businesses, a few documents a week |
| **Pro** | **490,000 UZS** | A small business with a bookkeeper: integrations, automatic documents, banking, deals |
| **Max** | **990,000 UZS** | Active trading, several organisations, a heavy flow of documents and AI |

**What separates the plans.** Not the number of buttons but access to things that
are heavy and expensive for us: document volume, the number of organisations and
staff, the depth of AI-agent and voice-orchestrator use, connections to external
systems (1C, MoySklad, CRMs, banking, cash registers), signing modes, support
priority.

The exact contents of each plan will be fixed together with the billing launch —
which is why what is stated here is the prices and the principle, rather than a
checklist that would have to be rewritten.

**Free entry stays.** Basic document work in the Telegram bot and demo mode are
available at no charge: a person should first see what the product does and only
then pay. This matches our
[position on support](08-with-and-without.md#87-support-our-position) — solve the
problem first, everything else second.

**Honest about the current state:** the plan interface is ready but the payment
loop is still being built — access is currently granted by invitation. This is the
first thing to close on the commercial side.

---

## 9.4. Stream 2: Promotion in UmagShop

The marketplace takes no commission on an order. It earns from **buyers'
attention** — and that is a far more honest model for B2B, where deals are large
and a percentage of them would be indecently big.

**What the seller pays for:**

- impressions of their
  **[short videos](03-roadmap.md#352--short-seller-videos--and-the-marketplaces-first-real-revenue)**
  in the marketplace feed;
- top positions in categories, curated collections and search results;
- participation in the
  **[live stream](03-roadmap.md#351--247-live-streaming--commerce-you-can-watch)**;
- banners on the home page and in themed sections.

**How it is charged.** The model is **payment per thousand impressions**: the
seller pays for their product actually being seen, not for the fact of placement.
The rate per thousand impressions is not fixed yet — it has to be set against live
traffic, once the feed has an audience. Naming a figure in advance would be
guesswork.

**Why this will work better than social advertising.** We know something about our
audience that no ad network does: **what this business buys and what it sells** —
from its own documents. So a clip about packaging is shown to firms that buy
packaging, rather than to "men aged 25–45". The advertising reaches the people who
need it — which is why it is worth its price.

---

## 9.5. Stream 3: The Corporate Environment — Hosted and On-Premise

A separate category of client: those whose security policy forbids storing data
with a third-party provider — large companies, banks, government bodies,
outsourcing firms holding hundreds of client keys.

**Two formats** (in detail:
[07-signing.md §7.7](07-signing.md#77-for-corporations-a-dedicated-environment-or-an-on-premise-install-)):

| Format | What the client gets | Who operates it |
|---|---|---|
| **A dedicated hosted environment** | A separate server running our software, with their keys and their data. None of their data sits on our main servers | Us: updates, monitoring, recovery |
| **An on-premise install (the "box")** | Our software on their hardware, inside their perimeter. Not a single request carrying their data reaches us | Them, with our support and updates |

**Pricing is per project.** There is no price list here and there cannot be: the
cost depends on scale, the number of organisations, load, support requirements and
contract length. This is classic enterprise delivery and it is priced
individually.

**Why this is a valuable stream.** One such contract is comparable to hundreds of
subscriptions, and the client stays for a long time: replacing a system deployed
inside your own perimeter is far harder than cancelling a service.

---

## 9.6. Stream 4: Warehouse and Fulfilment

Here the platform starts earning for the first time from **physical work with
goods** — see [Horizon X](03-roadmap.md#3111--a-smart-warehouse-and-fulfilment).

**What the client pays for:**

| Service | How it is charged |
|---|---|
| **Storage** | By space and duration |
| **Receiving and unpacking** | Per delivery or per item |
| **Sorting and preparation** | By volume of work |
| **Product records** | Per item: photo, description, specification, IKPU code |
| **Labelling** | Per unit |
| **Picking and dispatch** | Per order |
| **Delivery** | The carrier's tariff plus handling |

**Why a client will choose us over an ordinary fulfilment operator.** An ordinary
operator works with boxes: it does not know what the documents say is inside them,
cannot reconcile a receipt against an incoming invoice, will not create a catalogue
entry with the right IKPU code, and will not produce the dispatch documents. We do
all of that **on the very data already in the system** — the goods and their
paperwork are in one place.

**What it gives a business.** It stops buying warehouses, hiring storekeepers and
employing a logistics manager. What it needs is for the goods to exist; everything
else is a service paid for as used.

---

## 9.7. Stream 5: Service Exchanges

Two exchanges inside the ecosystem, built the same way:

- **[Accounting and outsourcing services](03-roadmap.md#33-horizon-ii--an-exchange-for-accounting-and-outsourcing-services)**
  — the owner describes the problem anonymously, partner firms send proposals, and
  they pick the best one.
- **[Customs and brokers](03-roadmap.md#3112--customs-and-brokers)** — the same
  thing for customs clearance: an anonymous request, brokers' proposals, a choice,
  a contract, and real-time tracking of the consignment.

**Where the revenue comes from.** We bring demand and supply together and provide
the loop of trust: anonymity of the request, comparable proposals, a contract and
a signature, the conduct of the work, and partner reputation based on tasks
actually closed. For that, the **partner** pays — the side that gains a client —
not the business looking for help. An owner with a problem should get the
marketplace for free.

The exact form (a partner retainer, a fee per introduced request, or a package)
will be settled together with the launch of the first exchange.

---

## 9.8. Stream 6: The Accounting Firm Workspace — a Fee per Client Served

One outsourcing firm keeps the books of 20–50 companies. Today, to work in
iHisobchi, it has to switch between accounts; tomorrow it will have a
[single workspace](03-roadmap.md#34-horizon-iii--the-accounting-firm-workspace)
with every client in one list, batch operations and a shared calendar of
deadlines.

**The model is not a subscription for the firm but a fee per client served**,
noticeably below the individual plan price. The arithmetic suits both sides: the
firm pays less for forty companies than forty separate subscriptions would cost,
and we earn several times more from one contract than from one subscription.

**Why this is the most effective growth channel there is.** One outsourcer brings
in forty companies **of its own accord** — because that is how it prefers to work.
No advertising spend, not a single cold call.

**The technical foundation already exists:** multi-TIN support through proof of
key ownership lets a single signing agent serve a hundred client keys
([07-signing.md](07-signing.md#73-method-2-an-agent-program-on-the-computer--signing-from-a-phone)).
The demand is visible even at today's scale: 13 owners already hold more than one
organisation, and one holds five or more.

---

## 9.9. Stream 7: The Business-Activity Certificate — Issued Only by the Business Itself

**An idea that inverts the usual scoring arrangement.** Normally ratings are
compiled *about* a company and sold *to somebody else*. We do the opposite: **the
business orders the certificate itself, about itself, and decides for itself who
sees it.**

### Why a business wants it

Small business in Uzbekistan constantly runs into "prove it":

| Who has to be convinced | Of what |
|---|---|
| **A bank**, on a credit application | That the turnover is real rather than painted on |
| **An investor** | That deals close rather than hang |
| **A large buyer** in a tender | That the supplier meets its obligations |
| **A new supplier** offering deferred payment | That the goods will be paid for |
| **A landlord, a lessor, an insurer** | That the company is alive and disciplined |

Today the answer is a stack of papers from the bank and the tax office, gathered
over weeks. Here all of it **already exists in the system** and is backed by signed
documents.

### What the certificate contains

Only **facts we observed** — not an assessment and not a rating:

- how many deals were completed in a period and for what total;
- what share of them **closed in full**, with signed documents;
- the average time from shipment to payment — payment discipline, in days;
- the regularity of document flow: how long and how steadily the company has been
  operating;
- how many counterparties there are and what share of them are regulars.

**We do not issue a creditworthiness score and we do not call this a rating.**
That is neither our role nor our licence. We confirm observable facts, and the
reader — a bank, an investor, a buyer — draws the conclusion.

### How the trust is constructed

| Principle | How it is implemented |
|---|---|
| **Only at the owner's decision** | Issuing is enabled in the settings. Off by default — a firm's condition belongs to the firm |
| **Every issue is a separate consent** | Not "permitted once and forgotten": the owner sees who received a certificate and when |
| **One-tap revocation** | The issued link goes dark and the certificate stops opening |
| **Verifiability** | The certificate has its own address and QR code: a bank opens it and confirms the document is genuine and unedited |
| **A validity date** | The certificate is bound to a date: month-old data is not passed off as today's |
| **An honest coverage boundary** | The certificate itself states **what share of the turnover we can see**. If a company runs half its deals outside the system, it says so plainly. A certificate that misleads a bank devalues every other one |

### How this earns

**The business itself pays** — for issuing a certificate, or for an "always
current" subscription where the document is needed regularly (tenders, several
banks, regular suppliers offering deferred payment).

A natural extension is **a badge on the storefront**: a seller with a verified
history can display it in their shop on
[UmagShop](02-modules.md#i-umagshop--a-marketplace-with-documents). For a B2B
marketplace where the parties do not know one another, that is the strongest trust
signal there is — and one more reason to buy the certificate.

### Why only we can do this

A bank handed a certificate normally has no way to verify it. Here it does: behind
every figure stand **documents digitally signed inside a state system** and the
movement of money through an account. This is not a form filled in on the owner's
say-so — it is a consolidated picture of what actually happened.

**What has to be done before launch:** legal review of the wording (we confirm
facts, we do not assess solvency), agreement with banks on recognising the
certificate, and a verification mechanism on their side.

---

## 9.10. Stream 8: Implementation, Training and a Partner Network

The simplest stream — and simultaneously the cure for the product's main
constraint.

**Paid implementation** for companies that want a result rather than an app:
migrating the catalogue and counterparties, connecting the bank, the cash register
and the accounting system, setting up signing, training the bookkeeper and the
owner, and support through the first month.

**Certified implementation partners.** A programme for integrators and IT
companies: training, certification, access to materials, referred leads. The
partner pays to take part in the programme and earns from the implementations
themselves.

**Why this is worth doing earlier than it seems.** We have 80 organisations, of
which 57 create documents — meaning the product's constraint is not in features
but in getting people to regular use. Implementation solves exactly that: **revenue
and activation in one movement**. And a partner network scales implementation
without growing our own team.

---

## 9.11. What Already Brings Money and What Does Not Yet

An honest picture, with no rounding in our own favour.

| Stream | Today |
|---|---|
| Subscription | 🔵 Plans defined, the payment loop under construction; access granted by invitation |
| Promotion in UmagShop | 🎯 Arrives together with the video section |
| Corporate environment | 🎯 Technically possible already; not packaged as a product |
| Warehouse and fulfilment | 🎯 Horizon X |
| Service exchanges | 🎯 Horizons II and X |
| Accounting firm workspace | 🎯 The technical foundation exists (multi-TIN); it needs an interface and a plan |
| Business-activity certificate | 🎯 The data exists in full; it needs legal wording and recognition by banks |
| Implementation and partner network | 🎯 Needs no development — it needs people and a programme |

**The conclusion that follows.** The product is built broadly, but the commercial
loop is its youngest part. That is not a hidden weakness but a deliberate
sequence: first we turn what already works into regular use (see
[priorities](03-roadmap.md#what-we-are-working-on-first)), and then we charge for
it. Nobody will pay for a tool they do not use every day — and they would be right
not to.

---

## 9.12. Why This Model Is Durable

**The eight streams do not compete; they compound.** A client arrives for
documents on a subscription, then places goods in the warehouse, then promotes
them on the storefront, then asks a broker for help. Each step is a distinct piece
of value and a distinct payment, and all of them run on the same data.

**Every stream rests on something a competitor does not have.** Promotion rests on
knowing what a business buys and sells. The warehouse rests on the goods and their
documents being in one place. The exchanges rest on the task's documents already
being digitised. The corporate environment rests on the product being deployable
in its entirety at the client's site. Any one stream can be copied; copying the
combination means building the whole platform.

**And what does not change under any pricing:** we take no percentage of a deal,
we do not hold clients' money and we do not sell their data. The platform's
economics are built so that our revenue grows because the client finds it **more
convenient**, not because they have **nowhere else to go**.

---

*Back to the beginning: [ecosystem overview](README.md)*
