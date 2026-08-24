# 8. With Us and Without Us

> Part 8 of 9. Back: [ecosystem](01-ecosystem.md) · [modules](02-modules.md) · [roadmap](03-roadmap.md) · [voice orchestrator](04-voice-orchestrator.md) · [security](05-security.md) · [first day](06-first-day.md) · [signing](07-signing.md). Next: [business model](09-business-model.md).

---

## 8.1. How the Market Works Today

Before saying how we differ, we have to show honestly **what a business currently
has to assemble its workplace out of**. We surveyed the market from public
sources.

### E-document exchange: 15 operators, all doing the same thing

Uzbekistan has **15 accredited e-document operators**. Roaming works between them,
so the choice of operator does not affect the ability to exchange documents — only
the price and the interface:

| Operator | Free allowance | Price per document |
|---|---|---|
| Soliqservis | 10/month free | 300–500 UZS |
| Faktura.uz *(the first official operator)* | none | from 50,000 UZS/month |
| **Didox** | 10 outgoing/month | 350–800 UZS |
| E-docs | 10 outgoing/month | 190–750 UZS |
| 1UZ Kuryer | 150 documents free | 300 UZS |
| Hujjat.uz | 15 outgoing/month | 400–600 UZS |
| L-Factura | none | 199–249 UZS |
| Contracts | 50 outgoing/month | 500–600 UZS |
| …and seven more | | 200–700 UZS |

**What that means.** Every operator solves one problem: deliver a document and
register it in the state system. None of them deals with what happens **around**
the document: the payment, the stock, the deal, the reporting, the correspondence
with the tax office. That is not a criticism — it is their role.

We work **on top** of that layer, through Didox. We do not compete with
e-document operators — we compete with the assembly of five to seven programs a
business is forced to keep around them.

### Accounting and trading software: a separate universe of its own

The market for trade and warehouse automation is crowded — BILLZ, SmartUp,
MoySklad, EasyTrade, Paloma 365, Bito ERP, Regos, HIPPO, OX System, Optimo,
Sellerpeak and others. Each covers its own patch: the till, the warehouse, a CRM,
purchasing, staff, analytics.

**The key observation from our market review:** among them there is no solution
that unites **e-documents + warehouse + CRM + bank + tax office in one loop**. The
closest is a single ERP ecosystem, and even that does not cover the full circle.

We are not trying to be a better warehouse program than MoySklad, or a better CRM
than AmoCRM. We **connect** them — and build what none of them has at all.

---

## 8.2. A Business's Working Day Without Us

This is how it looks today at a typical trading company. Every row is a separate
program, a separate login, a separate bill, a separate configuration.

| Task | What covers it | What it costs |
|---|---|---|
| Issue an e-invoice | the e-document operator's portal | 30–60 minutes of manual entry, plus hunting for the IKPU code in the Tasnif catalogue |
| Sign it | E-IMZO on a computer | only at that PC, only with the USB key, with a password prompt in the way |
| Post it to the books | 1C or a cloud accounting package | the same figures typed in a second time, by hand |
| Warehouse and stock | a warehouse package | the same products entered a third time |
| Customers and deals | AmoCRM / Bitrix24 | counterparties entered a fourth time |
| Find out whether money arrived | internet banking | a separate login, a statement export, reconciliation in Excel |
| Letters from the tax office | the my.soliq.uz portal | manual sign-in with a digital signature, checking "has anything come in?" |
| Fiscal cash-register receipts | the cash-register portal | downloading files one at a time |
| Understand what is happening in the business | Excel | assembled by hand and out of date the moment it is saved |
| A legal document | an outside lawyer | expensive and slow |
| Reporting | the bookkeeper, manually | days of work and a risk of error |

**In total: 7–9 systems, none of which knows the others exist.** The connective
tissue between them is a person. They move the same data across three or four
times, and it is on those transfers that the errors arise which later turn into
penalties.

And one more trait common to all of these systems: **they are built as
prohibitions.** Rigid forms, fixed scenarios, "you can't do that", no autonomy, no
AI. The program does not help — it demands that the human bend to fit it.

---

## 8.3. The Same Day With Us

