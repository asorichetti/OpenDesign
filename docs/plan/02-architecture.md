# Architecture

## What This Is

OpenDesign is a **collection of Open WebUI plugin functions** that, when installed on any Open WebUI instance, enable AI-powered design generation:

1. **Pipe Function** — Registers as a "Design Studio" model. When a user chats with it, the pipe orchestrates design generation using an underlying LLM.
2. **Action Function** — Adds "Generate Preview", "Export", and "Open Editor" buttons to chat messages.
3. **Filter Function** — Intercepts design prompts to enhance them with design system context.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Open WebUI                             │
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌───────────────┐ │
│  │  User Chat    │    │  Chat Sidebar│    │  Admin Panel  │ │
│  │  Interface    │    │  (Models)    │    │  (Functions)  │ │
│  └──────┬───────┘    └──────┬───────┘    └───────┬───────┘ │
│         │                   │                      │        │
│         ▼                   ▼                      ▼        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Function Loader                         │   │
│  │  (dynamic Python module exec + caching)             │   │
│  └──────────────┬──────────────────┬───────────────┘   │
│                 │                  │                     │
│          ┌──────▼──────┐   ┌──────▼──────┐   ┌────────▼──────┐
│          │   Pipe      │   │  Action     │   │   Filter      │
│          │  "Design    │   │  "Preview + │   │  "Enhance   │
│          │   Studio"   │   │  Export"    │   │  Prompts"   │
│          └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
│                 │                 │                 │
│          ┌──────▼─────────────────▼─────────────────▼──────┐
│          │              Design Engine                       │
│          │  - LLM call orchestration                        │
│          │  - HTML/CSS/JS generation                        │
│          │  - Preview validation                             │
│          │  - Template management                           │
│          │  - Live editor proxy (Phase 5)                   │
│          └───────────────────┬─────────────────────────────┘
│                              │
│                      ┌───────▼───────┐
│                      │  LLM Backend  │
│                      │  (any)        │
│                      └───────────────┘
└─────────────────────────────────────────────────────────────┘
```

## Plugin Structure

```
OpenDesign/
├── README.md
├── pyproject.toml
├── LICENSE
├── docs/
│   └── plan/
├── functions/
│   ├── design_studio/
│   │   ├── design_studio.py          # Pipe Function
│   │   ├── frontmatter.md           # Function metadata
│   │   ├── prompts/
│   │   │   ├── system.md            # System prompt template
│   │   │   ├── generate_html.md     # HTML generation prompt
│   │   │   ├── iterate.md           # Iteration prompt
│   │   │   ├── present.md           # Presentation prompt
│   │   │   ├── email.md             # Email template prompt
│   │   │   └── social.md            # Social asset prompt
│   │   ├── templates/
│   │   │   ├── landing/             # Landing page templates
│   │   │   ├── dashboard/           # Dashboard templates
│   │   │   ├── component/           # UI component templates
│   │   │   ├── presentation/        # Slide deck templates
│   │   │   ├── email/               # Email template layouts
│   │   │   └── social/              # Social media templates
│   │   ├── live/                    # Live editor assets
│   │   │   ├── editor.html          # Split-pane editor UI
│   │   │   └── websocket.js         # Live sync protocol
│   │   └── assets/                  # Design system presets
│   │       ├── light.css
│   │       ├── dark.css
│   │       └── accessible.css
│   ├── preview_generator/
│   │   ├── preview_generator.py     # Action Function
│   │   └── frontmatter.md
│   └── prompt_enhancer/
│       ├── prompt_enhancer.py       # Filter Function
│       └── frontmatter.md
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
└── scripts/
    ├── build.sh
    └── test.sh
```

## How the Pipe Works

1. User selects "Design Studio" from the model dropdown
2. User describes a design: "Create a landing page for a coffee shop"
3. The Pipe receives the chat body dict (Open WebUI format)
4. Pipe calls the underlying LLM with an enhanced design prompt
5. LLM returns HTML/CSS/JS code (possibly multiple blocks)
6. Pipe formats the response with a preview code block
7. Open WebUI displays the response with the preview button (Action)

## How the Action Works

1. User sees a message with design code
2. Buttons appear on the message toolbar: "Generate Preview", "Export", "Open Editor"
3. On click, Action extracts the HTML/CSS/JS from the message
4. Action returns a rich HTML preview rendered in an iframe
5. "Open Editor" opens the split-pane live editor (Phase 5)

## How the Filter Works

1. Filter runs as middleware on all model calls
2. When it detects a design-related prompt (keyword matching), it:
   - Injects design system context (color tokens, typography scale)
   - Adds accessibility requirements to the prompt
   - Appends template suggestions based on user history

## Deployment Options

### Option A: Open WebUI Function Install (primary)

```bash
# In Open WebUI Admin Panel > Functions > Import From Link
# Point to: https://raw.githubusercontent.com/asorichetti/OpenDesign/main/functions/design_studio/design_studio.py
# Repeat for preview_generator and prompt_enhancer
```

### Option B: Docker (bundled)

```bash
docker compose up -d
# Open WebUI starts with OpenDesign functions pre-installed
```
