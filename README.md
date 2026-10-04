# OpenDesign

An open-source, self-hostable design generation platform built as an **Open WebUI extension**. It takes conversational prompts and produces visual outputs — HTML prototypes, UI components, slide decks, email templates, and more — all rendered as interactive previews directly in chat.

## What This Is

Describe what you want to build: "Create a landing page for a coffee shop" or "Make a dashboard for analytics." OpenDesign generates complete, self-contained HTML/CSS/JS code and renders an interactive preview directly in your Open WebUI chat.

## Features

- 🎨 **Design Generation** — Conversational UI to generate landing pages, dashboards, UI components, emails, social assets, and presentations
- 👁️ **Live Preview** — Sandbox-secured iframe previews directly in chat
- 📋 **Version History** — Save iterations, compare versions, roll back
- 🖼️ **Template Library** — Pre-built templates for landing pages, dashboards, components, presentations, emails, social assets
- 🎭 **Design System Presets** — Light/dark themes, accessibility compliance, color tokens
- 📤 **Export** — Download as ZIP, copy clipboard, or share via link
- ✏️ **Live Editor** (Phase 5) — Split-pane code editor with real-time preview
- 🔀 **Multi-Model** (Phase 5) — Compare outputs from different LLMs side by side
- 🌍 **Community Templates** (Phase 5) — Share and discover templates from others
- 🔌 **Open WebUI Plugin** — Works with any LLM backend (Ollama, OpenAI, etc.)

## Installation

### Option 1: Open WebUI Community Plugin (Recommended)

1. Go to **Admin Panel → Functions → Import From Link**
2. Import each function from the `functions/` directory:
   - `https://raw.githubusercontent.com/asorichetti/OpenDesign/main/functions/design_studio/design_studio.py`
   - `https://raw.githubusercontent.com/asorichetti/OpenDesign/main/functions/preview_generator/preview_generator.py`
   - `https://raw.githubusercontent.com/asorichetti/OpenDesign/main/functions/prompt_enhancer/prompt_enhancer.py`
3. Save each function.
4. Select **Design Studio** from the model dropdown to start generating.

### Option 2: Docker Compose (Production)

Run OpenDesign in an isolated Docker container with any LLM backend:

```bash
git clone https://github.com/asorichetti/OpenDesign.git
cd OpenDesign/docker
docker compose up -d
```

This bundles Open WebUI with all three OpenDesign functions pre-installed.

### Option 3: Manual Import (Advanced)

For users who want to modify the plugin or run it in a custom Python environment:

```bash
git clone https://github.com/asorichetti/OpenDesign.git
cd OpenDesign
# Copy functions into your Open WebUI functions directory
cp -r functions/* /path/to/open-webui/functions/
```

### Option 2: Docker

```bash
git clone https://github.com/asorichetti/OpenDesign.git
cd OpenDesign/docker
docker compose up -d
```

## Configuration

### Valves (Admin Settings)

| Setting | Default | Description |
|---------|---------|-------------|
| `base_model` | `gpt-4o` | LLM to use for generation |
| `api_key` | *(empty)* | API key (if not using Ollama) |
| `preview_timeout` | `10` | Preview render timeout in seconds |

### UserValves (Per-User Settings)

| Setting | Default | Description |
|---------|---------|-------------|
| `template` | `landing/minimal` | Default template to use |
| `design_system` | `light` | Design system preset (light/dark) |
| `auto_preview` | `true` | Auto-generate preview on send |

## Models Available

| Model | Purpose |
|-------|---------|  
| Design Studio | General design generation (landing pages, dashboards, components, emails, social) |
| Design Editor | Live editing mode — split-pane code editor with real-time preview |
| Design Library | Browse and load saved designs |

## Project Structure

```
OpenDesign/
├── functions/
│   ├── design_studio/          # Pipe Function — HTML generation
│   ├── preview_generator/      # Action Function — sandboxed preview & export
│   └── prompt_enhancer/        # Filter Function — prompt enhancement
├── docker/                     # Docker Compose deployment
├── docs/plan/                  # Planning documents & task cards
├── tests/                      # Unit tests
├── pyproject.toml              # Python project config
└── Makefile                    # lint, test, build targets
```

## Development

```bash
make lint      # Run ruff linter
make test      # Run pytest
```

## License

MIT
