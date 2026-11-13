# Owner directives

Standing directives from the owner. Each entry is quoted exactly as given, followed by how it applies. Directives are append-only: a new directive supersedes an old one by naming it.

## DIR-1: Zero-user-action loop closure (2026-11-13)

> THE ULTRASTABLE SYSTEM SHALL ALWAYS CLOSE ALL LOOPS AUTOMATICALLY AND AUTONOMOUSLY, 100% SERVER-SIDE WITH ZERO USER ACTION

How it applies:

- Every loop closer runs server-side (a cron, worker or workflow). A local script or a step in a chat does not count as a closer.
- A loop that needs a user step to close is an open loop and a defect.
- The only exception is an action that is both irreversible and identity-bound: money, legal signing, or signing in to the owner's own accounts. The system records each one as an owner card with its reason. It never phrases the card as a question.

Related: US-SPEC-23 (closed system), SELF-CLOSED-LOOPS-1.
