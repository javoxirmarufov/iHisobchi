# 5. Security and Trust

> Part 5 of 9. Back: [ecosystem](01-ecosystem.md) · [modules](02-modules.md) · [roadmap](03-roadmap.md) · [voice orchestrator](04-voice-orchestrator.md). Next: [first day](06-first-day.md) · [signing](07-signing.md) · [with us and without us](08-with-and-without.md) · [business model](09-business-model.md).

---

## 5.1. Why This Document Stands Apart

A business does not entrust us with "data in general". It entrusts us with the
password to a state e-document system, a digital signature key, a bank statement,
its employees' personal data and its purchase prices — the things that in any
company are held by one or two people.

Which means something simple: **we have no right to a single incident.** Not "we
will try to minimise the risks" — precisely this: after the first leak, nobody
will trust us with their organisation again, and the product will cease to exist.
So security here is not a feature among features but the condition under which
everything else makes sense.

What follows is exactly what we do. Without generalities: which technology,
applied where, and what we do to stop the protection going stale.

---

## 5.2. Encryption: With What and How

**Everything sensitive is encrypted before it reaches disk.** Not "a database
behind a password" — the values themselves are stored encrypted, and what sits in
the database is ciphertext.

| What | How it is protected |
|---|---|
| Didox password, access tokens | Fernet (AES-128-CBC + HMAC-SHA256, an industry standard) |
| Bank tokens and identifiers | Fernet |
| Connection credentials for Soliq, 1C, MoySklad, CRMs | Fernet |
| Personal data (PINFL, passport details of instalment customers) | Fernet, with a separate data-class prefix |
| The contents of tax-office letters in the working cache | Fernet plus encryption of the identifiers |
| The signature key in "24/7 signing server" mode | A sealed box: X25519 + HKDF-SHA256 + AES-256-GCM (see §5.4) |
| Web sign-in passwords | bcrypt (a one-way hash, not recoverable) |
| Statement-report artefacts | Encrypted on disk with an integrity check on the contents |

**What this means in practice.** Ciphertext without the key is useless: brute
force is computationally impossible — this is the same class of protection banking
and government systems rest on. Even complete access to the contents of the
database yields no client passwords and no client keys.

**Key rotation.** The master key can be replaced without stopping the service: new
records are encrypted with the new key, old ones continue to be read with the
previous one, and we keep a counter showing how many records are still on the old
key. That turns rotation from an emergency into a managed procedure.

**Search without decryption.** Where a record has to be found without revealing
its contents (for example, "have we seen this letter before?"), we use
cryptographic blind indexes with purpose separation: the index allows a
comparison, but the original value cannot be reconstructed from it and cannot be
carried into another context.

---

## 5.3. Secrets and Access — the Principle of Least Privilege

- **Not one password, key or token in the code.** Everything comes from a
  protected environment. This is not a gentlemen's agreement between developers
  but an automatic check: a commit containing a secret does not go through.
- **Each client sees only their own data.** Every database query is scoped to the
  organisation it was made on behalf of; the isolation is covered by tests.
- **Employees' personal data sits behind a separate lock.** Having the "1C"
  accounting section switched on does **not** by itself unlock HR data: that needs
  a separate, deliberate switch, because consent to bookkeeping is not consent to
  people's personal data.
- **Separated environments.** Document signing lives in an isolated environment;
  parsing of untrusted client files happens in a minimum-privilege sandbox with no
  access to the network or the database.
- **File links are single-use and short-lived.** Downloading a document goes
  through a signed ticket that lives for seconds and burns on use — a forwarded
  link is useless to anyone else.

---

## 5.4. The "24/7 Signing Server" — What Exactly We Store

The most sensitive thing a business can entrust to anyone is its digital
signature key. So here we describe the model with complete precision, with no
rounding in our own favour.

**How it works:**

1. The client submits the key file and its password in a protected dialogue. Both
   messages are **deleted from the chat immediately** on receipt.
2. While the system waits for the password, the key file is already encrypted — it
   never sits in plaintext in a cache or in a queue.
3. The key and password are sealed **with the public key of the isolated signing
   environment** and stored in that form in the database.
4. The private key to that envelope does not exist on the production server.
   **Production physically cannot read what it stores** — it acts as a vault, not
   as an owner.

**An honest boundary that has to be stated directly.** At the moment of connection
— and only at that moment — the key file and the password are briefly present in
the process's memory so that they can be sealed. That is not storage and not a
write to disk, but neither is it "we never see them at all". We would rather say
so ourselves than let somebody find an inaccuracy in our description:
**at rest, zero knowledge; at the moment of connection, a brief window in
memory.**

A digital signature key is not required for managed mode at all: most clients use
the desktop signing agent, where the key **never leaves their computer** and the
system merely sends over a job to be signed.

---

## 5.5. Zero Data Retention: What Happens to Data Inside the AI

A separate question, and the first one businesses ask: **"you hand my data to an
artificial intelligence — what happens to it afterwards?"**

The answer: **nothing. It is not retained by the provider.** We operate in
zero-data-retention mode: the content of a request is used to produce an answer
and remains neither in the provider's logs, nor in its storage, nor in model
training.

**And we do not assume this — we verify it.** Zero retention is an account
setting, and a setting can be switched off by accident. So we run an automated
probe: **on a schedule, the system asks the provider directly** whether the mode
is enabled on our account, and raises an alert to the on-call engineer if the
answer changes. We deliberately built the probe so that it does not rely on
indirect signals: it reads the provider's own confirmation.

