#!/bin/bash
# OpenDesign Installer for existing OpenWebUI instance
# Usage: ./install-opendesign.sh [OPENWEBUI_DATA_DIR]
#
# Examples:
#   ./install-opendesign.sh
#   ./install-opendesign.sh /path/to/openwebui/data
#   ./install-opendesign.sh docker

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔══════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        OpenDesign Installer              ║${NC}"
echo -e "${BLUE}║        For: https://ai.s8i.app           ║${NC}"
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

FUNCTIONS_DIR="$DATA_DIR/functions/opendesign"
TEMPLATES_DIR="$DATA_DIR/opendesign/templates"
ASSETS_DIR="$DATA_DIR/opendesign/assets"
PROMPTS_DIR="$DATA_DIR/opendesign/prompts"

mkdir -p "$FUNCTIONS_DIR"
mkdir -p "$TEMPLATES_DIR/landing"
mkdir -p "$TEMPLATES_DIR/dashboard"
mkdir -p "$TEMPLATES_DIR/component"
mkdir -p "$TEMPLATES_DIR/presentation"
mkdir -p "$TEMPLATES_DIR/email"
mkdir -p "$TEMPLATES_DIR/social"
mkdir -p "$ASSETS_DIR"
mkdir -p "$PROMPTS_DIR"

echo -e "  ${GREEN}✓${NC} ${FUNCTIONS_DIR}"
echo -e "  ${GREEN}✓${NC} ${TEMPLATES_DIR}"
echo -e "  ${GREEN}✓${NC} ${ASSETS_DIR}"
echo -e "  ${GREEN}✓${NC} ${PROMPTS_DIR}"

echo ""
echo -e "${BLUE}Step 3: Installing functions...${NC}"

# Install the three plugin functions
for func in design_studio preview_generator prompt_enhancer; do
    cp "$SCRIPT_DIR/functions/${func}/${func}.py" "$FUNCTIONS_DIR/"
    echo -e "  ${GREEN}✓${NC} ${func}.py"
done

echo ""
echo -e "${BLUE}Step 4: Installing templates...${NC}"

for dir in landing dashboard component presentation email social; do
    for f in "$SCRIPT_DIR/functions/design_studio/templates/${dir}/"*.html; do
        if [ -f "$f" ]; then
            cp "$f" "$TEMPLATES_DIR/${dir}/"
        fi
    done
    echo -e "  ${GREEN}✓${NC} ${dir}/ ($(ls "$TEMPLATES_DIR/${dir}/" | wc -l) files)"
done

echo ""
echo -e "${BLUE}Step 5: Installing assets and prompts...${NC}"

cp "$SCRIPT_DIR/functions/design_studio/assets/"*.css "$ASSETS_DIR/"
echo -e "  ${GREEN}✓${NC} CSS assets (light, dark)"

cp "$SCRIPT_DIR/functions/design_studio/prompts/"*.md "$PROMPTS_DIR/"
echo -e "  ${GREEN}✓${NC} Prompt templates (7 files)"

echo ""
echo -e "${BLUE}Step 6: Verifying installation...${NC}"

FUNC_COUNT=$(find "$FUNCTIONS_DIR" -name "*.py" | wc -l)
TEMPLATE_COUNT=$(find "$TEMPLATES_DIR" -name "*.html" | wc -l)
ASSET_COUNT=$(find "$ASSETS_DIR" -name "*.css" | wc -l)
PROMPT_COUNT=$(find "$PROMPTS_DIR" -name "*.md" | wc -l)

if [ "$FUNC_COUNT" -eq 3 ]; then
    echo -e "  ${GREEN}✓${NC} 3 functions installed"
else
    echo -e "  ${RED}✗${NC} Expected 3 functions, found $FUNC_COUNT"
fi

if [ "$TEMPLATE_COUNT" -eq 14 ]; then
    echo -e "  ${GREEN}✓${NC} 14 templates installed"
else
    echo -e "  ${YELLOW}⚠${NC} Expected 14 templates, found $TEMPLATE_COUNT"
fi

if [ "$ASSET_COUNT" -ge 2 ]; then
    echo -e "  ${GREEN}✓${NC} Assets installed"
fi

if [ "$PROMPT_COUNT" -ge 7 ]; then
    echo -e "  ${GREEN}✓${NC} Prompts installed"
fi

echo ""
echo -e "${BLUE}╔══════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        Installation Complete!            ║${NC}"
echo -e "${BLUE}╠══════════════════════════════════════════╣${NC}"
echo -e "${BLUE}║        Next Steps                        ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════╝${NC}"
echo ""
echo -e "  Data directory: ${DATA_DIR}"
echo ""
echo -e "  1. Install Python dependencies in OpenWebUI's environment:"
echo ""
echo -e "     ${YELLOW}docker exec -it <container> pip install jinja2 beautifulsoup4 aiohttp pydantic${NC}"
echo ""
echo -e "  2. Restart OpenWebUI:"
echo ""
echo -e "     ${YELLOW}docker restart <container>${NC}"
echo ""
echo -e "  3. Open https://ai.s8i.app"
echo ""
echo -e "  4. Go to ${YELLOW}Settings → Extensions → Functions${NC}"
echo ""
echo -e "  5. Verify these are loaded:"
echo ""
echo -e "     • ${GREEN}Design Studio${NC} (Pipe)"
echo -e "     • ${GREEN}Preview Generator${NC} (Action)"
echo -e "     • ${GREEN}Prompt Enhancer${NC} (Filter)"
echo ""
echo -e "  6. Start a chat and try:"
echo ""
echo -e "     ${YELLOW}\"Create a landing page for a coffee shop\"${NC}"
echo ""
echo -e "${GREEN}🎉 Happy designing!${NC}"
echo ""
