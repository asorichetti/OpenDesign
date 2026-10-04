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
            return self._export_zip(code_blocks[0])

        return f"Unknown action: {action}"

    def _extract_code_blocks(self, content: str) -> list[str]:
        """Extract HTML code blocks from a message."""
        pattern = r"```(?:html)?\s*([\s\S]*?)```"
        matches = re.findall(pattern, content)
        # Filter to only HTML blocks (skip CSS/JS-only blocks)
        html_blocks = []
        for block in matches:
            if "<html" in block or "<!DOCTYPE" in block or "<div" in block:
                html_blocks.append(block.strip())
        return html_blocks

    def _render_preview(self, html: str) -> str:
        """Generate the preview HTML with sandboxed iframe."""
        # Escape for srcdoc
        escaped = html.replace("&", "&amp;").replace('"', "&quot;")
        escaped = escaped.replace("<", "&lt;").replace(">", "&gt;")

        return f"""<div class="opendesign-preview">
<div class="preview-toolbar">
  <span>🎨 Preview</span>
  <div class="preview-controls">
    <button class="preview-btn" data-mode="desktop">🖥️ Desktop</button>
    <button class="preview-btn" data-mode="tablet">📱 Tablet</button>
    <button class="preview-btn" data-mode="mobile">📲 Mobile</button>
    <button class="preview-btn" data-mode="fullscreen">⛶ Full</button>
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

<style>
.opendesign-preview {{
  margin: 1rem 0;
}}
.preview-toolbar {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0.75rem;
  background: #f7f7f8;
  border-radius: 8px 8px 0 0;
  border: 1px solid #e0e0e0;
  border-bottom: none;
  font-size: 0.875rem;
  font-weight: 500;
}}
.preview-controls {{
  display: flex;
  gap: 0.25rem;
}}
.preview-btn {{
  padding: 0.25rem 0.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  font-size: 0.75rem;
}}
.preview-btn:hover {{
  background: #f0f0f0;
}}
.preview-iframe {{
  border-radius: 0 0 8px 8px;
}}
</style>"""

    def _export_zip(self, html: str) -> str:
        """Return HTML for download (in production, return a Blob URL)."""
        return f"""Download this design:

```html
{html}
```

To save as a file, copy the code above and save it as `index.html`."""
