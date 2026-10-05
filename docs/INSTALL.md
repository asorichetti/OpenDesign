# OpenDesigner Studio — Installation Guide

Open-source design generation platform for [Open WebUI](https://github.com/open-webui/open-webui).

Generate beautiful, functional websites from natural language. Works as a plugin within Open WebUI.

## Quick Start

### Method 1: Manual Install (Recommended for Development)

```bash
# Clone the repository
git clone https://github.com/asorichetti/OpenDesigner.git
cd OpenDesigner

# Run the installer
chmod +x setup.sh
./setup.sh

# Restart OpenWebUI
docker compose restart
```

### Method 2: Docker Compose (Recommended for Production)

```bash
# Clone the repository
git clone https://github.com/asorichetti/OpenDesigner.git
cd OpenDesigner/docker

# Start everything
docker compose up -d

# Open in browser
open http://localhost:3000
```

### Method 3: Community Plugin

Coming soon — one-click install from Open WebUI community plugin repository.

---

## Installation Details

### Manual Install Step-by-Step

1. **Find your OpenWebUI data directory**

   Common locations:
   ```bash
   # Docker install
   echo $OPENWEBUI_DATA_DIR
   # or
   ls -d /var/lib/docker/volumes/*/_data 2>/dev/null | head -1

   # Local install
   ls -d ~/.open-webui 2>/dev/null
   ```

2. **Create the functions directory**

   ```bash
   mkdir -p $OPENWEBUI_DATA_DIR/functions/opendesigner
   ```

3. **Copy the function files**

   ```bash
   cp functions/design_studio/design_studio.py $OPENWEBUI_DATA_DIR/functions/opendesigner/
   cp functions/preview_generator/preview_generator.py $OPENWEBUI_DATA_DIR/functions/opendesigner/
   cp functions/prompt_enhancer/prompt_enhancer.py $OPENWEBUI_DATA_DIR/functions/opendesigner/
   ```

4. **Copy templates and assets**

   ```bash
   mkdir -p $OPENWEBUI_DATA_DIR/opendesigner/{templates/{landing,dashboard,component,presentation,email,social},assets,prompts}
   cp -r functions/design_studio/templates/* $OPENWEBUI_DATA_DIR/opendesigner/templates/
   cp functions/design_studio/assets/* $OPENWEBUI_DATA_DIR/opendesigner/assets/
   cp functions/design_studio/prompts/* $OPENWEBUI_DATA_DIR/opendesigner/prompts/
   ```

5. **Install dependencies**

   OpenWebUI loads the functions with its own Python environment. Make sure the following packages are available:
   ```bash
   pip install jinja2 beautifulsoup4 aiohttp pydantic
   ```

6. **Restart OpenWebUI**

   ```bash
   docker compose restart
   # or
   systemctl restart open-webui
   ```

### Docker Compose Install

The `docker/` directory contains a complete OpenWebUI setup with OpenDesigner pre-installed:

```yaml
# docker/docker-compose.yml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    volumes:
      - open-webui-data:/app/backend/data
      - ./functions:/app/backend/data/functions/opendesigner:ro
      - ./templates:/app/backend/data/opendesigner/templates:ro
      - ./assets:/app/backend/data/opendesigner/assets:ro
      - ./prompts:/app/backend/data/opendesigner/prompts:ro
    ports:
      - "3000:8080"
    environment:
      - OPENWEBUI_DATA=/app/backend/data
    restart: always
```

---

## Verifying Installation

### Check Functions Are Loaded

1. Open OpenWebUI (`http://localhost:3000`)
2. Go to **Settings → Extensions → Functions**
3. Verify these three functions appear:

   - ✅ **Design Studio** (Pipe) — Generates HTML from prompts
   - ✅ **Preview Generator** (Action) — Renders sandboxed previews
   - ✅ **Prompt Enhancer** (Filter) — Enhances design prompts

### Test the Installation

In the chat, try these prompts:

```
Create a landing page for a coffee shop
```

You should see:
1. The prompt is enhanced with design guidelines
2. The LLM generates HTML wrapped in markdown
3. The output is sanitized and attributed
4. A preview renders in a sandboxed iframe

### CLI Test (Without OpenWebUI)

```bash
# Run the standalone test runner
python opendesign_cli.py

# Run unit tests
python -m pytest tests/ -v

# Open the interactive demo
open demo/index.html
```

---

## Configuration

### Admin Valves (Settings)

Access via OpenWebUI Admin Panel → Extensions → Functions → Design Studio → Settings:

| Setting | Default | Description |
|---------|---------|-------------|
| `preview_timeout` | `30` | Preview render timeout in seconds |
| `default_model` | `gpt-4o` | Default LLM model for generation |

### User Valves (Per-User Settings)

Accessible from the Design Studio pipe settings:

| Setting | Default | Description |
|---------|---------|-------------|
| `template` | `landing/minimal` | Default template to use |
| `design_system` | `light` | Design system preset (light/dark) |
| `auto_preview` | `true` | Automatically generate preview |

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENWEBUI_DATA_DIR` | `~/.open-webui` | OpenWebUI data directory path |
| `OPENDESIGN_CACHE_TTL` | `3600` | Template cache TTL in seconds |
| `OPENDESIGN_LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |

---

## Troubleshooting

### Functions Not Showing Up

1. Check file permissions:
   ```bash
   ls -la $OPENWEBUI_DATA_DIR/functions/opendesigner/
   ```

2. Verify Python dependencies:
   ```bash
   python -c "import jinja2, bs4, aiohttp, pydantic; print('All dependencies OK')"
   ```

3. Check OpenWebUI logs:
   ```bash
   docker compose logs -f open-webui | grep -i "function"
   ```

### Templates Not Loading

1. Verify template files exist:
   ```bash
   ls $OPENWEBUI_DATA_DIR/opendesigner/templates/landing/
   ```

2. Check the CLI test:
   ```bash
   python opendesign_cli.py templates
   ```

### Preview Not Rendering

1. Check browser console for errors
2. Verify iframe sandbox attributes are correct
3. Test with `demo/index.html` to isolate the issue

### LLM Integration Issues

The Design Studio pipe calls OpenWebUI's internal API. Make sure:

1. OpenWebUI is running and accessible
2. The model specified in valves is available
3. Check OpenWebUI logs for API errors

---

## Uninstall

To remove OpenDesigner:

```bash
# Remove function files
rm -rf $OPENWEBUI_DATA_DIR/functions/opendesigner/
rm -rf $OPENWEBUI_DATA_DIR/opendesigner/

# Restart OpenWebUI
docker compose restart
```

---

## Development

### Running Tests

```bash
# Unit tests
python -m pytest tests/ -v

# CLI test runner
python opendesign_cli.py

# Test specific module
python opendesign_cli.py intent
```

### Running Locally

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Open interactive demo
open demo/index.html
```

---

## License

MIT License — See [LICENSE](../LICENSE) for details.

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.
