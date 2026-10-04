# Design System

## Design Philosophy

OpenDesign's UI is a faithful recreation of Claude.ai's interface — clean, minimal, and focused on the conversation. The design prioritizes readability and speed over decoration.

## Color Tokens

### Light Theme

| Token                | Hex      | Usage                    |
|----------------------|----------|--------------------------|
| `bg-primary`         | `#FFFFFF`| Main background          |
| `bg-secondary`       | `#F7F7F8`| Sidebar, panels          |
| `bg-tertiary`        | `#E5E5E7`| Hover states, dividers   |
| `text-primary`       | `#1A1A1A`| Body text                |
| `text-secondary`     | `#6B6B6B`| Muted text, timestamps   |
| `text-tertiary`      | `#999999`| Placeholders             |
| `accent`             | `#737373`| Links, active states     |
| `accent-hover`       | `#404040`| Hover on links           |
| `border`             | `#E0E0E0`| Borders, dividers        |
| `user-bubble`        | `#F0F0F0`| User message background  |
| `assistant-bubble`   | `transparent`| Assistant messages  |
| `code-bg`            | `#F4F4F5`| Code block background    |
| `code-text`          | `#18181B`| Code block text          |
| `danger`             | `#DC2626`| Error states, delete     |
| `success`            | `#16A34A`| Success states           |

### Dark Theme

| Token                | Hex      | Usage                    |
|----------------------|----------|--------------------------|
| `bg-primary`         | `#1A1A2B`| Main background          |
| `bg-secondary`       | `#13131F`| Sidebar, panels          |
| `bg-tertiary`        | `#2A2A3E`| Hover states, dividers   |
| `text-primary`       | `#E8E8ED`| Body text                |
| `text-secondary`     | `#9898A6`| Muted text, timestamps   |
| `text-tertiary`      | `#5C5C6B`| Placeholders             |
| `accent`             | `#A1A1AA`| Links, active states     |
| `accent-hover`       | `#D4D4D8`| Hover on links           |
| `border`             | `#3A3A4A`| Borders, dividers        |
| `user-bubble`        | `#2A2A3E`| User message background  |
| `assistant-bubble`   | `transparent`| Assistant messages  |
| `code-bg`            | `#252535`| Code block background    |
| `code-text`          | `#E8E8ED`| Code block text          |

Typography follows the Claude.ai spec: system font stack (Inter-like), 16px body, 14px code, 13px sidebar.

## Component Inventory

### Layout

- `App` — Full-page layout with sidebar + main
- `Sidebar` — Conversation list, new chat button, settings trigger
- `ChatPanel` — Main chat area with messages + input
- `SettingsPanel` — User settings drawer/modal

### Sidebar

- `NewChatButton` — "New Chat" button (top of sidebar)
- `ConversationList` — Grouped conversations (Today, Yesterday, etc.)
- `ConversationItem` — Single conversation in list
- `ConversationSearch` — Search input for conversations
- `FolderList` — Folder navigation (collapsible)
- `SettingsTrigger` — Gear icon, opens settings

### Chat

- `MessageList` — Scrollable message container
- `Message` — Single message (user or assistant)
- `MessageContent` — Markdown-rendered content
- `CodeBlock` — Syntax-highlighted code with copy button
- `AttachmentPreview` — File/image thumbnail in messages
- `InputBar` — Multi-line text input + send button
- `AttachmentUploader` — File upload zone with preview

### Settings

- `ThemeToggle` — Light/dark mode switch
- `ModelSelector` — LLM model dropdown
- `SystemPromptEditor` — Custom system prompt textarea
- `ApiKeyInput` — Self-host API key input

### Shared

- `Button` — Primary, secondary, ghost variants
- `Modal` — Backdrop, close on escape
- `Drawer` — Slide-out panel (settings)
- `Tooltip` — Hover tooltip
- `Skeleton` — Loading placeholder

## Spacing Scale

```
4px:  xs (4)
8px:  sm (8)
12px: md (12)
16px: lg (16)
24px: xl (24)
32px: 2xl (32)
48px: 3xl (48)
```

## Breakpoints

| Name  | Width  | Usage               |
|-------|--------|---------------------|
| sm    | 640px  | Mobile              |
| md    | 768px  | Tablet              |
| lg    | 1024px | Desktop             |
| xl    | 1280px | Large desktop       |