What else limits what is sent:

- **The minimum necessary.** What goes to the model is what the specific task
  requires, not "the whole business, just in case".
- **Transparency in the interface.** Where a file's contents are sent to the AI
  for parsing, the user is warned before the upload rather than after it.
- **A switch on every AI loop.** Any AI feature can be killed separately and
  instantly — the model's access to the data ends without a new version being
  shipped.
- **Our own code is not the model's black box.** Financial checks, IKPU codes,
  amounts and VAT are computed by deterministic code. The model cannot slip an
  invented number into a place where arithmetic decides.

---

## 5.6. What We Do Not Write to the Logs

Logs are an underrated leak channel: they live a long time, they get copied, and
they end up in monitoring systems.

- Passwords, tokens and keys pass through a masking filter and **never reach the
  logs under any scenario** — including inside error messages.
- Page addresses do not retain credentials from query parameters — a dedicated
  access logger takes care of that.
- In the 1C integration, responses concerning HR and payroll objects are logged
  **without the response body**: an error can be investigated from the status code
  and the address, and names, PINFLs and amounts are not needed for that — so they
  are not there.
- The contents of tax-office letters, along with their subject, sender and number,
  are written neither to the logs nor to the error-monitoring system — only
  technical identifiers and the outcome.
- Sending errors to the monitoring system works on the principle "no consent, no
  send".

**An open position.** We do not claim that across the project's whole history not
one file name has ever landed in a service record: in a few places where user
files are parsed, the file name is written into a diagnostic message. That is not
content and not personal data, but it is an exception to the rule, and we would
rather name it than sign up to an absolute statement. Bringing those places into
line with the general rule is work in progress.

---

## 5.7. Protection Against Malicious Content

Every file a user uploads is treated as untrusted by default.

- **Checks before parsing**: limits on size, structure and nesting — a zip bomb
  never reaches decompression.
- **Bank statements are parsed in a sandbox** with minimal privileges, in a
  separate process communicating over a local socket: even a successful attack on
  the parser gains access to neither the database nor the network.
- **Protection against forged requests to internal addresses** — any URL a user
  supplies passes through a dedicated guard.
- **Signed irreversible buttons**: a tap that destroys or sends something carries
  a cryptographic signature that cannot be forged from outside.
- **Rate limiting at several levels at once**: by address, by user, by route, and
  separately for expensive AI operations.

---

## 5.8. Compliance with Uzbek Law

The product operates under **Law ZRU-547 "On Personal Data"** — and that is
reflected in its construction, not only in the text of a policy:

- **Versioned consent.** The user accepts a specific revision of the policy; the
  system records which one and when. When the policy changes, consent is requested
  again.
- **Withdrawing consent** is available as a command, not as a letter to support.
- **Consent inside the order.** In public scenarios (a storefront order, a QR
  order) the consent is stored in the order itself together with the version of
  the text, not only in a log.
- **The policy in three languages** — Russian, Uzbek, English.
- **Retention periods.** Service logs are cleaned on a schedule by a dedicated
  process; personal data in the more sensitive modules (instalment sales) has a
  retention policy of its own.

---

## 5.9. What We Do Every Day So the Protection Does Not Go Stale

Security is not a state but a working regime. Ours looks like this:

**Every night at 06:00 Tashkent time**, automatically:

- **the entire repository history** is re-examined for an accidentally committed
  secret — by two independent scanners;
- static analysis is run against vulnerable constructs in the code;
- **every dependency** is checked against known vulnerabilities (CVEs);
- the built container images are scanned.

A red result from the nightly run is treated as an **incident**, not as an item in
a queue: it is investigated first thing in the morning, ahead of everything else.

**On every code change**, before it reaches the shared branch: a secret check on
the changed files, static analysis, and — for anything touching authentication,
encryption, personal data, signing or payments — a separate review focused on
security.

**Continuously:** we read what is happening in the industry — vulnerabilities in
the libraries we use, changes in providers' requirements, new classes of attack on
AI systems. Updating a dependency with a known vulnerability is not "when we get
round to it" but work with a higher priority than new features. Several such
updates have shipped the same day the vulnerability became public.

**Everything that happened is visible.** Users' actions and the AI's actions are
written to logs the business owner can read in the interface. Monitoring raises
an alert into the on-call engineer's messenger, not into an inbox read once a
week.

---

## 5.10. Our Position, Briefly

1. **The client's data belongs to the client.** We do not sell it, do not pass it
   to third parties and do not use it for anything except running their own
   business.
2. **We encrypt everything sensitive** with industrial-grade algorithms and rotate
   the keys; access to the database does not grant access to passwords and keys.
3. **The AI retains nothing** — zero-retention mode, and we verify it
   automatically rather than taking it on trust.
4. **The signing key is either on the client's computer or inside an isolated
   environment** that the production server cannot read.
5. **A human performs the irreversible.** Even a fully autonomous loop, in future,
   will acquire that right only through the owner's explicit, bounded and
   revocable permission.
6. **We name our own weak points.** Everything marked as open in this document is
   open. A product that hides what is inconvenient cannot be verified — and
   therefore cannot be trusted.

**One incident is enough to end this product. We work on exactly that
assumption.**

---

*Back to the beginning: [ecosystem overview](README.md)*
