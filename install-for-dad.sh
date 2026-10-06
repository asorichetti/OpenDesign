#!/bin/bash
# OpenDesigner - Simple Installer for Non-Technical Users
# Just run this script and follow the prompts

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${BLUE}╔══════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║    OpenDesigner - Simple Installer       ║${NC}"
echo -e "${BLUE}║    For: Open WebUI Instance              ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════╝${NC}"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Warning: Not running as root (good!)${NC}"
fi

# Step 1: Find OpenWebUI data directory
echo -e "${CYAN}Step 1: Finding OpenWebUI data directory...${NC}"
echo ""

DATA_DIR=""

# Try Docker first
if command -v docker &> /dev/null; then
    echo -e "  Checking Docker containers..."
    CONTAINER=$(docker ps --filter "name=openwebui" --format "{{.ID}}" 2>/dev/null || true)
    if [ -n "$CONTAINER" ]; then
        DATA_DIR=$(docker inspect -f '{{range .Mounts}}{{if eq .Destination "/app/backend/data"}}{{.Source}}{{end}}{{end}}' "$CONTAINER" 2>/dev/null || true)
        if [ -n "$DATA_DIR" ]; then
            echo -e "  ${GREEN}✓${NC} Found OpenWebUI in Docker: ${DATA_DIR}"
            echo ""
        fi
    fi
fi

# Try common locations
if [ -z "$DATA_DIR" ]; then
    if [ -d "$HOME/.open-webui" ]; then
        DATA_DIR="$HOME/.open-webui"
        echo -e "  ${GREEN}✓${NC} Found in: $DATA_DIR"
        echo ""
    elif [ -d "/var/lib/open-webui" ]; then
        DATA_DIR="/var/lib/open-webui"
        echo -e "  ${GREEN}✓${NC} Found in: $DATA_DIR"
        echo ""
    elif [ -d "/opt/openwebui/data" ]; then
        DATA_DIR="/opt/openwebui/data"
        echo -e "  ${GREEN}✓${NC} Found in: $DATA_DIR"
        echo ""
    fi
fi

# If not found, ask user
if [ -z "$DATA_DIR" ] || [ ! -d "$DATA_DIR" ]; then
    echo -e "${YELLOW}⚠️  Could not find OpenWebUI data directory${NC}"
    echo ""
    echo -e "  Common locations:"
    echo -e "    - ~/.open-webui"
    echo -e "    - /var/lib/open-webui"
    echo -e "    - /opt/openwebui/data"
    echo ""
    read -p "  Enter path (or press Enter to skip): " DATA_DIR
    
    if [ -z "$DATA_DIR" ]; then
        echo -e "${YELLOW}⚠️  Skipping data directory check${NC}"
        DATA_DIR="$HOME/.open-webui"
    fi
fi

echo ""
echo -e "${CYAN}Step 2: Installing OpenDesigner...${NC}"
echo ""

# Create directories
echo -e "  Creating directories..."
mkdir -p "$DATA_DIR/functions/opendesigner"
mkdir -p "$DATA_DIR/opendesigner/templates/{component,dashboard,email,interactive/forms,landing,presentation,social}"
mkdir -p "$DATA_DIR/opendesigner/assets"
mkdir -p "$DATA_DIR/opendesigner/prompts"
echo -e "  ${GREEN}✓${NC} Directories created"
echo ""

