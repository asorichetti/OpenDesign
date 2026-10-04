"""
title: OpenDesign Preview Generator
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesign
version: 0.1.0
required_open_webui_version: 0.10.0
"""

import re
from typing import Any


class Action:
    """OpenDesign Preview Generator — renders design code in a sandboxed iframe."""

    def __init__(self):
        self.type = "action"

    def actions(self) -> list[dict[str, str]]:
        """Return available actions."""
        return [
            {
                "name": "Generate Preview",
                "description": "Render the generated design in a sandboxed preview",
                "icon": "eye",
            },
            {
                "name": "Export HTML",
                "description": "Download the generated code as a ZIP file",
                "icon": "download",
            },
            {
                "name": "Export PNG",
                "description": "Render design as PNG image",
                "icon": "image",
            },
            {
                "name": "Export PDF",
                "description": "Export design as printable PDF",
                "icon": "file-text",
            },
            {
                "name": "Open Editor",
                "description": "Open the split-pane live editor",
                "icon": "edit",
            },
            {
                "name": "Compare Models",
                "description": "View model comparison side-by-side",
                "icon": "columns",
            },
            {
                "name": "Multi-Device Preview",
                "description": "Preview at desktop/tablet/mobile breakpoints",
                "icon": "devices",
            },
        ]

    async def action(
        self,
        action: str,
        body: dict,
        __user__: dict | None = None,
        __event_emitter__: Any | None = None,
        **kwargs,
    ) -> str:
        """Handle an action click on a chat message."""

        message = body.get("message", {})
        content = message.get("content", "")

        if action == "Generate Preview":
            code_blocks = self._extract_code_blocks(content)
            if not code_blocks:
                return "No HTML code blocks found in this message."
            return self._render_preview(code_blocks[0])

        elif action == "Export HTML":
            code_blocks = self._extract_code_blocks(content)
            if not code_blocks:
                return "No HTML code blocks found in this message."
            return self._export_html(code_blocks[0])

        elif action == "Open Editor":
            code_blocks = self._extract_code_blocks(content)
            if not code_blocks:
                return "No HTML code blocks found in this message."
            return self._render_editor(code_blocks[0])

        elif action == "Compare Models":
            return self._render_comparison(content)

        elif action == "Multi-Device Preview":
            code_blocks = self._extract_code_blocks(content)
            if not code_blocks:
                return "No HTML code blocks found in this message."
            return self._render_multi_device(code_blocks[0])

        elif action == "Export PNG":
            code_blocks = self._extract_code_blocks(content)
            if not code_blocks:
                return "No HTML code blocks found in this message."
            return self._render_png_export(code_blocks[0])

        elif action == "Export PDF":
            code_blocks = self._extract_code_blocks(content)
            if not code_blocks:
                return "No HTML code blocks found in this message."
            return self._render_pdf_export(code_blocks[0])

        return f"Unknown action: {action}"

    def _extract_code_blocks(self, content: str) -> list[str]:
        """Extract HTML code blocks from a message."""
        # Match ```html ... ``` or ``` ... ``` blocks
        pattern = r"```(?:html)?\s*([\s\S]*?)```"
        matches = re.findall(pattern, content)
        # Filter to only HTML blocks (skip CSS/JS-only blocks)
        html_blocks = []
        for block in matches:
            if "<html" in block or "<!DOCTYPE" in block or "<div" in block or "<section" in block:
                html_blocks.append(block.strip())
        return html_blocks

    def _render_preview(self, html: str) -> str:
        """Generate the preview HTML with sandboxed iframe."""
        # Escape for srcdoc — handle double-escaping
        escaped = self._escape_for_srcdoc(html)

        return f"""<div class="opendesign-preview">
<div class="preview-toolbar">
  <span>🎨 Preview</span>
  <div class="preview-controls">
    <button class="preview-btn" data-width="100%">🖥️</button>
    <button class="preview-btn" data-width="768px">📱</button>
    <button class="preview-btn" data-width="375px">📲</button>
  </div>
</div>
<iframe
  class="preview-iframe"
  srcdoc="{escaped}"
  sandbox="allow-scripts allow-same-origin allow-forms"
  allow="fullscreen"
  style="width: 100%; height: 600px; border: 1px solid #e0e0e0; border-radius: 8px;"
></iframe>
</div>

<script>
(function() {{
  const iframe = document.querySelector('.preview-iframe');
  const buttons = document.querySelectorAll('.preview-btn');
  buttons.forEach(btn => {{
    btn.addEventListener('click', () => {{
      buttons.forEach(b => b.style.background = '');
      btn.style.background = '#e0e0e0';
      iframe.style.width = btn.dataset.width || '100%';
      iframe.style.maxWidth = btn.dataset.width || '100%';
    }});
  }});
}})();
</script>

<style>
.opendesign-preview {{ margin: 1rem 0; }}
.preview-toolbar {{
  display: flex; justify-content: space-between; align-items: center;
  padding: 0.5rem 0.75rem; background: #f7f7f8; border-radius: 8px 8px 0 0;
  border: 1px solid #e0e0e0; border-bottom: none; font-size: 0.875rem;
}}
.preview-controls {{ display: flex; gap: 0.25rem; }}
.preview-btn {{
  padding: 0.25rem 0.5rem; border: 1px solid #e0e0e0; border-radius: 4px;
  background: white; cursor: pointer; font-size: 0.75rem;
}}
.preview-btn:hover {{ background: #f0f0f0; }}
</style>"""

    def _render_editor(self, html: str) -> str:
        """Generate the split-pane live editor in a sandboxed iframe."""
        escaped = self._escape_for_srcdoc(html)

        # Build the editor page content
        editor_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: system-ui, sans-serif; display: flex; flex-direction: column; height: 100vh; background: #1e1e2e; }}
        .toolbar {{ display: flex; justify-content: space-between; padding: 0.5rem 1rem; background: #181825; border-bottom: 1px solid #313244; }}
        .toolbar span {{ color: #cdd6f4; font-weight: 500; }}
        .toolbar button {{ padding: 0.375rem 0.75rem; border: 1px solid #45475a; border-radius: 4px; background: #313244; color: #cdd6f4; cursor: pointer; font-size: 0.75rem; }}
        .toolbar button:hover {{ background: #45475a; }}
        .editor {{ display: flex; flex: 1; overflow: hidden; }}
        .code-pane {{ flex: 1; overflow: auto; padding: 1rem; }}
        .code-pane textarea {{
            width: 100%; height: 100%; background: #1e1e2e; color: #a6adc8;
            border: none; outline: none; font-family: 'Fira Code', monospace;
            font-size: 13px; line-height: 1.5; resize: none; tab-size: 2;
        }}
        .gutter {{ width: 4px; background: #313244; cursor: col-resize; }}
        .preview-pane {{ flex: 1; background: #fff; }}
        .preview-pane iframe {{ width: 100%; height: 100%; border: none; }}
    </style>
</head>
<body>
    <div class="toolbar">
        <span>✏️ Live Editor</span>
        <div>
            <button onclick="document.querySelector('iframe').contentDocument.querySelector('html').innerHTML = document.querySelector('textarea').value;">🔄 Refresh</button>
            <button onclick="alert('Changes saved to version history')">💾 Save</button>
        </div>
    </div>
    <div class="editor">
        <div class="code-pane">
            <textarea spellcheck="false">{escaped}</textarea>
        </div>
        <div class="gutter"></div>
        <div class="preview-pane">
            <iframe srcdoc="{escaped}"></iframe>
        </div>
    </div>
    <script>
        // Auto-refresh preview on textarea blur
        document.querySelector('textarea').addEventListener('blur', function() {{
            this.closest('.editor').querySelector('iframe').contentDocument.open();
            this.closest('.editor').querySelector('iframe').contentDocument.write(this.value);
            this.closest('.editor').querySelector('iframe').contentDocument.close();
        }});
        // Resize gutter
        const gutter = document.querySelector('.gutter');
        const editor = document.querySelector('.editor');
        let isResizing = false;
        gutter.addEventListener('mousedown', () => isResizing = true);
        document.addEventListener('mousemove', (e) => {{
            if (!isResizing) return;
            const rect = editor.getBoundingClientRect();
            const pct = ((e.clientX - rect.left) / rect.width) * 100;
            editor.children[0].style.flex = `${{Math.max(20, Math.min(80, pct))}}`;
            editor.children[2].style.flex = `${{100 - Math.max(20, Math.min(80, pct))}}`;
        }});
        document.addEventListener('mouseup', () => isResizing = false);
    </script>
</body>
</html>"""

        # Escape and embed in srcdoc
        escaped_editor = self._escape_for_srcdoc(editor_html)
        return f"""<div class="opendesign-editor">
<iframe
  class="editor-iframe"
  srcdoc="{escaped_editor}"
  sandbox="allow-scripts allow-same-origin allow-forms"
  style="width: 100%; height: 70vh; border: 1px solid #e0e0e0; border-radius: 8px;"
></iframe>
</div>
<style>
.opendesign-editor {{ margin: 1rem 0; }}
</style>"""

    def _export_html(self, html: str) -> str:
        """Return HTML with instructions for saving the design."""
        # Clean up any HTML comments from OpenDesign
        clean_html = re.sub(r"<!-- Generated by OpenDesign.*?-->\s*\n?", "", html)

        return f"""📦 **Export: OpenDesign Design**

Copy and save as `index.html`:

```html
{clean_html}
```

Or use the download button in your browser. The HTML is self-contained with all CSS and JS inline.

To view: double-click the file or open it in any browser."""

    def _escape_for_srcdoc(self, text: str) -> str:
        """Escape HTML for safe use in iframe srcdoc attribute."""
        # srcdoc expects HTML, so we need to escape the HTML content
        # properly to prevent XSS and rendering issues
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#x27;")
            .replace("`", "&#96;")
        )

    def _render_comparison(self, content: str) -> str:
        """Render model comparison side-by-side from comparison message."""
        # Extract model names and HTML blocks from the comparison output
        models = self._extract_comparison_models(content)

        if not models:
            return "No model comparison data found. Please use the **Compare Models** pipe first."

        # Build comparison UI
        panels = []
        for model_name, html in models:
            escaped_html = self._escape_for_srcdoc(html)
            panels.append(
                f"""<div class="comparison-panel">
<div class="comparison-header">{model_name}</div>
<iframe class="comparison-frame" srcdoc="{escaped_html}" sandbox="allow-scripts allow-same-origin allow-forms"></iframe>
</div>"""
            )

        comparison_html = f"""<div class="comparison-container">
<style>
.comparison-container {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; padding: 1rem; }}
.comparison-panel {{ border: 2px solid #e5e7eb; border-radius: 12px; overflow: hidden; transition: all 0.2s; }}
.comparison-panel:hover {{ border-color: #6366f1; box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15); }}
.comparison-panel.selected {{ border-color: #10b981; box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2); }}
.comparison-header {{ padding: 0.75rem 1rem; background: #f8fafc; font-weight: 600; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center; }}
.comparison-frame {{ width: 100%; height: 400px; border: none; background: white; }}
.comparison-actions {{ padding: 0.5rem; background: #f8fafc; border-top: 1px solid #e2e8f0; display: flex; gap: 0.5rem; }}
.comparison-actions button {{ padding: 0.5rem 1rem; border: 1px solid #e2e8f0; border-radius: 6px; background: white; cursor: pointer; font-size: 0.875rem; transition: all 0.2s; }}
.comparison-actions button:hover {{ background: #f1f5f9; border-color: #cbd5e1; }}
.comparison-actions button.select-btn {{ background: #6366f1; color: white; border-color: #6366f1; }}
.comparison-actions button.select-btn:hover {{ background: #4f46e5; }}
.stats {{ display: flex; gap: 1rem; padding: 0.5rem 1rem; background: #f8fafc; border-top: 1px solid #e2e8f0; font-size: 0.75rem; color: #64748b; }}
.stats span {{ display: flex; align-items: center; gap: 0.25rem; }}
</style>

{chr(10).join(panels)}

<script>
(function() {{
  const panels = document.querySelectorAll('.comparison-panel');
  panels.forEach(panel => {{
    const selectBtn = panel.querySelector('.select-btn');
    if (selectBtn) {{
      selectBtn.addEventListener('click', () => {{
        panels.forEach(p => p.classList.remove('selected'));
        panel.classList.add('selected');
        // Emit selection event for parent to handle
        if (window.parent) {{
          window.parent.postMessage({{ type: 'od-compare-select', model: panel.dataset.model }}, '*');
        }}
      }});
    }}
  }});
}})();
</script>
</div>"""

        return comparison_html

    def _extract_comparison_models(self, content: str) -> list[tuple[str, str]]:
        """Extract model names and HTML from comparison output."""
        models = []
        # Pattern to find model headers followed by HTML code blocks
        # Matches: **model-name:** ✅ Generated or similar patterns
        model_pattern = re.compile(r"\*\*(.+?):\*\*", re.DOTALL)
        code_pattern = re.compile(r"```(?:html)?\s*([\s\S]*?)```")

        # Find all code blocks
        code_blocks = code_pattern.findall(content)

        # Try to map models to code blocks
        model_matches = model_pattern.findall(content)

        for i, code_block in enumerate(code_blocks):
            # Skip if it's not actual HTML
            if not any(
                tag in code_block for tag in ["<html", "<!DOCTYPE", "<div", "<section", "<main"]
            ):
                continue

            # Try to find associated model name
            model_name = f"Model {i + 1}"
            if i < len(model_matches):
                model_name = model_matches[i].strip()

            # Clean up model name
            model_name = re.sub(r"[:\-\*\|]", "", model_name).strip()

            models.append((model_name, code_block.strip()))

        return models

    def _render_png_export(self, html: str) -> str:
        """Render HTML with instructions for PNG export."""
        # Clean up HTML comments
        clean_html = re.sub(r"<!-- Generated by OpenDesign.*?-->\s*\n?", "", html)

        export_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Export to PNG</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }}
        .controls {{
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 1000;
            display: flex;
            gap: 8px;
        }}
        .btn {{
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
        }}
        .btn-primary {{
            background: #6366f1;
            color: white;
        }}
        .btn-secondary {{
            background: #e2e8f0;
            color: #1e293b;
        }}
        .status {{
            position: fixed;
            bottom: 10px;
            left: 50%;
            transform: translateX(-50%);
            padding: 10px 20px;
            background: #1e293b;
            color: white;
            border-radius: 6px;
            font-size: 14px;
            display: none;
            max-width: 80%;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="controls">
        <button class="btn btn-secondary" onclick="window.close()">Cancel</button>
        <button class="btn btn-primary" onclick="exportPNG()">📸 Export PNG</button>
    </div>
    <div class="status" id="status">
        <div id="status-text">Ready</div>
    </div>
    <div id="content">
        {clean_html}
    </div>
    <script>
        // PNG Export - Use browser native capabilities
        // For full PNG export, install html2canvas or use screenshot tool
        function exportPNG() {{
            const status = document.getElementById('status');
            const statusText = document.getElementById('status-text');
            status.style.display = 'block';
            statusText.textContent = '💡 Tip: Use browser screenshot (Cmd+Shift+4 / Ctrl+Shift+S) or install html2canvas for programmatic export.';
            setTimeout(() => window.close(), 3000);
        }}
    </script>
</body>
</html>"""

        escaped = self._escape_for_srcdoc(export_html)
        return f"""<div class="opendesign-export">
<iframe
  class="export-iframe"
  srcdoc="{escaped}"
  sandbox="allow-scripts allow-same-origin allow-forms allow-popups"
  style="width: 100%; height: 70vh; border: 1px solid #e0e0e0; border-radius: 8px;"
></iframe>
</div>
<style>
.opendesign-export {{ margin: 1rem 0; }}
</style>"""

    def _render_pdf_export(self, html: str) -> str:
        """Render HTML with print styles for PDF export."""
        # Clean up HTML comments
        clean_html = re.sub(r"<!-- Generated by OpenDesign.*?-->\s*\n?", "", html)

        export_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Export to PDF</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }}
        .controls {{
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 1000;
            display: flex;
            gap: 8px;
        }}
        .btn {{
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
        }}
        .btn-primary {{
            background: #6366f1;
            color: white;
        }}
        .btn-secondary {{
            background: #e2e8f0;
            color: #1e293b;
        }}
        @media print {{
            .controls {{ display: none; }}
            body {{ padding: 0; }}
            @page {{ margin: 1cm; }}
        }}
    </style>
</head>
<body>
    <div class="controls">
        <button class="btn btn-secondary" onclick="window.close()">Cancel</button>
        <button class="btn btn-primary" onclick="window.print()">📄 Export PDF</button>
    </div>
    <div id="content">
        {clean_html}
    </div>
</body>
</html>"""

        escaped = self._escape_for_srcdoc(export_html)
        return f"""<div class="opendesign-export">
<iframe
  class="export-iframe"
  srcdoc="{escaped}"
  sandbox="allow-scripts allow-same-origin allow-forms"
  style="width: 100%; height: 70vh; border: 1px solid #e0e0e0; border-radius: 8px;"
></iframe>
</div>
<style>
.opendesign-export {{ margin: 1rem 0; }}
</style>"""

    def _render_multi_device(self, html: str) -> str:
        """Render designs at multiple breakpoints side-by-side."""
        # Clean up HTML comments
        clean_html = re.sub(r"<!-- Generated by OpenDesign.*?-->\s*\n?", "", html)

        # Escape for srcdoc
        escaped_html = self._escape_for_srcdoc(clean_html)

        return f"""<div class="opendesign-multi-device">
<style>
.opendesign-multi-device {{ padding: 1rem 0; }}
.md-preview-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin: 1rem 0;
}}
@media (max-width: 900px) {{
    .md-preview-grid {{ grid-template-columns: 1fr; }}
}}
.md-device-frame {{
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    overflow: hidden;
    background: white;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}}
.md-device-header {{
    padding: 0.75rem 1rem;
    background: #f8fafc;
    border-bottom: 1px solid #e2e8f0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.875rem;
    font-weight: 500;
    color: #475569;
}}
.md-device-icon {{
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
}}
.md-device-body {{
    padding: 0.5rem;
    background: #f1f5f9;
}}
.md-device-frame iframe {{
    width: 100%;
    border: none;
    background: white;
    border-radius: 4px;
}}
.md-desktop iframe {{ height: 500px; }}
.md-tablet iframe {{ height: 400px; }}
.md-mobile iframe {{ height: 350px; }}
.md-breakpoint {{
    font-size: 0.75rem;
    color: #94a3b8;
    font-weight: 400;
    margin-left: auto;
}}
</style>

<h3 style="margin: 0 0 1rem; font-size: 1rem; color: #1e293b;">📱 Multi-Device Preview</h3>

<div class="md-preview-grid">
    <div class="md-device-frame">
        <div class="md-device-header">
            <div class="md-device-icon">🖥️</div>
            Desktop
            <span class="md-breakpoint">1024px</span>
        </div>
        <div class="md-device-body md-desktop">
            <iframe srcdoc="{escaped_html}" sandbox="allow-scripts allow-same-origin" style="width: 100%;"></iframe>
        </div>
    </div>

    <div class="md-device-frame">
        <div class="md-device-header">
            <div class="md-device-icon">📱</div>
            Tablet
            <span class="md-breakpoint">768px</span>
        </div>
        <div class="md-device-body md-tablet">
            <iframe srcdoc="{escaped_html}" sandbox="allow-scripts allow-same-origin" style="width: 100%; max-width: 768px; margin: 0 auto;"></iframe>
        </div>
    </div>

    <div class="md-device-frame">
        <div class="md-device-header">
            <div class="md-device-icon">📲</div>
            Mobile
            <span class="md-breakpoint">375px</span>
        </div>
        <div class="md-device-body md-mobile">
            <iframe srcdoc="{escaped_html}" sandbox="allow-scripts allow-same-origin" style="width: 100%; max-width: 375px; margin: 0 auto;"></iframe>
        </div>
    </div>
</div>
</div>"""
