# 6. The Client's First Day

> Part 6 of 9. Back: [ecosystem](01-ecosystem.md) · [modules](02-modules.md) · [roadmap](03-roadmap.md) · [voice orchestrator](04-voice-orchestrator.md) · [security](05-security.md). Next: [signing](07-signing.md) · [with us and without us](08-with-and-without.md) · [business model](09-business-model.md).

---

## 6.1. Why This Document Exists

A map of features answers the question "what can the product do". It does not
answer the other, more important one: **what happens to a person who opens us for
the first time.**

What follows is the whole journey: from the first message to the first signed
document that a counterparty will see in their own Didox account. With every step
a person actually goes through, and with an explanation of why each of them is
built the way it is.

---

## 6.2. The Journey End to End

```
   FIRST LOOK                 SIGN-UP                 ORGANISATION
        │                        │                         │
  opened the bot        language → consent → phone    TIN → "is this your
  or app.ihisobchi.uz     → SMS code → name           company?" → Didox
        │                        │                    password → details
   can be explored         ~2 minutes                 pulled in automatically
   in demo mode                                              │
        │                                                    │
        └────────────────────────────────────────────────────┤
                                                             ▼
                                                    SIGNING (set up once)
                                              choose one of four methods
                                                             │
                                                             ▼
                                                    THE FIRST DOCUMENT
                                          create → check → sign →
                                          delivered to the counterparty in Didox
```

After that it is ordinary work: incoming documents arrive on their own, deals
assemble themselves, money is allocated automatically.

---

## 6.3. Step 0. A First Look — Before Handing Over Any Passwords

A person can walk **the entire path of creating and signing a document without
registering**: demo mode runs on safe, fictional data for an Uzbek company. The
wizard, the products, the IKPU codes, the signature, the delivery — all exactly as
in production, but nothing leaves the building.

This is deliberate. We ask the client for the password to a state e-document
system — that is a great deal of trust to request on a first screen. It is more
honest to first show what happens after the password is entered, and only then
ask for it.

---

## 6.4. Step 1. Sign-up — About Two Minutes

| # | Screen | What happens | Why it is done this way |
|---|---|---|---|
| 1 | **Language** | Russian or Uzbek | The very first screen in the user's own language, not "register first, switch later" |
| 2 | **Consent** | The personal-data screen (Law ZRU-547) with the text's version | Consent is taken **before** the first byte of personal data. The system records which revision the person accepted |
| 3 | **Phone** | A +998 number | The primary identifier: everyone has a phone; in this segment, not everyone has e-mail |
| 4 | **SMS code** | A one-time code via Eskiz.uz | Confirmation that the number really is theirs |
| 5 | **Name** | How to address them | — |
| 6 | **Access token** | Pro edition only: a code of the form `BH-XXXX-XXXX` | Pro is still issued by invitation rather than self-service |

In a browser, instead of Telegram, the same path works, plus an alternative:
**e-mail and password**. The session runs on a JWT, so the app opens without a
messenger too.

---

## 6.5. Step 2. The Organisation — a TIN Instead of a Form

The classic competitor scenario: a twenty-field form — company name, address,
director, bank, account, activity code, VAT status. People abandon it at the
fifth field.

We have three steps:

**1. Enter the TIN** (or PINFL for a sole trader).

**2. Confirm the company.** The system shows the organisation's record from the
state register and asks directly: **"Is this your company?"** The person sees the
name, the director and the address, and either confirms or corrects the TIN. A
one-digit typo is caught here, not a month later inside a signed document.

**3. Enter the Didox password.** After that the system pulls in and saves every
detail itself: full legal name, director, registered address, bank, settlement
account, bank code, activity code, VAT status.

Not a single field typed by hand.

**What happens next without any human involvement:** incoming documents start
mirroring from Didox, counterparties are pulled from the correspondence history,
deals assemble themselves from the documents. By the time the client creates their
first document, the system already knows their counterparties.

**Additional organisations** are added the same way and switched between in one
tap, across every surface at once. For an owner of two or three companies this is
the primary working mode.

---

## 6.6. Step 3. Signing — the One Setting Worth Doing Straight Away

A document can be created without a signature key. But for it to **reach the
counterparty** it has to be signed — that is the law's requirement, not ours.