| Task | What happens |
|---|---|
| Issue an e-invoice | By voice, from a photograph of a delivery note, or pasted from Excel. IKPU codes matched, VAT calculated, buyer filled in. **2–5 minutes** |
| Sign it | From a phone, from home, at night — [four signing methods](07-signing.md), including a round-the-clock server |
| Post it to the books | The document is **already** in the system. With 1C or MoySklad connected, it travels there by itself |
| Warehouse and stock | The same catalogue the documents use. An accepted incoming invoice changes stock levels on its own |
| Customers and deals | Counterparties pulled in from the e-document history. Deals assemble themselves from the documents |
| Find out whether money arrived | A Telegram push, tied to its contract and invoice |
| Letters from the tax office | Delivered to Telegram, with an explanation and a deadline reminder |
| Fiscal cash-register receipts | Pulled in automatically, posted to the books, reconciled against the documents |
| Understand what is happening | Business Pulse: one page in plain language plus a detector for unusual transactions |
| A legal document | The AI Lawyer: a claim, a lawsuit, a contract — citing Uzbek statutes |
| Reporting | The basis is assembled by the system; [full automation](03-roadmap.md#39-horizon-viii--tax-reporting-that-prepares-itself) is the next horizon |

**One system. One way in. One AI that sees all of it at once.**

---

## 8.4. The Difference Integrations Cannot Close

One could object: "we will connect our programs with integrations and get the
same thing". You will not, and here is why — three things only arise when the data
lives in one loop from the outset.

**1. The deal as a whole.** The contract, the payment, the power of attorney, the
e-invoice, the act and the waybill become **one entity** with a state and an
answer to "whose move is it". An integration between a warehouse and a bank does
not give you that: it passes records, not meaning. Our engine holds 85 thousand
deals, 73% of them closed automatically.

**2. The owner sees the truth.** Business Pulse can look for duplicate payments,
structured amounts and turnover without documents only because it sees money,
documents, stock and the till **simultaneously**. No single program sees that —
each has only its own fragment.

**3. An AI that knows the business.** You can tell the voice orchestrator "invoice
Artel for the same as last time but at the new price" — because it knows Artel,
and last time, and the current prices, and the stock. An assistant plugged into
one program out of seven physically cannot construct that answer.

---

## 8.5. What Exists Nowhere Else

Features for which we found no equivalent on the Uzbek market.

| What | Why it matters |
|---|---|
| **Official mass-mailing of commercial proposals** | Send a proposal to hundreds of counterparties in one action — legally significant, through the e-document system. Detailed below, §8.6 |
| **Running a business by voice** | Not voice input but an [orchestrator](04-voice-orchestrator.md) that executes operations through conversation |
| **Business Pulse** | An X-ray of the company for the owner, including a detector for transactions being hidden from them |
| **The deals engine** | Automatic assembly of a chain of documents and money into a deal with a state |
| **24/7 signing without your own PC** | Your own server in one command, or a turnkey vault cell |
| **Tax-office letters in a messenger** | With an AI explanation and a deadline reminder |
| **Live streaming that ends in a transaction** 🎯 | A round-the-clock broadcast of goods with orders placed live on air and an AI presenter. Plenty of people have live commerce; live commerce that ends in a signed contract and an invoice, nobody does ([§3.5.1](03-roadmap.md#351--247-live-streaming--commerce-you-can-watch)) |
| **A marketplace where the order becomes the documents** | [UmagShop](02-modules.md#i-umagshop--a-marketplace-with-documents): everywhere else an order ends in a basket; here it ends in a signed invoice |
| **An AI Lawyer citing Uzbek statutes** | The claim and the lawsuit inside the same system that holds the documents the case is about |

---

## 8.6. Mass-mailing of Commercial Proposals — What Nobody Else Has

> ✅ In production

### A problem nobody had solved

With an e-document operator you can send **an arbitrary document** — one at a
time, by hand, to each recipient separately. Sending **a commercial proposal to
many recipients at once** is not possible anywhere.

And the need is enormous. Picture it:

> A supplier has a batch of goods left that has to be sold at a 30% discount
> before the end of the month. Their database holds 300 counterparties. Phoning
> them all is several days of a sales manager's work, and half of them will not
> pick up. Messaging each of them on Telegram is not serious enough for a
> wholesale deal worth tens of millions. E-mailing them lands in spam and carries
> no status at all.

The same situation faces any business: a new service, a price-list update, a
seasonal offer, the hunt for a buyer for remaining stock, an invitation to a
tender.

### How it works here

**1. The recipient list, however you like it.** Paste it as text into the chat, or
attach a file: `.txt`, `.csv`, `.xlsx`, `.docx`, even `.pdf`. The system finds the
TINs (9 digits) and PINFLs (14 digits) inside it and removes duplicates. If the
list is messy — an export from somebody else's program, a spreadsheet with headers
and footnotes — the AI steps in and parses it.

**2. Recipients are identified.** Every TIN is checked against the state register:
the organisation's name and address are pulled in. The owner sees **a list of
companies**, not a column of digits, and can strike out the wrong ones before
sending.

**3. One proposal, delivered to everyone.** The commercial proposal is composed
once, and then the system builds an official document **for each recipient**,
signs it with your digital signature and sends it through the e-document system.
In their account it appears as an ordinary incoming document from your company —
with full company details and legal force, not as a marketing e-mail.

**4. Progress is visible.** A single message in the chat updates as it goes: how
many sent, how many delivered, where a rejection occurred. Each recipient's state
is persisted, so the campaign survives a restart and **never sends duplicates**.

### What is built in

| Parameter | Value |
|---|---|
| Recipients per campaign | up to **20,000** |
| List input | text, `.txt`, `.csv`, `.tsv`, `.xlsx`, `.docx`, `.pdf` |
| Recipient identification | TIN and PINFL, deduplication, a check against the register |
| Signing | your digital signature, document by document |
| Sending pace | deliberately throttled, so as not to overload the e-document system or look like spam |
| Concurrent campaigns | one per organisation — protection against an accidental duplicate |

Signing runs sequentially: the signature channel is physically singular per TIN,
and trying to parallelise it would produce race conditions rather than speed.

### What this opens up for a business

**Sales stop being limited by the number of sales staff.** One proposal reaches
three hundred companies in the time it would take a manager to make ten phone
calls — and it reaches them **as an official document**, which the recipient sees
in their working account next to invoices and contracts rather than in a
"Promotions" folder.

There are as many uses as there are reasons to address the market: clear remaining
stock, announce a new price list, offer a service, look for a contractor, invite
firms to a tender, notify counterparties of changed terms. **We gave businesses a
direct channel to the market that they simply did not have.**

---

## 8.7. Support: Our Position

> 🔵 In development

A word on something we consider no less important than features.

### The principle

**We meet the user halfway before they have paid.** If someone has a problem, it
needs solving, and the conversation about money can come afterwards. A business
entrusts us with its documents, its signatures and its money; in that kind of
work, support is not a department but part of the product.

We treat every request as urgent by default. For a business, "wait until Monday"
can mean a missed shipment, a missed deadline to answer the tax office, or a month
that cannot be closed.

### What we are building

Not a bot that collects the question and hands it to a human — there are plenty of
those and they irritate everyone. **A specialised AI support agent** that answers
on the substance and is able to act.

**What it learns on.** We have been collecting real material for several years:
users' requests to the support desks of various services, public groups where
people describe their problems with e-documents, digital signatures, tax and
bookkeeping — and how those problems ended. Not invented scenarios but the actual
situations of Uzbek business, with their actual resolutions.

**How we prepare it.** The agent is trained on that material and then put through
checks: how it answers, whether it invents things, whether it copes with rare
cases. **It reaches users only after it passes evaluation.** A bad answer in
support costs more than no answer at all.

**What it will be able to do:**

- **Answer instantly, round the clock**, sustaining hundreds of thousands of
  requests — the place where a machine has an advantage people cannot have.
- **Explain what is going on** — in the user's own language, not as a link to a
  manual.
- **Act, on human confirmation.** Not only advise but change settings, repair
  state, lift a block.

**The example this is being built for.** A client urgently needs to sign a
document, but access is restricted — say their account has gone into arrears. By
the old logic they write to support and wait until morning while the shipment
stands still. Our agent works out the situation and **opens a one-off passage** so
the person can sign the document right now — and the payment question is settled
separately and later.

That is the position we want to hold: **solve the person's problem first,
everything else second.** That is what keeps a business with a product for years —
not a list of features.

---

## 8.8. In Brief

**Without us:** seven to nine programs, none of which knows the others exist, with
a human carrying the data across three times, no AI, no autonomy, and everything
built as a set of prohibitions.

**With us:** one loop in which a document immediately becomes part of a deal, the
deal reconciles itself against the bank and the tax office, the owner sees the
truth about their company — and all of it can be run by voice.

We do not replace the tools a business is used to — we become the layer in which
they finally start working together.

---

**Market sources:**
[BUXGALTER.UZ — a comparison of e-document operators](https://buxgalter.uz/publish/doc/text171838_kak_opredelitsya_s_operatorom_esf_sravnitelnaya_tablica) ·
[FAKTURA.UZ](https://faktura.uz/) ·
[Didox.uz](https://didox.uz/) ·
[BILLZ — a review of 20 automation packages in Uzbekistan](https://billz.io/blog/avtomatizatsiya-biznesa-v-uzbekistane-obzor) ·
[Smartup](https://smartup.one/) ·
[MoySklad Uzbekistan](https://www.moysklad.uz/)

*Operator and software data as of August 2026, from public sources. Tariffs
change; re-check them before using any of this in commercial material.*

---

*Back to the beginning: [ecosystem overview](README.md)*
