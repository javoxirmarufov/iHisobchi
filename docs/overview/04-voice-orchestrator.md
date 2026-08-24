# 4. The Voice AI Business Orchestrator

> Part 4 of 9. Back: [ecosystem](01-ecosystem.md) · [modules](02-modules.md) · [roadmap](03-roadmap.md). Next: [security](05-security.md) · [first day](06-first-day.md) · [signing](07-signing.md) · [with us and without us](08-with-and-without.md) · [business model](09-business-model.md).

---

## 4.1. The Product's Main Bet

Everything described in this overview — documents, deals, inventory, banking,
tax, HR, the marketplace — was built with one final purpose:

> **The owner talks. The business works.**

Not "voice input". Not "commands to an assistant". A **manager** — an AI that
knows this company in full: its products and prices, its counterparties and how
reliably they pay, its stock, its debts and obligations, its documents and
deadlines. You speak to it the way you would speak to a capable managing
director:

> "What's happening with Artel?"
> "Invoice them for the same laptops as last time, but at the new price."
> "How much tax do we owe before the end of the month?"
> "Who hasn't paid for over a month — write to all of them."
> "What are we running out of in the warehouse?"

And it **does it** — it does not locate a menu section, it performs the operation
in the system.

This is not a bolt-on. It is the interface the product has been heading towards
all along: every capability written over these months was written so that it
could be invoked not only by a finger but by a voice.

---

## 4.2. Why This Is Possible Specifically Here

Everyone has a voice assistant that can talk. The difference is in **what it can
reach**.

