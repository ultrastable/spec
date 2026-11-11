<!-- SPDX-License-Identifier: LicenseRef-Ultrastable-USL-1.0 -->
<!-- Copyright (c) 2026 Rowan Brad Quni-Gudzinas -->

# Loop ledger

Every loop the system has, so the system can read its own loops (US-SPEC-24-R06). A loop not listed here is invisible and therefore open. Status as of 2026-11-11.

| Loop | Reads | Changes | Closing probe | Privilege it needs | Status |
|---|---|---|---|---|---|
| Tick / heartbeat | org state, items | runs due work | `/health` last_tick | Worker cron or DO alarm | BUILT in seed; preview accounts have none (issue workers#20) |
| Plus loop | last pass output | raises next pass | metric delta | write to specs/records | PLANNED in this repo |
| Managers | program health, focus | roadmap items | issue closed with evidence | file issues | RUNNING in QNFO, BUILT in seed |
| Probes (spec_truth, selfhost_check, agent-setup verify) | repo, live URL | pass/fail records | the probe itself, run by CI | read repo | BUILT |
| Loop closer | open issues, epics | closes issues, ticks children, labels open loops | label `open-loop` count | issue write | built on branch `loops/closer`, not merged |
| Doer/reviewer runner | PR records | PR state machine | merged and verified | PR write | BUILT (core/runner) |
| Actions budget watchdog | GitHub usage endpoint | alert, stop | `actions_budget.py` exit code | org billing read | BUILT in workers#58 (unmerged) |
| Launcher (Door A) | person's answers | a preview account | `/health` on preview | none stored | BUILT, unmerged (workers#56) |
| Plow-back at session end | session knowledge | glossary, directives, specs, tests | PR record names knowledge written | repo write | PLANNED (check T04) |

Open loops known today: no privilege to flip repos public (owner-only); counsel review of the license; claim step of a preview is the person's own.
