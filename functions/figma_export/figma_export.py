"""
title: Export to Figma
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesigner
version: 1.0.0
required_open_webui_version: 0.10.0
"""

from typing import Any


class Action:
    """Export to Figma — Convert designs to Figma-ready formats."""

    def __init__(self):
        self.type = "action"

    def actions(self) -> list[dict[str, str]]:
        """Return available actions."""
        return [
            {
                "name": "Export to Figma",
                "description": "Export design to Figma format",
                "icon": "figma",
            },
            {
                "name": "Design Tokens Sync",
                "description": "Sync design tokens with Figma",
                "icon": "sync",
            },
            {
                "name": "Component Mapping",
                "description": "Map components to Figma components",
                "icon": "box",
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
        """Handle Figma export action."""
        if action == "Export to Figma":
            return self._render_export_ui(body)
        elif action == "Design Tokens Sync":
            return self._render_tokens_sync()
        elif action == "Component Mapping":
            return self._render_component_mapping()

        return f"Unknown action: {action}"

    def _render_export_ui(self, body: dict) -> str:
        """Render Figma export interface."""
        return """
        <div class="figma-export" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .figma-export {{ max-width: 1000px; }}
                .export-header {{ text-align: center; margin-bottom: 2rem; }}
                .export-header h3 {{ font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0 0 0.5rem; }}
                .export-header p {{ color: #64748b; }}
                .export-options {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; }}
                .option-group {{ margin-bottom: 1.5rem; }}
                .option-group:last-child {{ margin-bottom: 0; }}
                .option-group h4 {{ font-size: 1rem; font-weight: 600; color: #1e293b; margin: 0 0 0.75rem; }}
                .option-list {{ display: flex; flex-direction: column; gap: 0.75rem; }}
                .option-item {{ display: flex; align-items: center; gap: 0.75rem; }}
                .option-item input[type="checkbox"] {{ width: 18px; height: 18px; }}
                .option-item span {{ font-size: 0.875rem; color: #1e293b; }}
                .export-btn {{ padding: 1rem 2rem; background: #6366f1; color: white; border: none; border-radius: 12px; font-weight: 600; cursor: pointer; font-size: 1rem; }}
                .export-btn:hover {{ background: #4f46e5; }}
                .api-section {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; }}
                .api-section h4 {{ font-size: 1rem; font-weight: 600; color: #1e293b; margin: 0 0 1rem; }}
                .api-input {{ width: 100%; padding: 0.75rem; border: 1px solid #e2e8f0; border-radius: 8px; font-family: 'JetBrains Mono', monospace; font-size: 0.875rem; }}
            </style>

            <div class="figma-export">
                <div class="export-header">
                    <h3>🎨 Export to Figma</h3>
                    <p>Convert your OpenDesigner creation to Figma-ready files</p>
                </div>

                <div class="export-options">
                    <div class="option-group">
                        <h4>Export Options</h4>
                        <div class="option-list">
                            <div class="option-item">
                                <input type="checkbox" id="figma-frames" checked>
                                <span>Use Figma frames for responsive layouts</span>
                            </div>
                            <div class="option-item">
                                <input type="checkbox" id="figma-components" checked>
                                <span>Convert components to Figma components</span>
                            </div>
                            <div class="option-item">
                                <input type="checkbox" id="figma-styles" checked>
                                <span>Apply design styles and tokens</span>
                            </div>
                            <div class="option-item">
                                <input type="checkbox" id="figma-auto-layout">
                                <span>Use Auto Layout for all frames</span>
                            </div>
                            <div class="option-item">
                                <input type="checkbox" id="figma-assets" checked>
                                <span>Include images and assets</span>
                            </div>
                            <div class="option-item">
                                <input type="checkbox" id="figma-variants">
                                <span>Create component variants</span>
                            </div>
                        </div>
                    </div>

                    <div class="option-group">
                        <h4>Page Settings</h4>
                        <div class="option-list">
                            <div class="option-item">
                                <input type="checkbox" id="figma-page" checked>
                                <span>Create new page in Figma file</span>
                            </div>
                            <div class="option-item">
                                <input type="checkbox" id="figma-frame">
                                <span>Use frame as component</span>
                            </div>
                            <div class="option-item">
                                <input type="checkbox" id="figma-description" checked>
                                <span>Add description from OpenDesigner</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="api-section">
                    <h4>🔑 Figma API Token</h4>
                    <input type="password" class="api-input" placeholder="Enter your Figma personal access token" id="figma-token">
                    <p style="font-size: 0.75rem; color: #64748b; margin-top: 0.5rem;">
                        Get your token from <a href="https://www.figma.com/developers/api#access-tokens" target="_blank" style="color: #6366f1;">Figma Developers</a>
                    </p>
                </div>

                <div style="text-align: center; margin-top: 1.5rem;">
                    <button class="export-btn" onclick="exportToFigma()">🚀 Export to Figma</button>
                </div>
            </div>

            <script>
                function exportToFigma() {{
                    const token = document.getElementById('figma-token').value;
                    if (!token) {{
                        alert('Please enter your Figma API token');
                        return;
                    }}

                    const event = new CustomEvent('exportToFigma', {{
                        detail: {{ token: token }}
                    }});
                    window.parent.postMessage(event, '*');
                }}
            </script>
        </div>
        """

    def _render_tokens_sync(self) -> str:
        """Render tokens sync interface."""
        return """
        <div style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .tokens-sync {{ max-width: 800px; }}
                .token-map {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; }}
                .token-row {{ display: flex; align-items: center; padding: 1rem 1.5rem; border-bottom: 1px solid #e2e8f0; }}
                .token-row:last-child {{ border-bottom: none; }}
                .token-name {{ width: 150px; font-weight: 600; color: #1e293b; }}
                .token-arrow {{ margin: 0 1rem; color: #6366f1; }}
                .token-figma {{ flex: 1; padding: 0.5rem 1rem; background: #f8fafc; border-radius: 6px; font-size: 0.875rem; }}
                .sync-btn {{ padding: 0.75rem 1.5rem; background: #6366f1; color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; margin-top: 1.5rem; }}
            </style>

            <div class="tokens-sync">
                <h3 style="margin-bottom: 1.5rem;">🔄 Design Tokens Sync</h3>

                <div class="token-map">
                    <div class="token-row">
                        <div class="token-name">Primary</div>
                        <div class="token-arrow">→</div>
                        <div class="token-figma">Colors / Primary (#6366f1)</div>
                    </div>
                    <div class="token-row">
                        <div class="token-name">Secondary</div>
                        <div class="token-arrow">→</div>
                        <div class="token-figma">Colors / Secondary (#10b981)</div>
                    </div>
                    <div class="token-row">
                        <div class="token-name">Body Font</div>
                        <div class="token-arrow">→</div>
                        <div class="token-figma">Typography / Body (Inter, 16px)</div>
                    </div>
                    <div class="token-row">
                        <div class="token-name">H1 Size</div>
                        <div class="token-arrow">→</div>
                        <div class="token-figma">Typography / H1 (Inter, 40px)</div>
                    </div>
                    <div class="token-row">
                        <div class="token-name">Shadow-MD</div>
                        <div class="token-arrow">→</div>
                        <div class="token-figma">Effects / Shadow Medium</div>
                    </div>
                </div>

                <button class="sync-btn">🔄 Sync All Tokens</button>
            </div>
        </div>
        """

    def _render_component_mapping(self) -> str:
        """Render component mapping interface."""
        return """
        <div style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .component-map {{ max-width: 1000px; }}
                .map-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }}
                .map-column {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; }}
                .map-column h4 {{ font-size: 1.125rem; font-weight: 600; color: #1e293b; margin: 0 0 1rem; }}
                .map-item {{ padding: 0.75rem; background: #f8fafc; border-radius: 6px; margin-bottom: 0.5rem; display: flex; align-items: center; justify-content: space-between; }}
                .map-item-name {{ font-size: 0.875rem; font-weight: 600; color: #1e293b; }}
                .map-select {{ padding: 0.375rem 0.75rem; border: 1px solid #e2e8f0; border-radius: 4px; font-size: 0.75rem; }}
                .map-btn {{ padding: 0.75rem 1.5rem; background: #6366f1; color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; margin-top: 1.5rem; width: 100%; }}
            </style>

            <div class="component-map">
                <h3 style="margin-bottom: 1.5rem;">📦 Component Mapping</h3>

                <div class="map-grid">
                    <div class="map-column">
                        <h4>OpenDesigner</h4>
                        <div class="map-item">
                            <span class="map-item-name">Button</span>
                            <span style="font-size: 1.5rem;">→</span>
                        </div>
                        <div class="map-item">
                            <span class="map-item-name">Card</span>
                            <span style="font-size: 1.5rem;">→</span>
                        </div>
                        <div class="map-item">
                            <span class="map-item-name">Navigation</span>
                            <span style="font-size: 1.5rem;">→</span>
                        </div>
                        <div class="map-item">
                            <span class="map-item-name">Form</span>
                            <span style="font-size: 1.5rem;">→</span>
                        </div>
                        <div class="map-item">
                            <span class="map-item-name">Modal</span>
                            <span style="font-size: 1.5rem;">→</span>
                        </div>
                    </div>

                    <div class="map-column">
                        <h4>Figma Components</h4>
                        <div class="map-item">
                            <span class="map-item-name">Button / Primary</span>
                            <select class="map-select">
                                <option>Select...</option>
                                <option selected>Button / Primary</option>
                                <option>Button / Secondary</option>
                                <option>Button / Outline</option>
                            </select>
                        </div>
                        <div class="map-item">
                            <span class="map-item-name">Card / Default</span>
                            <select class="map-select">
                                <option>Select...</option>
                                <option selected>Card / Default</option>
                                <option>Card / Horizontal</option>
                                <option>Card / Profile</option>
                            </select>
                        </div>
                        <div class="map-item">
                            <span class="map-item-name">Navigation / Top</span>
                            <select class="map-select">
                                <option>Select...</option>
                                <option selected>Navigation / Top</option>
                                <option>Navigation / Side</option>
                                <option>Navigation / Mobile</option>
                            </select>
                        </div>
                        <div class="map-item">
                            <span class="map-item-name">Form / Input</span>
                            <select class="map-select">
                                <option>Select...</option>
                                <option selected>Form / Input</option>
                                <option>Form / Textarea</option>
                                <option>Form / Select</option>
                            </select>
                        </div>
                        <div class="map-item">
                            <span class="map-item-name">Modal / Dialog</span>
                            <select class="map-select">
                                <option>Select...</option>
                                <option selected>Modal / Dialog</option>
                                <option>Modal / Alert</option>
                                <option>Modal / Confirm</option>
                            </select>
                        </div>
                    </div>
                </div>

                <button class="map-btn">✅ Map & Export Components</button>
            </div>
        </div>
        """
