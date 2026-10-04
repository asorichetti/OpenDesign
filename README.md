# OpenDesign

An open-source, self-hostable recreation of **Claude Design** — the capability to take conversational prompts and generate visual assets, interactive prototypes, and presentations. Built as an **Open WebUI extension**.

## What This Is

Describe what you want to build: "Create a landing page for a coffee shop" or "Make a dashboard for analytics." OpenDesign generates complete, self-contained HTML/CSS/JS code and renders an interactive preview directly in your Open WebUI chat.

## Features

- 🎨 **Design Generation** — Conversational UI to generate landing pages, dashboards, presentations, and UI components
- 👁️ **Live Preview** — Sandbox-secured iframe previews directly in chat
- 📋 **Version History** — Save iterations, compare versions, roll back
- 🖼️ **Template Library** — Pre-built templates for landing pages, dashboards, presentations
- 🎭 **Design System Presets** — Light/dark themes, accessibility compliance
- 📤 **Export** — Download as ZIP or copy to clipboard
- 🔌 **Open WebUI Plugin** — Works with any LLM backend (Ollama, OpenAI, etc.)

## Installation

### Option 1: Open WebUI Functions (Recommended)

Import each function from this repository:

1. Go to **Admin Panel → Functions → Import From Link**
2. Import: `https://raw.githubusercontent.com/asorichetti/OpenDesign/main/functions/design_agent/design_agent.py`
3. Import: `https://raw.githubusercontent.com/asorichetti/OpenDesign/main/functions/preview_generator/preview_generator.py`
4. Import: `https://raw.githubusercontent.com/asorichetti/OpenDesign/main/functions/prompt_enhancer/prompt_enhancer.py`
5. Save each function. Select "OpenDesign Design Agent" from the model dropdown.

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
| OpenDesign Design Agent | General design generation (landing pages, dashboards) |
| OpenDesign Presentations | Slide deck generation with presenter notes |
| OpenDesign Components | UI component generation (buttons, cards, forms) |
| OpenDesign Library | Browse and load saved designs |

## Project Structure

```
OpenDesign/
├── functions/
│   ├── design_agent/           # Pipe Function (main generation)
│   ├── preview_generator/      # Action Function (preview rendering)
│   └── prompt_enhancer/        # Filter Function (prompt enhancement)
├── docker/                     # Docker deployment
├── docs/plan/                  # Planning documents
└── tests/                      # Unit tests
```

## Development

```bash
make lint      # Run ruff linter
make test      # Run pytest
```

## License

MIT
