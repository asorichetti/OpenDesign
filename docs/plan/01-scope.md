# Scope

## What Claude Design Does

Claude Design is the capability to describe a visual interface conversationally and receive:

1. **Static HTML/CSS/JS pages** — Complete, self-contained web pages
2. **Interactive prototypes** — Clickable, navigable multi-page prototypes
3. **Presentation slides** — Slide decks with transitions and layouts
4. **UI component libraries** — Reusable, themed component sets
5. **Iterative refinement** — Conversational editing: "make the header darker"

## What This Project Rebuilds

This project recreates the **generation + preview** pipeline as an Open WebUI extension:

### ✅ In Scope

- **Design generation via chat** — Describe what you want, get HTML/CSS/JS back
- **Preview rendering** — Sandbox iframe preview directly in Open WebUI chat
- **Version history** — Save iterations, compare versions, roll back
- **Template library** — Pre-built templates for landing pages, dashboards, presentations
- **Design system presets** — Color tokens, typography, spacing presets (light/dark)
- **Iterative refinement** — Conversational editing of generated designs
- **Export** — Download as ZIP (HTML/CSS/JS), copy to clipboard
- **LLM-agnostic** — Works with any model Open WebUI supports (Ollama, OpenAI, etc.)

### ❌ Out of Scope (v1)

- Drag-and-drop design tool (that's a different product)
- Native mobile app generation
- Real design software (Figma/Sketch file export)
- Asset generation (images, icons) — handled by Open WebUI's image gen tools
- Collaborative editing (multi-user)
- Version control (Git integration)
- Custom CSS framework compilation (Tailwind build step)

## Feature Parity Map

| Claude Design Feature | OpenDesign Equivalent |
|----------------------|----------------------|
| "Make me a landing page for..." | Pipe generates HTML from prompt |
| Preview in browser | Action renders iframe preview |
| "Change the font to Inter" | Iterative refinement via chat |
| "Show me a dark mode version" | Template variant generation |
| Export as code | Download ZIP with HTML/CSS/JS |
| Presentation mode | Slide deck generation + presenter view |
| Component library | Template system with presets |
| Design system tokens | CSS custom property presets |
