# P4 Model

**P4 Model** is a way to describe software as precise processes, at four levels of detail: from a list of processes anyone can read, down to code design.

---

## In short

A **process** is a single interaction with the system: someone does something (or something happens at a given time), the system handles it, and the process ends. Example: *Registration* is submitting the sign-up form; it ends when the activation email is sent. Clicking the link in that email is a separate process: *Account activation*.

You describe any change to a system (a new feature, a fix, a whole new system) as a list of such processes. Then you describe the same processes in more and more detail:

| # | Level | Question | Example |
|---|---|---|---|
| 1 | **Processes** | What are the processes? | P-01 Place order: the customer submits an order. |
| 2 | **Contracts** | What is visible from the outside? | Input: products, address, email. Output: order number and an email. If a product runs out, no order is created. |
| 3 | **Implementation plan** | What happens inside, and where do we build it? | Steps: check stock, recalculate prices, reserve stock, save. Orders module, order tables, same approach as the Returns module. |
| 4 | **Pseudocode** | What exactly will the code look like? | Classes, methods, arguments, tables, list of tests, no method bodies. |

The line between levels 2 and 3 is simple: **can you see it from outside the system?** If yes, it belongs to level 2. If it happens inside, it belongs to level 3.

---

## Details

### Process

A process is a single interaction with the system, from start to end.

- It has **one start**: someone does something (submits a form, clicks a button, calls an API) or something happens (a scheduled time, a message from another system).
- It has **one end**: the system is in a new state, or it has given something back (a response, an email, a file).
- It is **as small as possible**. The smaller the process, the easier it is to understand, discuss and build.

What people usually call a process, such as "creating an account" or "fulfilling an order", is a **group of processes** in P4:

- Creating an account = *Registration* + *Account activation*
- Fulfilling an order = *Place order* + *Confirm order* + *Export orders*

**Is it one process?** Check three things:
1. **One trigger from outside.** A person, another system or the clock starts it. Something the system does to itself halfway through is not a new process.
2. **Complete input.** The input makes sense on its own. A multi-step form that only means something when finished is one process, not one per step.
3. **One uninterrupted reaction.** The system handles it from start to end without waiting for anyone. If the system has to wait for a person or another event, the part after the wait is a new process.

Signs that a new process starts:
- the description says "then the user…", "next, the admin…", "after clicking the link…";
- there is a gap in time and the system waits for someone or something;
- a different person or system starts it.

Each process gets an ID and a name, e.g. `P-01 Place order`. The ID never changes between levels.

### Rules

