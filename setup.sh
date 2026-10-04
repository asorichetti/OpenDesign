#!/bin/bash
set -e

# OpenDesign Installer — Sets up functions in OpenWebUI
# Usage: ./setup.sh

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔══════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        OpenDesign Installer              ║${NC}"
echo -e "${BLUE}╠══════════════════════════════════════════╣${NC}"
echo -e "${BLUE}║        OpenWebUI Plugin Setup            ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════╝${NC}"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo -e "${YELLOW}Script location: ${SCRIPT_DIR}${NC}"
echo ""

# Find OpenWebUI data directory
echo -e "${BLUE}Step 1: Finding OpenWebUI data directory...${NC}"
echo ""

# Try common locations
OPENWEBUI_DATA=""

# Check OPENWEBUI_DATA_DIR environment variable
if [ -n "$OPENWEBUI_DATA_DIR" ]; then
    OPENWEBUI_DATA="$OPENWEBUI_DATA_DIR"
    echo -e "  ${GREEN}✓${NC} Found via OPENWEBUI_DATA_DIR: ${OPENWEBUI_DATA}"
elif [ -d "$HOME/.open-webui" ]; then
    OPENWEBUI_DATA="$HOME/.open-webui"
    echo -e "  ${GREEN}✓${NC} Found in default location: ${OPENWEBUI_DATA}"
elif [ -d "/app/.open-webui" ]; then
    OPENWEBUI_DATA="/app/.open-webui"
    echo -e "  ${GREEN}✓${NC} Found in Docker location: ${OPENWEBUI_DATA}"
elif [ -d "$PWD/.open-webui" ]; then
    OPENWEBUI_DATA="$PWD/.open-webui"
    echo -e "  ${GREEN}✓${NC} Found in current directory: ${OPENWEBUI_DATA}"
else
    echo -e "  ${RED}✗${NC} OpenWebUI data directory not found"
    echo ""
    echo "  You can set OPENWEBUI_DATA_DIR environment variable:"
    echo "    export OPENWEBUI_DATA_DIR=/path/to/openwebui/data"
    echo ""
    echo "  Or provide it directly:"
    echo "    ./setup.sh /path/to/openwebui/data"
    echo ""
    read -p "  Enter path or press Enter to skip: " OPENWEBUI_DATA
    if [ -z "$OPENWEBUI_DATA" ]; then
        echo -e "${RED}Cannot proceed without OpenWebUI data directory.${NC}"
        echo -e "${YELLOW}Skipping function installation.${NC}"
        exit 0
    fi
fi

# Create functions directory
echo ""
echo -e "${BLUE}Step 2: Setting up functions directory...${NC}"
FUNCTIONS_DIR="$OPENWEBUI_DATA/functions/opendesign"
mkdir -p "$FUNCTIONS_DIR"
echo -e "  ${GREEN}✓${NC} Created: ${FUNCTIONS_DIR}"

# Copy function files
echo ""
echo -e "${BLUE}Step 3: Installing plugin functions...${NC}"

echo "  Installing Design Studio..."
cp "$SCRIPT_DIR/functions/design_studio/design_studio.py" "$FUNCTIONS_DIR/design_studio.py"
echo -e "    ${GREEN}✓${NC} design_studio.py"

echo "  Installing Preview Generator..."
cp "$SCRIPT_DIR/functions/preview_generator/preview_generator.py" "$FUNCTIONS_DIR/preview_generator.py"
echo -e "    ${GREEN}✓${NC} preview_generator.py"

echo "  Installing Prompt Enhancer..."
cp "$SCRIPT_DIR/functions/prompt_enhancer/prompt_enhancer.py" "$FUNCTIONS_DIR/prompt_enhancer.py"
echo -e "    ${GREEN}✓${NC} prompt_enhancer.py"

# Create templates directory
echo ""
echo -e "${BLUE}Step 4: Installing templates...${NC}"
TEMPLATES_DIR="$OPENWEBUI_DATA/opendesign/templates"
mkdir -p "$TEMPLATES_DIR/landing"
mkdir -p "$TEMPLATES_DIR/dashboard"
mkdir -p "$TEMPLATES_DIR/component"
mkdir -p "$TEMPLATES_DIR/presentation"
mkdir -p "$TEMPLATES_DIR/email"
mkdir -p "$TEMPLATES_DIR/social"

echo "  Installing landing templates..."
for f in "$SCRIPT_DIR/functions/design_studio/templates/landing/"*.html; do
    cp "$f" "$TEMPLATES_DIR/landing/"
    echo -e "    ${GREEN}✓${NC} $(basename $f)"
done

echo "  Installing dashboard templates..."
for f in "$SCRIPT_DIR/functions/design_studio/templates/dashboard/"*.html; do
    cp "$f" "$TEMPLATES_DIR/dashboard/"
    echo -e "    ${GREEN}✓${NC} $(basename $f)"
