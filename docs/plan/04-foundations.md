# Foundations

## Tech Choices

| Layer          | Choice                    | Why                                                                 |
|----------------|---------------------------|---------------------------------------------------------------------|
| Language (BE)  | Go                        | Single static binary, strong typing, great concurrency primitives   |
| Language (FE)  | TypeScript + React        | Type safety, component model, ecosystem maturity                    |
| API Protocol   | ConnectRPC + Protobuf     | Type-safe across Go/TS, auto-generated code, SSE streaming support  |
| Build System   | Turborepo + Yarn 4        | Monorepo caching, workspace management, reproducible builds         |
| Database       | PostgreSQL                | ACID, JSONB, trigram search, mature Go driver (pgx)                 |
| ORM/Query      | pgx + hand-written SQL    | Full control, reviewable SQL, no magic                              |
| Auth           | bcrypt + JWT              | Simple, self-hosted, no external deps                               |
| File Storage   | Local filesystem (S3 opt) | Simple first, S3 configurable later                                 |
| LLM Backend    | OpenAI-compatible API     | Provider abstraction, swap providers via config                     |
| Linting        | Biome (TS) + golangci-lint (Go) | Fast, opinionated, single config per language                  |
| Formatting     | Biome (TS) + gofmt (Go)   | Zero-config, deterministic                                       |
| Testing (FE)   | Playwright                | Evidence-based E2E, matches mono/baking-companion pattern           |
| Testing (BE)   | Go test + pgx testutil    | Standard library, no framework overhead                             |
| Icons          | Lucide React              | Clean, consistent, MIT licensed                                     |
| Markdown       | react-markdown + remark   | Safe rendering, plugins for code blocks                             |
| Syntax Highlighting | react-syntax-highlighter | Widely used, supports many languages                              |
| State Mgmt     | Zustand                   | Minimal boilerplate, TypeScript-friendly                            |
| Routing        | React Router v7           | Standard, file-based routing ready                                 |

## Non-Negotiables

These are the things that separate a production tool from a demo. Do not drop any of them.

1. **Every conversation message stores the full text.** No partial rendering tricks. The database is the source of truth. Streaming is purely a UX layer.

2. **No floating point for IDs.** UUIDv7 everywhere. Generated in the application layer, never the database.

3. **Timestamps are RFC 3339 UTC strings.** Stored in PostgreSQL `timestamptz`, serialized as RFC 3339 text in JSON. Never Unix epoch in the API.

4. **SQL lives in hand-written files.** No ORMs, no code generators for queries. Each migration is a `.sql` file reviewed by humans.

5. **The domain layer knows nothing about SQL or network.** Pure types, pure logic. `store/` translates; `domain/` calculates; `service/` orchestrates.

6. **Every mutating RPC with an irreversible effect takes validation.** Deleting a conversation checks ownership. Uploading a file checks size and type. Never trust the client.

7. **Markdown rendering is sanitized.** All HTML is stripped. Only safe elements are allowed. This is a hard block, not a warning.

8. **The codebase must compile at every checkpoint.** Build in order, verify at each step. Never write 20 files and try to compile once.

9. **Every user-visible string is i18n-ready.** Even if we only ship English today, no hard-coded strings in component code.

10. **The frontend must be keyboard-complete.** Tab navigation, Enter to submit, Escape to close modals. Zero axe violations.

## Commit Conventions

Conventional Commits scoped by service:

```
feat(api): stream chat with SSE protocol
feat(web): add streaming message component
fix(api): handle empty conversation on regenerate
docs(plan): update data model for attachments
```

Scope formats:
- `api` — Go backend
- `web` — React frontend
- `ui` — shared component library
- `proto` — protobuf definitions
- `plan` — planning documents
- `docker` — docker compose files
- `deps` — dependency updates

## Project Structure

See `02-architecture.md` for the full monorepo layout.
