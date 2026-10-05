# Scope

## What OpenDesigner Does

OpenDesigner turns natural language into deployable visual output. Describe what you want to build and receive:

1. **HTML prototypes** — Complete, self-contained web pages (landing pages, dashboards, forms, navigation)
2. **UI components** — Buttons, cards, modals, tables, data grids, navbars
3. **Slide decks** — Professional presentations with presenter notes, keyboard navigation, print-to-PDF
4. **Email templates** — Responsive HTML email layouts
5. **Social media assets** — Hero banners, card previews, OG images
6. **Iterative refinement** — Conversational editing: "make the header darker", "add a pricing section"

## What OpenDesigner Is

- An **Open WebUI plugin** (Pipe + Action + Filter functions in Python)
- **Model-agnostic** — works with any LLM backend Open WebUI supports (Ollama, OpenAI, Anthropic, etc.)
- **Self-hostable** — runs entirely on your infrastructure
- **Extensible** — add templates, design systems, and output types without touching core code

## What OpenDesigner Is Not

- A drag-and-drop visual editor (that's a different product category)
- A replacement for design tools (Figma, Sketch, Framer)
- An image generation tool (Open WebUI already has this via DALL-E, ComfyUI)
- A full-stack framework (outputs are HTML/CSS/JS only, no API/backend)

## Output Type Matrix

| Output Type | Phase | Description |
|-------------|-------|-------------|
| Landing pages | Phase 1 | Hero, features, CTA, footer layouts |
| Dashboards | Phase 1 | Stat cards, data tables, chart placeholders |
| UI components | Phase 1 | Buttons, cards, forms, navbars, modals |
| Slide decks | Phase 4 | Multi-slide presentations with notes |
| Email templates | Phase 4 | Responsive HTML email layouts |
| Social assets | Phase 4 | Hero banners, OG image previews |
| Component libraries | Phase 5 | Full design system with variants |
| Live editor | Phase 5 | Split-pane: code + real-time preview |

## Feature Goals

- **Zero-config setup** — install 3 Python files, start generating
- **Template library** — pre-built templates users can extend
- **Design system presets** — light/dark themes, color tokens, typography scales
- **Version history** — save iterations, diff between versions, roll back
- **Export options** — download ZIP, copy clipboard, share via link
- **Live preview** — sandboxed iframe with responsive views
- **Live editor** (Phase 5) — split-pane code editor with real-time preview sync
- **Multi-model** (Phase 5) — compare outputs from different LLMs side by side
- **Community templates** (Phase 5) — share and discover templates from others
