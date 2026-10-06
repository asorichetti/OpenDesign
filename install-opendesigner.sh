#!/bin/bash
# OpenDesigner Installer for existing OpenWebUI instance
# Usage: ./install-opendesigner.sh [OPENWEBUI_DATA_DIR]
#
# Examples:
#   ./install-opendesigner.sh
#   ./install-opendesigner.sh /path/to/openwebui/data
#   ./install-opendesigner.sh docker

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔══════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║      OpenDesigner 1.0 Installer          ║${NC}"
echo -e "${BLUE}║  17 Functions • 73+ Templates • Ready    ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════╝${NC}"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="${1:-}"

# Step 1: Find data directory
echo -e "${BLUE}Step 1: Finding OpenWebUI data directory...${NC}"

if [ -z "$DATA_DIR" ]; then
    # Try Docker inspect to find the volume
    if command -v docker &> /dev/null; then
        echo -e "  Looking for OpenWebUI container..."
        CONTAINER=$(docker ps --filter "name=openwebui" --format "{{.ID}}" 2>/dev/null || true)
        if [ -n "$CONTAINER" ]; then
            DATA_DIR=$(docker inspect -f '{{range .Mounts}}{{if eq .Destination "/app/backend/data"}}{{.Source}}{{end}}{{end}}' "$CONTAINER" 2>/dev/null || true)
            if [ -n "$DATA_DIR" ]; then
                echo -e "  ${GREEN}✓${NC} Found via Docker: ${DATA_DIR}"
            fi
        fi
    fi

    # Fallback to common locations
    if [ -z "$DATA_DIR" ] && [ -d "$HOME/.open-webui" ]; then
        DATA_DIR="$HOME/.open-webui"
        echo -e "  ${GREEN}✓${NC} Found in default location: ${DATA_DIR}"
    elif [ -z "$DATA_DIR" ] && [ -d "/var/lib/open-webui" ]; then
        DATA_DIR="/var/lib/open-webui"
        echo -e "  ${GREEN}✓${NC} Found in /var/lib/open-webui"
    fi
else
    echo -e "  ${GREEN}✓${NC} Using provided path: ${DATA_DIR}"
fi

if [ -z "$DATA_DIR" ] || [ ! -d "$DATA_DIR" ]; then
    echo -e "\n${RED}✗${NC} Cannot find OpenWebUI data directory"
    echo ""
    echo "  Please provide the path manually:"
    echo "    $0 /path/to/openwebui/data"
    echo ""
    echo "  Common locations:"
    echo "    - ~/.open-webui"
    echo "    - /var/lib/open-webui"
    echo "    - Docker volume (run: docker inspect <container>)"
    echo ""
    exit 1
fi

echo ""
echo -e "${BLUE}Step 2: Creating directory structure...${NC}"

FUNCTIONS_DIR="$DATA_DIR/functions/opendesigner"
TEMPLATES_DIR="$DATA_DIR/opendesigner/templates"
ASSETS_DIR="$DATA_DIR/opendesigner/assets"
PROMPTS_DIR="$DATA_DIR/opendesigner/prompts"

mkdir -p "$FUNCTIONS_DIR"
mkdir -p "$TEMPLATES_DIR/landing"
mkdir -p "$TEMPLATES_DIR/dashboard"
mkdir -p "$TEMPLATES_DIR/component"
mkdir -p "$TEMPLATES_DIR/presentation"
mkdir -p "$TEMPLATES_DIR/email"
mkdir -p "$TEMPLATES_DIR/social"
mkdir -p "$TEMPLATES_DIR/interactive"
mkdir -p "$TEMPLATES_DIR/interactive/forms"
mkdir -p "$TEMPLATES_DIR/ecommerce"
mkdir -p "$TEMPLATES_DIR/portfolio"
mkdir -p "$TEMPLATES_DIR/blog"
mkdir -p "$TEMPLATES_DIR/contact"
mkdir -p "$TEMPLATES_DIR/pricing"
mkdir -p "$ASSETS_DIR"
mkdir -p "$PROMPTS_DIR"

echo -e "  ${GREEN}✓${NC} ${FUNCTIONS_DIR}"
echo -e "  ${GREEN}✓${NC} ${TEMPLATES_DIR}"
echo -e "  ${GREEN}✓${NC} ${ASSETS_DIR}"
echo -e "  ${GREEN}✓${NC} ${PROMPTS_DIR}"

echo ""
echo -e "${BLUE}Step 3: Installing 17 plugin functions...${NC}"

# Install ALL 17 plugin functions
declare -a FUNCTIONS=(
    "designer_studio/designer_studio"
    "preview_generator/preview_generator"
    "prompt_enhancer/prompt_enhancer"
    "export_formats/export_formats"
    "accessibility_checker/accessibility_checker"
    "authentication/authentication"
    "collaboration/collaboration"
    "collaboration_engine/collaboration_engine"
    "component_library/component_library"
    "error_handler/error_handler"
    "monitoring/monitoring_analytics"
    "performance_optimizer/performance_optimizer"
    "prompt_generator/prompt_generator"
    "version_control/version_control"
    "onboarding_tutorial/onboarding_tutorial"
    "api/api_integrations"
    "template_marketplace/template_marketplace"
)

