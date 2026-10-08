"""
title: Design-to-Code AI
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesigner
version: 1.0.0
required_open_webui_version: 0.10.0
"""

from typing import Any


class Action:
    """Design-to-Code AI — Convert designs to production-ready code with AI."""

    def __init__(self):
        self.type = "action"

    def actions(self) -> list[dict[str, str]]:
        """Return available actions."""
        return [
            {
                "name": "Design to Code",
                "description": "Convert design to production-ready code",
                "icon": "wand",
            },
            {
                "name": "Code Inspector",
                "description": "Inspect and understand generated code",
                "icon": "search",
            },
            {
                "name": "Code Export",
                "description": "Export generated code in various formats",
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
        """Handle design-to-code action."""
        if action == "Design to Code":
            return self._render_generator(body)
        elif action == "Code Inspector":
            return self._render_inspector()
        elif action == "Code Export":
            return self._render_export()

        return f"Unknown action: {action}"

    def _render_generator(self, body: dict) -> str:
        """Render design-to-code generator."""
        return """
        <div class="design-to-code" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .design-to-code {{ max-width: 1200px; margin: 0 auto; }}
                .generator-header {{ text-align: center; margin-bottom: 2rem; }}
                .generator-header h3 {{ font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0 0 0.5rem; }}
                .generator-header p {{ color: #64748b; }}
                .input-section {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; }}
                .upload-area {{ border: 2px dashed #e2e8f0; border-radius: 12px; padding: 3rem; text-align: center; cursor: pointer; transition: all 0.2s; }}
                .upload-area:hover {{ border-color: #6366f1; background: #f8fafc; }}
                .upload-icon {{ font-size: 3rem; margin-bottom: 1rem; }}
                .upload-text {{ font-size: 1.125rem; font-weight: 600; color: #1e293b; margin-bottom: 0.5rem; }}
                .upload-hint {{ font-size: 0.875rem; color: #64748b; }}
                .framework-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-top: 1.5rem; }}
                .framework-card {{ padding: 1rem; border: 2px solid #e2e8f0; border-radius: 12px; text-align: center; cursor: pointer; transition: all 0.2s; }}
                .framework-card:hover {{ border-color: #6366f1; }}
                .framework-card.selected {{ border-color: #6366f1; background: #f8fafc; }}
                .framework-icon {{ font-size: 2rem; margin-bottom: 0.5rem; }}
                .framework-name {{ font-weight: 600; color: #1e293b; }}
                .generate-btn {{ padding: 1rem 2rem; background: #6366f1; color: white; border: none; border-radius: 12px; font-weight: 600; cursor: pointer; font-size: 1rem; margin-top: 1.5rem; width: 100%; }}
                .code-output {{ background: #1e293b; color: #e2e8f0; border-radius: 12px; padding: 1.5rem; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; line-height: 1.6; overflow-x: auto; }}
            </style>

            <div class="design-to-code">
                <div class="generator-header">
                    <h3>🤖 Design-to-Code AI</h3>
                    <p>Upload a design or screenshot and get production-ready code</p>
                </div>

                <div class="input-section">
                    <div class="upload-area" onclick="document.getElementById('file-input').click()">
                        <input type="file" id="file-input" style="display: none;" accept="image/*">
                        <div class="upload-icon">📤</div>
                        <div class="upload-text">Drop your design here or click to upload</div>
                        <div class="upload-hint">Supports PNG, JPG, SVG, Figma, Sketch</div>
                    </div>

                    <div style="margin-top: 1.5rem;">
                        <label style="display: block; font-weight: 600; color: #1e293b; margin-bottom: 0.5rem;">Select Framework</label>
                        <div class="framework-grid">
                            <div class="framework-card selected" onclick="selectFramework(this)">
                                <div class="framework-icon">⚛️</div>
                                <div class="framework-name">React</div>
                            </div>
                            <div class="framework-card" onclick="selectFramework(this)">
                                <div class="framework-icon">💚</div>
                                <div class="framework-name">Vue</div>
                            </div>
                            <div class="framework-card" onclick="selectFramework(this)">
                                <div class="framework-icon">▲</div>
                                <div class="framework-name">Next.js</div>
                            </div>
                            <div class="framework-card" onclick="selectFramework(this)">
                                <div class="framework-icon">🅰️</div>
                                <div class="framework-name">Angular</div>
                            </div>
                            <div class="framework-card" onclick="selectFramework(this)">
                                <div class="framework-icon">🅱️</div>
                                <div class="framework-name">Bootstrap</div>
                            </div>
                            <div class="framework-card" onclick="selectFramework(this)">
                                <div class="framework-icon">🍃</div>
                                <div class="framework-name">Tailwind</div>
                            </div>
                        </div>
                    </div>

                    <button class="generate-btn" onclick="generateCode()">🤖 Generate Code</button>
                </div>

                <div id="code-output" class="code-output" style="display: none;">
{{/* Code output will appear here */}}
                </div>
            </div>

            <script>
                function selectFramework(card) {{
                    document.querySelectorAll('.framework-card').forEach(c => c.classList.remove('selected'));
                    card.classList.add('selected');
                }}

                function generateCode() {{
                    const event = new CustomEvent('generateCode', {{
                        detail: {{}}
                    }});
                    window.parent.postMessage(event, '*');
                }}
            </script>
        </div>
        """

    def _render_inspector(self) -> str:
        """Render code inspector."""
        return """
        <div style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .code-inspector {{ max-width: 1200px; }}
                .inspector-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }}
                .inspector-panel {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; }}
                .panel-header {{ padding: 1rem 1.5rem; background: #f8fafc; border-bottom: 1px solid #e2e8f0; font-weight: 600; color: #1e293b; }}
                .panel-content {{ padding: 1.5rem; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; line-height: 1.6; max-height: 400px; overflow-y: auto; }}
                .code-block {{ background: #1e293b; color: #e2e8f0; padding: 1rem; border-radius: 8px; }}
                .code-keyword {{ color: #c678dd; }}
                .code-string {{ color: #98c379; }}
                .code-tag {{ color: #e06c75; }}
                .code-attr {{ color: #d19a66; }}
                .code-comment {{ color: #5c6370; font-style: italic; }}
            </style>

            <div class="code-inspector">
                <h3 style="margin-bottom: 1.5rem;">🔍 Code Inspector</h3>

                <div class="inspector-grid">
                    <div class="inspector-panel">
                        <div class="panel-header">📄 HTML Structure</div>
                        <div class="panel-content">
                            <div class="code-block">
<span class="code-keyword">&lt;div</span> <span class="code-attr">class</span>=<span class="code-string">"container"</span><span class="code-keyword">&gt;</span>
  <span class="code-keyword">&lt;header</span> <span class="code-attr">class</span>=<span class="code-string">"hero"</span><span class="code-keyword">&gt;</span>
    <span class="code-keyword">&lt;h1&gt;</span>Welcome<span class="code-keyword">&lt;/h1&gt;</span>
    <span class="code-keyword">&lt;p&gt;</span>Subtitle<span class="code-keyword">&lt;/p&gt;</span>
    <span class="code-keyword">&lt;button&gt;</span>CTA<span class="code-keyword">&lt;/button&gt;</span>
  <span class="code-keyword">&lt;/header&gt;</span>
<span class="code-keyword">&lt;/div&gt;</span>
                            </div>
                        </div>
                    </div>

                    <div class="inspector-panel">
                        <div class="panel-header">🎨 CSS Styles</div>
                        <div class="panel-content">
                            <div class="code-block">
<span class="code-keyword">.container</span> {{
  <span class="code-attr">max-width</span>: <span class="code-string">1200px</span>;
  <span class="code-attr">margin</span>: <span class="code-string">0 auto</span>;
  <span class="code-attr">padding</span>: <span class="code-string">2rem</span>;
}}

<span class="code-keyword">.hero</span> {{
  <span class="code-attr">text-align</span>: <span class="code-string">center</span>;
  <span class="code-attr">padding</span>: <span class="code-string">4rem 0</span>;
}}

<span class="code-keyword">.hero h1</span> {{
  <span class="code-attr">font-size</span>: <span class="code-string">3rem</span>;
  <span class="code-attr">font-weight</span>: <span class="code-string">700</span>;
}}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """

    def _render_export(self) -> str:
        """Render code export interface."""
        return """
        <div style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .code-export {{ max-width: 800px; }}
                .export-options {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; }}
                .export-card {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; text-align: center; cursor: pointer; transition: all 0.2s; }}
                .export-card:hover {{ border-color: #6366f1; transform: translateY(-4px); }}
                .export-icon {{ font-size: 3rem; margin-bottom: 1rem; }}
                .export-name {{ font-weight: 600; color: #1e293b; margin-bottom: 0.5rem; }}
                .export-desc {{ font-size: 0.875rem; color: #64748b; }}
            </style>

            <div class="code-export">
                <h3 style="margin-bottom: 1.5rem;">📥 Code Export</h3>

                <div class="export-options">
                    <div class="export-card">
                        <div class="export-icon">⚛️</div>
                        <div class="export-name">React</div>
                        <div class="export-desc">JSX components with hooks</div>
                    </div>
                    <div class="export-card">
                        <div class="export-icon">💚</div>
                        <div class="export-name">Vue</div>
                        <div class="export-desc">Composition API SFCs</div>
                    </div>
                    <div class="export-card">
                        <div class="export-icon">▲</div>
                        <div class="export-name">Next.js</div>
                        <div class="export-desc">App Router pages</div>
                    </div>
                    <div class="export-card">
                        <div class="export-icon">🅱️</div>
                        <div class="export-name">HTML/CSS</div>
                        <div class="export-desc">Static files</div>
                    </div>
                    <div class="export-card">
                        <div class="export-icon">🍃</div>
                        <div class="export-name">Tailwind</div>
                        <div class="export-desc">Utility classes</div>
                    </div>
                    <div class="export-card">
                        <div class="export-icon">📦</div>
                        <div class="export-name">ZIP Package</div>
                        <div class="export-desc">Complete project</div>
                    </div>
                </div>
            </div>
        </div>
        """
