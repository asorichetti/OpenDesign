# OpenDesigner API Reference

## Overview

OpenDesigner is a collection of Open WebUI plugin functions that work together to create an AI-powered design generation platform.

## Architecture

```
┌─────────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Prompt Enhancer   │────▶│   Design Studio  │────▶│  Preview Gen    │
│      (Filter)       │     │     (Pipe)       │     │    (Action)     │
└─────────────────────┘     └──────────────────┘     └─────────────────┘
                                       │                        │
                                       ▼                        ▼
                              ┌──────────────────┐     ┌─────────────────┐
                              │  Template Store  │     │  Template       │
                              │  & Marketplace   │     │  Marketplace    │
                              └──────────────────┘     └─────────────────┘
```

## Plugin Functions

### 1. Design Studio (Pipe)

The core generation engine. Processes design prompts through:
1. Intent detection (is this a design request?)
2. Template selection
3. Prompt construction with system instructions
4. LLM API call
5. HTML extraction and sanitization
6. Version history saving

#### Manifold Models

- `Design Studio` - General design generation
- `Design Editor (Live)` - Split-pane code editor mode
- `Design Library` - Browse saved designs and templates
- `Compare Models` - Parallel LLM comparison

#### API Endpoints

```python
# Pipe signature
def stream(messages: list, user: dict | None = None, **kwargs) -> AsyncIterator[str]
```

#### Configuration (Valves)

```python
class Valves:
    data_directory: str  # Base directory for storing designs
    default_template: str  # Default template type
    auto_preview: bool  # Auto-generate preview on design creation
    llm_api_url: str  # Open WebUI API endpoint
    ollama_base_url: str  # Ollama fallback URL
```

#### Example Usage

```python
from functions.design_studio.design_studio import Pipe

pipe = Pipe()
pipe.valves.default_template = "landing"
pipe.valves.data_directory = "/path/to/openwebui/data"

async for response in pipe.stream(messages):
    print(response)
```

### 2. Preview Generator (Action)

Handles preview rendering, export, and live editing.

#### Actions

- `Generate Preview` - Render HTML in sandboxed iframe
- `Export HTML` - Download raw HTML file
- `Open Editor` - Launch split-pane live editor
- `Compare Models` - View multi-model comparison
- `Submit Template` - Share design as community template
- `Import Template` - Import template from URL
- `View Marketplace` - Browse community templates

#### API Endpoints

```python
# Action signature
async def action(action: str, body: dict, user: dict | None = None, 
                 event_emitter=None, **kwargs) -> str
```

#### Sandbox Configuration

All previews render in iframes with:
- `sandbox="allow-scripts allow-same-origin allow-forms"`
- `srcdoc` attribute (no URL-based loading)
- No external script/style sources
- Inline CSS/JS only

### 3. Prompt Enhancer (Filter)

Enhances user prompts with design guidelines and metadata.

#### Enhancement Rules

- Adds design best practices
- Includes responsive design guidance
- Suggests color palettes
- Adds accessibility requirements

#### API Endpoints

```python
# Filter signature
def outlet(messages: list, user: dict | None = None, **kwargs) -> list
```

## Template System

### Template Structure

```
templates/
├── landing/
│   ├── hero.html
│   ├── feature-grid.html
│   └── minimal.html
├── dashboard/
│   └── analytics.html
├── component/
│   ├── button.html
│   ├── card.html
│   └── form.html
├── presentation/
│   └── sections.html
├── email/
│   ├── newsletter.html
│   └── transactional.html
├── social/
│   ├── hero-banner.html
│   └── og-card.html
└── interactive/
    ├── nav.html
    ├── carousel.html
    └── ... (25+ components)
```

### Template Variables

Templates use Jinja2-style variable substitution:

```html
<!-- template.html -->
<h1>{{ title }}</h1>
<p>{{ description }}</p>
<div class="hero" style="background: {{ color }};">
  {{ content }}
</div>
```

### Design Tokens

```css
/* assets/design-tokens.css */
:root {
  --od-color-primary: #6366f1;
  --od-color-secondary: #8b5cf6;
  --od-color-background: #ffffff;
  --od-color-foreground: #1e293b;
  --od-radius-sm: 4px;
  --od-radius-md: 8px;
  --od-radius-lg: 12px;
  --od-shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
}
```

## Data Model

### Design History

```json
// <data_dir>/opendesigner/designs/<user_id>/<design_id>/history.json
[
  {
    "id": "design-uuid",
    "version": 1,
    "prompt": "Create a landing page for a coffee shop",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "llm_model": "gpt-4o",
    "template": "landing/hero"
  }
]
```

### Template Manifest

```json
// <data_dir>/opendesigner/community_templates/<user_id>/<slug>/manifest.json
{
  "slug": "my-cool-template",
  "title": "My Cool Template",
  "description": "A beautiful template",
  "template_type": "custom",
  "version": "1.0.1",
  "author": "user@example.com",
  "content_hash": "abc123def456",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

## Template Marketplace API

### Submit Template

```python
# Via action
action(
    "Submit Template",
    {
        "message": {
            "content": "Here's my template:\n\n```html\n<!DOCTYPE html>...\n```\n\n# title: My Template\n# description: A beautiful template\n# type: custom"
        }
    },
)
```

### Import Template

```python
# Via action
action("Import Template", {"message": {"content": "Import https://example.com/template.html"}})
```

### Browse Marketplace

```python
# Via action
action("View Marketplace", {})
```

## Security Model

### HTML Sanitization

The following patterns are stripped from generated HTML:

```python
SANITIZE_PATTERNS = [
    r'form\s+action\s*=\s*["\'][^"\']*["\']',  # Form actions
    r'on\w+\s*=\s*["\'][^"\']*["\']',  # Inline event handlers
    r'href\s*=\s*["\']javascript:[^"\']*["\']',  # JavaScript links
    r"eval\s*\(",  # eval() calls
]
```

### Template Validation

Community templates are scanned for:
- Dangerous Python patterns: `import`, `exec`, `eval`, `os.system`
- External script sources
- External style sources
- External form actions
- External iframe sources

### iframe Sandboxing

All previews use strict iframe sandboxing:
- `allow-scripts` - JavaScript execution
- `allow-same-origin` - CSS/JS access to parent
- `allow-forms` - Form submission
- No `allow-popups`, `allow-modals`, or `allow-top-navigation`

## Deployment

### Manual Installation

```bash
./setup.sh /path/to/openwebui/data
```

### Existing OpenWebUI Instance

```bash
./install-opendesigner.sh https://ai.s8i.app
```

### Docker

```bash
cd docker
docker-compose up -d
```

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `No data directory found` | OpenWebUI data dir not detected | Set `data_directory` in valves |
| `Template not found` | Invalid template path | Check template name |
| `LLM API timeout` | Model generation took too long | Increase timeout or use faster model |
| `HTML sanitization failed` | Invalid HTML structure | Check template syntax |

### Debug Mode

```python
pipe.valves.debug = True
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

MIT License - See [LICENSE](../LICENSE) for details.
