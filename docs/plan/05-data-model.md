# Data Model

## Entity Overview

```
┌──────────┐     ┌──────────────────┐     ┌──────────┐
│  User    │────<│ Conversation     │>────│ Message  │
│          │     │   - id (UUIDv7)  │     │          │
│  - id    │     │   - user_id      │     │  - id    │
│  - email │     │   - title        │     │  - conv  │
│  - pass  │     │   - created_at   │     │  - type  │
│  - api_  │     │   - updated_at   │     │  - role  │
│    key   │     │   - folder_id    │     │  - text  │
└──────────┘     │   - metadata     │     │  - opts  │
                 └──────────────────┘     │  - order │
                 ┌──────────┐              └──────────┘
                 │  Folder  │
                 │  - id    │────< ┌──────────────┐
                 │  - name  │      │ Attachment   │
                 │  - user  │      │  - id        │
                 └──────────┘      │  - message   │
                                   │  - file_type │
                                   │  - path      │
                                   └──────────────┘
```

## Tables

### `users`

| Column      | Type         | Notes                    |
|-------------|--------------|--------------------------|
| id          | uuid         | PK, UUIDv7               |
| email       | text         | UK, indexed              |
| password    | text         | bcrypt hashed            |
| api_key     | text         | Nullable, for self-host  |
| created_at  | timestamptz  | UTC, RFC 3339            |
| updated_at  | timestamptz  | UTC, RFC 3339            |

### `conversations`

| Column      | Type         | Notes                    |
|-------------|--------------|--------------------------|
| id          | uuid         | PK, UUIDv7               |
| user_id     | uuid         | FK → users.id            |
| title       | text         | Auto-generated from 1st msg |
| folder_id   | uuid         | FK → folders.id, nullable |
| created_at  | timestamptz  | UTC, RFC 3339            |
| updated_at  | timestamptz  | UTC, RFC 3339            |
| metadata    | jsonb        | Extra metadata           |

### `messages`

| Column      | Type         | Notes                    |
|-------------|--------------|--------------------------|
| id          | uuid         | PK, UUIDv7               |
| conversation_id | uuid     | FK → conversations.id, indexed |
| role        | text         | `'user'` or `'assistant'` |
| content     | text         | Markdown text            |
| attachments | jsonb        | File refs                |
| order_num   | int          | Sort order within conv   |
| created_at  | timestamptz  | UTC, RFC 3339            |

### `folders`

| Column      | Type         | Notes                    |
|-------------|--------------|--------------------------|
| id          | uuid         | PK, UUIDv7               |
| user_id     | uuid         | FK → users.id            |
| name        | text         |                          |
| created_at  | timestamptz  | UTC, RFC 3339            |

### `settings`

| Column      | Type         | Notes                    |
|-------------|--------------|--------------------------|
| user_id     | uuid         | PK, FK → users.id        |
| theme       | text         | `'light'` or `'dark'`    |
| model       | text         | LLM model name           |
| system_prompt | text       | Custom system prompt     |
| created_at  | timestamptz  | UTC, RFC 3339            |

## Indexes

- `conversations(user_id, updated_at DESC)` — sidebar listing
- `conversations(user_id, title)` — search by title (GIN trigram)
- `messages(conversation_id, order_num)` — message ordering
- `users(email)` — login lookup

## Migration Strategy

Migrations are forward-only and numbered:
```
migrations/
├── 001_create_users.sql
├── 002_create_conversations.sql
├── 003_create_messages.sql
├── 004_create_folders.sql
└── 005_create_settings.sql
```

Tracked by `PRAGMA user_version` equivalent in PostgreSQL via a `schema_migrations` table.
A released migration is never edited.
