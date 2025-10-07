╭────────────────────── Next Steps ──────────────────────╮
│                                                        │
│  1. You're already in the project directory!           │
│  2. Set CODEX_HOME environment variable before         │
│  running Codex: export                                 │
│  CODEX_HOME='/Users/bbrenner/Documents/Scripting       │
│  Projects/docker-mcp-server/.codex'                    │
│  3. Start using slash commands with your AI agent:     │
│     2.1 /speckit.constitution - Establish project      │
│  principles                                            │
│     2.2 /speckit.specify - Create baseline             │
│  specification                                         │
│     2.3 /speckit.plan - Create implementation plan     │
│     2.4 /speckit.tasks - Generate actionable tasks     │
│     2.5 /speckit.implement - Execute implementation    │
│                                                        │
╰────────────────────────────────────────────────────────╯

╭───────────────── Enhancement Commands ─────────────────╮
│                                                        │
│  Optional commands that you can use for your specs     │
│  (improve quality & confidence)                        │
│                                                        │
│  ○ /speckit.clarify (optional) - Ask structured        │
│  questions to de-risk ambiguous areas before planning  │
│  (run before /speckit.plan if used)                    │
│  ○ /speckit.analyze (optional) - Cross-artifact        │
│  consistency & alignment report (after                 │
│  /speckit.tasks, before /speckit.implement)            │
│  ○ /speckit.checklist (optional) - Generate quality    │
│  checklists to validate requirements completeness,     │
│  clarity, and consistency (after /speckit.plan)

## Constitution Quick Reference
- Containerized Determinism — ship pinned Docker images, document env/ports/volumes, and keep smoke tests green.
- MCP Protocol Fidelity — cite the spec version, advertise capabilities, and cover handshake/tool contracts in tests.
- Contract-First Automation — write failing tests before code and reference their commands in plans and tasks.
- Observability & Incident Readiness — log in structured formats, expose health checks, and document incident scripts.
- Security & Least Privilege — run as non-root, isolate secrets, and justify every external dependency.

Refer back to `.specify/memory/constitution.md` whenever planning, specifying, or implementing features.
