# 7. Document Signing

> Part 7 of 9. Back: [ecosystem](01-ecosystem.md) · [modules](02-modules.md) · [roadmap](03-roadmap.md) · [voice orchestrator](04-voice-orchestrator.md) · [security](05-security.md) · [first day](06-first-day.md). Next: [with us and without us](08-with-and-without.md) · [business model](09-business-model.md).

---

## 7.1. The Problem Nobody in Uzbekistan Had Solved

The **E-IMZO** digital signature is mandatory: without it a document will not
reach the counterparty and carries no legal force. And it works like this:

- you need a **computer** with the E-IMZO module installed;
- you need a **physical key** — a USB token or a `.pfx` file on disk;
- every signature pops up a **password prompt** for the key;
- which means you can sign **only while sitting at that computer**.

What that means in life. The director is away on business — the documents wait.
The bookkeeper is ill — the shipment stands still. A payment arrives on Friday
evening — the invoice goes out on Monday. An outsourcing firm handles forty
clients — forty keys on one desk and forty password prompts a day.

We built **four ways to sign**, from the classic to the fully autonomous. The
client chooses one at setup and can change it whenever they like. Separately, for
corporations with security policies of their own, there are two further delivery
formats — [§7.7](#77-for-corporations-a-dedicated-environment-or-an-on-premise-install-).

| | Method | Computer needed? | Sign from a phone | Works 24/7 | Where the key lives |
|---|---|---|---|---|---|
| 1 | **From the browser** | yes, seated at it | no | no | on the client's PC |
| 2 | **An agent program on a PC** | switched on | **yes** | while the PC is on | on the client's PC |
| 3 | **Your own server** | no | **yes** | **yes** | on the client's server |
| 4 | **A turnkey server** | no | **yes** | **yes** | in an isolated vault cell |

---

## 7.2. Method 1. From the Browser — the Classic

The path everyone knows. The client opens the web app on a computer with the
E-IMZO module installed, presses "Sign", picks their key from a list and enters
the password — the document is signed and sent.

**Who it suits:** people who work at one computer anyway and do not need to sign
from home or on the road.

**The limitation, stated honestly:** this is not our own development and cannot be
better than it is. Only at that PC, only with the module installed, only by hand.
The other three methods exist precisely because that is not enough.

---

## 7.3. Method 2. An Agent Program on the Computer — Signing from a Phone

> **E-IMZO Agent** — our own development, a Windows application.

The client installs the program on their work computer once. It gains access to
the signature key (a USB token or a file) and holds a **secured connection to our
server**.

**What that changes.** The computer stays switched on in the office — and the
client signs documents **from anywhere**: from the Telegram bot, from the app on
their phone, from a browser on any device. Press "Sign" on a phone in a car — the
job goes to their computer, the program signs with the key, and the document
comes back signed and travels on to the counterparty. It takes seconds.

**What the program can do:**

| Capability | What it gives |
|---|---|
| **Signing from a job sent by the bot or the app** | You do not have to be at the computer — the computer has to be switched on |
| **Working without a password prompt** | The program enters the key's password itself. The E-IMZO window no longer pops up over your work and steals focus |
| **Several organisations on one agent** | One program serves several TINs. For an accounting firm holding a hundred client keys this is fundamental: access to another company's TIN opens only once the agent has **proved ownership of that organisation's key** through a signed server challenge |
| **Self-updating** | The program updates itself |
| **A tray icon and a log** | You can see whether the agent is connected and what it has signed |
| **An installer** | An ordinary `.exe`: next → next → done |

**The limitation, stated honestly:** the computer has to be switched on and
online. A power cut, a lost connection, Windows deciding to update — and signing
is unavailable until the machine comes back. Which is exactly why methods 3 and 4
exist.

---

## 7.4. Method 3. Your Own Server — Signing That Depends on Nothing

> For anyone who needs signing to be available **genuinely** round the clock.

The client takes an inexpensive Ubuntu server (a VPS for a few dollars a month,
or their own machine in the office) and runs **one command**:

```bash
curl -fsSL https://app.ihisobchi.uz/agent/install.sh | sudo AGENT_ID='...' AGENT_SECRET='...' bash
```

The installer sets up Java, checks E-IMZO, asks for the key file, **works out the
TIN and the serial number** from the key itself, and raises a service that runs
24/7. No graphical interface, no password prompt.

**The key and its password stay on the client's server.** We do not receive them,
do not store them and cannot obtain them — we supply only the program. This is the
same trust model as with the PC program: the software is ours, the key is yours.

**How the client gets an access key.** The bot has a section called **"🖥 24/7
signing server"**:

- **"Create a server key"** — issues an identifier and secret pair plus a
  **ready-made installation command** to copy onto the server.
- The secret is shown **exactly once** and is never written to any log.
- The list shows **when each server was last seen** — "🟢 seen 3 minutes ago" or
  "⚪️ has not connected yet".
- **"Revoke key"** — the server instantly loses the right to sign. Irreversible,
  and without our involvement.
- Up to 10 active keys per organisation — enough for a primary and a backup.

**What it gives a business.** Signing stops depending on the office: the power,
the internet, somebody's laptop and the bookkeeper's holiday no longer matter. The
server sits in a data centre and signs round the clock. The client can delete the
key, replace it, or rebuild the server from scratch at any time — it is their
server and their key.

**Verified on a live configuration:** Ubuntu 24.04, E-IMZO 6.4.7 for Linux,
OpenJDK 17 — the agent registers, proves ownership of the key and signs without a
single pop-up window.

---

## 7.5. Method 4. A Turnkey Server — Like a Safe Deposit Box

> For anyone who does not want to deal with servers at all.

A fair question: "What if I have no server and know nothing about them? I want
somebody to set it up reliably, cheaply and turnkey."

That option exists. We raise a **separate protected server** on which an
**isolated cell** is created for each client — architecturally the closest thing
to a bank's safe deposit vault.

**What it looks like to the client.** They send the key file and its password —
and a few seconds later signing works round the clock. That is all.

**What happens inside, step by step:**

1. Both messages — the key file and the password — are **deleted from the
   conversation immediately** on receipt.
2. The key is encrypted **at once**, before the system even asks for the
   password: in plaintext it never reaches a cache or a queue.
3. The key and password are sealed **with the public key of the isolated
   environment** and only stored in that form. The private key to that envelope
   **does not exist** on the main server — it physically cannot read what it
   stores.
4. Inside the isolated environment a **personal cell** is created: a separate
   service, separate storage, separate credentials. Neighbouring clients are
   isolated from one another.
5. Before starting, the system **checks that the TIN in the key matches** the
   client's organisation. Somebody else's key will not fit the cell.

**The cell belongs to the client.** At any moment they can replace the key, update
it after a certificate reissue, or **delete the cell entirely**, contents and all.
We do not "own" the key; we provide the safe.

**The one boundary we point out ourselves:** at the moment of connection — and
only at that moment — the file and the password pass briefly through memory so
that they can be sealed. That is not storage and not a write to disk, but neither
is it "we never see them at all". We would rather say so directly than let
somebody find an inaccuracy in our description. In detail:
[05-security.md](05-security.md#54-the-247-signing-server--what-exactly-we-store).

---

## 7.6. The Central Question: "Could It Sign Something Without Me?"

This is the first question any business owner asks, and it is entirely the right
one. We answer it as concretely as possible, because what matters here is the
construction, not the phrasing.

### No signature ever starts by itself

**Signing always begins with a human action.** Neither the agent program, nor the
server, nor the vault cell **can initiate a signature** — they are technically
incapable of it. They do not walk through your documents deciding that something
ought to be signed. They wait for a job.

A job is created **only** when a person has:

- created a document in the wizard and confirmed it; **or**
- pressed "Sign" on a specific document; **or**
- confirmed a card the AI assistant presented to them.

No human action, no job. No job, and the server stays silent, however
round-the-clock it runs.

### What "auto-signing" actually means

The word frightens people more than it should, because it does not mean what it
seems to.

**"Auto-signing" is not "the system decides what to sign".** It is a setting that
removes the **second** question. Compare:

```
WITHOUT auto-signing:
  you filled in the invoice → "Create the document?" → YES
  → document created → "Sign it?" → YES → signed

WITH auto-signing:
  you filled in the invoice → "Create the document?" → YES
  → document created and signed straight away
```

In both cases **you** created the document, **you** checked its contents, **you**
gave the command. Auto-signing saves one redundant confirmation on a document you
have just assembled with your own hands. You switch it on and off in the
organisation's settings whenever you like.

**On the PC program specifically:** it has a similar setting, and it means
something narrower still — the program enters the **password to your key** itself,
so that the system's E-IMZO window does not pop up over your work. It still does
not decide which document to sign.

### What you see before signing

- **A full preview of the document**: goods, amounts, VAT, both parties' details,
  the number. Before you press, not after.
- **Automatically assembled documents** (an invoice from a power of attorney, an
  act from an invoice, a waybill from an invoice) are **never signed silently** —
  they arrive as a card with a preview and buttons.
- **Incoming documents from regular suppliers** likewise arrive as an "accept"
  card, not as silent acceptance. This is a direct product requirement: accepting
  an incoming invoice has tax consequences.
- **The voice assistant** speaks the operation aloud before executing it, and the
  confirmation phrase is **composed by the server, not by the language model** —
  you hear exactly the number and the amount that will be executed.

### Additional constraints that always apply

- **A key signs only for its own organisation.** The match between the TIN in the
  key and the organisation is checked on the server every time the agent
  connects.
- **The access secret is revoked instantly** — from the bot, without our
  involvement.
- **A repeat signature is impossible.** On a connection failure the system does
  not sign blindly but verifies the document's actual state in Didox.
- **Everything is recorded.** Every signature — who, what, when, from which agent
  — goes into a log the owner can read.

### And most importantly

**No document will be signed without your knowledge and your permission.** That is
not a promise in a text; it is the construction: the signing loop simply has no
way to start work by itself.

When we do build genuinely autonomous signing (for instance,
[the invoice issued on payment](03-roadmap.md#321-the-first-step-towards-it--automatic-e-invoice-on-payment-)),
it will acquire the right to operate **only through a separate, explicit
permission from the owner, bounded by amount and duration and revocable in one
tap** — and that will be stated just as directly as this is.

---

## 7.7. For Corporations: a Dedicated Environment or an On-Premise Install 🎯

The four methods above cover the needs of small and medium businesses. But some
clients have a different requirement: **a large company, a bank, a government
body, an outsourcing firm with a hundred keys** — organisations whose security
policy explicitly forbids storing anything with a third-party provider.

For them there are two formats, currently in preparation.

### A dedicated hosted environment

We provide the client with a **separate server and deploy our software on it**.
The client puts their keys, their data and their organisations there, and works.

- The environment belongs to the client: only their organisations, only their
  keys, no neighbours.
- **None of their data is stored on our main servers.**
- We are responsible for keeping it running: updates, monitoring, recovery.
- The client does not have to hire an administrator or learn how to install it.

A format for anyone who wants isolation but not infrastructure work.

### An on-premise install (the "box")

The maximum degree of independence: **our software is deployed on the client's own
hardware** — in their data centre, in their server room, inside their perimeter.

- Keys, documents, database — **all physically with the client**.
- **Not a single request carrying their data reaches us.** Not "we promise not to
  look", but "there is technically nothing to look at".
- We supply updates and support under a contract.
- The client buys a product rather than a subscription to somebody else's
  service.

This is how corporations that are obliged to keep everything internal operate —
and it usually cuts them off from modern tooling altogether. Here they get the
same platform as everyone else, entirely on their own premises.

**Pricing is per project.** Both formats are priced individually: they depend on
scale, the number of organisations, load and support requirements. The model is
described in
[09-business-model.md](09-business-model.md#95-stream-3-the-corporate-environment--hosted-and-on-premise).

---

## 7.8. How to Choose

| Your situation | Method |
|---|---|
| I work at one computer and sign a couple of documents a week | **From the browser** |
| I want to sign from a phone; the office computer is on anyway | **The agent program on a PC** |
| Documents must go out round the clock; office power and internet must not affect that | **Your own server** |
| I want the same thing, but without dealing with a server | **A turnkey server** |
| An accounting firm with dozens of client keys | **Your own server**, or **an agent with several TINs** |

The methods are not mutually exclusive: you can keep a server as the primary path
and the PC program as a fallback.

---

*Back to the beginning: [ecosystem overview](README.md)*
