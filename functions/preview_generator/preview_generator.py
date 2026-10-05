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
            {
                "name": "AI Prompt Generator",
                "description": "Generate a prompt to recreate this design in any AI model",
                "icon": "message-circle",
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

        elif action == "AI Prompt Generator":
            code_blocks = self._extract_code_blocks(content)
            if not code_blocks:
                return "No HTML code blocks found in this message."
            return self._render_ai_prompt(code_blocks[0])

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
<style>
.opendesigner-preview {{
    padding: 1rem 0;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}}
.preview-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
    padding: 0 0.5rem;
}}
.preview-title {{
    font-size: 1rem;
    font-weight: 600;
    color: #1e293b;
}}
.preview-frame {{
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    overflow: hidden;
    background: white;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}}
.preview-frame iframe {{
    width: 100%;
    height: 70vh;
    border: none;
}}
</style>

<div class="preview-header">
    <span class="preview-title">🎨 Design Preview</span>
</div>
<div class="preview-frame">
    <iframe srcdoc="{escaped}" sandbox="allow-scripts allow-same-origin allow-forms" style="width: 100%; height: 70vh; border: 1px solid #e0e0e0; border-radius: 8px;"></iframe>
</div>
</div>"""

    def _render_editor(self, html: str) -> str:
        """Generate the editor HTML with split pane."""
        escaped = self._escape_for_srcdoc(html)

        return f"""<div class="opendesigner-editor">
<style>
.opendesigner-editor {{
    display: flex;
    height: 80vh;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    overflow: hidden;
    background: white;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}}
.editor-pane {{
    flex: 1;
    display: flex;
    flex-direction: column;
}}
.editor-header {{
    padding: 0.75rem 1rem;
    background: #f8fafc;
    border-bottom: 1px solid #e2e8f0;
    font-size: 0.875rem;
    font-weight: 500;
    color: #475569;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}
.editor-content {{
    flex: 1;
    overflow: auto;
}}
.editor-content iframe {{
    width: 100%;
    height: 100%;
    border: none;
}}
.editor-gutter {{
    width: 4px;
    background: #e2e8f0;
    cursor: col-resize;
    transition: background 0.2s;
}}
.editor-gutter:hover {{
    background: #6366f1;
}}
</style>

<div class="editor-pane">
    <div class="editor-header">📝 HTML Source</div>
    <div class="editor-content">
        <pre style="padding: 1rem; font-family: 'JetBrains Mono', monospace; font-size: 0.8125rem; line-height: 1.6; color: #334155; white-space: pre-wrap;">{html}</pre>
    </div>
</div>
<div class="editor-gutter"></div>
<div class="editor-pane">
    <div class="editor-header">👁️ Live Preview</div>
    <div class="editor-content">
        <iframe srcdoc="{escaped}" sandbox="allow-scripts allow-same-origin allow-forms"></iframe>
    </div>
</div>
</div>"""

    def _render_comparison(self, content: str) -> str:
        """Render model comparison view."""
        # Extract models from comparison content
        models = self._extract_comparison_models(content)
        escaped_htmls = []

        for model, html in models:
            escaped = self._escape_for_srcdoc(html)
            escaped_htmls.append((model, escaped))

        return f"""<div class="opendesigner-comparison">
<style>
.opendesigner-comparison {{
    padding: 1rem 0;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}}
.comparison-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1rem;
    margin: 1rem 0;
}}
.comparison-card {{
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    overflow: hidden;
    background: white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}}
