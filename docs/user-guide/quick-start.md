# Quick Start Guide

Get up and running with OpenDesigner in under 5 minutes.

---

## Prerequisites

- Open WebUI instance (v0.10.0 or later)
- Python 3.11+ (for local development)
- Git (optional, for installation)

---

## Installation Methods

### Method 1: Open WebUI Marketplace (Recommended)

1. Open your Open WebUI instance
2. Go to **Admin Settings** → **Community Plugins**
3. Search for "OpenDesigner"
4. Click **Install**
5. Restart Open WebUI
6. Start designing! 🎉

### Method 2: Manual Installation

```bash
# Clone the repository
git clone https://github.com/asorichetti/OpenDesigner.git

# Navigate to Open WebUI data directory
cd /path/to/openwebui/data

# Copy plugin functions
cp -r OpenDesigner/functions/* ./plugin-functions/

# Copy templates
cp -r OpenDesigner/templates ./templates/

# Restart Open WebUI
```

### Method 3: Docker Installation

```bash
# Clone the repository
git clone https://github.com/asorichetti/OpenDesigner.git

# Navigate to docker directory
cd OpenDesigner/docker

# Start with Docker Compose
docker-compose up -d

# Access at http://localhost:3000
```

---

## First Design

1. **Open Open WebUI** and navigate to the chat interface
2. **Type a design prompt**, for example:
   ```
   Create a modern landing page for a SaaS product
   ```
3. **Review the generated design** in the preview panel
4. **Customize** using the Visual Customization Panel
5. **Export** to your preferred framework

---

## Using the Features

### AI Design Iteration

```
User: "Make the hero section bigger and change to dark theme"
System: Updates design with those changes
```

### Visual Customization

1. Click the **Customization Panel** icon
2. Adjust colors, fonts, and spacing
3. Preview changes in real-time
4. Click **Apply** to save

### Export to Framework

1. Click the **Export** button
2. Select framework (React, Vue, Next.js)
3. Configure export options
4. Download code

---

## Next Steps

- [Installation Guide](./installation.md) — Detailed installation options
- [Feature Guide](./features.md) — Learn all 15 features
- [API Reference](../api/overview.md) — Plugin API documentation
- [Tutorials](../tutorials/overview.md) — Step-by-step tutorials

---

## Troubleshooting

### Plugin not loading

1. Check Open WebUI version (must be v0.10.0+)
2. Verify plugin functions are in the correct directory
3. Restart Open WebUI
4. Check browser console for errors

### Preview not rendering

1. Ensure iframe sandbox is enabled
2. Check for external URLs in HTML
3. Verify no `eval()` in code

### Export not working

1. Verify framework is supported
2. Check browser compatibility
3. Ensure no security restrictions

---

## Need Help?

- [GitHub Issues](https://github.com/asorichetti/OpenDesigner/issues)
- [GitHub Discussions](https://github.com/asorichetti/OpenDesigner/discussions)
- [FAQ](./faq.md)