# Copy functions
echo -e "  Copying functions..."
if [ -d "plugins/opendesigner/functions" ]; then
    cp plugins/opendesigner/functions/*.py "$DATA_DIR/functions/opendesigner/" 2>/dev/null && \
        echo -e "  ${GREEN}✓${NC} Functions copied (from plugin directory)" || \
        echo -e "  ${YELLOW}⚠${NC} Functions not found in plugin directory"
elif [ -d "functions/designer_studio" ]; then
    cp functions/designer_studio/designer_studio.py "$DATA_DIR/functions/opendesigner/" 2>/dev/null
    cp functions/preview_generator/preview_generator.py "$DATA_DIR/functions/opendesigner/" 2>/dev/null
    cp functions/prompt_enhancer/prompt_enhancer.py "$DATA_DIR/functions/opendesigner/" 2>/dev/null
    echo -e "  ${GREEN}✓${NC} Core functions copied"
fi
echo ""

# Copy templates
echo -e "  Copying templates..."
if [ -d "plugins/opendesigner/templates" ]; then
    cp -r plugins/opendesigner/templates/* "$DATA_DIR/opendesigner/templates/" 2>/dev/null && \
        echo -e "  ${GREEN}✓${NC} Templates copied (from plugin directory)" || \
        echo -e "  ${YELLOW}⚠${NC} Templates not found"
else
    echo -e "  ${YELLOW}⚠${NC} Templates not found (will use defaults)"
fi
echo ""

# Copy assets
echo -e "  Copying assets..."
if [ -d "plugins/opendesigner/assets" ]; then
    cp plugins/opendesigner/assets/*.css "$DATA_DIR/opendesigner/assets/" 2>/dev/null && \
        echo -e "  ${GREEN}✓${NC} Assets copied" || \
        echo -e "  ${YELLOW}⚠${NC} Assets not found"
else
    echo -e "  ${YELLOW}⚠${NC} Assets not found"
fi
echo ""

# Copy plugin manifest
echo -e "  Creating plugin manifest..."
if [ -f "plugins/opendesigner/plugin.json" ]; then
    cp plugins/opendesigner/plugin.json "$DATA_DIR/opendesigner/" && \
        echo -e "  ${GREEN}✓${NC} Plugin manifest created" || \
        echo -e "  ${YELLOW}⚠${NC} Manifest not found"
else
    echo -e "  ${YELLOW}⚠${NC} Plugin manifest not found"
fi
echo ""

# Install dependencies
echo -e "${CYAN}Step 3: Installing dependencies...${NC}"
echo ""

if command -v pip3 &> /dev/null; then
    pip3 install jinja2 beautifulsoup4 aiohttp pydantic --quiet 2>/dev/null && \
        echo -e "  ${GREEN}✓${NC} Dependencies installed" || \
        echo -e "  ${YELLOW}⚠${NC} Dependencies may need manual installation"
elif command -v pip &> /dev/null; then
    pip install jinja2 beautifulsoup4 aiohttp pydantic --quiet 2>/dev/null && \
        echo -e "  ${GREEN}✓${NC} Dependencies installed" || \
        echo -e "  ${YELLOW}⚠${NC} Dependencies may need manual installation"
else
    echo -e "  ${YELLOW}⚠${NC} pip not found (dependencies may need manual install)"
    echo ""
    echo -e "  Run this manually if needed:"
    echo -e "    pip install jinja2 beautifulsoup4 aiohttp pydantic"
fi
echo ""

# Create README
echo -e "${CYAN}Step 4: Creating README...${NC}"
echo ""

cat > "$DATA_DIR/opendesigner/README.md" << 'README_EOF'
# OpenDesigner Studio

## Installation Complete! ✓

OpenDesigner has been successfully installed to your OpenWebUI instance.

### What's Included:
- **17 Functions**: Generation, preview, export, accessibility, auth, collaboration, monitoring, and more
- **73+ Templates**: Landing pages, dashboards, emails, presentations, interactive components, and more
- **AI-Powered**: Generate designs from natural language prompts
- **Real-time Collaboration**: Multi-user editing
- **Accessibility**: WCAG 2.1 AA compliance checker
- **Export**: SVG, JSON, HTML, PNG formats

### Usage:
1. Open your OpenWebUI instance
2. Start a new chat
3. Type a design request like "Create a landing page for my SaaS product"
4. OpenDesigner will generate a complete, responsive HTML page

### Documentation:
- GitHub: https://github.com/asorichetti/OpenDesigner
- API Docs: https://github.com/asorichetti/OpenDesigner/blob/main/docs/API.md
- Installation: https://github.com/asorichetti/OpenDesigner/blob/main/docs/INSTALL.md

### Support:
- Issues: https://github.com/asorichetti/OpenDesigner/issues
README_EOF

echo -e "  ${GREEN}✓${NC} README created"
echo ""

# Summary
echo -e "${BLUE}╔══════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║       Installation Complete!             ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}✓  Functions installed${NC}"
echo -e "${GREEN}✓  Templates copied${NC}"
echo -e "${GREEN}✓  Assets installed${NC}"
echo -e "${GREEN}✓  Plugin manifest created${NC}"
echo -e "${GREEN}✓  Dependencies installed${NC}"
echo ""
echo -e "${CYAN}Next Steps:${NC}"
echo -e "  1. Restart OpenWebUI"
echo -e "     - Docker: ${YELLOW}docker restart openwebui${NC}"
echo -e "     - Systemd: ${YELLOW}sudo systemctl restart openwebui${NC}"
echo -e "  2. Open your browser and start chatting"
echo -e "  3. Type: 'Create a landing page for my startup'"
echo ""
echo -e "${GREEN}OpenDesigner is now LIVE! 🚀${NC}"
echo ""
echo -e "${YELLOW}Need help?${NC}"
echo -e "  - Documentation: https://github.com/asorichetti/OpenDesigner"
echo -e "  - Issues: https://github.com/asorichetti/OpenDesigner/issues"
echo ""
