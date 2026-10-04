# Preview Engine

## Rendering Strategy

Designs are rendered in **sandboxed iframes** within Open WebUI's chat interface. No server-side rendering needed — the HTML is fully self-contained and runs client-side.

## Sandbox Security

Every preview iframe uses strict sandbox attributes:

```html
<iframe
  srcdoc="<html>...</html>"
  sandbox="allow-scripts allow-same-origin allow-forms"
  allow="fullscreen"
  style="width: 100%; height: 600px; border: 1px solid #e0e0e0; border-radius: 8px;"
></iframe>
```

### Sandbox Rules

| Attribute | Value | Reason |
|-----------|-------|--------|
| `sandbox` | `allow-scripts` | Allow JS for interactivity |
| `sandbox` | `allow-same-origin` | Allow CSS/JS to run (same origin) |
| `sandbox` | `allow-forms` | Allow form submission |
| `sandbox` | `allow-popups` | **NOT allowed** — prevents popup spam |
| `sandbox` | `allow-top-navigation` | **NOT allowed** — prevents frame busting |
| `srcdoc` | inline HTML | No external URL = no mixed content |

### Additional Hardening

1. **No external resources.** All CSS and JS is inlined. No `<link>` tags, no `<script src="">`.
2. **No `eval()`.** The generated HTML is validated to exclude dangerous patterns.
3. **No `postMessage`.** Iframes cannot communicate with parent.
4. **Content-Length limit.** Max preview size: 2MB. Larger designs are truncated with a warning.

## Preview UI

The Action function returns a rich HTML response that renders:

```
┌─────────────────────────────────────────────────────────────┐
│  🎨 Generated Preview                    [🔄 Refresh]       │
├─────────────────────────────────────────────────────────────┤
│  [🖥️ Desktop] [📱 Tablet] [📲 Mobile] [⛶ Fullscreen]       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  [ Preview renders here — fully interactive ]       │   │
│  │                                                     │   │
│  │  ┌─────────────────────────────────────────────┐    │   │
│  │  │  ☕ Bean & Brew                             │    │   │
│  │  │                                             │    │   │
│  │  │  Fresh coffee, brewed with care           │    │   │
│  │  │  [ Order Now ] [ View Menu ]              │    │   │
│  │  │                                             │    │   │
│  │  │  ┌──────┐ ┌──────┐ ┌──────┐              │    │   │
│  │  │  │☕ Espresso│☕ Latte │☕ Cappucc│              │    │   │
│  │  │  └──────┘ └──────┘ └──────┘              │    │   │
│  │                                             │    │   │
│  │  ┌─────────────────────────────────────────────┐    │   │
│  │  │  © 2025 Bean & Brew                          │    │   │
│  │  └─────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  Version 2 of 3          ← Previous  |  Next →             │
└─────────────────────────────────────────────────────────────┘
```

## Responsive Preview

The preview adapts to the chat width:

| Mode | Width | Trigger |
|------|-------|---------|
| Desktop | 100% of chat panel | Default |
| Tablet | 768px | "Tablet" view button |
| Mobile | 375px | "Mobile" view button |
| Fullscreen | 100vw × 100vh | "Fullscreen" button |

## Live Editor (Phase 5)

The split-pane editor provides real-time code-preview sync:

```
┌───────────────────────────────────────────────────────────────┐
│  ✏️ Design Editor                         [💾 Save] [👁️ Preview] │
├──────────────────────────────┬────────────────────────────────┤
│  < > Code                    │  <iframe> Preview               │
│                              │                                │
│  <html>                      │  ┌──────────────────────────┐  │
│  <head>                      │  │  [Live preview updates   │  │
│  <style>                     │  │   as you type]           │  │
│  </style>                    │  │                          │  │
│  </head>                     │  │  ☕ Bean & Brew          │  │
│  <body>                      │  │  ...                   │  │
│  <div>...</div>              │  └──────────────────────────┘  │
│  </body>                     │                                │
│  </html>                     │                                │
│                              │                                │
│  ──── resizable gutter ────  │                                │
│                              │                                │
│  Syntax highlighting         │  Auto-refresh on save/blur    │
│  Line numbers                │  Responsive toggle            │
│  Auto-complete (basic)       │  Fullscreen mode              │
└──────────────────────────────┴────────────────────────────────┘
```

### Live Editor Features

| Feature | Description |
|---------|-------------|
| Syntax highlighting | Basic HTML/CSS/JS coloring |
| Auto-refresh | Preview updates on save or blur |
| Resizable panes | Drag the divider to adjust |
| Fullscreen | Editor takes over the browser |
| Save | Persist changes to version history |
| Reset | Discard changes, reload last version |

### Editor Architecture

The live editor is rendered **inside the iframe** (not in the parent page) for security:

```
┌─────────────── Open WebUI ───────────────┐
│  ┌─────────────────────────────────────┐ │
│  │  <iframe sandbox="...">             │ │
│  │    ┌───────────┬─────────────────┐  │ │
│  │    │ Editor    │ Preview         │  │ │
│  │    │ (code)    │ (rendered HTML) │  │ │
│  │    │           │                 │  │ │
│  │    │ textarea  │ iframe srcdoc   │  │ │
│  │    │           │                 │  │ │
│  │    └───────────┴─────────────────┘  │ │
│  │  </iframe>                          │ │
│  └─────────────────────────────────────┘ │
└──────────────────────────────────────────┘
```

The editor page is served as inline `srcdoc` in a sandboxed iframe. It uses `postMessage` to communicate between the editor pane and preview pane (both inside the same sandbox).