Here the client chooses **one of four methods**, and the choice determines whether
they can sign from a phone, at night and on holiday, or only sitting at their
office computer.

| Method | In brief | Who it suits |
|---|---|---|
| **From the browser** | The E-IMZO module on your own computer, with the key picked from a list | People who work at one PC |
| **An agent program on a PC** | Installed once, the computer stays switched on — signing becomes available from a phone | People who want to sign away from their desk |
| **Your own server** | One command on your own Ubuntu server, the key stays with the client | People who need signing without depending on an office PC |
| **A turnkey server** | We raise a protected vault cell; setup takes seconds | People who do not want to deal with servers at all |

Every method — including the answer to the central fear, "what if it signs
something without me?" — is examined in detail in
**[07-signing.md](07-signing.md)**.

---

## 6.7. Step 4. The First Document

Take an e-invoice — the most common document there is.

**1. Products.** Four ways, whichever suits the client: dictate them by voice ·
paste a list from Excel or WhatsApp · photograph a delivery note · pick them from
your own stock.

**2. IKPU codes.** The system matches the state classifier codes itself and shows
them for confirmation. The category name is **always** taken from the Tasnif
catalogue rather than composed — a wrong code means a penalty under Article 223 of
the Tax Code of Uzbekistan.

**3. The buyer.** From saved counterparties, from the imported Didox history, or
by TIN with a check against the state register.

**4. Review.** One screen: goods, amounts, VAT, both parties' details, and the
document number from your own numbering series.

**5. Sign and send.** One button. The document is signed, registered in Didox and
delivered to the counterparty.

**Two to five minutes in total**, against 30–60 on the Didox portal — and that is
on first use, with no practice.

### If something goes wrong

The failure paths deserve saying out loud, because a first bad experience decides
the fate of the product:

- **Didox is unavailable or the network drops.** What was typed is not lost: the
  document lands in "Unfinished", and when Didox comes back the system **writes to
  the person itself** and returns them to the exact step of the wizard where they
  stopped.
- **The Didox password is wrong.** The system says so plainly and lets them try
  again, instead of showing a technical error.
- **The signature key is not set up yet.** The document is saved as a draft; the
  system will remind them tactfully about signing rather than abandoning them
  halfway.
- **"Sign" is pressed twice.** A second signature is impossible: on a connection
  failure the system does not sign blindly but verifies the document's actual
  state in Didox.

---

## 6.8. What Happens on Day Two and After

The first document is not the end of the journey but the point after which the
product starts working for the client on its own:

| When | What the system does |
|---|---|
| A counterparty sends a document | It appears in "Incoming" with a notification; regular suppliers arrive as a one-tap "accept" card |
| A payment arrives | Visible in Telegram, tied to its contract and invoice (if the bank is connected) |
| Documents accumulate | They assemble themselves into deals: contract → payment → power of attorney → invoice → act |
| A deal goes unclosed | The "Needs you" feed shows whose move it is |
| A week passes | The Business Pulse digest: money, sales, debts, what needs attention |
| A letter arrives from the tax office | It comes to Telegram instead of waiting for a visit to the portal |

The client has studied not a single section — all of it switched itself on once
the organisation was connected.

---

## 6.9. Where People Drop Out — and What We Do About It

An honest section: we know the narrow points of the journey and we do not hide
them.

| Where | Why it is hard | What has already been done |
|---|---|---|
| **The Didox password** | We ask for the password to a state system three minutes into the acquaintance | Demo mode before sign-up; the company record shown before the password is requested |
| **No Didox account** | Some businesses are not registered in the e-document system at all | Didox registration **from inside the bot**, with no trip to the portal |
| **The signature key** | The heaviest step: it needs a physical key and installed software | Four signing methods instead of one; reminders if no key is connected |
| **The first document** | With no products in the catalogue, the wizard looks empty | Voice, photo, paste from Excel — the catalogue fills up as work proceeds |

**This is the product's current priority.** As
[the current figures](01-ecosystem.md#19-where-we-stand-scale-and-maturity) show,
the platform is built broadly, and the constraint is right here: carrying a person
from the first screen to regular use.

---

**Next:** [7. Document signing](07-signing.md) — every method, and why none of
them will sign anything without you.
