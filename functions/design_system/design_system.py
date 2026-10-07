"""
title: Design System Manager
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesigner
version: 1.0.0
required_open_webui_version: 0.10.0
"""

from typing import Any


class DesignSystem:
    """Design System Manager — Create and manage design tokens, components, and styles."""

    def __init__(self):
        self.type = "action"

    def actions(self) -> list[dict[str, str]]:
        """Return available actions."""
        return [
            {
                "name": "Design Tokens",
                "description": "Manage colors, typography, spacing, and shadows",
                "icon": "palette",
            },
            {
                "name": "Component Library",
                "description": "Browse and manage reusable components",
                "icon": "box",
            },
            {
                "name": "Style Guide",
                "description": "View and export complete style guide",
                "icon": "book",
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
        """Handle design system action."""
        if action == "Design Tokens":
            return self._render_tokens(body)
        elif action == "Component Library":
            return self._render_components()
        elif action == "Style Guide":
            return self._render_style_guide()

        return f"Unknown action: {action}"

    def _render_tokens(self, body: dict) -> str:
        """Render design tokens editor."""
        return """
        <div class="design-tokens" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .design-tokens {{ max-width: 1200px; }}
                .tokens-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; }}
                .token-card {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; }}
                .token-card h4 {{ font-size: 1.125rem; font-weight: 600; color: #1e293b; margin: 0 0 1rem; display: flex; align-items: center; gap: 0.5rem; }}
                .token-list {{ display: flex; flex-direction: column; gap: 0.75rem; }}
                .token-item {{ display: flex; align-items: center; justify-content: space-between; padding: 0.75rem; background: #f8fafc; border-radius: 8px; }}
                .token-name {{ font-size: 0.875rem; font-weight: 600; color: #1e293b; }}
                .token-value {{ font-size: 0.75rem; color: #64748b; font-family: 'JetBrains Mono', monospace; }}
                .token-preview {{ display: flex; gap: 0.5rem; flex-wrap: wrap; }}
                .color-swatch {{ width: 32px; height: 32px; border-radius: 6px; border: 2px solid #e2e8f0; }}
                .export-btn {{ padding: 0.75rem 1.5rem; background: #6366f1; color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; margin-top: 1rem; }}
            </style>

            <div class="design-tokens">
                <h3 style="margin-bottom: 1.5rem;">🎨 Design Tokens</h3>

                <div class="tokens-grid">
                    <div class="token-card">
                        <h4>🎨 Colors</h4>
                        <div class="token-list">
                            <div class="token-item">
                                <div class="token-name">Primary</div>
                                <div class="token-preview">
                                    <div class="color-swatch" style="background: #6366f1;"></div>
                                    <span class="token-value">#6366f1</span>
                                </div>
                            </div>
                            <div class="token-item">
                                <div class="token-name">Secondary</div>
                                <div class="token-preview">
                                    <div class="color-swatch" style="background: #10b981;"></div>
                                    <span class="token-value">#10b981</span>
                                </div>
                            </div>
                            <div class="token-item">
                                <div class="token-name">Accent</div>
                                <div class="token-preview">
                                    <div class="color-swatch" style="background: #f59e0b;"></div>
                                    <span class="token-value">#f59e0b</span>
                                </div>
                            </div>
                            <div class="token-item">
                                <div class="token-name">Background</div>
                                <div class="token-preview">
                                    <div class="color-swatch" style="background: #ffffff;"></div>
                                    <span class="token-value">#ffffff</span>
                                </div>
                            </div>
                            <div class="token-item">
                                <div class="token-name">Text</div>
                                <div class="token-preview">
                                    <div class="color-swatch" style="background: #1e293b;"></div>
                                    <span class="token-value">#1e293b</span>
                                </div>
                            </div>
                        </div>
                        <button class="export-btn">Export CSS</button>
                    </div>

                    <div class="token-card">
                        <h4>🔤 Typography</h4>
                        <div class="token-list">
                            <div class="token-item">
                                <div class="token-name">Heading Font</div>
                                <span class="token-value">Inter, sans-serif</span>
                            </div>
                            <div class="token-item">
                                <div class="token-name">Body Font</div>
                                <span class="token-value">Inter, sans-serif</span>
                            </div>
                            <div class="token-item">
                                <div class="token-name">H1 Size</div>
                                <span class="token-value">2.5rem (40px)</span>
                            </div>
                            <div class="token-item">
                                <div class="token-name">H2 Size</div>
                                <span class="token-value">2rem (32px)</span>
                            </div>
                            <div class="token-item">
                                <div class="token-name">Body Size</div>
                                <span class="token-value">1rem (16px)</span>
                            </div>
                        </div>
                        <button class="export-btn">Export CSS</button>
                    </div>

                    <div class="token-card">
                        <h4>📐 Spacing</h4>
                        <div class="token-list">
                            <div class="token-item">
                                <div class="token-name">XS</div>
                                <span class="token-value">4px</span>
                            </div>
                            <div class="token-item">
                                <div class="token-name">SM</div>
                                <span class="token-value">8px</span>
                            </div>
                            <div class="token-item">
                                <div class="token-name">MD</div>
                                <span class="token-value">16px</span>
                            </div>
                            <div class="token-item">
                                <div class="token-name">LG</div>
                                <span class="token-value">24px</span>
                            </div>
                            <div class="token-item">
                                <div class="token-name">XL</div>
                                <span class="token-value">32px</span>
                            </div>
                        </div>
                        <button class="export-btn">Export CSS</button>
                    </div>

                    <div class="token-card">
                        <h4>🌗 Border Radius</h4>
                        <div class="token-list">
                            <div class="token-item">
                                <div class="token-name">Small</div>
                                <span class="token-value">4px</span>
                            </div>
                            <div class="token-item">
                                <div class="token-name">Medium</div>
                                <span class="token-value">8px</span>
                            </div>
                            <div class="token-item">
                                <div class="token-name">Large</div>
                                <span class="token-value">12px</span>
                            </div>
                            <div class="token-item">
                                <div class="token-name">XLarge</div>
                                <span class="token-value">16px</span>
                            </div>
                            <div class="token-item">
                                <div class="token-name">Round</div>
                                <span class="token-value">999px</span>
                            </div>
                        </div>
                        <button class="export-btn">Export CSS</button>
                    </div>

                    <div class="token-card">
                        <h4>✨ Shadows</h4>
                        <div class="token-list">
                            <div class="token-item">
                                <div class="token-name">Sm</div>
                                <span class="token-value">0 1px 2px rgb(0 0 0 / 0.05)</span>
                            </div>
                            <div class="token-item">
                                <div class="token-name">Md</div>
                                <span class="token-value">0 4px 6px rgb(0 0 0 / 0.1)</span>
                            </div>
                            <div class="token-item">
                                <div class="token-name">Lg</div>
                                <span class="token-value">0 10px 15px rgb(0 0 0 / 0.1)</span>
                            </div>
                            <div class="token-item">
                                <div class="token-name">Xl</div>
                                <span class="token-value">0 20px 25px rgb(0 0 0 / 0.1)</span>
                            </div>
                        </div>
                        <button class="export-btn">Export CSS</button>
                    </div>

                    <div class="token-card">
                        <h4>⚡ Transitions</h4>
                        <div class="token-list">
                            <div class="token-item">
                                <div class="token-name">Fast</div>
                                <span class="token-value">150ms ease</span>
                            </div>
                            <div class="token-item">
                                <div class="token-name">Normal</div>
                                <span class="token-value">300ms ease</span>
                            </div>
                            <div class="token-item">
                                <div class="token-name">Slow</div>
                                <span class="token-value">500ms ease</span>
                            </div>
                        </div>
                        <button class="export-btn">Export CSS</button>
                    </div>
                </div>
            </div>
        </div>
        """

    def _render_components(self) -> str:
        """Render component library."""
        return """
        <div style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .component-library {{ max-width: 1200px; }}
                .component-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; }}
                .component-card {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; transition: all 0.2s; }}
                .component-card:hover {{ border-color: #6366f1; transform: translateY(-4px); box-shadow: 0 20px 40px rgb(0 0 0 / 0.1); }}
                .component-header {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem; }}
                .component-name {{ font-size: 1.125rem; font-weight: 600; color: #1e293b; }}
                .component-badge {{ padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.75rem; font-weight: 600; }}
                .component-badge.default {{ background: #dcfce7; color: #16a34a; }}
                .component-preview {{ min-height: 100px; display: flex; align-items: center; justify-content: center; background: #f8fafc; border-radius: 8px; margin-bottom: 1rem; }}
                .component-btn {{ padding: 0.5rem 1rem; border: 2px solid #6366f1; border-radius: 8px; background: white; color: #6366f1; font-weight: 600; cursor: pointer; }}
                .component-btn:hover {{ background: #6366f1; color: white; }}
                .component-actions {{ display: flex; gap: 0.5rem; }}
                .component-action {{ flex: 1; padding: 0.5rem; border: 1px solid #e2e8f0; border-radius: 6px; background: white; cursor: pointer; font-size: 0.75rem; font-weight: 600; }}
                .component-action:hover {{ background: #f1f5f9; }}
            </style>

            <div class="component-library">
                <h3 style="margin-bottom: 1.5rem;">📦 Component Library</h3>

                <div class="component-grid">
                    <div class="component-card">
                        <div class="component-header">
                            <div class="component-name">Button</div>
                            <span class="component-badge default">5 variants</span>
                        </div>
                        <div class="component-preview">
                            <button class="component-btn">Button</button>
                        </div>
                        <div class="component-actions">
                            <button class="component-action">Preview</button>
                            <button class="component-action">Edit</button>
                            <button class="component-action">Copy</button>
                        </div>
                    </div>

                    <div class="component-card">
                        <div class="component-header">
                            <div class="component-name">Card</div>
                            <span class="component-badge default">3 variants</span>
                        </div>
                        <div class="component-preview">
                            <div style="width: 200px; background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 1rem;">
                                <div style="height: 100px; background: #e2e8f0; border-radius: 4px; margin-bottom: 0.75rem;"></div>
                                <div style="height: 12px; background: #e2e8f0; border-radius: 4px; width: 80%;"></div>
                            </div>
                        </div>
                        <div class="component-actions">
                            <button class="component-action">Preview</button>
                            <button class="component-action">Edit</button>
                            <button class="component-action">Copy</button>
                        </div>
                    </div>

                    <div class="component-card">
                        <div class="component-header">
                            <div class="component-name">Navigation</div>
                            <span class="component-badge default">4 variants</span>
                        </div>
                        <div class="component-preview">
                            <div style="display: flex; gap: 1rem; align-items: center;">
                                <span style="font-weight: 700;">Logo</span>
                                <span style="color: #64748b;">Home</span>
                                <span style="color: #64748b;">About</span>
                                <span style="color: #64748b;">Contact</span>
                            </div>
                        </div>
                        <div class="component-actions">
                            <button class="component-action">Preview</button>
                            <button class="component-action">Edit</button>
                            <button class="component-action">Copy</button>
                        </div>
                    </div>

                    <div class="component-card">
                        <div class="component-header">
                            <div class="component-name">Form</div>
                            <span class="component-badge default">6 variants</span>
                        </div>
                        <div class="component-preview">
                            <div style="width: 200px;">
                                <input type="text" placeholder="Enter your name" style="width: 100%; padding: 0.5rem; border: 1px solid #e2e8f0; border-radius: 6px;">
                            </div>
                        </div>
                        <div class="component-actions">
                            <button class="component-action">Preview</button>
                            <button class="component-action">Edit</button>
                            <button class="component-action">Copy</button>
                        </div>
                    </div>

                    <div class="component-card">
                        <div class="component-header">
                            <div class="component-name">Modal</div>
                            <span class="component-badge default">2 variants</span>
                        </div>
                        <div class="component-preview">
                            <div style="width: 200px; height: 120px; background: white; border: 2px solid #6366f1; border-radius: 8px; display: flex; align-items: center; justify-content: center; position: relative;">
                                <div style="position: absolute; top: -20px; left: 0; right: 0; bottom: 0; background: rgb(0 0 0 / 0.5); border-radius: 8px;"></div>
                                <span style="font-weight: 600;">Modal</span>
                            </div>
                        </div>
                        <div class="component-actions">
                            <button class="component-action">Preview</button>
                            <button class="component-action">Edit</button>
                            <button class="component-action">Copy</button>
                        </div>
                    </div>

                    <div class="component-card">
                        <div class="component-header">
                            <div class="component-name">Alert</div>
                            <span class="component-badge default">4 variants</span>
                        </div>
                        <div class="component-preview">
                            <div style="width: 200px; padding: 0.75rem; background: #dcfce7; border-left: 4px solid #16a34a; border-radius: 4px; font-size: 0.875rem;">
                                ✅ Success message
                            </div>
                        </div>
                        <div class="component-actions">
                            <button class="component-action">Preview</button>
                            <button class="component-action">Edit</button>
                            <button class="component-action">Copy</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """

    def _render_style_guide(self) -> str:
        """Render style guide."""
        return """
        <div style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .style-guide {{ max-width: 1000px; }}
                .guide-section {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 2rem; margin-bottom: 1.5rem; }}
                .guide-section h3 {{ font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0 0 1.5rem; }}
                .guide-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; }}
                .guide-item {{ text-align: center; }}
                .guide-preview {{ height: 80px; background: #6366f1; border-radius: 8px; margin-bottom: 0.75rem; display: flex; align-items: center; justify-content: center; color: white; font-weight: 600; }}
                .guide-label {{ font-size: 0.875rem; color: #64748b; }}
                .export-btn {{ padding: 1rem 2rem; background: #6366f1; color: white; border: none; border-radius: 12px; font-weight: 600; cursor: pointer; }}
            </style>

            <div class="style-guide">
                <h2 style="margin-bottom: 1.5rem;">📖 Style Guide</h2>

                <div class="guide-section">
                    <h3>🎨 Colors</h3>
                    <div class="guide-grid">
                        <div class="guide-item">
                            <div class="guide-preview" style="background: #6366f1;">Primary</div>
                            <div class="guide-label">#6366f1</div>
                        </div>
                        <div class="guide-item">
                            <div class="guide-preview" style="background: #10b981;">Secondary</div>
                            <div class="guide-label">#10b981</div>
                        </div>
                        <div class="guide-item">
                            <div class="guide-preview" style="background: #f59e0b;">Accent</div>
                            <div class="guide-label">#f59e0b</div>
                        </div>
                        <div class="guide-item">
                            <div class="guide-preview" style="background: #1e293b; color: white;">Dark</div>
                            <div class="guide-label">#1e293b</div>
                        </div>
                    </div>
                </div>

                <div class="guide-section">
                    <h3>🔤 Typography</h3>
                    <div style="display: flex; flex-direction: column; gap: 1.5rem;">
                        <div>
                            <h1 style="font-size: 3rem; font-weight: 700; margin: 0;">Heading 1 - 40px</h1>
                        </div>
                        <div>
                            <h2 style="font-size: 2.5rem; font-weight: 700; margin: 0;">Heading 2 - 32px</h2>
                        </div>
                        <div>
                            <h3 style="font-size: 2rem; font-weight: 600; margin: 0;">Heading 3 - 24px</h3>
                        </div>
                        <div>
                            <p style="font-size: 1rem; color: #64748b; margin: 0;">Body text - 16px - This is how your body text will look throughout the design.</p>
                        </div>
                    </div>
                </div>

                <div class="guide-section">
                    <h3>📏 Spacing Scale</h3>
                    <div style="display: flex; align-items: flex-end; gap: 1rem;">
                        <div style="width: 4px; height: 4px; background: #6366f1; border-radius: 2px;" title="4px"></div>
                        <div style="width: 8px; height: 8px; background: #6366f1; border-radius: 4px;" title="8px"></div>
                        <div style="width: 16px; height: 16px; background: #6366f1; border-radius: 8px;" title="16px"></div>
                        <div style="width: 24px; height: 24px; background: #6366f1; border-radius: 12px;" title="24px"></div>
                        <div style="width: 32px; height: 32px; background: #6366f1; border-radius: 16px;" title="32px"></div>
                    </div>
                </div>

                <button class="export-btn">📄 Export Complete Style Guide</button>
            </div>
        </div>
        """
