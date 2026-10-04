# Backend Architecture

## Layering

Within each domain package (following baking-companion pattern):

```
services/api/internal/chat/
├── domain.go         — Pure types: Message, Conversation, Chunk
├── domain_test.go    — Unit tests for pure logic
├── service.go        — Connect handler: validates, calls domain + store
├── service_test.go   — Handler tests with mock store
└── store.go          — DB queries: SaveMessage, ListConversations
    └── store_test.go — Integration tests with test database
```

Dependency direction: `service → domain ← store`
- `domain` knows nothing about DB or network
- `store` returns domain types
- `service` orchestrates: validate → domain → store → respond

## Service Startup

```go
// cmd/api/main.go
func main() {
    rootCmd := cobra.Command{
        Use:   "api",
        Short: "OpenDesign API server",
        RunE:  runServer,
    }
    rootCmd.PersistentFlags().String("addr", ":8080", "listen address")
    rootCmd.PersistentFlags().Bool("migrate-up", false, "run migrations and exit")
    // ...
}
```

Two modes:
1. `api --migrate-up` — applies all migrations, exits
2. `api` — starts HTTP server with gRPC/Connect endpoints

## Middleware Stack

```
Request
  → Auth (JWT validation, skip for public routes)
  → Tenant (extract user from JWT, attach to context)
  → RateLimit (optional, per-user)
  → Handler
  → Response
```

## Database Layer

Uses `pgx/v5` directly. Each table has a `store_X.go` file.

```go
// store/conversation.go
func (s *Store) GetConversation(ctx context.Context, id uuid.UUID) (*domain.Conversation, error) {
    row := s.db.QueryRow(ctx, getConversationSQL, id)
    var c domain.Conversation
    err := row.Scan(&c.ID, &c.UserID, &c.Title, ...)
    return &c, err
}
```

SQL files live in `internal/store/sql/`:
```
sql/
├── conversation.sql
├── message.sql
├── folder.sql
├── settings.sql
└── user.sql
```

## LLM Provider Abstraction

```go
// internal/llm/provider.go
type Provider interface {
    Stream(ctx context.Context, req StreamRequest) (<-chan StreamChunk, error)
    Name() string
}

type StreamChunk struct {
    Text  string
    Error error
    Done  bool
}

type StreamRequest struct {
    Messages     []domain.Message
    Model        string
    SystemPrompt string
}
```

Default implementation: `OpenAICompatibleProvider`
- Supports any OpenAI-compatible API (OpenAI, Ollama, vLLM, etc.)
- Configurable via env vars: `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL`

## Error Handling

```go
// internal/errors/errors.go
var (
    ErrNotFound       = errors.New("not found")
    ErrUnauthorized   = errors.New("unauthorized")
    ErrBadRequest     = errors.New("bad request")
    ErrProviderDown   = errors.New("LLM provider unavailable")
)
```

Mapped to Connect RPC codes in service layer.

## Migrations

```bash
# Run all pending migrations
make migrate-up

# Rollback last migration
make migrate-down
```

Migration files in `migrations/`:
```
001_create_users.sql
002_create_conversations.sql
003_create_messages.sql
004_create_folders.sql
005_create_settings.sql
```

Tracked via `schema_migrations` table.
