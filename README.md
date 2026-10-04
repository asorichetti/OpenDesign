# OpenDesign

An open-source, self-hostable alternative to the Claude.ai chat interface.

## What this is

A faithful recreation of Claude's chat UI — conversation threads, streaming markdown rendering, code blocks with syntax highlighting, file uploads, and conversation management — built as a standalone, self-hostable application.

## Tech Stack

- **Backend:** Go (Cobra CLI, ConnectRPC, PostgreSQL)
- **Frontend:** TypeScript + React + Vite
- **Database:** PostgreSQL (SQLite for local dev)
- **Monorepo:** Yarn workspaces + Turborepo
- **API:** Protobuf + Connect
- **Testing:** Playwright for E2E
- **Linting/Formatting:** Biome (TS) + golangci-lint (Go)

## Status

**Planning.** See `docs/plan/` for the architecture and task breakdown.

## License

MIT
