# 🎨 OpenDesigner Studio

> Generate beautiful, functional websites from natural language. Open-source design generation platform for [Open WebUI](https://github.com/open-webui/open-webui).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Open WebUI](https://img.shields.io/badge/OpenWebUI-0.10.0+-green.svg)](https://github.com/open-webui/open-webui)
[![Tests](https://github.com/asorichetti/OpenDesigner/actions/workflows/tests.yml/badge.svg)](https://github.com/asorichetti/OpenDesigner/actions)

---

## ✨ What is OpenDesigner?

OpenDesigner is an open-source design generation platform that lives inside [Open WebUI](https://github.com/open-webui/open-webui). It transforms conversational prompts into working HTML prototypes — landing pages, dashboards, components, presentations, emails, and social media assets.

### Key Features

- 🎨 **30+ Templates** — Landing pages, dashboards, components, presentations, emails, social media, interactive components
- 🔒 **Sandboxed Previews** — iframe rendering with strict security
- ✏️ **Live Editor** — Split-pane code editor with real-time preview
- 🎤 **Presenter Mode** — Keyboard navigation, fullscreen, PDF export
- 📋 **Version History** — Save, browse, and rollback design iterations
- 🏪 **Template Marketplace** — Submit, import, and browse community templates
- 🤖 **LLM Agnostic** — Works with Ollama, OpenAI, or any Open WebUI-compatible model
- 🐳 **Docker Ready** — One-command deployment
- 🧪 **Tested** — 37 unit tests + 12 integration tests

---

## 🚀 Quick Start

### Method 1: Docker Compose (Easiest)

```bash
git clone https://github.com/asorichetti/OpenDesigner.git
cd OpenDesigner/docker
docker compose up -d
```

Open [http://localhost:3000](http://localhost:3000) and start chatting.

### Method 2: Manual Install

```bash
git clone https://github.com/asorichetti/OpenDesigner.git
cd OpenDesigner
chmod +x setup.sh
./setup.sh
```

See [INSTALL.md](docs/INSTALL.md) for detailed instructions.

### Method 3: Community Plugin

Coming soon — one-click install from Open WebUI's community plugin repository.

---

## 📸 What Does It Look Like?

### Try the Interactive Demo

```bash
open demo/index.html
```

This shows all 14 templates rendered live with:
- Click any template to preview it
- Live code editor with real-time updates
- Responsive view toggles (desktop/tablet/mobile)
- Version history browser

### Run the Test Suite

```bash
# Unit tests
python -m pytest tests/ -v

# CLI integration tests
python opendesign_cli.py
```

**37 unit tests pass. 12 CLI tests pass.**

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [API Reference](docs/API.md) | Complete API documentation |
| [Installation Guide](docs/INSTALL.md) | Step-by-step installation |
| [Contributing Guide](docs/CONTRIBUTING.md) | How to contribute |
| [Security Policy](docs/SECURITY.md) | Security features and reporting |
| [FAQ & Troubleshooting](docs/FAQ.md) | Common issues and solutions |

---

## 📚 Usage

### Generating Designs

In OpenWebUI, use the **Design Studio** pipe with prompts like:

```
Create a landing page for a coffee shop
```

```
Build me a dashboard with analytics
```

```
Design a button component with primary and secondary variants
```

### Available Modes

OpenDesigner exposes 4 models through the OpenWebUI manifold:

1. **Design Studio** — Generate new designs from prompts
2. **Compare Models** — Parallel LLM generation, side-by-side comparison
3. **Design Library** — Browse saved designs and templates
4. **Design Editor (Live)** — Split-pane code editor mode

### Actions

After generating a design, use these actions:

- **Generate Preview** — Render the design in a sandboxed iframe
- **Export HTML** — Download the raw HTML file
- **Open Editor** — Launch the split-pane live editor
- **Compare Models** — View multi-model comparison side-by-side
- **Submit Template** — Share your design as a community template
- **Import Template** — Import a template from a URL
- **View Marketplace** — Browse community templates

---

## 🏗️ Architecture

```
OpenWebUI
├── Pipe: Design Studio
│   ├── Intent detection (keyword-based)
│   ├── Template loading (14 templates)
│   ├── Prompt construction (Jinja2-style)
│   ├── LLM integration (OpenWebUI API + Ollama fallback)
│   ├── HTML extraction & sanitization
│   └── Version persistence (atomic writes)
│
├── Action: Preview Generator
│   ├── Code block extraction
│   ├── Sanitized preview iframe (sandboxed)
│   ├── Live editor (split-pane, auto-refresh)
│   └── HTML export
│
└── Filter: Prompt Enhancer
    ├── Design intent detection
    ├── Prompt enhancement with guidelines
    └── Metadata injection
```

### Security

All previews render in sandboxed iframes:
- `allow-scripts allow-same-origin allow-forms`
- No external URLs or resources
- No `eval()` or `javascript:` URLs
- Inline CSS/JS only
- Dangerous HTML patterns stripped

---

## 📦 Installation

See [INSTALL.md](docs/INSTALL.md) for complete installation instructions.

### Requirements

- Open WebUI 0.10.0+
- Python 3.11+
- Docker & Docker Compose (for containerized deployment)

### Dependencies

- `jinja2` — Template engine
- `beautifulsoup4` — HTML parsing
- `aiohttp` — Async HTTP client
- `pydantic` — Configuration validation

---

## 🧪 Testing

### Unit Tests

```bash
python -m pytest tests/ -v
```

### CLI Integration Tests

```bash
python opendesign_cli.py
```

### Test Coverage

| Test Suite | Tests | Status |
|------------|-------|--------|
| Intent Detection | 5 | ✅ Pass |
| Template Loading | 4 | ✅ Pass |
| Prompt Construction | 4 | ✅ Pass |
| HTML Extraction | 3 | ✅ Pass |
| Version Persistence | 5 | ✅ Pass |
| Preview Generator | 7 | ✅ Pass |
| Prompt Enhancer | 3 | ✅ Pass |
| Model Comparison | 5 | ✅ Pass |
| Template Validation | 10 | ✅ Pass |
| **Total** | **52** | **✅ All Pass** |

---

## 🎨 Templates

OpenDesigner includes 14 templates across 6 categories:

### Landing Pages
- `landing/minimal` — Clean, distraction-free
- `landing/hero` — Hero-section centered, CTA-driven
- `landing/feature-grid` — Feature showcase with grid layout

### Dashboards
- `dashboard/analytics` — Sidebar navigation, stat cards, chart area

### Components
- `component/button` — Primary, secondary, ghost variants
- `component/card` — Image card with title and description
- `component/modal` — Dialog with header, body, footer
- `component/form` — Input, textarea, submit button

### Presentations
- `presentation/blank` — Blank canvas
- `presentation/sections` — Multi-slide with keyboard nav, presenter mode

### Emails
- `email/newsletter` — Marketing email with CTA button
- `email/transactional` — Receipts, confirmations, order updates

### Social Media
- `social/hero-banner` — 1200×630px OG-optimized banner
- `social/og-card` — Social preview card with image and text

---

## 📁 Project Structure

```
OpenDesigner/
├── functions/
│   ├── design_studio/          # Pipe: Design generation
│   │   ├── design_studio.py    # Main pipe logic
│   │   ├── template_marketplace.py  # Template validation & marketplace
│   │   ├── templates/          # HTML templates
│   │   ├── prompts/            # LLM prompt templates
│   │   └── assets/             # CSS design tokens
│   ├── preview_generator/      # Action: Preview & export
│   │   └── preview_generator.py
│   └── prompt_enhancer/        # Filter: Prompt enhancement
│       └── prompt_enhancer.py
├── tests/                      # Unit tests
├── demo/                       # Interactive demo
│   └── index.html
├── docker/                     # Docker deployment
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── docker-compose.dev.yml
├── docs/                       # Documentation
│   ├── INSTALL.md              # Installation guide
│   ├── API.md                  # API reference
│   ├── CONTRIBUTING.md         # Contributing guidelines
│   ├── SECURITY.md             # Security policy
│   └── FAQ.md                  # Troubleshooting & FAQ
├── plugins/                    # Community plugin manifest
├── opendesign_cli.py           # CLI test runner
├── setup.sh                    # Installation script
├── pyproject.toml              # Project configuration
└── README.md                   # This file
```

---

## 🔧 Configuration

### Admin Valves

| Setting | Default | Description |
|---------|---------|-------------|
| `preview_timeout` | `30` | Preview render timeout (seconds) |
| `default_model` | `gpt-4o` | Default LLM model |

### User Valves

| Setting | Default | Description |
|---------|---------|-------------|
| `template` | `landing/minimal` | Default template |
| `design_system` | `light` | Design system preset |
| `auto_preview` | `true` | Auto-generate previews |

See [INSTALL.md](docs/INSTALL.md) for environment variables and full configuration guide.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📜 License

MIT License — See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- [Open WebUI](https://github.com/open-webui/open-webui) — The foundation
- [Ollama](https://github.com/ollama/ollama) — Local LLM support
- All template designers and contributors

---

## 🔗 Links

- [Repository](https://github.com/asorichetti/OpenDesigner)
- [API Reference](docs/API.md)
- [Installation Guide](docs/INSTALL.md)
- [Contributing Guide](docs/CONTRIBUTING.md)
- [Security Policy](docs/SECURITY.md)
- [FAQ & Troubleshooting](docs/FAQ.md)
- [Issue Tracker](https://github.com/asorichetti/OpenDesigner/issues)
- [Discussions](https://github.com/asorichetti/OpenDesigner/discussions)
