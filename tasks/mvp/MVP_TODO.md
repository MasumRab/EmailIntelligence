 # MVP Pivot TODO

 This is a separated list of MVP-focused tasks and planning items.

 ## Epic A: Ingest + Normalize
 - [ ] A1: Mailbox source selection + API/IMAP setup
 - [ ] A2: Robust email parser (headers, bodies, threading headers)
 - [ ] A3: Persistence layer (schema + migrations)
 - [ ] A4: CLI for sync + inspect (debugging surface)

 ## Epic B: Intelligence
 - [ ] B1: Thread reconstruction + conversation view
 - [ ] B2: Signal extraction (participants, orgs, action classification)
 - [ ] B3: Idempotent reprocessing + result storage
 - [ ] B4: Search/filter API (sender, domain, tags, action-required)

 ## Epic C: Present + Polish
 - [ ] C1: Web UI or TUI (thread list + details)
 - [ ] C2: Structured logging + error reporting
 - [ ] C3: Tests (parser, pipeline idempotency, sync regressions)
 - [ ] C4: Packaging + README (single "run locally" command)

 ## MVP Pivot Setup Work
 - [ ] Define which mailbox source (Gmail API or IMAP) is in scope
 - [ ] Confirm data storage target (SQLite or Postgres)
 - [ ] Define minimal schema (emails, threads, labels, results)
 - [ ] Decide MVP UI surface (CLI or local web view)
 - [ ] Document Definition of Done for MVP tasks
 - [ ] Validate task sizing (<= 2 days per task)
