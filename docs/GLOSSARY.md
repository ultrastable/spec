<!-- SPDX-License-Identifier: LicenseRef-Ultrastable-USL-1.0 -->
<!-- Copyright (c) 2026 Rowan Brad Quni-Gudzinas -->

# Glossary: the owner's keywords

The owner's terms shift as the system is understood. This file is the memory of what each means. When a term changes, edit the entry and keep the older wording under "Was". Read this first in every session (US-SPEC-24).

| Term | Meaning | Where it bites |
|---|---|---|
| **Autonomy** | A system is autonomous if it has self-referential loops and the privilege to close them. Knowing without being able to act is useless. | US-SPEC-24 |
| **Self-referential loop** | A cycle that reads the system's own state (its records, specs, metrics) and changes it. Managers, the plus loop, probes, reconciliation, self-heal, review are all loops. | US-SPEC-04, 17, 24 |
| **Closed loop / closed system** | Detect, act, verify, record, all inside the system. Anything that needs a chat, an agent's memory or a human's recollection is outside and gets lost. | US-SPEC-24 |
| **Open loop** | A known gap with no owner, no next action or no closing probe. Itself a defect. | US-SPEC-17 |
| **Privilege to close** | The permission a loop needs to act on what it finds (merge, deploy, write). Without it the loop reports `blocked: no privilege` and names who grants it. | US-SPEC-06, 24 |
| **Plow-back** | Knowledge gained by doing is written into the system (spec, test, probe, runbook, glossary) in the same change. Not in the repo means not known. | US-SPEC-24 |
| **System memory** | The repo and the system's records. Never a chat or an agent session. | US-SPEC-24 |
| **Self-referential closure** | The whole system's loops close on themselves: it can read its own loops, its own docs and its own lessons and change them. | US-SPEC-20, 24 |
| **Self-hosting** | Ultrastable runs on itself: its own work goes through its own contract and checks. Stage ladder 0 to 4. | US-SPEC-20 |
| **Plus loop (plussing)** | Each pass improves what the last pass produced; the loop that keeps raising the bar. | US-SPEC-04 |
| **Probe** | A check, written by someone other than the change author, that measures reality and can close or reopen an item. | US-SPEC-05, 17 |
| **Manager** | A virtual staff role that watches a program's state, sets the constraint and originates work. | US-SPEC-02 |
| **Interrupt gate** | The only reason to stop for the owner: an action both irreversible and identity-bound. | US-SPEC-06 |
| **Capability Pack** | Opt-in capability outside default scope (business plan, marketing, legal, outreach). | SCOPE.md |
| **Door A / Door B** | Two ways in: A is the no-terminal web launcher; B is the paste-into-agent prompt. | US-SPEC-19 |
| **Preview (temporary account)** | A live Cloudflare preview with no account, valid about an hour unless claimed. | US-SPEC-19 |
| **Owner directive** | A statement from the owner that sets direction; stored verbatim in DIRECTIVES.md. | US-SPEC-24 |
| **Never stop, always improve** | When requested work is done, the next improvement is chosen and started; no status echoes. | DIRECTIVES.md |
| **Done** | Built, deployed in code, verified live. Never a chat reply. | DIRECTIVES.md |
