# Frontend Architecture

## Component Hierarchy

```
App
├── Sidebar (fixed width, scrollable)
│   ├── NewChatButton
│   ├── ConversationSearch
│   ├── FolderList
│   │   └── FolderItem (collapsible)
│   ├── ConversationList
│   │   └── ConversationItem (clickable, shows preview)
│   └── SettingsTrigger (gear icon)
│
├── ChatPanel (flex: 1, takes remaining width)
│   ├── EmptyState (shown when no conversation selected)
│   ├── MessageList (scrollable, flex: 1)
│   │   ├── Message (user)
│   │   │   └── MessageContent
│   │   │       ├── MarkdownRenderer
│   │   │       └── CodeBlock
│   │   └── Message (assistant)
│   │       └── MessageContent
│   │           ├── MarkdownRenderer
│   │           └── CodeBlock
│   │
│   └── InputBar (fixed to bottom)
│       ├── AttachmentPreview (horizontal scroll)
│       ├── Textarea (auto-resize)
│       ├── FileUploadButton
│       └── SendButton
│
└── SettingsDrawer (slide-out from right)
    ├── ThemeToggle
    ├── ModelSelector
    ├── SystemPromptEditor
    └── ApiKeyInput (self-host mode)
```

## State Management (Zustand)

### Store Structure

```typescript
// conversations/store.ts
interface ConversationsState {
  items: Conversation[];
  selectedId: string | null;
  folderFilter: string | null;
  load: () => Promise<void>;
  create: () => Promise<string>;
  select: (id: string) => void;
  delete: (id: string) => void;
  updateTitle: (id: string, title: string) => void;
}

// chat/store.ts
interface ChatState {
  messages: Message[];
  streaming: boolean;
  error: string | null;
  send: (content: string, attachments: Attachment[]) => Promise<void>;
  regenerate: () => Promise<void>;
  clear: () => void;
}

// settings/store.ts
interface SettingsState {
  theme: 'light' | 'dark';
  model: string;
  systemPrompt: string;
  load: () => Promise<void>;
  update: (updates: Partial<SettingsState>) => Promise<void>;
}
```

## Data Flow

1. User types in `InputBar` and presses Enter
2. `InputBar` calls `chatStore.send(content, attachments)`
3. `send()` creates a user message in the store (optimistic)
4. `send()` calls `ChatService.StreamChat()` via ConnectRPC
5. `useStream` hook reads SSE chunks and appends to messages
6. On `done: true`, save full conversation to database
7. Sidebar updates automatically (Zustand subscription)

## Key React Hooks

- `useConversations()` — load, create, delete conversations
- `useCurrentConversation()` — selected conversation + messages
- `useStream()` — SSE streaming for chat responses
- `useSettings()` — load/save user settings
- `useTheme()` — current theme + toggle
- `useUpload()` — file upload with progress

## Routing

```typescript
// React Router v7
<Route path="/" element={<ChatView />} />
<Route path="/folder/:folderId" element={<ChatView />} />
<Route path="/settings" element={<SettingsDrawer />} />
```

URL query parameters:
- `?conv=xxx` — selected conversation ID
- `?folder=yyy` — folder filter
