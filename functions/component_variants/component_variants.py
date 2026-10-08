"""
title: Component Variants & States
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesigner
version: 1.0.0
required_open_webui_version: 0.10.0
"""

from typing import Any


class Action:
    """Component Variants & States — Add hover, focus, active, disabled, loading states."""

    def __init__(self):
        self.type = "action"

    def actions(self) -> list[dict[str, str]]:
        """Return available actions."""
        return [
            {
                "name": "Component States",
                "description": "Add hover, focus, active, disabled, loading states",
                "icon": "layers",
            },
            {
                "name": "Variant Manager",
                "description": "Manage component variants and properties",
                "icon": "sliders",
            },
            {
                "name": "Interactive Preview",
                "description": "Preview all component states interactively",
                "icon": "eye",
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
        """Handle variant action."""
        if action == "Component States":
            return self._render_component_states(body)
        elif action == "Variant Manager":
            return self._render_variant_manager()
        elif action == "Interactive Preview":
            return self._render_interactive_preview()

        return f"Unknown action: {action}"

    def _render_component_states(self, body: dict) -> str:
        """Render component states editor."""
        return """
        <div class="component-states" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .component-states {{ max-width: 1200px; }}
                .states-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 1.5rem; }}
                .state-card {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; }}
                .state-card h4 {{ font-size: 1.125rem; font-weight: 600; color: #1e293b; margin: 0 0 1rem; display: flex; align-items: center; gap: 0.5rem; }}
                .state-preview {{ min-height: 100px; display: flex; align-items: center; justify-content: center; background: #f8fafc; border-radius: 8px; margin-bottom: 1rem; }}
                .state-button {{ padding: 0.75rem 1.5rem; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; background: #6366f1; color: white; transition: all 0.2s; }}
                .state-button:hover {{ background: #4f46e5; transform: translateY(-2px); }}
                .state-button:focus {{ outline: 3px solid #c7d2fe; outline-offset: 2px; }}
                .state-button:active {{ transform: translateY(0); }}
                .state-button:disabled {{ background: #cbd5e1; cursor: not-allowed; }}
                .state-button.loading {{ position: relative; color: transparent; }}
                .state-button.loading::after {{ content: ''; position: absolute; width: 20px; height: 20px; top: 50%; left: 50%; margin-left: -10px; margin-top: -10px; border: 2px solid #fff; border-radius: 50%; border-right-color: transparent; animation: spin 0.75s linear infinite; }}
                @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
                .state-controls {{ display: grid; gap: 0.75rem; }}
                .control-group {{ display: flex; align-items: center; justify-content: space-between; }}
                .control-group label {{ font-size: 0.875rem; color: #64748b; }}
                .control-group input[type="color"] {{ width: 40px; height: 40px; border: 2px solid #e2e8f0; border-radius: 6px; cursor: pointer; }}
                .control-group input[type="range"] {{ width: 120px; }}
            </style>

            <div class="component-states">
                <h3 style="margin-bottom: 1.5rem;">🎭 Component States</h3>

                <div class="states-grid">
                    <div class="state-card">
                        <h4>⚪ Default</h4>
                        <div class="state-preview">
                            <button class="state-button">Button</button>
                        </div>
                        <div class="state-controls">
                            <div class="control-group">
                                <label>Background</label>
                                <input type="color" value="#6366f1">
                            </div>
                            <div class="control-group">
                                <label>Text Color</label>
                                <input type="color" value="#ffffff">
                            </div>
                        </div>
                    </div>

                    <div class="state-card">
                        <h4>🖱️ Hover</h4>
                        <div class="state-preview">
                            <button class="state-button" style="background: #4f46e5; transform: translateY(-2px);">Button</button>
                        </div>
                        <div class="state-controls">
                            <div class="control-group">
                                <label>Background</label>
                                <input type="color" value="#4f46e5">
                            </div>
                            <div class="control-group">
                                <label>Transform</label>
                                <input type="range" min="0" max="10" value="2">
                            </div>
                        </div>
                    </div>

                    <div class="state-card">
                        <h4>👆 Active</h4>
                        <div class="state-preview">
                            <button class="state-button" style="background: #4338ca; transform: translateY(0);">Button</button>
                        </div>
                        <div class="state-controls">
                            <div class="control-group">
                                <label>Background</label>
                                <input type="color" value="#4338ca">
                            </div>
                            <div class="control-group">
                                <label>Transform</label>
                                <input type="range" min="0" max="10" value="0">
                            </div>
                        </div>
                    </div>

                    <div class="state-card">
                        <h4>🎯 Focus</h4>
                        <div class="state-preview">
                            <button class="state-button" style="outline: 3px solid #c7d2fe; outline-offset: 2px;">Button</button>
                        </div>
                        <div class="state-controls">
                            <div class="control-group">
                                <label>Outline Color</label>
                                <input type="color" value="#c7d2fe">
                            </div>
                            <div class="control-group">
                                <label>Outline Width</label>
                                <input type="range" min="0" max="6" value="3">
                            </div>
                        </div>
                    </div>

                    <div class="state-card">
                        <h4>🚫 Disabled</h4>
                        <div class="state-preview">
                            <button class="state-button" style="background: #cbd5e1; cursor: not-allowed;">Button</button>
                        </div>
                        <div class="state-controls">
                            <div class="control-group">
                                <label>Background</label>
                                <input type="color" value="#cbd5e1">
                            </div>
                            <div class="control-group">
                                <label>Opacity</label>
                                <input type="range" min="0" max="100" value="50">
                            </div>
                        </div>
                    </div>

                    <div class="state-card">
                        <h4>⏳ Loading</h4>
                        <div class="state-preview">
                            <button class="state-button loading">Button</button>
                        </div>
                        <div class="state-controls">
                            <div class="control-group">
                                <label>Spinner Color</label>
                                <input type="color" value="#ffffff">
                            </div>
                            <div class="control-group">
                                <label>Spinner Size</label>
                                <input type="range" min="10" max="30" value="20">
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """

    def _render_variant_manager(self) -> str:
        """Render variant manager."""
        return """
        <div style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .variant-manager {{ max-width: 1000px; }}
                .variant-table {{ width: 100%; border-collapse: collapse; }}
                .variant-table th {{ background: #f8fafc; padding: 1rem; text-align: left; font-weight: 600; color: #1e293b; }}
                .variant-table td {{ padding: 1rem; border-bottom: 1px solid #e2e8f0; }}
                .variant-badge {{ padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.75rem; font-weight: 600; }}
                .variant-badge.default {{ background: #dcfce7; color: #16a34a; }}
                .variant-badge.hover {{ background: #dbeafe; color: #1e40af; }}
                .variant-badge.active {{ background: #fef3c7; color: #92400e; }}
                .variant-badge.disabled {{ background: #f1f5f9; color: #64748b; }}
                .add-variant-btn {{ padding: 0.75rem 1.5rem; background: #6366f1; color: white; border: none; border-radius: 12px; font-weight: 600; cursor: pointer; }}
            </style>

            <div class="variant-manager">
                <h3 style="margin-bottom: 1.5rem;">📋 Variant Manager</h3>

                <table class="variant-table">
                    <thead>
                        <tr>
                            <th>Component</th>
                            <th>Variant</th>
                            <th>Properties</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Button</td>
                            <td><span class="variant-badge default">Default</span></td>
                            <td>bg: #6366f1, color: #fff</td>
                            <td><button style="padding: 0.5rem; border: 1px solid #e2e8f0; border-radius: 6px; cursor: pointer;">Edit</button></td>
                        </tr>
                        <tr>
                            <td>Button</td>
                            <td><span class="variant-badge hover">Hover</span></td>
                            <td>bg: #4f46e5, transform: translateY(-2px)</td>
                            <td><button style="padding: 0.5rem; border: 1px solid #e2e8f0; border-radius: 6px; cursor: pointer;">Edit</button></td>
                        </tr>
                        <tr>
                            <td>Button</td>
                            <td><span class="variant-badge active">Active</span></td>
                            <td>bg: #4338ca, transform: translateY(0)</td>
                            <td><button style="padding: 0.5rem; border: 1px solid #e2e8f0; border-radius: 6px; cursor: pointer;">Edit</button></td>
                        </tr>
                        <tr>
                            <td>Button</td>
                            <td><span class="variant-badge disabled">Disabled</span></td>
                            <td>bg: #cbd5e1, cursor: not-allowed</td>
                            <td><button style="padding: 0.5rem; border: 1px solid #e2e8f0; border-radius: 6px; cursor: pointer;">Edit</button></td>
                        </tr>
                    </tbody>
                </table>

                <button class="add-variant-btn" style="margin-top: 1.5rem;">+ Add New Variant</button>
            </div>
        </div>
        """

    def _render_interactive_preview(self) -> str:
        """Render interactive preview."""
        return """
        <div style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .interactive-preview {{ max-width: 1000px; }}
                .preview-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; }}
                .preview-item {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 2rem; text-align: center; }}
                .preview-button {{ padding: 0.75rem 1.5rem; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; background: #6366f1; color: white; transition: all 0.2s; }}
                .preview-button:hover {{ background: #4f46e5; transform: translateY(-2px); }}
                .preview-label {{ margin-top: 1rem; font-size: 0.875rem; color: #64748b; }}
            </style>

            <div class="interactive-preview">
                <h3 style="margin-bottom: 1.5rem;">👁️ Interactive Preview</h3>

                <div class="preview-grid">
                    <div class="preview-item">
                        <button class="preview-button">Default</button>
                        <div class="preview-label">Default State</div>
                    </div>
                    <div class="preview-item">
                        <button class="preview-button">Hover Me</button>
                        <div class="preview-label">Hover State</div>
                    </div>
                    <div class="preview-item">
                        <button class="preview-button">Click Me</button>
                        <div class="preview-label">Active State</div>
                    </div>
                    <div class="preview-item">
                        <button class="preview-button" tabindex="0">Focus Me</button>
                        <div class="preview-label">Focus State</div>
                    </div>
                    <div class="preview-item">
                        <button class="preview-button" disabled>Disabled</button>
                        <div class="preview-label">Disabled State</div>
                    </div>
                </div>
            </div>
        </div>
        """
