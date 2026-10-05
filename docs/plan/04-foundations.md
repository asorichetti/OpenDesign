# Foundations

## Tech Choices

| Layer | Choice | Why |
|-------|--------|-----|
| Plugin Runtime | Open WebUI Python Functions | In-process, full Python access, auto-loaded |
| Design Generation | LLM (user-configurable) | Works with any model Open WebUI supports |
| Preview Rendering | Sandboxed iframe | Safe HTML rendering, no SSR needed |
| Live Editor | WebSocket proxy (Phase 5) | Real-time code-preview sync |
| Template Storage | Static files (markdown + HTML) | Simple, versionable, no database needed |
| Design State | JSON files | Per-user design history, lightweight |
| Styling | CSS custom properties | Theme switching, design tokens |
| Linting | ruff (Python) | Fast, auto-formatting |
| Testing | pytest | Standard Python test framework |

## Non-Negotiables

1. **Preview sandboxes never trust user input.** Every preview is rendered in an iframe with `sandbox` attributes. No `allow-scripts` without restrictions. No `allow-same-origin`. This is a hard security block.

2. **The Pipe never calls the LLM directly.** It always uses Open WebUI's request context (`__user__`, `__event_emitter__`, `__metadata__`). This ensures proper auth, rate limiting, and token tracking.

3. **All design prompts are stored as separate markdown files.** Never in Python strings. This lets users edit them without touching code.

4. **Templates are static, not generated from code.** A template is a `.html` file with placeholder comments (`<!-- {{title}} -->`). The LLM fills them in. No runtime template engine needed.

5. **No persistent database required.** Designs are stored as JSON files in Open WebUI's data directory. If no data dir is configured, the Pipe gracefully falls back to in-memory-only mode.

6. **The filter must not slow down non-design conversations.** Keyword detection happens on the first 100 chars of the prompt. If no design keywords match, the filter returns immediately with no LLM call.

7. **All generated HTML must be valid and accessible.** WCAG 2.1 AA contrast ratios, semantic HTML elements, ARIA attributes on interactive elements. This is validated before returning to the user.

8. **Template sharing must be safe.** Community templates are validated for dangerous patterns before loading. No `eval()`, no `import`, no file system access.

## Python Function Conventions

Following Open WebUI's plugin patterns:

```python
"""
title: OpenDesigner Design Studio
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesigner
version: 0.1.0
icon_url: https://example.com/icon.svg
required_open_webui_version: 0.10.0
requirements: jinja2, beautifulsoup4, requests
"""

from pydantic import BaseModel, Field
from typing import Optional


class Valves(BaseModel):
    """Admin-configurable settings."""

    base_model: str = Field(default="gpt-4o", description="LLM to use for generation")
    api_key: Optional[str] = Field(default=None, description="API key (if not using Ollama)")
    preview_timeout: int = Field(default=10, description="Preview render timeout in seconds")


class UserValves(BaseModel):
    """User-configurable settings."""

    template: str = Field(default="landing", description="Default template to use")
    design_system: str = Field(default="light", description="Design system preset")
    auto_preview: bool = Field(default=True, description="Auto-generate preview on send")


class Pipe:
    def __init__(self):
        self.type = "pipe"
        self.name = "Design Studio"
        self.valves = Valves()
        self.user_valves = UserValves()

    async def pipe(self, body: dict, __user__=None, __event_emitter__=None, **kwargs):
        # Implementation
        ...
```

## Prompt Engineering Strategy

Design prompts are stored as templates with Jinja2 variables:

```
# prompts/generate_html.md
You are a senior front-end designer. Create a complete, self-contained HTML page based on the user's request.

## Requirements
- Single HTML file with embedded CSS and JavaScript
- Semantic HTML5 elements (header, main, footer, nav, section, article)
- WCAG 2.1 AA accessible (proper contrast, ARIA labels, keyboard navigation)
- Responsive design (mobile-first)
- {{ design_system }} design system

## Output Format
Return ONLY the HTML code. Wrap it in a code block:
```html
{{ code }}
```
```

## File Layout

```
functions/design_studio/
├── design_studio.py          # Pipe (400-600 lines)
├── prompts/
│   ├── system.md             # Base system prompt (200 chars)
│   ├── generate_html.md      # HTML generation (400 chars)
│   ├── iterate.md            # Iteration/refinement (300 chars)
│   ├── present.md            # Presentation mode (350 chars)
│   ├── email.md              # Email template prompt (300 chars)
│   └── social.md             # Social asset prompt (250 chars)
├── templates/
│   ├── landing/
│   │   ├── minimal.html      # Clean, minimal landing
│   │   ├── feature-grid.html # Feature showcase layout
│   │   └── hero.html         # Hero-section focused
│   ├── dashboard/
│   │   ├── analytics.html    # Data dashboard
│   │   └── admin.html        # Admin panel layout
│   ├── component/
│   │   ├── button.html       # Button variants
│   │   ├── card.html         # Card layouts
│   │   ├── modal.html        # Modal/dialog
│   │   └── form.html         # Form elements
│   ├── presentation/
│   │   ├── blank.html        # Blank slide deck
│   │   └── sections.html     # Pre-sectioned deck
│   ├── email/
│   │   ├── newsletter.html   # Newsletter layout
│   │   └── transactional.html # Receipt/confirmation
│   └── social/
│       ├── hero-banner.html  # Hero banner
│       └── og-card.html      # Open Graph card
├── live/
│   ├── editor.html           # Split-pane editor UI
│   └── websocket.js          # Live sync protocol
├── assets/
│   ├── light.css             # Light theme tokens
│   ├── dark.css              # Dark theme tokens
│   └── accessible.css        # WCAG AA compliance layer
└── frontmatter.md            # Plugin metadata

functions/preview_generator/
├── preview_generator.py      # Action (200-300 lines)
└── frontmatter.md

functions/prompt_enhancer/
├── prompt_enhancer.py        # Filter (100-200 lines)
└── frontmatter.md
```
