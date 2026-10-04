# Architecture

## System Overview

```
┌──────────────────────────────────────────────────────┐
│                    Frontend (Vite/TS)                 │
│  ┌───────────┐  ┌──────────────┐  ┌───────────────┐ │
│  │   Sidebar │  │  Chat Panel  │  │   Settings    │ │
│  │  Convs.   │  │  Messages    │  │    / Auth     │ │
│  └───────────┘  └──────────────┘  └───────────────┘ │
└──────────────────────┬───────────────────────────────┘
                       │ ConnectRPC (HTTP/JSON + SSE)
┌──────────────────────▼───────────────────────────────┐
│                 Backend (Go)                          │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │  Chat RPC   │  │  Conv RPC    │  │  Auth RPC  │  │
│  │  (stream)   │  │  (REST)      │  │  (JWT)     │  │
│  └──────┬──────┘  └──────┬───────┘  └─────┬──────┘  │
│         │                │                │          │
│  ┌──────▼────────────────▼────────────────▼──────┐  │
│  │              Domain Layer                      │  │
│  │  Chat · Conversation · Auth · Settings         │  │
│  └──────┬───────────────────────────────────────┘  │
│         │                                           │
│  ┌──────▼──────┐  ┌──────────────┐  ┌───────────┐ │
│  │  PostgreSQL │  │  Filesystem  │  │  LLM API  │ │
│  │  (data)     │  │  (uploads)   │  │  (stream) │ │
│  └─────────────┘  └──────────────┘  └───────────┘ │
└──────────────────────────────────────────────────────┘
```

## Monorepo Layout

```
OpenDesign/
├── package.json              # Workspace root (yarn workspaces + turbo)
├── turbo.json
├── tsconfig.json
├── biome.json
├── go.work
├── docker-compose.yml
├── docker-compose.dev.yml
├── docs/
│   └── plan/                 # Planning documents
├── services/
│   ├── api/                  # Go backend (ConnectRPC server)
│   │   ├── cmd/
│   │   │   └── api/
│   │   │       └── main.go   # Entry point
│   │   ├── internal/
│   │   │   ├── chat/         # Chat domain + handler
│   │   │   ├── conversation/ # Conversation domain + handler
│   │   │   ├── auth/         # Auth domain + handler
│   │   │   ├── settings/     # Settings domain + handler
│   │   │   ├── store/        # Database layer
│   │   │   ├── llm/          # LLM provider abstraction
│   │   │   └── upload/       # File upload handler
│   │   ├── proto/            # Protobuf definitions
│   │   │   └── v1/
│   │   │       ├── chat.proto
│   │   │       ├── conversation.proto
│   │   │       ├── auth.proto
│   │   │       └── settings.proto
│   │   └── Makefile
│   └── web/                  # React frontend (Vite)
│       ├── src/
│       │   ├── components/   # Reusable UI components
│       │   │   ├── Sidebar/
│       │   │   ├── ChatPanel/
│       │   │   ├── Message/
│       │   │   ├── InputBar/
│       │   │   └── Settings/
│       │   ├── hooks/        # React hooks (useStream, useConversations)
│       │   ├── store/        # State management (Zustand)
│       │   ├── lib/          # ConnectRPC clients, utils
│       │   ├── styles/       # Global styles, theme
│       │   └── App.tsx
│       └── package.json
├── packages/
│   ├── ui/                   # Shared UI component library
│   │   └── src/
│   ├── tsconfig/             # Shared TS configs
│   └── types/                # Shared TypeScript types
└── tools/
    └── service-creator/      # Go CLI to scaffold new services
```

## Service Boundaries

### `services/api` — The backend service

A single Go binary that exposes:
- **ConnectRPC** over HTTP/JSON (with SSE for streaming)
- **File uploads** via multipart form
- **Static file serving** in production (serves the web build)

Internal layers (following baking-companion pattern):
- **`proto/`** — Protobuf definitions (single source of truth for API)
- **`internal/store/`** — PostgreSQL queries using pgx, returning domain types
- **`internal/<domain>/service.go`** — Connect handlers, no business logic
- **`internal/<domain>/domain.go`** — Pure domain logic, no DB or network deps
- **`internal/llm/`** — Provider abstraction for LLM streaming

### `services/web` — The frontend

A Vite + React SPA that:
- Communicates with `api` via generated ConnectRPC clients
- Handles routing, state (Zustand), and local storage
- Provides the full Claude.ai UI clone

### `packages/ui` — Shared component library

Components used by both the web frontend and future mobile apps. Built with Storybook.

## Deployment

### Development
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
# or
yarn dev
```

### Production
```bash
docker compose up -d
```

Single binary (`api`) serves both gRPC/HTTP and the static frontend.
PostgreSQL runs in Docker. File uploads stored on disk (configurable S3).

## Non-goals (v1)

- Multi-model switching (single LLM provider at a time)
- Code interpreter / advanced tool use
- File search across conversations
- Team sharing / collaborative editing
- Native mobile apps (responsive web only)
