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
│  🎨 Generated Preview                    [🔄 Refresh] [⛶ Full] │
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
│  │  │  │☕ Espress│☕ Latte │☕ Cappucc│              │    │   │
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
| Fullscreen | 100vw × 100vh | "Full" view button |

## Live Edit (Future)

Phase 5+ may include a split-pane live editor:
- Left: code editor with syntax highlighting
- Right: live preview that updates as you type
- Powered by a WebSocket connection to a preview server
