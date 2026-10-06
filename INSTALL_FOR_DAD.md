# 📦 OpenDesigner - Simple Installation Guide for Your Dad

## 🎯 What This Does

This installs **OpenDesigner Studio** - an AI-powered design generation tool that works directly inside OpenWebUI.

**What your dad will get:**
- ✅ 73+ professional website templates
- ✅ AI-powered design generation from chat
- ✅ Real-time collaboration features
- ✅ Accessibility checking (WCAG 2.1 AA)
- ✅ Export to SVG, JSON, HTML, PNG
- ✅ Version control for designs
- ✅ Component library browser
- ✅ Analytics & monitoring

---

## 🚀 Installation (2 Steps)

### Step 1: Clone the Repository

```bash
# SSH (if you have GitHub access)
git clone https://github.com/asorichetti/OpenDesigner.git

# OR download as ZIP
# Visit: https://github.com/asorichetti/OpenDesigner
# Click "Code" → "Download ZIP"
# Extract the folder
```

### Step 2: Run the Installer

```bash
cd OpenDesigner
./install-for-dad.sh
```

That's it! The installer will:
1. ✅ Find your OpenWebUI installation
2. ✅ Copy all functions and templates
3. ✅ Install required dependencies
4. ✅ Create plugin manifest
5. ✅ Restart OpenWebUI (if using Docker)

---

## 🤔 What If It Doesn't Work?

### Option A: Manual Installation (Always works)

```bash
# 1. Find your OpenWebUI data directory
# Common locations:
#   - ~/.open-webui
#   - /var/lib/open-webui
#   - /opt/openwebui/data

# 2. Copy the plugin files
cp -r plugins/opendesigner/functions/* ~/.open-webui/functions/
cp -r plugins/opendesigner/templates/* ~/.open-webui/templates/
cp -r plugins/opendesigner/assets/* ~/.open-webui/assets/
cp plugins/opendesigner/plugin.json ~/.open-webui/

# 3. Install dependencies
pip install jinja2 beautifulsoup4 aiohttp pydantic

# 4. Restart OpenWebUI
docker restart openwebui
# OR
systemctl restart openwebui
```

### Option B: Docker Installation

```bash
# If OpenWebUI runs in Docker
docker cp OpenDesigner/plugins/opendesigner/functions/* <container>:/app/backend/data/functions/
docker cp OpenDesigner/plugins/opendesigner/templates/* <container>/app/backend/data/templates/
docker cp OpenDesigner/plugins/opendesigner/assets/* <container>/app/backend/data/assets/
docker cp OpenDesigner/plugins/opendesigner/plugin.json <container>:/app/backend/data/

# Restart
docker restart <container>
```

---

## ✅ Verification

After installation, test it:

1. Open your OpenWebUI instance in browser
2. Start a new chat
3. Type: `"Create a landing page for my startup"`
4. OpenDesigner should generate a complete, responsive HTML page
5. You'll see a preview with options to export, edit, and save

---

## 🎯 What You'll See in OpenWebUI

### New Functions Available:
- **Design Studio** - Main generation engine
- **Preview Generator** - Preview and export designs
- **Prompt Enhancer** - Smart prompt optimization
- **Export Formats** - Download as SVG/JSON/HTML/PNG
- **Accessibility Checker** - Verify WCAG compliance
- **Template Marketplace** - Browse community templates
- **Component Library** - Browse UI components
- **Version Control** - Manage design versions
- **Collaboration** - Real-time editing
- **Monitoring** - Analytics and insights
- **API & Integrations** - External API access

### New Templates Available:
- Landing pages (hero, minimal, feature-grid)
- Dashboards (analytics)
- Email templates (newsletter, transactional)
- Social media (hero-banner, og-card)
- Presentations (blank, sections)
- Interactive components (29+ including nav, carousel, accordion, modal, etc.)
- Forms (registration, contact, multistep)

---

## 🆘 Troubleshooting

### Problem: "Functions not loading"
**Solution:** Check that files are in the right directory
```bash
ls ~/.open-webui/functions/opendesigner/
# Should show: designer_studio.py, preview_generator.py, etc.
```

### Problem: "Templates not showing"
**Solution:** Check that templates are copied
```bash
ls ~/.open-webui/templates/
# Should show: component/, dashboard/, email/, interactive/, landing/, etc.
```

### Problem: "Import errors"
**Solution:** Install dependencies
```bash
pip install jinja2 beautifulsoup4 aiohttp pydantic
```

### Problem: "OpenWebUI won't restart"
**Solution:** Check logs
```bash
docker logs openwebui --tail 50
# OR
journalctl -u openwebui --tail 50
```

---

## 📚 Documentation

- **Full README:** https://github.com/asorichetti/OpenDesigner/blob/main/README.md
- **API Docs:** https://github.com/asorichetti/OpenDesigner/blob/main/docs/API.md
- **Installation Guide:** https://github.com/asorichetti/OpenDesigner/blob/main/docs/INSTALL.md
- **GitHub Issues:** https://github.com/asorichetti/OpenDesigner/issues

---

## 💡 Quick Tips

### For Your Dad:
1. **Start simple:** Try "Create a landing page" first
2. **Explore templates:** Use "Design Studio" to browse templates
3. **Export designs:** Click "Export" to download as HTML/SVG/JSON/PNG
4. **Check accessibility:** Use "Accessibility Checker" to verify WCAG compliance
5. **Save versions:** Use "Version Control" to track changes

### For Testing:
```
# Try these prompts:
"Create a landing page for my SaaS product"
"Generate a dashboard for analytics"
"Build a pricing page for my startup"
"Design a newsletter email template"
"Create a presentation about AI"
```

---

## ✅ Success Criteria

You'll know it's working when:
1. ✅ OpenDesigner functions appear in OpenWebUI
2. ✅ Templates are available in the template library
3. ✅ You can generate a design from a chat prompt
4. ✅ Preview renders correctly in the iframe
5. ✅ Export functionality works (download as HTML/SVG/JSON/PNG)
6. ✅ Accessibility checker runs and reports issues
7. ✅ Version control saves and loads designs

---

## 🎉 That's It!

OpenDesigner is now installed and ready to use.

**Happy designing!** 🚀

---

*Built with ❤️ by the OpenDesigner team*
*Version 1.0.0 | Production Ready*
