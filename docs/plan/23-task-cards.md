# Task Cards

## Status Legend

- `○` — Not started
- `▶` — In progress
- `✓` — Done
- `_blocked: ..._` — Blocked on external factor

## Phase 0: Foundations

**Goal:** Monorepo scaffold, CI pipeline, build system, service scaffolding.

### Card 0.1

**Title:** Initialize monorepo with Yarn workspaces + Turborepo

**Status:** ○

**Description:**
- Create root `package.json` with yarn workspaces config
- Add `turbo.json` with pipeline definitions
- Add root `tsconfig.json` extending `packages/tsconfig`
- Add `biome.json` for TS linting
- Add `go.work` for Go workspace
- Create workspace structure: `services/`, `packages/`, `tools/`
- Add root `Makefile` with common targets

**Verification:**
- `yarn install` succeeds
- `yarn turbo run build` succeeds (even if workspaces are empty)
- `go work edit -json` shows workspace

### Card 0.2

**Title:** Create Go backend service scaffold (`services/api`)

**Status:** ○

**Description:**
- Create `services/api/cmd/api/main.go` with Cobra root command
- Add `services/api/internal/` with empty domain packages: `chat`, `conversation`, `auth`, `settings`, `store`, `llm`
- Add `services/api/proto/` with empty protobuf directory
- Add `services/api/Makefile` with `build`, `proto`, `lint`, `test` targets
- Add `services/api/go.mod`

**Verification:**
- `go build ./cmd/api` compiles
- `go test ./...` runs (no tests yet)
- `make build` works in `services/api/`

### Card 0.3

**Title:** Create React frontend scaffold (`services/web`)

**Status:** ○

**Description:**
- Create `services/web/` with Vite + React + TypeScript template
- Add `package.json` with workspace reference
- Add `src/App.tsx` with placeholder layout
- Add `src/index.css` with CSS reset
- Add basic Vite config

**Verification:**
- `yarn dev` starts the dev server
- `yarn build` produces a production build
- Page renders "OpenDesign" placeholder

### Card 0.4

**Title:** Set up Protobuf + ConnectRPC codegen

**Status:** ○

**Description:**
- Add `buf.yaml`, `buf.gen.yaml` to `services/api/proto/`
- Create first proto file: `services/api/proto/v1/service.proto` (empty service)
- Add `make proto` target that runs `buf generate`
- Generate TypeScript client into `services/web/src/lib/proto/`

**Verification:**
- `make proto` in `services/api/` generates Go stubs
- TypeScript client appears in `services/web/src/lib/proto/`
- Generated code compiles in both languages

### Card 0.5

**Title:** Docker Compose for local development

**Status:** ○

**Description:**
- Create `docker-compose.yml` with PostgreSQL service
- Create `docker-compose.dev.yml` with dev overrides (volume mounts, hot reload)
- Add `Dockerfile` for the Go backend (multi-stage)
- Create `migrations/` directory with empty migration

**Verification:**
- `docker compose up -d` starts PostgreSQL
- `docker compose exec api make migrate-up` applies migrations
- Container stops cleanly with `docker compose down`

## Phase 1: Core UI

**Goal:** Static chat layout — sidebar, message area, input bar (no data yet).

### Card 1.1

**Title:** Implement sidebar layout with conversation list shell

**Status:** ○

**Description:**
- Create `Sidebar` component with left panel (~280px)
- Add `NewChatButton` at top
- Add `ConversationList` with mock data (5 conversations grouped by date)
- Add `ConversationItem` with title and timestamp
- Style to match Claude.ai sidebar (light/dark)

**Verification:**
- Sidebar renders on left, takes full viewport height
- Conversations group correctly (Today, Yesterday, Previous 7 Days)
- Hover states on conversation items

### Card 1.2

**Title:** Implement main chat panel layout

**Status:** ○

**Description:**
- Create `ChatPanel` component as main content area
- Add empty state when no conversation selected (centered prompt)
- Add `MessageList` component container (scrollable)
- Add `InputBar` component at bottom (static, no functionality yet)
- Match Claude.ai spacing and proportions

**Verification:**
- Main panel fills remaining viewport width
- Empty state shows "What can I help with?" prompt
- Input bar固定在 bottom with text area and send button

### Card 1.3

**Title:** Implement message rendering components

**Status:** ○

**Description:**
- Create `Message` component with user/assistant variants
- User messages: right-aligned, light background, rounded corners
- Assistant messages: full-width, no background, markdown-ready
- Create `MessageContent` wrapper for markdown rendering
- Create `CodeBlock` component with copy button

**Verification:**
- User message bubble appears on right with gray background
- Assistant message appears full-width with no background
- Code block has syntax highlighting placeholder and copy button

### Card 1.4

**Title:** Implement dark/light theme system

**Status:** ○

