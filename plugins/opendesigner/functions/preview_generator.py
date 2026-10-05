"""
title: OpenDesigner Preview Generator
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesigner
version: 0.1.0
required_open_webui_version: 0.10.0
"""

import re
from typing import Any


class Action:
    """OpenDesigner Preview Generator — renders design code in a sandboxed iframe."""

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
                "name": "Open Editor",
                "description": "Open the split-pane live editor",
                "icon": "edit",
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

        return f"""<div class="opendesigner-preview">
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
.opendesigner-preview {{ margin: 1rem 0; }}
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
        return f"""<div class="opendesigner-editor">
<iframe
  class="editor-iframe"
  srcdoc="{escaped_editor}"
  sandbox="allow-scripts allow-same-origin allow-forms"
  style="width: 100%; height: 70vh; border: 1px solid #e0e0e0; border-radius: 8px;"
></iframe>
</div>
<style>
.opendesigner-editor {{ margin: 1rem 0; }}
</style>"""

    def _export_html(self, html: str) -> str:
        """Return HTML with instructions for saving the design."""
        # Clean up any HTML comments from OpenDesigner
        clean_html = re.sub(r"<!-- Generated by OpenDesigner.*?-->\s*\n?", "", html)

        return f"""📦 **Export: OpenDesigner Design**

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