Our voice does not sit on top of the product but **inside its core**: it invokes
the same capability registry the interface buttons use (see
[the architecture](01-ecosystem.md#15-how-it-works-inside-one-brain-many-windows)).
Three things follow that cannot be copied quickly:

**1. The voice can do exactly what the app can.** Not a separate, cut-down, less
scrutinised branch of code — the same operations, with the same checks on
amounts, VAT, IKPU codes and permissions. It is physically incapable of making a
different mistake from the one the interface would make.

**2. Every new product feature becomes a voice feature immediately.** We do not
write a feature twice. A section appears — a capability appears — and the voice
already knows it.

**3. It sees the whole business at once.** Answering "can we ship to Artel on
credit?" requires, simultaneously: the deal history with that counterparty, their
payment discipline, current stock, receivables and the account balance. In any
other system that is four different programs and half a day of a bookkeeper's
time. Here it is one spoken question.

---

## 4.3. What the Orchestrator Can Already Do, Module by Module

The registry's capabilities are available to the voice as they are. Below is what
that means in practice for each part of the business.

| Module | What you can ask for and delegate by voice |
|---|---|
| **Documents** | "Show me what isn't signed", "what's the status of invoice 145", "find every document for Artel in July", "issue an invoice for…", "make a waybill from this delivery note", "draft a contract for…" |
| **Deals** | "What's still open?", "whose move is it on the deal with…?", "re-check this deal", "link this payment to this contract", "show me everything where we shipped and were not paid" |
| **Money and banking** | "How much is in the account?", "did the money from… come in?", "what did we receive this week?", "how much are we owed and since when?", "show me the cash movement for the month" |
| **Business Pulse** | "How is the company doing?", "what needs attention?", "how many days of cash do we have?" |
| **Tax** | "Are there letters from the tax office?", "what do they want and by when?", "how much went through the till today?", "show me the latest receipts" |
| **Inventory and products** | "What's running out?", "how much… is left?", "find the IKPU code for…", "add the product…" |
| **Counterparties** | "Check TIN…", "who are our biggest buyers?", "how much have we traded with… this year?" |
| **Reports** | "How much did we sell this month?", "compare that with last month", "show me VAT", "who buys the most" |
| **UmagShop marketplace** | "How many orders?", "what sells best?", "write descriptions for these products", "add these items to the shop" |
| **Incoming mail** | "What's arrived?", "show me the incoming document from…", "accept it" *(with confirmation)* |
| **Instalments** | "Who has missed a payment?", "how much are we owed on instalment plans?" |

Irreversible operations — signing, sending, accepting an incoming document — are
**prepared and presented** by the orchestrator, and executed after confirmation.
How exactly that works is in §4.5.

---

## 4.4. Which Devices It Runs On

**Everywhere a person has a voice and a connection.** The orchestrator lives in
the app, and the app lives on every surface at once:

| Where | What it looks like |
|---|---|
| **Phone, Telegram** | The "Assistant" section in the Mini App — press and talk |
| **Phone, browser** | The same app at `app.ihisobchi.uz`, installed to the home screen — works without Telegram |
| **Computer** | The same section in a browser: useful when you want to talk and see cards and tables at the same time |
| **Tablet, any screen** | The interface is responsive; the voice loop does not depend on screen size |
| **Voice messages in the bot** | Anyone used to Telegram dictates a voice message, and the agent handles it the same way |
| **Native iOS / Android apps** | [The next horizon](03-roadmap.md#38-horizon-vii--mobile-applications-ios-and-android) — background work and fingerprint confirmation arrive there too |

One conversation, one business context, one set of permissions. Nobody "enters
voice mode" — the voice is simply present wherever the product is.

---

## 4.5. Why a Business Can Be Trusted to It

Running a company by voice is worth exactly as much as it can be trusted.
So trust here is built on construction, not on the model's promises.

**It reads silently and changes things in the open.** Anything that only reads
(stock, statuses, amounts, reports) executes immediately. Anything that changes
the world (signing, sending, accepting a document) is shown to a human first.

**The confirmation phrase is composed by the server, not by the model.** This is
the crucial detail. When the orchestrator says "signing invoice number 145 for
eighteen million for Artel", those words were assembled by our code out of the
actual operation about to execute. The model cannot say one thing and do another:
it does not compose that line.

**Consent has to be genuine.** In voice-confirmation mode the system accepts a
"yes" only when: the person started speaking while the speaker was already silent
(so it is not an echo of the assistant's own voice), the client confirmed that
playback had finished, the consent window is still open (45 seconds), and the
person's answer is actual agreement rather than a murmur mid-sentence. An
additional safeguard: by invariant, the confirmation phrase itself contains not a
single word from the agreement list — which is verified by a test.

**Identity is not the voice.** We deliberately do not use the voice as proof of
identity: voiceprints are neither collected nor compared. A person is identified
the same way as in the app — by a cryptographic session signature. A recorded or
synthesised voice grants access to nothing.

**Everything is recorded.** Every action by the agent is written to a separate
log with no personal data in it: what was done, when, in which business, with
what outcome.

**It can be killed instantly.** The voice loop has switches of its own — one for
voice, one for its right to take actions, one for tap-free confirmation. Any of
them can be flipped in a second, with no new version shipped.

**Data does not stay with the provider.** Speech and the content of the
conversation are processed in zero-data-retention mode, and we do not assume this
— we **verify it on a schedule**; details in
[05-security.md](05-security.md#55-zero-data-retention-what-happens-to-data-inside-the-ai).

---

## 4.6. Where This Is Going: 99% on the Agent, 1% on the Owner

> 🎯 The next horizon

Today the agent does the work and asks permission for every irreversible action.
That is right for a stage at which trust is still being built. But the final
picture is different, and we are moving towards it deliberately:

**Ninety-nine per cent of the operational work is done by the agent. One per cent
— where a human decision is needed — it brings to the owner.**

What that looks like in a working day:

- A payment arrives → the agent finds the contract itself, produces and sends the
  e-invoice, closes the deal. **The owner sees a receipt, not a question.**
- A supplier sends an incoming document from a familiar counterparty for a normal
  amount → accepted, posted to the books, stock updated.
- Stock reaches its threshold → a purchase order to the supplier is prepared, all
  that remains is a nod.
- A filing deadline arrives → the return is assembled from actual data and awaits
  approval.
- But when the amount is out of the ordinary, the counterparty is new, the
  document is unusual or something does not add up — **the agent stops and
  asks**. With an explanation, with the figures, with a proposed answer.

The owner does not confirm a hundred operations a day. They look at a feed of
what was done and take a handful of real decisions — the kind that made them the
owner in the first place.

### What has to be built for that

We do not claim this as a property of today. Giving the agent the right to act
without asking requires things that do not yet exist, and they are being built:

| What | Why |
|---|---|
| **Explicit standing permission** | Not "we decided it was more convenient" but the owner's consent: for which operations, up to what amount, with which counterparties, for how long |
| **One-tap revocation** | Permission is withdrawn instantly, together with any operations already queued |
| **Boundaries of autonomy** | An amount limit, a list of document types, a counterparty whitelist, an expiry date |
| **Raising the bar with risk** | The more unusual the operation, the stricter the treatment: from "done, here is the receipt" to "we need you" |
| **Handling the abnormal** | What to do when half a chain succeeded and half failed; how to roll back, how to correct it, who finds out |
| **A feed of what was done** | The owner must be able to see everything the agent did on their behalf within a minute, and expand any action down to its evidence |

Separately: the right to sign is a legally significant act, and the authority
model for autonomous signing is being drawn up as a decision of its own, with
legal review — not as a setting in the interface.

---

## 4.7. Why We Regard This as a Generational Change

Over the past thirty years, running a business has travelled a path: paper →
spreadsheets → accounting programs → apps on a phone. Every step **reduced the
number of clicks**, but not one removed the essential thing: a person still has
to know **where to click**.

The voice orchestrator removes that too. The owner no longer has to know which
section the reconciliation statement lives in, how a power of attorney differs
from the newer form of power of attorney, or in what order a deal is closed. They
talk about the business — the system knows how it is done under Uzbek law.

We are convinced that in a few years this is simply what working with business
systems will look like, and we want Uzbekistan to get there first — in Uzbek and
Russian, with local documents, a local tax authority and local banks.

---

**Next:** [5. Security and trust](05-security.md) — what underpins the right to
entrust all of this to a system.