**Description:**
- Create CSS custom property tokens for light and dark themes
- Add `ThemeProvider` provider component
- Add `ThemeToggle` switch component
- Persist preference to localStorage
- Style sidebar, chat panel, messages in both themes

**Verification:**
- Theme toggles between light and dark
- All components update colors on theme change
- Preference persists across page reloads

### Card 1.5

**Title:** Wire up routing and navigation

**Status:** ○

**Description:**
- Add React Router v7
- Route `/` shows chat view
- Route `/folder/:id` filters conversations
- Route `/settings` shows settings drawer
- Sidebar navigation updates URL

**Verification:**
- Navigating to `/settings` opens settings drawer
- Clicking a conversation updates URL to `/?conv=xxx`
- Browser back button works

## Phase 2: Streaming Chat

**Goal:** Real-time chat with LLM streaming, markdown rendering.

### Card 2.1

**Title:** Implement LLM provider abstraction

**Status:** ○

**Description:**
- Create `llm/Provider` interface in Go with `Stream(ctx, messages) <-chan Chunk`
- Implement `OpenAICompatibleProvider` that calls OpenAI-compatible API
- Configurable via environment variables (base URL, API key, model)
- Support standard OpenAI streaming format

**Verification:**
- `go test ./internal/llm/` passes
- Provider streams text when given messages
- Errors (invalid key, timeout) propagate correctly

### Card 2.2

**Title:** Implement ChatService RPC with streaming

**Status:** ○

**Description:**
- Define `ChatService.StreamChat` in proto with `stream StreamChatResponse`
- Implement handler that calls LLM provider and forwards chunks via SSE
- Handle conversation persistence (save user message, stream assistant response)
- Add error handling and graceful shutdown

**Verification:**
- `make proto` generates streaming stubs
- `grpcurl` can call `StreamChat` and receive SSE stream
- Assistant response is saved to database on completion

### Card 2.3

**Title:** Implement frontend streaming hook

**Status:** ○

**Description:**
- Create `useStream` hook that calls `ChatService.StreamChat`
- Reads SSE stream and yields delta chunks
- Handles connection errors with retry logic
- Exposes `status: 'loading' | 'streaming' | 'done' | 'error'`

**Verification:**
- Hook receives each delta as it arrives
- UI updates in real-time (character-by-character feel)
- Connection error shows retry message

### Card 2.4

**Title:** Implement markdown and code rendering

**Status:** ○

**Description:**
- Add `react-markdown` + `remark-gfm` for markdown rendering
- Add `react-syntax-highlighter` + `prism-react-renderer` for code
- Sanitize all HTML (DOMPurify)
- Code blocks get copy button with clipboard API
- Add line numbers toggle

**Verification:**
- Markdown renders headers, lists, bold, italic, links
- Code blocks show syntax highlighting with copy button
- No HTML injection possible (sanitization verified)

### Card 2.5

**Title:** Implement message input and send flow

**Status:** ○

**Description:**
- Wire `InputBar` to send user message
- Auto-resize textarea (grows with content)
- Enter to send, Shift+Enter for newline
- Cmd/Ctrl+Enter to send
- Disable send button while streaming
- Show loading indicator on send button

**Verification:**
- Typing in input bar sends message on Enter
- Textarea grows vertically with content
- Send button shows spinner while streaming
- Shift+Enter adds newline without sending

## Phase 3: Conversation Management

**Goal:** Full CRUD for conversations, sidebar integration.

### Card 3.1

**Title:** Implement ConversationService RPC

**Status:** ○

**Description:**
- Define CRUD operations in proto
- Implement `ListConversations` with date grouping
- Implement `CreateConversation` (returns empty conversation)
- Implement `GetConversation` with full message history
- Implement `UpdateConversation` (rename, move to folder)
- Implement `DeleteConversation` (cascading delete messages)
- Add search with trigram similarity

**Verification:**
- All CRUD operations work via grpcurl
- List groups conversations by date (Today, Yesterday, etc.)
- Search returns results by title match
- Delete cascades to messages

### Card 3.2

**Title:** Wire sidebar to real conversations

**Status:** ○

**Description:**
- Replace mock data with real `useConversations` hook
- New Chat button creates conversation via RPC
- Clicking a conversation loads it in the chat panel
- Delete button on conversation items
- Auto-scroll to bottom on new conversation

**Verification:**
- Sidebar shows real conversations from database
- "New Chat" creates conversation and switches to it
- Clicking a conversation loads its message history
- Deleting a conversation removes it from sidebar

### Card 3.3

**Title:** Implement auto-naming of conversations

**Status:** ○

**Description:**
- After first assistant response, extract a title from the conversation
- Use first meaningful sentence or first 50 characters
- Store title in conversation record
- Update sidebar in real-time (optimistic update)

**Verification:**
- New conversation shows "New Chat" as placeholder
- After first response, title updates automatically
- User can still manually rename

