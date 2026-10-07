"""
title: AI Design Iteration Engine
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesigner
version: 1.0.0
required_open_webui_version: 0.10.0
"""

from typing import Any


class DesignIterationEngine:
    """AI Design Iteration Engine — Refine designs through natural language."""

    def __init__(self):
        self.type = "action"
        self.iteration_history = {}

    def actions(self) -> list[dict[str, str]]:
        """Return available actions."""
        return [
            {
                "name": "AI Design Iteration",
                "description": "Refine your design with natural language commands",
                "icon": "wand",
            },
            {
                "name": "Iteration History",
                "description": "View and revert design iterations",
                "icon": "clock",
            },
            {
                "name": "Quick Adjustments",
                "description": "Common design tweaks (colors, spacing, typography)",
                "icon": "sliders",
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
        """Handle iteration action."""
        if action == "AI Design Iteration":
            return self._render_iteration_ui(body)
        elif action == "Iteration History":
            return self._render_iteration_history()
        elif action == "Quick Adjustments":
            return self._render_quick_adjustments()

        return f"Unknown action: {action}"

    def _render_iteration_ui(self, body: dict) -> str:
        """Render iteration interface."""
        design_id = body.get("design_id", "current")
        current_html = body.get("html", "<html><body>No design loaded</body></html>")

        return f"""
        <div class="iteration-engine" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .iteration-engine {{ max-width: 1000px; margin: 0 auto; }}
                .header {{ text-align: center; margin-bottom: 2rem; }}
                .header h3 {{ font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0 0 0.5rem; }}
                .header p {{ color: #64748b; }}
                .command-input {{ display: flex; gap: 0.75rem; margin-bottom: 1.5rem; }}
                .command-input input {{ flex: 1; padding: 1rem; border: 2px solid #e2e8f0; border-radius: 12px; font-size: 1rem; }}
                .command-input input:focus {{ outline: none; border-color: #6366f1; }}
                .command-input button {{ padding: 1rem 2rem; background: #6366f1; color: white; border: none; border-radius: 12px; font-weight: 600; cursor: pointer; }}
                .command-input button:hover {{ background: #4f46e5; }}
                .suggestions {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-bottom: 1.5rem; }}
                .suggestion-card {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1rem; cursor: pointer; transition: all 0.2s; }}
                .suggestion-card:hover {{ background: #f1f5f9; border-color: #6366f1; }}
                .suggestion-card h4 {{ font-size: 0.875rem; font-weight: 600; color: #1e293b; margin: 0 0 0.5rem; }}
                .suggestion-card p {{ font-size: 0.75rem; color: #64748b; margin: 0; }}
                .preview-section {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; }}
                .preview-section h4 {{ font-size: 1rem; font-weight: 600; color: #1e293b; margin: 0 0 1rem; }}
                .preview-frame {{ width: 100%; height: 400px; border: 1px solid #e2e8f0; border-radius: 8px; }}
            </style>

            <div class="header">
                <h3>🎨 AI Design Iteration</h3>
                <p>Describe what you want to change and I'll update your design</p>
            </div>

            <div class="command-input">
                <input type="text" id="iteration-command" placeholder="e.g., Make the hero section bigger, Change to dark theme, Add more whitespace">
                <button onclick="submitIteration()">Apply</button>
            </div>

            <h4 style="margin: 1.5rem 0 1rem; font-weight: 600; color: #1e293b;">Quick Suggestions</h4>
            <div class="suggestions">
                <div class="suggestion-card" onclick="applySuggestion('Make the design more modern')">
                    <h4>🎯 Modernize</h4>
                    <p>Update to modern design patterns</p>
                </div>
                <div class="suggestion-card" onclick="applySuggestion('Change to a dark theme')">
                    <h4>🌙 Dark Theme</h4>
                    <p>Switch to dark color scheme</p>
                </div>
                <div class="suggestion-card" onclick="applySuggestion('Add more whitespace')">
                    <h4>📐 Spacing</h4>
                    <p>Increase padding and margins</p>
                </div>
                <div class="suggestion-card" onclick="applySuggestion('Make it more professional')">
                    <h4>💼 Professional</h4>
                    <p>Refine for business use</p>
                </div>
                <div class="suggestion-card" onclick="applySuggestion('Add better typography')">
                    <h4>🔤 Typography</h4>
                    <p>Improve font hierarchy</p>
                </div>
                <div class="suggestion-card" onclick="applySuggestion('Optimize for mobile')">
                    <h4>📱 Mobile-First</h4>
                    <p>Enhance mobile experience</p>
                </div>
            </div>

            <div class="preview-section">
                <h4>Current Design Preview</h4>
                <iframe class="preview-frame" srcdoc="${current_html}" sandbox="allow-scripts"></iframe>
            </div>

            <script>
                function applySuggestion(command) {{
                    document.getElementById('iteration-command').value = command;
                    submitIteration();
                }}

                function submitIteration() {{
                    const command = document.getElementById('iteration-command').value;
                    if (command) {{
                        const event = new CustomEvent('designIteration', {{
                            detail: {{ command: command, design_id: '{design_id}' }}
                        }});
                        window.parent.postMessage(event, '*');
                    }}
                }}
            </script>
        </div>
        """

    def _render_iteration_history(self) -> str:
        """Render iteration history."""
        return """
        <div style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .history {{ max-width: 800px; }}
                .history-item {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; }}
                .history-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; }}
                .history-command {{ font-weight: 600; color: #1e293b; }}
                .history-time {{ font-size: 0.75rem; color: #64748b; }}
                .history-actions {{ display: flex; gap: 0.5rem; }}
                .history-btn {{ padding: 0.5rem 1rem; border-radius: 6px; font-size: 0.875rem; font-weight: 600; cursor: pointer; border: none; }}
                .history-btn.primary {{ background: #6366f1; color: white; }}
                .history-btn.secondary {{ background: #f1f5f9; color: #1e293b; }}
                .empty-state {{ text-align: center; padding: 3rem; color: #64748b; }}
            </style>

            <div class="history">
                <h3 style="margin-bottom: 1.5rem;">📜 Iteration History</h3>

                <div class="empty-state">
                    <h4>No iterations yet</h4>
                    <p>Your design iterations will appear here</p>
                </div>
            </div>
        </div>
        """

    def _render_quick_adjustments(self) -> str:
        """Render quick adjustments panel."""
        return """
        <div style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .adjustments {{ max-width: 1000px; }}
                .adjustment-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; }}
                .adjustment-card {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; }}
                .adjustment-card h4 {{ font-size: 1.125rem; font-weight: 600; color: #1e293b; margin: 0 0 1rem; }}
                .adjustment-group {{ margin-bottom: 1rem; }}
                .adjustment-group label {{ display: block; font-size: 0.875rem; font-weight: 600; color: #1e293b; margin-bottom: 0.5rem; }}
                .adjustment-group select, .adjustment-group input[type="range"] {{ width: 100%; padding: 0.5rem; border: 1px solid #e2e8f0; border-radius: 6px; }}
                .apply-btn {{ width: 100%; padding: 1rem; background: #6366f1; color: white; border: none; border-radius: 12px; font-weight: 600; cursor: pointer; margin-top: 1rem; }}
                .apply-btn:hover {{ background: #4f46e5; }}
            </style>

            <div class="adjustments">
                <h3 style="margin-bottom: 1.5rem;">🎛️ Quick Adjustments</h3>

                <div class="adjustment-grid">
                    <div class="adjustment-card">
                        <h4>🎨 Colors</h4>
                        <div class="adjustment-group">
                            <label>Primary Color</label>
                            <select id="primary-color">
                                <option value="#6366f1">Indigo (Default)</option>
                                <option value="#3b82f6">Blue</option>
                                <option value="#10b981">Green</option>
                                <option value="#f59e0b">Amber</option>
                                <option value="#ef4444">Red</option>
                                <option value="#8b5cf6">Purple</option>
                            </select>
                        </div>
                        <div class="adjustment-group">
                            <label>Theme</label>
                            <select id="theme-mode">
                                <option value="light">Light</option>
                                <option value="dark">Dark</option>
                                <option value="system">System</option>
                            </select>
                        </div>
                    </div>

                    <div class="adjustment-card">
                        <h4>📐 Spacing</h4>
                        <div class="adjustment-group">
                            <label>Padding Scale: <span id="padding-value">1x</span></label>
                            <input type="range" id="padding-scale" min="0.5" max="2" step="0.25" value="1" oninput="document.getElementById('padding-value').textContent = this.value + 'x'">
                        </div>
                        <div class="adjustment-group">
                            <label>Border Radius: <span id="radius-value">12px</span></label>
                            <input type="range" id="border-radius" min="0" max="24" step="2" value="12" oninput="document.getElementById('radius-value').textContent = this.value + 'px'">
                        </div>
                    </div>

                    <div class="adjustment-card">
                        <h4>🔤 Typography</h4>
                        <div class="adjustment-group">
                            <label>Font Family</label>
                            <select id="font-family">
                                <option value="system-ui">System UI</option>
                                <option value="Georgia">Georgia (Serif)</option>
                                <option value="'Courier New'">Courier New (Monospace)</option>
                            </select>
                        </div>
                        <div class="adjustment-group">
                            <label>Font Size Scale: <span id="size-value">1x</span></label>
                            <input type="range" id="font-size-scale" min="0.75" max="1.5" step="0.125" value="1" oninput="document.getElementById('size-value').textContent = this.value + 'x'">
                        </div>
                    </div>
                </div>

                <button class="apply-btn" onclick="applyAdjustments()">Apply All Adjustments</button>
            </div>

            <script>
                function applyAdjustments() {{
                    const adjustments = {{
                        primaryColor: document.getElementById('primary-color').value,
                        theme: document.getElementById('theme-mode').value,
                        paddingScale: document.getElementById('padding-scale').value,
                        borderRadius: document.getElementById('border-radius').value,
                        fontFamily: document.getElementById('font-family').value,
                        fontSizeScale: document.getElementById('font-size-scale').value
                    }};

                    const event = new CustomEvent('designAdjustments', {{ detail: adjustments }});
                    window.parent.postMessage(event, '*');
                }}
            </script>
        </div>
        """
