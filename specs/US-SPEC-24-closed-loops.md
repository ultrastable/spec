<!-- SPDX-License-Identifier: LicenseRef-Ultrastable-USL-1.0 -->
<!-- Copyright (c) 2026 Rowan Brad Quni-Gudzinas -->

# US-SPEC-24: Autonomy is closed self-referential loops; nothing lives only in a chat

| Field | Value |
|---|---|
| ID | US-SPEC-24 |
| Title | Closed loops: autonomy definition, system memory, knowledge plow-back |
| Version | 0.1.0 (draft) |
| Date | 2026-11-11 |
| Status | Draft |

## 1. Purpose

Tagline: **A system is autonomous if it has self-referential loops and the privilege to close them.** Knowing something and being unable to act on it is useless. A coding agent or chat that holds knowledge the system cannot read has taken that knowledge out of the system: it is lost the moment the session ends. This specification makes the repository, and the running system built from it, the only memory.

## 2. Terms

The canonical glossary is [docs/GLOSSARY.md](../docs/GLOSSARY.md). Core terms: **loop**, **self-referential loop**, **closed loop**, **privilege to close**, **open loop**, **plow-back**, **system memory**, **owner directive**.

## 3. Requirements

- **US-24-R01 Definition.** A loop is any cycle that reads the system's own state and changes it (managers, plus loop, probes, reconciliation, self-heal, review). Autonomy of a component is measured by whether it has (a) a loop that reads its own state and (b) the privilege to act on what it reads.
- **US-24-R02 Closed system.** Every loop closes inside the system: detect, act, verify, record. A step that needs something outside the system (a chat, an agent's memory, a person's recollection) is an open loop and is itself a defect with an owner and a closing probe.
- **US-24-R03 Nothing stays in a chat.** Every decision, directive, definition, finding, lesson and unfinished item from any session (chat or coding agent) is written to the repository or the system's records before the session ends. A session may not end holding knowledge that exists only in its context.
- **US-24-R04 Owner directives are records.** Each owner statement that sets direction is stored verbatim with its date in `docs/DIRECTIVES.md`, with a one-line reading and the requirement or loop it produced. Terms the owner uses are defined in the glossary and kept current; a changed term updates the glossary entry (with the old wording noted), it is never left to be remembered.
- **US-24-R05 Plow-back.** Knowledge gained by doing (a failed probe, a platform fact, a cost surprise) is plowed back: into a spec requirement, a test, a probe, a runbook or the glossary, in the same change that learned it. A fact verified in a session but absent from the repo counts as not known.
- **US-24-R06 The system reads its own loops.** The loop ledger (`docs/LOOPS.md`, later a table) lists every loop: name, what it reads, what it changes, who may close it, closing probe, status (BUILT, RUNNING, PLANNED). A loop absent from the ledger is invisible to the system and therefore open.
- **US-24-R07 Privilege to close.** For each loop the ledger names the authority that lets it act (permissions, tokens scoped, merge rights). A loop that detects but lacks the privilege is reported as `blocked: no privilege`, with the exact privilege and who must grant it, never as complete.
- **US-24-R08 Session hand-off.** Before a session ends it commits (or files) its open items, directives heard, and facts learned. The session record references the commit or issue. The next session starts by reading the glossary, directives, loop ledger and open items, not a summary.

## 4. Conformance tests

- **US-24-T01** Every term in the owner's list appears in the glossary with a definition. Pass: `tools/glossary_check` finds none missing.
- **US-24-T02** Every loop named in a spec's status section appears in the loop ledger. Pass: none missing.
- **US-24-T03** Each `docs/DIRECTIVES.md` entry links to a requirement, loop or issue. Pass: no orphan directive.
- **US-24-T04** An agent session ends with uncommitted knowledge files. Pass: the self-hosting check fails the record (the PR record must name the knowledge written back).

## 5. Reference implementation status

- Glossary, directives and loop ledger files: BUILT as documents in this repository (2026-11-11). Their automated checks (T01 to T04) are PLANNED.
- The PR record's plow-back field and the loop-closer (probes close issues, epics tick their own children): PLANNED to be tied together; the loop closer exists on branch `loops/closer` in `ultrastable/workers` (unmerged at the time of writing).
- Privilege column in the ledger: PLANNED.