### Card 3.4

**Title:** Implement folder organization

**Status:** ○

**Description:**
- Add `FolderService` in proto (CRUD for folders)
- Add folder creation/deletion in sidebar
- Drag conversations between folders (or use dropdown)
- Filter sidebar by folder
- Default "Uncategorized" folder

**Verification:**
- Folders appear in sidebar navigation
- Conversations can be moved to folders
- Filtering by folder shows correct conversations
- Uncategorized folder collects ungrouped conversations

## Phase 4: File Attachments

**Goal:** Upload and display images/files in conversations.

### Card 4.1

**Title:** Implement file upload backend

**Status:** ○

**Description:**
- Add `UploadService` with `UploadFile` RPC (multipart form)
- Store files in `uploads/` directory (configurable)
- Validate file type (image/*, .pdf, .txt, etc.)
- Validate file size (max 25MB default)
- Return file metadata (id, path, mime type, size)

**Verification:**
- Upload endpoint accepts multipart form
- Invalid files are rejected with proper error
- Files stored in uploads directory with UUID names
- File metadata saved to database

### Card 4.2

**Title:** Implement attachment UI

**Status:** ○

**Description:**
- Add file upload button to InputBar
- Add attachment preview zone (shows selected files before send)
- Remove attachments from preview
- Display images in messages as thumbnails
- Download button for non-image attachments

**Verification:**
- Clicking upload button opens file picker
- Selected files show as previews before sending
- Images render as thumbnails in message bubbles
- Non-image files show filename with download icon

## Phase 5: Settings & Auth

**Goal:** Self-hosted authentication and user settings.

### Card 5.1

**Title:** Implement user authentication

**Status:** ○

**Description:**
- Add `AuthService` with Register, Login, Logout, WhoAmI
- Password hashing with bcrypt
- JWT token generation and validation
- Auth middleware for protected routes
- Session persistence (token in localStorage + httpOnly cookie)

**Verification:**
- Register creates new user, returns JWT
- Login validates credentials, returns JWT
- Protected RPCs reject requests without valid token
- Logout invalidates session

### Card 5.2

**Title:** Implement user settings

**Status:** ○

**Description:**
- Add `SettingsService` RPC (GetSettings, UpdateSettings)
- Settings panel in UI with theme, model, system prompt
- Save settings to database per user
- Settings persist across sessions
- Default model from environment variable

**Verification:**
- Settings panel loads current user settings
- Changing model/system prompt saves to database
- Theme setting persists across reloads
- Settings apply immediately without restart

### Card 5.3

**Title:** Implement self-hosted API key mode

**Status:** ○

**Description:**
- When API key is configured (no user auth), skip auth entirely
- Use API key for LLM provider authentication
- Add configuration via environment variable
- Support both modes: auth-required and API-key-only

**Verification:**
- With API_KEY set: no auth needed, direct API access
- Without API_KEY: full auth flow required
- LLM calls use configured API key

## Phase 6: Polish & Deploy

**Goal:** Production hardening, Docker deployment, documentation.

### Card 6.1

**Title:** Docker production build

**Status:** ○

**Description:**
- Multi-stage Dockerfile for Go backend (Alpine)
- Nginx reverse proxy for static files + API
- Production `docker-compose.yml` (no dev overrides)
- Health check endpoints
- Graceful shutdown

**Verification:**
- `docker compose up -d` starts full stack
- Health check returns 200
- Frontend served at `/`, API at `/api/v1/`
- `docker compose down` cleans up

### Card 6.2

**Title:** Write documentation

**Status:** ○

**Description:**
- README with setup instructions (Docker, source)
- Configuration guide (env vars, options)
- Self-hosting guide
- Migration guide (if any)
- Contribution guidelines

**Verification:**
- README has clear getting started instructions
- All environment variables documented
- Docker setup works from scratch in 10 minutes

### Card 6.3

**Title:** E2E test suite with Playwright

**Status:** ○

**Description:**
- Set up Playwright in `services/web/`
- Journey: send message, receive streaming response
- Journey: create and switch between conversations
- Journey: settings panel toggle
- Journey: dark/light theme switch

**Verification:**
- `yarn test:e2e` runs all journeys
- All journeys pass on clean build
- Evidence bundles generated on failure

### Card 6.4

**Title:** Accessibility audit and fixes

**Status:** ○

**Description:**
- Run axe-core audit on all pages
- Fix all contrast violations
- Ensure keyboard navigation is complete
- Add ARIA labels where needed
- Test with screen reader

**Verification:**
- Zero axe violations
- All interactive elements reachable via Tab
- Screen reader announces message roles
- Focus visible on all interactive elements

## Summary

**Total cards:** 27
**Phases:** 6
**Estimated complexity:** Medium-Large

Phase 0-2 deliver a working chat interface. Phase 3-5 add production features. Phase 6 hardens for deployment.