done

echo "  Installing component templates..."
for f in "$SCRIPT_DIR/functions/design_studio/templates/component/"*.html; do
    cp "$f" "$TEMPLATES_DIR/component/"
    echo -e "    ${GREEN}✓${NC} $(basename $f)"
done

echo "  Installing presentation templates..."
for f in "$SCRIPT_DIR/functions/design_studio/templates/presentation/"*.html; do
    cp "$f" "$TEMPLATES_DIR/presentation/"
    echo -e "    ${GREEN}✓${NC} $(basename $f)"
done

echo "  Installing email templates..."
for f in "$SCRIPT_DIR/functions/design_studio/templates/email/"*.html; do
    cp "$f" "$TEMPLATES_DIR/email/"
    echo -e "    ${GREEN}✓${NC} $(basename $f)"
done

echo "  Installing social templates..."
for f in "$SCRIPT_DIR/functions/design_studio/templates/social/"*.html; do
    cp "$f" "$TEMPLATES_DIR/social/"
    echo -e "    ${GREEN}✓${NC} $(basename $f)"
done

# Copy assets
echo ""
echo -e "${BLUE}Step 5: Installing design system assets...${NC}"
ASSETS_DIR="$OPENWEBUI_DATA/opendesign/assets"
mkdir -p "$ASSETS_DIR"
cp "$SCRIPT_DIR/functions/design_studio/assets/light.css" "$ASSETS_DIR/"
cp "$SCRIPT_DIR/functions/design_studio/assets/dark.css" "$ASSETS_DIR/"
echo -e "  ${GREEN}✓${NC} light.css"
echo -e "  ${GREEN}✓${NC} dark.css"

# Copy prompts
echo ""
echo -e "${BLUE}Step 6: Installing prompt templates...${NC}"
PROMPTS_DIR="$OPENWEBUI_DATA/opendesign/prompts"
mkdir -p "$PROMPTS_DIR"
cp "$SCRIPT_DIR/functions/design_studio/prompts/"*.md "$PROMPTS_DIR/"
for f in "$PROMPTS_DIR"/*.md; do
    echo -e "  ${GREEN}✓${NC} $(basename $f)"
done

# Verify installation
echo ""
echo -e "${BLUE}Step 7: Verifying installation...${NC}"
echo ""

FUNCTIONS_COUNT=$(find "$FUNCTIONS_DIR" -name "*.py" -type f 2>/dev/null | wc -l | xargs)
TEMPLATE_COUNT=$(find "$TEMPLATES_DIR" -name "*.html" -type f 2>/dev/null | wc -l | xargs)

if [ "$FUNCTIONS_COUNT" -eq 3 ]; then
    echo -e "  ${GREEN}✓${NC} 3 function files installed"
else
    echo -e "  ${RED}✗${NC} Expected 3 functions, found $FUNCTIONS_COUNT"
fi

if [ "$TEMPLATE_COUNT" -eq 14 ]; then
    echo -e "  ${GREEN}✓${NC} 14 templates installed"
else
    echo -e "  ${YELLOW}⚠${NC} Expected 14 templates, found $TEMPLATE_COUNT"
fi

if [ -d "$ASSETS_DIR" ] && [ "$(find "$ASSETS_DIR" -name "*.css" | wc -l)" -eq 2 ]; then
    echo -e "  ${GREEN}✓${NC} 2 design system assets installed"
else
    echo -e "  ${RED}✗${NC} Design system assets missing"
fi

# Next steps
echo ""
echo -e "${BLUE}╔══════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        Installation Complete!            ║${NC}"
echo -e "${BLUE}╠══════════════════════════════════════════╣${NC}"
echo -e "${BLUE}║        Next Steps                        ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════╝${NC}"
echo ""
echo -e "  1. Restart OpenWebUI if it's running:"
echo ""
echo -e "     ${YELLOW}docker compose restart${NC}"
echo ""
echo -e "  2. Open OpenWebUI in your browser:"
echo ""
echo -e "     ${YELLOW}http://localhost:3000${NC}"
echo ""
echo -e "  3. Go to ${YELLOW}Settings → Extensions → Functions${NC}"
echo ""
echo -e "  4. Verify the following are installed:"
echo ""
echo -e "     • ${GREEN}Design Studio${NC} (Pipe)"
echo -e "     • ${GREEN}Preview Generator${NC} (Action)"
echo -e "     • ${GREEN}Prompt Enhancer${NC} (Filter)"
echo ""
echo -e "  5. Start designing! Try prompts like:"
echo ""
echo -e "     • ${YELLOW}\"Create a landing page for a coffee shop\"${NC}"
echo -e "     • ${YELLOW}\"Build me a dashboard with analytics\"${NC}"
echo -e "     • ${YELLOW}\"Design a button component\"${NC}"
echo ""
echo -e "${GREEN}🎉 Happy designing!${NC}"
echo ""