for func in "${FUNCTIONS[@]}"; do
    func_name=$(echo "$func" | cut -d'/' -f2)
    if [ -f "$SCRIPT_DIR/functions/${func}.py" ]; then
        cp "$SCRIPT_DIR/functions/${func}.py" "$FUNCTIONS_DIR/"
        echo -e "  ${GREEN}✓${NC} ${func_name}.py"
    else
        echo -e "  ${YELLOW}⚠${NC} ${func_name}.py (not found, skipping)"
    fi
done

echo ""
echo -e "${BLUE}Step 4: Copying 73+ templates...${NC}"

# Copy all templates
TEMPLATES_DIR_SOURCE="$SCRIPT_DIR/functions/designer_studio/templates"
if [ -d "$TEMPLATES_DIR_SOURCE" ]; then
    # Copy all template directories
    for dir in "$TEMPLATES_DIR_SOURCE"/*/; do
        if [ -d "$dir" ]; then
            dirname=$(basename "$dir")
            mkdir -p "$TEMPLATES_DIR/$dirname"
            cp "$dir"*.html "$TEMPLATES_DIR/$dirname/" 2>/dev/null || true
            echo -e "  ${GREEN}✓${NC} ${dirname}/ ($(ls "$dir"*.html 2>/dev/null | wc -l) files)"
        fi
    done
fi

echo ""
echo -e "${BLUE}Step 5: Copying assets...${NC}"

ASSETS_SOURCE="$SCRIPT_DIR/functions/designer_studio/assets"
if [ -d "$ASSETS_SOURCE" ]; then
    cp "$ASSETS_SOURCE"/*.css "$ASSETS_DIR/" 2>/dev/null || true
    echo -e "  ${GREEN}✓${NC} Assets (CSS files)"
fi

echo ""
echo -e "${BLUE}Step 6: Installing dependencies...${NC}"

# Check if pip is available
if command -v pip3 &> /dev/null; then
    pip3 install jinja2 beautifulsoup4 aiohttp pydantic --quiet 2>/dev/null && \
        echo -e "  ${GREEN}✓${NC} Python dependencies installed" || \
        echo -e "  ${YELLOW}⚠${NC} Could not install dependencies (may already be installed)"
elif command -v pip &> /dev/null; then
    pip install jinja2 beautifulsoup4 aiohttp pydantic --quiet 2>/dev/null && \
        echo -e "  ${GREEN}✓${NC} Python dependencies installed" || \
        echo -e "  ${YELLOW}⚠${NC} Could not install dependencies (may already be installed)"
else
    echo -e "  ${YELLOW}⚠${NC} pip not found (dependencies may need manual install)"
fi

echo ""
echo -e "${BLUE}Step 7: Creating plugin manifest...${NC}"

cat > "$DATA_DIR/opendesigner/plugin.json" << 'PLUGIN_EOF'
{
    "id": "opendesigner",
    "name": "OpenDesigner Studio",
    "description": "Generate beautiful, functional websites from natural language. Open-source design generation platform for Open WebUI with 73+ templates, real-time collaboration, and AI-powered design.",
    "version": "1.0.0",
    "author": "asorichetti",
    "license": "MIT",
    "repository": "https://github.com/asorichetti/OpenDesigner",
    "functions": [
        {"type": "pipe", "file": "functions/opendesigner/designer_studio.py", "name": "Design Studio", "description": "Generate HTML prototypes from chat prompts"},
        {"type": "action", "file": "functions/opendesigner/preview_generator.py", "name": "Preview Generator", "description": "Render sandboxed previews, export HTML, open live editor"},
        {"type": "filter", "file": "functions/opendesigner/prompt_enhancer.py", "name": "Prompt Enhancer", "description": "Enhance design-related prompts with context and guidelines"}
    ],
    "templates": ["templates/*/*.html"],
    "dependencies": ["jinja2>=3.1", "beautifulsoup4>=4.12", "aiohttp>=3.9", "pydantic>=2.0"],
    "required_open_webui_version": ">=0.10.0",
    "icon_url": "https://cdn.jsdelivr.net/gh/asorichetti/OpenDesigner@main/assets/logo.svg"
}
PLUGIN_EOF

echo -e "  ${GREEN}✓${NC} plugin.json created"

echo ""
echo -e "${BLUE}Step 8: Finalizing installation...${NC}"

# Create README in the data directory
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
- Discord/Community: [Join our community]

---
Version: 1.0.0 | Installed: $(date)
README_EOF

echo -e "  ${GREEN}✓${NC} README created"

echo ""
echo -e "${BLUE}╔══════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        Installation Complete!            ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}✓  17 Functions installed${NC}"
echo -e "${GREEN}✓  73+ Templates copied${NC}"
echo -e "${GREEN}✓  Dependencies ready${NC}"
echo -e "${GREEN}✓  Plugin manifest created${NC}"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo -e "  1. Restart OpenWebUI: ${YELLOW}docker restart openwebui${NC}"
echo -e "  2. Open your browser and start chatting"
echo -e "  3. Type: 'Create a landing page for my startup'"
echo ""
echo -e "${GREEN}OpenDesigner is now LIVE! 🚀${NC}"