.comparison-header {{
    padding: 0.75rem 1rem;
    background: #f8fafc;
    border-bottom: 1px solid #e2e8f0;
    font-size: 0.875rem;
    font-weight: 600;
    color: #1e293b;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}
.comparison-body {{
    padding: 0.5rem;
    background: #f1f5f9;
}}
.comparison-body iframe {{
    width: 100%;
    height: 400px;
    border: none;
    background: white;
    border-radius: 4px;
}}
</style>

<h3 style="margin: 0 0 1rem; font-size: 1rem; color: #1e293b;">🔄 Model Comparison</h3>

<div class="comparison-grid">
    {
            "".join(
                f'''<div class="comparison-card">
        <div class="comparison-header">🤖 {model}</div>
        <div class="comparison-body">
            <iframe srcdoc="{escaped}" sandbox="allow-scripts allow-same-origin allow-forms"></iframe>
        </div>
    </div>'''
                for model, escaped in escaped_htmls
            )
        }
</div>
</div>"""

    def _render_png_export(self, html: str) -> str:
        """Render PNG export UI with instruction overlay."""
        escaped = self._escape_for_srcdoc(html)

        return f"""<div class="opendesigner-png-export">
<style>
.opendesigner-png-export {{
    padding: 1.5rem 0;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    text-align: center;
}}
.export-container {{
    max-width: 900px;
    margin: 0 auto;
    background: white;
    border-radius: 16px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    overflow: hidden;
}}
.export-header {{
    padding: 1.5rem 2rem;
    background: #f8fafc;
    border-bottom: 1px solid #e2e8f0;
}}
.export-title {{
    font-size: 1.25rem;
    font-weight: 600;
    color: #1e293b;
    margin: 0 0 0.5rem;
}}
.export-instructions {{
    color: #64748b;
    font-size: 0.875rem;
    margin: 0;
}}
.export-preview {{
    padding: 2rem;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 400px;
    background: #f1f5f9;
}}
.export-preview iframe {{
    width: 100%;
    max-width: 800px;
    height: 500px;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    background: white;
}}
.export-footer {{
    padding: 1rem 2rem;
    background: #f8fafc;
    border-top: 1px solid #e2e8f0;
    display: flex;
    justify-content: center;
    gap: 1rem;
}}
.export-btn {{
    padding: 0.75rem 1.5rem;
    background: #6366f1;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}}
.export-btn:hover {{
    background: #4f46e5;
    transform: translateY(-1px);
}}
.export-btn-secondary {{
    padding: 0.75rem 1.5rem;
    background: white;
    color: #6366f1;
    border: 1px solid #6366f1;
    border-radius: 8px;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}}
.export-btn-secondary:hover {{
    background: #f0f0ff;
}}
</style>

<div class="export-container">
    <div class="export-header">
        <h3 class="export-title">📤 Export to PNG</h3>
        <p class="export-instructions">Use browser's screenshot tool: Right-click the preview → "Take screenshot" (Firefox) or use a tool like Lightshot</p>
    </div>
    <div class="export-preview">
        <iframe srcdoc="{escaped}" sandbox="allow-scripts allow-same-origin"></iframe>
    </div>
    <div class="export-footer">
        <button class="export-btn" onclick="window.print()">📋 Copy to Clipboard</button>
        <button class="export-btn-secondary" onclick="location.reload()">↻ Refresh</button>
    </div>
</div>
</div>"""

    def _render_pdf_export(self, html: str) -> str:
        """Render PDF export UI with print optimization."""
        escaped = self._escape_for_srcdoc(html)

        return f"""<div class="opendesigner-pdf-export">
<style>
.opendesigner-pdf-export {{
    padding: 1.5rem 0;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    text-align: center;
}}
.pdf-container {{
    max-width: 900px;
    margin: 0 auto;
    background: white;
    border-radius: 16px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    overflow: hidden;
}}
.pdf-header {{
    padding: 1.5rem 2rem;
    background: #f8fafc;
    border-bottom: 1px solid #e2e8f0;
}}
.pdf-title {{
    font-size: 1.25rem;
    font-weight: 600;
    color: #1e293b;
    margin: 0 0 0.5rem;
}}
.pdf-instructions {{
    color: #64748b;
    font-size: 0.875rem;
    margin: 0;
}}
.pdf-preview {{
    padding: 2rem;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 400px;
    background: #f1f5f9;
}}
.pdf-preview iframe {{
    width: 100%;
    max-width: 800px;
    height: 500px;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    background: white;
}}
.pdf-footer {{
    padding: 1rem 2rem;
    background: #f8fafc;
    border-top: 1px solid #e2e8f0;
    display: flex;
    justify-content: center;
    gap: 1rem;
}}
.pdf-btn {{
    padding: 0.75rem 1.5rem;
    background: #6366f1;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}}
.pdf-btn:hover {{
    background: #4f46e5;
    transform: translateY(-1px);
}}
.pdf-btn-secondary {{
    padding: 0.75rem 1.5rem;
    background: white;
    color: #6366f1;
    border: 1px solid #6366f1;
    border-radius: 8px;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}}
.pdf-btn-secondary:hover {{
    background: #f0f0ff;
}}
@media print {{
    .opendesigner-pdf-export > :not(.print-content) {{ display: none; }}
    .print-content iframe {{ width: 100%; height: auto; border: none; }}
}}
</style>

<div class="pdf-container">
    <div class="pdf-header">
        <h3 class="pdf-title">📄 Export to PDF</h3>
        <p class="pdf-instructions">Click "Print" and select "Save as PDF" in your browser's print dialog</p>
    </div>
    <div class="pdf-preview">
        <iframe srcdoc="{escaped}" sandbox="allow-scripts allow-same-origin"></iframe>
    </div>
    <div class="pdf-footer">
        <button class="pdf-btn" onclick="window.print()">🖨️ Print / Save as PDF</button>
        <button class="pdf-btn-secondary" onclick="location.reload()">↻ Refresh</button>
    </div>
</div>
</div>"""

    def _render_multi_device(self, html: str) -> str:
        """Render designs at multiple breakpoints side-by-side."""
        # Clean up HTML comments
        clean_html = re.sub(r"<!-- Generated by OpenDesigner.*?-->\s*\n?", "", html)

        # Escape for srcdoc
        escaped_html = self._escape_for_srcdoc(clean_html)

        return f"""<div class="opendesigner-multi-device">
<style>
.opendesigner-multi-device {{ padding: 1rem 0; }}
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
            <iframe srcdoc="{escaped_html}" sandbox="allow-scripts allow-same-origin" style="width: 75%;"></iframe>
        </div>
    </div>

    <div class="md-device-frame">
        <div class="md-device-header">
            <div class="md-device-icon">📲</div>
            Mobile
            <span class="md-breakpoint">375px</span>
        </div>
        <div class="md-device-body md-mobile">
            <iframe srcdoc="{escaped_html}" sandbox="allow-scripts allow-same-origin" style="width: 100%;"></iframe>
        </div>
    </div>
</div>
</div>"""

    def _render_ai_prompt(self, html: str) -> str:
        """Generate an AI prompt to recreate this design in any model."""
        # Analyze HTML to extract key design features
        analysis = self._analyze_html_for_prompt(html)

        return f"""<div class="ai-prompt-generator" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
<style>
.ai-prompt-generator {{
    max-width: 800px;
    margin: 0 auto;
}}
.ai-prompt-header {{
    text-align: center;
    margin-bottom: 2rem;
}}
.ai-prompt-header h3 {{
    font-size: 1.5rem;
    font-weight: 700;
    color: #1e293b;
    margin: 0 0 0.5rem;
}}
.ai-prompt-header p {{
    color: #64748b;
    margin: 0;
}}
.ai-prompt-card {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}}
.ai-prompt-label {{
    font-size: 0.875rem;
    font-weight: 600;
    color: #475569;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}
.ai-prompt-text {{
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 1rem;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    font-size: 0.8125rem;
    line-height: 1.7;
    color: #334155;
    white-space: pre-wrap;
    word-wrap: break-word;
    max-height: 400px;
    overflow-y: auto;
}}
.ai-model-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 0.75rem;
    margin-top: 1rem;
}}
.ai-model-card {{
    padding: 1rem;
    background: white;
    border: 2px solid #e2e8f0;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: center;
}}
.ai-model-card:hover {{
    border-color: #6366f1;
    background: #f0f0ff;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15);
}}
.ai-model-icon {{
    font-size: 1.75rem;
    margin-bottom: 0.5rem;
}}
.ai-model-name {{
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 0.25rem;
}}
.ai-model-desc {{
    font-size: 0.75rem;
    color: #64748b;
}}
.copy-btn {{
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.625rem 1.25rem;
    background: #6366f1;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 0.875rem;
    font-weight: 600;
    cursor: pointer;
    margin-top: 1rem;
    transition: all 0.2s;
}}
.copy-btn:hover {{
    background: #4f46e5;
    transform: translateY(-1px);
}}
.design-tags {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.75rem;
}}
.tag {{
    padding: 0.375rem 0.75rem;
    background: #ede9fe;
    color: #6366f1;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 500;
}}
</style>

<div class="ai-prompt-header">
    <h3>🤖 Generate AI Prompt</h3>
    <p>Create a prompt to recreate this design in any AI model</p>
</div>

<div class="ai-prompt-card">
    <div class="ai-prompt-label">
        📋 Analysis Summary
    </div>
    <div class="design-tags">
        {self._generate_tags(analysis)}
    </div>
</div>

<div class="ai-prompt-card">
    <div class="ai-prompt-label">
        ✨ Generated Prompt
    </div>
    <div class="ai-prompt-text" id="generated-prompt">{self._build_prompt_text(analysis)}</div>
    <button class="copy-btn" onclick="navigator.clipboard.writeText(document.getElementById('generated-prompt').textContent).then(() => {{ this.textContent = '✅ Copied!'; setTimeout(() => {{ this.textContent = '📋 Copy Prompt'; }}, 2000); }})">
        📋 Copy Prompt
    </button>
</div>

<div class="ai-prompt-card">
    <div class="ai-prompt-label">
        🚀 Quick Start — Choose Your Model
    </div>
    <div class="ai-model-grid">
        <div class="ai-model-card" onclick="alert('Copy the prompt above and paste into ChatGPT')">
            <div class="ai-model-icon">🧠</div>
            <div class="ai-model-name">ChatGPT</div>
            <div class="ai-model-desc">OpenAI</div>
        </div>
        <div class="ai-model-card" onclick="alert('Copy the prompt above and paste into Claude')">
            <div class="ai-model-icon">🟣</div>
            <div class="ai-model-name">Claude</div>
            <div class="ai-model-desc">Anthropic</div>
        </div>
        <div class="ai-model-card" onclick="alert('Copy the prompt above and paste into your local Ollama instance')">
            <div class="ai-model-icon">🦙</div>
            <div class="ai-model-name">Ollama</div>
            <div class="ai-model-desc">Local</div>
        </div>
        <div class="ai-model-card" onclick="alert('Copy the prompt above and paste into Gemini')">
            <div class="ai-model-icon">🌈</div>
            <div class="ai-model-name">Gemini</div>
            <div class="ai-model-desc">Google</div>
        </div>
        <div class="ai-model-card" onclick="alert('Copy the prompt above and paste into your Open WebUI instance')">
            <div class="ai-model-icon">💬</div>
            <div class="ai-model-name">Open WebUI</div>
            <div class="ai-model-desc">Self-hosted</div>
        </div>
        <div class="ai-model-card" onclick="alert('Copy the prompt above and paste into your preferred AI')">
            <div class="ai-model-icon">🔮</div>
            <div class="ai-model-name">Any AI</div>
            <div class="ai-model-desc">Universal</div>
        </div>
    </div>
</div>
</div>"""

    def _analyze_html_for_prompt(self, html: str) -> dict:
        """Analyze HTML to extract key design features for prompt generation."""
        analysis = {
            "type": "unknown",
            "components": [],
            "layout": "unknown",
            "has_navigation": False,
            "has_hero": False,
            "has_footer": False,
            "is_responsive": False,
            "has_animations": False,
            "has_forms": False,
            "has_images": False,
            "has_tables": False,
            "has_carousel": False,
            "has_accordion": False,
            "has_tabs": False,
            "has_modal": False,
            "has_video": False,
            "style_category": "modern",
            "complexity": "medium",
        }

        # Detect page type
        if "<nav" in html or 'class="nav' in html:
            analysis["has_navigation"] = True
        if "<header" in html or 'class="hero' in html or 'class="hero-' in html:
            analysis["has_hero"] = True
        if "<footer" in html or 'class="footer' in html:
            analysis["has_footer"] = True
        if "media" in html or "responsive" in html or "viewport" in html:
            analysis["is_responsive"] = True
        if "animation" in html.lower() or "@keyframes" in html or "transition" in html:
            analysis["has_animations"] = True
        if "<form" in html or "<input" in html:
            analysis["has_forms"] = True
        if "<img" in html or "background" in html.lower():
            analysis["has_images"] = True
        if "<table" in html:
            analysis["has_tables"] = True
        if "<carousel" in html.lower() or "carousel" in html.lower():
            analysis["has_carousel"] = True
        if "<accordion" in html.lower() or "accordion" in html.lower():
            analysis["has_accordion"] = True
        if "<tabs" in html.lower() or "tabs" in html.lower():
            analysis["has_tabs"] = True
        if "<modal" in html.lower() or "modal" in html.lower():
            analysis["has_modal"] = True
        if "<video" in html:
            analysis["has_video"] = True

        # Detect components
        component_patterns = {
            "button": "<button",
            "card": 'class="card"',
            "form": "<form",
            "navigation": "<nav",
            "header": "<header",
            "footer": "<footer",
            "hero": 'class="hero"',
            "grid": "display: grid",
            "flex": "display: flex",
            "section": "<section",
            "container": 'class="container"',
        }
        for comp, pattern in component_patterns.items():
            if pattern in html:
                analysis["components"].append(comp)

        # Detect page type
        type_keywords = {
            "landing page": ["landing", "hero", "cta", "call to action"],
            "dashboard": ["dashboard", "analytics", "chart", "widget"],
            "component": ["component", "widget", "module"],
            "presentation": ["slide", "presentation", "fullscreen"],
            "email": ["email", "newsletter", "transactional"],
            "social": ["og:image", "og card", "social media"],
            "portfolio": ["portfolio", "gallery", "showcase"],
            "pricing": ["pricing", "plan", "subscription"],
        }
        for page_type, keywords in type_keywords.items():
            if any(kw in html.lower() for kw in keywords):
                analysis["type"] = page_type
                break

        # Detect complexity
        if len(analysis["components"]) > 8:
            analysis["complexity"] = "advanced"
        elif len(analysis["components"]) < 3:
            analysis["complexity"] = "simple"

        # Detect layout
        layout_keywords = ["grid", "flexbox", "columns", "sidebar"]
        for layout in layout_keywords:
            if layout in html.lower():
                analysis["layout"] = layout
                break

        return analysis

    def _build_prompt_text(self, analysis: dict) -> str:
        """Build a detailed prompt from the analysis."""
        type_info = analysis.get("type", "unknown")
        complexity = analysis.get("complexity", "medium")

        type_display = type_info.title() if type_info != "unknown" else "Web Page"
        components_list = ", ".join(
            f"• {c.title()}" for c in analysis.get("components", ["container", "section"])
        )
        layout_display = analysis.get("layout", "responsive grid")

        prompt_lines = [
            f"Create a {type_info} with the following specifications:",
            "",
            "## Page Type",
            type_display,
            "",
            "## Required Components",
            components_list,
            "",
            "## Layout Style",
            layout_display,
            "",
            "## Features",
        ]

        features = []
        if analysis.get("has_navigation"):
            features.append("• Navigation bar with menu items")
        if analysis.get("has_hero"):
            features.append("• Hero section with call-to-action")
        if analysis.get("has_footer"):
            features.append("• Footer with links and copyright")
        if analysis.get("has_forms"):
            features.append("• Interactive forms with validation")
        if analysis.get("has_animations"):
            features.append("• Smooth animations and transitions")
        if analysis.get("is_responsive"):
            features.append("• Fully responsive design")

        prompt_lines.extend(features if features else ["• Basic responsive layout"])

        prompt_lines.extend(
            [
                "",
                "## Design Requirements",
                "- Modern, clean aesthetic",
                f"- {complexity} complexity level",
                "- Professional typography",
                "- Cohesive color scheme",
                "- Accessible (WCAG 2.1 AA compliant)",
                "- Mobile-first responsive design",
                "",
                "## Technical Requirements",
                "- Single HTML file with inline CSS",
                "- No external dependencies",
                "- Semantic HTML5 elements",
                "- CSS custom properties for theming",
                "- Smooth transitions and micro-interactions",
                "",
                "Generate the complete, production-ready HTML code.",
            ]
        )

        return "\n".join(prompt_lines)

    def _generate_tags(self, analysis: dict) -> str:
        """Generate HTML tags for the analysis summary."""
        tags = []
        if analysis.get("type") != "unknown":
            tags.append(analysis["type"].replace(" ", "-").title())
        if analysis.get("has_navigation"):
            tags.append("Navigation")
        if analysis.get("has_hero"):
            tags.append("Hero")
        if analysis.get("has_forms"):
            tags.append("Forms")
        if analysis.get("has_animations"):
            tags.append("Animations")
        if analysis.get("is_responsive"):
            tags.append("Responsive")
        if analysis.get("has_carousel"):
            tags.append("Carousel")
        if analysis.get("has_accordion"):
            tags.append("Accordion")
        if analysis.get("has_tabs"):
            tags.append("Tabs")
        if analysis.get("has_modal"):
            tags.append("Modal")

        if not tags:
            tags = ["Standard Layout"]

        return "".join(f'<span class="tag">{tag}</span>' for tag in tags)

    def _escape_for_srcdoc(self, html: str) -> str:
        """Escape HTML for safe use in iframe srcdoc attribute."""
        # Handle common escaping needs for srcdoc
        escaped = html.replace("&", "&amp;")
        escaped = escaped.replace("<", "&lt;")
        escaped = escaped.replace(">", "&gt;")
        escaped = escaped.replace('"', "&quot;")
        escaped = escaped.replace("'", "&#x27;")
        return escaped

    def _export_html(self, html: str) -> str:
        """Generate HTML for export with download prompt."""
        return f"""<div class="opendesigner-export">
<style>
.opendesigner-export {{
    padding: 1rem 0;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    text-align: center;
}}
.export-container {{
    max-width: 800px;
    margin: 0 auto;
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    overflow: hidden;
}}
.export-header {{
    padding: 1.5rem;
    background: #f8fafc;
    border-bottom: 1px solid #e2e8f0;
}}
.export-title {{
    font-size: 1.25rem;
    font-weight: 600;
    color: #1e293b;
    margin: 0 0 0.5rem;
}}
.export-subtitle {{
    color: #64748b;
    margin: 0;
    font-size: 0.875rem;
}}
.export-content {{
    padding: 1.5rem;
}}
.export-code {{
    background: #1e293b;
    color: #e2e8f0;
    padding: 1rem;
    border-radius: 8px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    line-height: 1.6;
    overflow-x: auto;
    white-space: pre-wrap;
    word-break: break-all;
    text-align: left;
}}
.export-footer {{
    padding: 1rem 1.5rem;
    background: #f8fafc;
    border-top: 1px solid #e2e8f0;
    display: flex;
    justify-content: center;
    gap: 1rem;
}}
.export-btn {{
    padding: 0.75rem 1.5rem;
    background: #6366f1;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}}
.export-btn:hover {{
    background: #4f46e5;
}}
</style>

<div class="export-container">
    <div class="export-header">
        <h3 class="export-title">📤 HTML Export</h3>
        <p class="export-subtitle">Your design is ready to download</p>
    </div>
    <div class="export-content">
        <pre class="export-code">{html[:1000]}{"..." if len(html) > 1000 else ""}</pre>
    </div>
    <div class="export-footer">
        <button class="export-btn" onclick="navigator.clipboard.writeText(this.closest('.opendesigner-export').querySelector('.export-code').textContent)">
            📋 Copy to Clipboard
        </button>
        <a class="export-btn" href="data:text/html;charset=utf-8,{html}" download="design.html" style="text-decoration: none; display: inline-flex; align-items: center;">
            💾 Download HTML
        </a>
    </div>
</div>
</div>"""

    def _extract_comparison_models(self, content: str) -> list[tuple[str, str]]:
        """Extract model comparison data from content."""
        # Look for model comparison markers
        models = []
        # Pattern: ### Model: name\n```html\n...\n```
        pattern = r"### Model: ([\w\s-]+?)\s*\n```(?:html)?\s*([\s\S]*?)```"
        matches = re.findall(pattern, content)
        for model_name, html in matches:
            if "<html" in html or "<!DOCTYPE" in html or "<div" in html:
                models.append((model_name.strip(), html.strip()))

        # If no marked models, try to find multiple code blocks
        if not models:
            code_blocks = self._extract_code_blocks(content)
            model_names = ["Model 1", "Model 2", "Model 3"]
            for i, block in enumerate(code_blocks[:3]):
                models.append((model_names[i], block))

        return models