1. **One document that grows downward.** Level 1 lists all processes. Level 2 repeats all of them and describes each one in more detail. Levels 3 and 4 do the same.
2. **A lower level never changes a higher one.** If something above needs to change, go back to that level, fix it, agree on the change, and come down again.
3. **Every level stands on its own.** Stop where the next level is no longer needed. Level 1 alone is a complete use of P4.
4. **Precision depends on the need.** A contract can say "products, address, email" or be an exact API description with fields and types. A simple process may have a three-line plan.
5. **Levels can be added or skipped.** Four levels are the default. A large or distributed system may need an extra level (see [Extra levels](#extra-levels)).
6. **If you don't know how, you don't write code.** The implementation plan points to an existing place in the system that the new code will follow. Open questions must be resolved before coding starts.

### Who uses which level

- **Levels 1–2** describe the system from the outside, without technology. Anyone who knows the product can read them: client, owner, analyst, tester. They settle **what** the system does.
- **Levels 3–4** describe the system from the inside. They settle **where and how** to build it.

Typical uses:
- **With the business:** write and agree on levels 1–2 together. The technical team then does levels 3–4.
- **Without the business** (your own product, the team decides): the team goes as deep as it needs.
- **Quick scoping:** level 1 only. A quarter of an hour, and you can see whether anything is missing.
- **API design:** level 2 with exact fields is a ready API contract.
- **Working with a developer:** the developer delivers the document up to level 3 (or 4), and writes code only after it is accepted. An experienced developer with a good plan usually doesn't need level 4.

---

### Level 1: Processes

**Goal:** a list of all processes. A quick overview of scope: is this everything, is anything missing?

**Template:**

```markdown
## Level 1: Processes

- P-01 <name>: <who> <does what, in one sentence>
- P-02 <name>: <who> <does what, in one sentence>
```

**Done when:**
- [ ] every interaction with the system is a separate process;
- [ ] every process has an ID, a name, who starts it, and a one-sentence description;
- [ ] every process passes the "is it one process?" check.

---

### Level 2: Contracts

**Goal:** everything visible from outside the system: what comes in, what goes out, the rules, how the state changes, and what happens when something goes wrong. Someone who reads this level knows how the system behaves without looking inside.

A contract here is more than an interface. It is everything the system promises to the outside world: what it needs, what it gives back (including emails, files and messages), what changes, and what happens when something goes wrong.

"When something goes wrong" does not mean "the customer doesn't want to order". It means specific situations along the way: a product ran out, an email failed to send, someone clicked twice, the order was cancelled in the meantime.

**Template:**

```markdown
## Level 2: Contracts

### P-01 <name>
- Who: <who or what starts the process>
- Start: <what they do>
- Conditions: <what must be true for the process to start: who is allowed, what state things must be in>
- Input: <data that comes in>
- Result: <what changes, what the person who started it sees>
- Output: <what the system gives back: response, email, file, message>
- State: <state before> → <state after>
- Rules: <rules and limits: quotas, expiry times, permissions, what the system calculates>
- When something goes wrong:
  - <situation> → <what happens, what the user sees>
- Always true: <what holds even when something goes wrong>
```

Input and output can be described in words ("products with quantities, address") or exactly (fields, types, sample data, file columns). Choose the precision you need.

**Done when:**
- [ ] all processes from level 1 are repeated;
- [ ] every process has: who, start, conditions, input, result, output, state;
- [ ] every process has at least one "when something goes wrong" situation, or an explicit "none";
- [ ] nothing is described that cannot be seen from outside: no tables, class names, or internal order of steps.

---

### Level 3: Implementation plan

**Goal:** what happens inside the system, and where it will be built. No finished code, but enough to see whether the solution fits the system.

This is the level where the developer has to think about **where** something belongs before writing it. Without it, it is easy to get finished code in the wrong place.

**Template:**

```markdown
## Level 3: Implementation plan

### P-01 <name>
- Steps: <what the system does inside, in order>
- Data: <what is stored and where: tables, fields, files>
- Safeguards: <how each "when something goes wrong" situation and each "always true" from level 2 is handled>
- Place in code: <module; what is new: service, handler, repository, endpoint; what existing parts are reused>
- Pattern: <existing place in the system that we follow>
- Extra steps: <non-business work: database changes, configuration, email templates, scheduled jobs, permissions>
- Open questions: <what we don't know yet; must be "none" before coding>
```

**Done when:**
- [ ] all processes from level 2 are repeated;
- [ ] every "when something goes wrong" situation and every "always true" from level 2 has a safeguard;
- [ ] every process has a module and a list of new elements;
- [ ] every process has a pattern, or a reason why something new is needed;
- [ ] open questions: none.

---

### Level 4: Pseudocode

**Goal:** the exact shape of the code: classes, methods, arguments, types, tables, list of tests. No method bodies.

**Template:**

```markdown
## Level 4: Pseudocode

### P-01 <name>
- Structures: <input and output objects with fields and types>
- Classes and methods: <signatures>
- Tables: <columns, types>
- Tests: <one per rule, per "when something goes wrong" situation and per "always true" from level 2>
```

**Done when:**
- [ ] all processes from level 3 are repeated;
- [ ] every new element from the plan has a signature;
- [ ] the list of tests covers the rules, the "when something goes wrong" situations and the "always true" items from level 2.

---

### Extra levels

Examples of levels you can add:

- **Map** (above Processes): groups of processes, e.g. "Creating an account = P-01 Registration + P-02 Account activation". Useful when there are many processes.
- **Services** (between Implementation plan and Pseudocode): which service or system handles which step, and how they talk to each other. Useful in distributed systems.

An added level follows the same rules: it repeats all processes and never changes the levels above it.

---

## Example: registration

What people call "creating an account" is four processes in P4. One of them is started by the clock, not by a person.

### Level 1: Processes

- P-01 Registration: a visitor submits the sign-up form.
- P-02 Account activation: the user clicks the activation link from the email.
- P-03 Resend activation link: the user asks for a new activation link.
- P-04 Remove unactivated accounts: every night the system removes accounts that were not activated within 7 days.

### Level 2: Contracts

#### P-01 Registration
- Who: visitor
- Start: submits the sign-up form
- Conditions: not logged in
- Input: email, password, name, terms accepted
- Result: the account is created, the visitor sees "Check your inbox"
- Output: email with an activation link
- State: none → **Inactive**
- Rules:
  - password has at least 10 characters
  - terms must be accepted
  - the activation link is valid for 24 hours
  - email addresses are compared without regard to upper and lower case
- When something goes wrong:
  - invalid data → the form shows an error next to each wrong field, nothing is created
  - the email is already registered → the visitor sees the same "Check your inbox"; that address gets an email "someone tried to register with your address" (the form never reveals whether an address is registered)
  - the email failed to send → the account stays, the email arrives later; the user can also use P-03
- Always true: one account per email address

#### P-02 Account activation
- Who: user
- Start: clicks the link in the activation email
- Conditions: none
- Input: the code contained in the link
- Result: the account is active, the user sees "Account activated" and can log in
- Output: none
- State: Inactive → **Active**
- Rules: each link works once and for 24 hours
- When something goes wrong:
  - the link has expired → a message with a "Send a new link" button (P-03)
  - the account is already active → a message "Your account is already active, log in"
  - the link is unknown or was replaced by a newer one → a message "This link is not valid"
- Always true: an account becomes active only through a valid link

#### P-03 Resend activation link
- Who: user
- Start: clicks "Send a new link" and enters the email address
- Conditions: none
- Input: email
- Result: the user sees "If an inactive account exists for this address, we have sent a new link"
- Output: a new activation email
- State: no change
- Rules:
  - a new link cancels all previous links
  - at most 3 links per address per hour
- When something goes wrong:
  - no account, or the account is already active → the same message, no email is sent
  - more than 3 requests in an hour → a message "Too many attempts, try again later"
- Always true: only the newest link works

#### P-04 Remove unactivated accounts
- Who: the clock, every night at 03:00
- Start: scheduled time
- Conditions: none
- Input: none
- Result: inactive accounts older than 7 days no longer exist
- Output: none
- State: Inactive → removed
- Rules: an account is removed 7 days after registration if it is still inactive
- When something goes wrong:
  - one account cannot be removed → the others are still removed, the failed one is retried the next night
- Always true: an active account is never removed

### Level 3: Implementation plan

#### P-01 Registration
- Steps: validate the form → normalise the email → check whether the address exists → if it exists, save the "someone tried" email to be sent and stop → create the inactive user → create the activation link → save the activation email to be sent
- Data: users table, activation links table (only a fingerprint of each link is stored, with its expiry time), table of emails to be sent
- Safeguards:
  - one account per address: the email column is unique in the database, so two forms submitted at the same moment cannot create two accounts
  - email: saved in the table of emails to be sent together with the account; a separate job sends it and retries on failure
  - repeated submits: the form has a limit of attempts per minute from one address
- Place in code: Accounts module; new: "register" handler, activation links repository; reuses the existing password hashing and email sending services
- Pattern: inviting a user in the Team module
- Extra steps: database changes (new table, unique email column), two email templates, configuration of the attempt limit
- Open questions: none

#### P-02 Account activation
- Steps: find the link by its fingerprint → check that it is unused and not expired → set the account to active → mark the link as used
- Data: users table, activation links table
- Safeguards:
  - single use: setting the account to active and marking the link as used happen together or not at all
  - only fingerprints are stored, so a leaked database does not expose working links
- Place in code: Accounts module; new: "activate account" handler, activation page
- Pattern: password reset in the Accounts module
- Extra steps: none
- Open questions: none

#### P-03 Resend activation link
- Steps: find the inactive account by email → cancel its existing links → create a new link → save the activation email to be sent
- Data: activation links table, table of emails to be sent
- Safeguards:
  - limit: requests are counted per address in the last hour
  - only the newest link works: cancelling old links and creating the new one happen together
- Place in code: Accounts module; new: "resend activation link" handler; reuses link creation from P-01
- Pattern: P-01
- Extra steps: configuration of the hourly limit
- Open questions: none

#### P-04 Remove unactivated accounts
- Steps: find inactive accounts older than 7 days in batches → remove each account with its links
- Data: users table, activation links table
- Safeguards:
  - one failure doesn't stop the job: each account is removed separately, errors are logged and the account is picked up again the next night
  - active accounts are safe: the search only selects accounts with status "inactive"
- Place in code: Accounts module; new: scheduled job
- Pattern: the nightly cleanup of expired sessions
- Extra steps: entry in the job scheduler
- Open questions: none

### Level 4: Pseudocode

#### P-01 Registration
- Structures: `RegisterCommand { email: string, password: string, name: string, termsAccepted: bool }`
- Classes and methods: `RegisterHandler::handle(RegisterCommand): void`, `ActivationLinks::create(userId): Link`
- Tables: `users(id, email unique, password_hash, name, status, created_at)`, `activation_links(id, user_id, fingerprint, expires_at, used_at, cancelled_at)`
- Tests: valid registration; each invalid field; terms not accepted; existing email gives the same response and sends the "someone tried" email; two simultaneous submits create one account; email saved to be sent

#### P-02 Account activation
- Structures: `ActivateAccountCommand { code: string }`
- Classes and methods: `ActivateAccountHandler::handle(ActivateAccountCommand): void`
- Tests: valid link; expired link; used link; cancelled link; unknown link; already active account

#### P-03 Resend activation link
- Structures: `ResendActivationLinkCommand { email: string }`
- Classes and methods: `ResendActivationLinkHandler::handle(ResendActivationLinkCommand): void`
- Tests: inactive account gets a new link and old links stop working; unknown address sends nothing; active account sends nothing; fourth request in an hour is refused

#### P-04 Remove unactivated accounts
- Structures: none
- Classes and methods: `RemoveUnactivatedAccountsJob::run(now: datetime): int`
- Tests: removes inactive accounts older than 7 days; keeps inactive accounts younger than 7 days; never removes active accounts; continues after one failure

---

## Example: online shop

### Level 1: Processes

- P-01 Place order: the customer submits an order from the cart.
- P-02 Confirm order: the admin confirms a new order.
- P-03 Export orders: the admin downloads orders from a chosen period as a CSV file.

### Level 2: Contracts

#### P-01 Place order
- Who: customer
- Start: submits the order form
- Conditions: the cart is not empty
- Input: products with quantities, delivery address, email
- Result: the order is accepted, the customer sees the order number
- Output: order confirmation email
- State: none → **New**
- Rules:
  - the system calculates the price; the price sent by the form is ignored
  - stock is reserved until the order is confirmed or cancelled
- When something goes wrong:
  - a product ran out in the meantime → no order is created, the customer sees which product is missing
  - the email failed to send → the order stays, the email arrives later
  - double click → only one order is created
- Always true: no stock stays reserved without an order

The same contract in exact form, when designing an API:

```
POST /orders
{
  "items": [{ "sku": "A-100", "qty": 2 }],
  "shipping": { "street": "1 Long St", "city": "Springfield", "zip": "12345" },
  "email": "jane@example.com"
}

201 Created
{ "orderNumber": "ORD-2026-0001" }

409 Conflict
{ "error": "out_of_stock", "sku": "A-100" }
```

#### P-02 Confirm order
- Who: admin
- Start: clicks "Confirm" on an order
- Conditions: admin is logged in, the order is in state "New"
- Input: order number
- Result: the order is confirmed
- Output: email to the customer "your order is being prepared"
- State: New → **Confirmed**
- Rules: only admins with the orders permission can confirm
- When something goes wrong:
  - the order is already confirmed or cancelled → nothing changes, the admin sees a message
  - the email failed to send → the order stays confirmed, the email arrives later
- Always true: an order is confirmed at most once

#### P-03 Export orders
- Who: admin
- Start: clicks "Export" and picks a date range
- Conditions: admin is logged in
- Input: date from, date to
- Result: the admin downloads a file
- Output: CSV file with columns: number, date, customer email, total, status
- State: no change
- Rules: the range is at most 12 months
- When something goes wrong:
  - no orders in the range → a file with only the header row
  - range longer than 12 months → a message, no file
- Always true: the export never changes any order

### Level 3: Implementation plan

#### P-01 Place order
- Steps: check stock → recalculate prices → reserve stock → save the order → save the email to be sent
- Data: orders and order items tables, reservations in the stock table, table of emails to be sent
- Safeguards:
  - out of stock: all writes happen together or not at all, so nothing is saved when a product is missing (this also keeps "no stock reserved without an order")
  - email: saved in the table of emails to be sent together with the order; a separate job sends it and retries on failure
  - double click: the form carries a one-time token; a second submit with the same token returns the same order
- Place in code: Orders module; new: "place order" handler, `POST /orders` endpoint; reuses the existing stock and pricing services
- Pattern: creating a return in the Returns module
- Extra steps: database changes (new tables), email template
- Open questions: none

#### P-02 Confirm order
- Steps: check state → change state → save the email to be sent
- Data: state change in the orders table, table of emails to be sent
- Safeguards:
  - already confirmed: the state changes only if the order is "New", checked at the moment of saving, so two clicks cannot confirm twice
  - email: same as P-01
- Place in code: Orders module; new: "confirm order" handler, button in the admin panel
- Pattern: accepting a return in the Returns module
- Extra steps: email template, new permission for confirming orders
- Open questions: none

#### P-03 Export orders
- Steps: check the range → read orders in batches → write rows to the file
- Data: read-only access to the orders table
- Safeguards:
  - large range: the file is built in batches, without loading all orders at once
  - range over 12 months: checked before reading any data
- Place in code: Orders module; new: "export orders" handler, button in the admin panel
- Pattern: invoice export in the Invoices module
- Extra steps: new permission for exporting orders
- Open questions: none

### Level 4: Pseudocode

#### P-01 Place order
- Structures: `PlaceOrderCommand { items: OrderItem[], shipping: Address, email: string, formToken: string }`
- Classes and methods: `PlaceOrderHandler::handle(PlaceOrderCommand): OrderNumber`
- Tables: `orders(id, number, email, status, total, form_token, created_at)`, `order_items(order_id, sku, qty, price)`
- Tests: valid order; out of stock saves nothing; resubmit with the same token returns the same order; form price ignored; email saved to be sent

#### P-02 Confirm order
- Structures: `ConfirmOrderCommand { orderNumber: string }`
- Classes and methods: `ConfirmOrderHandler::handle(ConfirmOrderCommand): void`
- Tests: confirm from "New"; attempt from "Confirmed"; attempt from "Cancelled"; missing permission; email saved to be sent

#### P-03 Export orders
- Structures: `ExportOrdersQuery { from: date, to: date }`
- Classes and methods: `ExportOrdersHandler::handle(ExportOrdersQuery): CsvFile`
- Tests: export with data; empty range gives only the header; range over 12 months rejected; missing permission

---

## FAQ

**Is a process the same as a use case or a user story?**
Close, but smaller and stricter. A user story can cover many interactions ("as a customer I want to create an account"). In P4 that is a group of processes: Registration and Account activation. A P4 process is close to a use case at the "user goal" level (Cockburn), with the "is it one process?" check on top.

**How small should a process be?**
As small as the "is it one process?" check allows: one trigger from outside, complete input, one uninterrupted reaction. Don't split further than that. A multi-step form that only makes sense when finished is still one process.

**Are scheduled jobs and integrations processes too?**
Yes. "Every day at 02:00 cancel unpaid orders older than 7 days" is a process started by the clock. "The payment provider reports a payment" is a process started by another system.

**Are read-only actions processes?**
Yes, when someone needs to agree on what they return. Exporting orders or showing an order history has a contract (what you get, in what format, with what limits) but no state change. Trivial screens can be left out.

**Do I have to write all four levels?**
No. Every level stands on its own. Level 1 alone is useful for scoping. Levels 1–2 are a full specification. Levels 3–4 are for when the code is about to be written.

**Why repeat all processes on every level?**
So that each level can be read, reviewed and accepted on its own, and nothing gets lost. The reader of level 3 does not need to jump back to level 2 to see which processes are covered.

**What if the implementation shows that the contract is wrong?**
Stop. Go back to level 2, change the contract, agree on the change with whoever accepted it, then update the levels below.

**What is one P4 document for?**
Usually one change: a ticket, a feature, an epic. A whole new system can also be one document, with a Map level on top.

**How do I describe a bug fix?**
Pick the process the bug is in and describe it at level 2: what happens now, what should happen, what must stay the same. Then levels 3–4 if needed.

**Where do non-functional requirements go?**
If they are visible from outside (response time, limits, permissions, file size), they go into the rules on level 2. How they are achieved (caching, batching, indexes) goes into level 3.

**How does P4 relate to the C4 model?**
C4 describes the structure of a system (context, containers, components, code). P4 describes its behaviour, as processes. The "Place in code" on level 3 can refer to C4 containers and components.

**How do I use P4 with an LLM?**
Give it the link to this README and ask, for example: "Describe the order checkout using the P4 Model, up to level 2" or "Here is our P4 document up to level 2. Read the codebase and write level 3."

---

## For LLMs

When asked to describe something "using the P4 Model" or "up to level N":

1. Write a single document with the sections `## Level 1: Processes`, `## Level 2: Contracts`, `## Level 3: Implementation plan`, `## Level 4: Pseudocode`, only up to the requested level.
2. Always start from level 1, even when asked for a deeper level. Each level is derived from the one above.
3. Split into processes using the "is it one process?" check. Give them IDs `P-01`, `P-02`… and never change them between levels.
4. On every level, repeat **all** processes and use that level's template.
5. On levels 1–2, describe only what is visible from outside the system. Do not use technical vocabulary unless an API contract was requested.
6. On every level, use plain names that do not require knowing specific design patterns. Instead of naming a pattern, describe what the solution does.
7. Do not write implementation code. Level 4 has signatures and structures, not method bodies.
8. On level 3, read the existing code and point to a real pattern. If you have no access to the code, put that under "Open questions".
9. Do not invent anything. Put missing information under "Open questions", or ask before writing.
10. If a lower level shows that a higher one is wrong or incomplete, do not fix it silently. Stop, describe the problem, and propose a change to the higher level.
11. At the end, go through the "Done when" checklist of every level you wrote, and list any items that are not met.

---

## Related approaches

P4 is a lightweight combination of older ideas, written as a markdown template for people and for LLMs.

- **Communication Analysis** (España, Pastor et al., Universitat Politècnica de València): business processes split into "communicative events" by the unity criteria (trigger, communication, reaction). The "is it one process?" check in P4 comes from here. [Technical report](https://arxiv.org/abs/1205.0987)
- **Essential Systems Analysis / event partitioning** (McMenamin & Palmer, 1984): a list of events, and a planned response of the system to each one. The system is split into small "mini-systems", one per event.
- **Cleanroom software engineering** (Harlan Mills, IBM): black box → state box → clear box. Each level is checked against the one above. Same line as between P4 levels 2 and 3.
- **Use cases** (Alistair Cockburn): the "user goal" level ("one sitting") is close to a P4 process. The main scenario, extensions and guarantees map to the P4 contract.
- **Operation contracts** (Craig Larman, *Applying UML and Patterns*): system events with pre- and postconditions, then the design that realises them.
- **C4 model** (Simon Brown): levels of detail for architecture. P4 does the same for behaviour.
- **Event Modeling** and **Use-Case 2.0**: small vertical slices as the unit of work.
- **Spec-driven development** (GitHub Spec Kit, OpenSpec, Kiro): P4 levels 1–2 correspond to the specification, levels 3–4 to the technical plan.
