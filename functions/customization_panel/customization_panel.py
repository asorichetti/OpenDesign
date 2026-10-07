"""
title: Visual Customization Panel
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesigner
version: 1.0.0
required_open_webui_version: 0.10.0
"""

from typing import Any


class CustomizationPanel:
    """Visual Customization Panel — Tweak designs without touching code."""

    def __init__(self):
        self.type = "action"
        self.customizations = {}

    def actions(self) -> list[dict[str, str]]:
        """Return available actions."""
        return [
            {
                "name": "Visual Customizer",
                "description": "Customize colors, fonts, spacing, and layout visually",
                "icon": "palette",
            },
            {
                "name": "Theme Builder",
                "description": "Create and manage custom themes",
                "icon": "sun",
            },
            {
                "name": "Layout Editor",
                "description": "Adjust layout, spacing, and alignment",
                "icon": "layout",
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
        """Handle customization action."""
        if action == "Visual Customizer":
            return self._render_customizer(body)
        elif action == "Theme Builder":
            return self._render_theme_builder()
        elif action == "Layout Editor":
            return self._render_layout_editor()

        return f"Unknown action: {action}"

    def _render_customizer(self, body: dict) -> str:
        """Render visual customizer."""
        return """
        <div class="customizer" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .customizer {{ max-width: 1200px; margin: 0 auto; }}
                .customizer-grid {{ display: grid; grid-template-columns: 300px 1fr; gap: 2rem; }}
                .customizer-panel {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; }}
                .customizer-preview {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; }}
                .customizer-panel h3 {{ font-size: 1.25rem; font-weight: 700; color: #1e293b; margin: 0 0 1.5rem; }}
                .control-group {{ margin-bottom: 1.5rem; }}
                .control-group label {{ display: block; font-size: 0.875rem; font-weight: 600; color: #1e293b; margin-bottom: 0.5rem; }}
                .color-picker {{ display: flex; align-items: center; gap: 0.75rem; }}
                .color-picker input[type="color"] {{ width: 48px; height: 48px; border: 2px solid #e2e8f0; border-radius: 8px; cursor: pointer; }}
                .color-picker input[type="text"] {{ flex: 1; padding: 0.75rem; border: 1px solid #e2e8f0; border-radius: 8px; font-family: monospace; }}
                .range-control {{ display: flex; align-items: center; gap: 1rem; }}
                .range-control input[type="range"] {{ flex: 1; }}
                .range-control span {{ min-width: 50px; font-size: 0.875rem; color: #64748b; }}
                .font-selector {{ display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; }}
                .font-option {{ padding: 0.75rem; border: 2px solid #e2e8f0; border-radius: 8px; cursor: pointer; text-align: center; transition: all 0.2s; }}
                .font-option:hover, .font-option.active {{ border-color: #6366f1; background: #f8fafc; }}
                .font-option .preview {{ font-size: 1.25rem; margin-bottom: 0.25rem; }}
                .font-option .name {{ font-size: 0.75rem; color: #64748b; }}
                .spacing-control {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.75rem; }}
                .spacing-input {{ padding: 0.5rem; border: 1px solid #e2e8f0; border-radius: 6px; width: 100%; }}
                .apply-btn {{ width: 100%; padding: 1rem; background: #6366f1; color: white; border: none; border-radius: 12px; font-weight: 600; cursor: pointer; margin-top: 1.5rem; }}
                .apply-btn:hover {{ background: #4f46e5; }}
                .preview-container {{ position: relative; }}
                .preview-frame {{ width: 100%; height: 600px; border: 1px solid #e2e8f0; border-radius: 8px; }}
                .toolbar {{ display: flex; gap: 0.75rem; margin-bottom: 1rem; }}
                .toolbar-btn {{ padding: 0.5rem 1rem; border: 1px solid #e2e8f0; border-radius: 6px; background: white; cursor: pointer; font-size: 0.875rem; }}
                .toolbar-btn.active {{ background: #6366f1; color: white; border-color: #6366f1; }}
            </style>

            <div class="customizer-grid">
                <div class="customizer-panel">
                    <h3>🎨 Customize Design</h3>

                    <div class="control-group">
                        <label>Primary Color</label>
                        <div class="color-picker">
                            <input type="color" id="primary-color" value="#6366f1" onchange="updateColor('primary', this.value)">
                            <input type="text" id="primary-color-text" value="#6366f1" onchange="updateColor('primary', this.value)">
                        </div>
                    </div>

                    <div class="control-group">
                        <label>Secondary Color</label>
                        <div class="color-picker">
                            <input type="color" id="secondary-color" value="#8b5cf6" onchange="updateColor('secondary', this.value)">
                            <input type="text" id="secondary-color-text" value="#8b5cf6" onchange="updateColor('secondary', this.value)">
                        </div>
                    </div>

                    <div class="control-group">
                        <label>Background Color</label>
                        <div class="color-picker">
                            <input type="color" id="bg-color" value="#ffffff" onchange="updateColor('bg', this.value)">
                            <input type="text" id="bg-color-text" value="#ffffff" onchange="updateColor('bg', this.value)">
                        </div>
                    </div>

                    <div class="control-group">
                        <label>Text Color</label>
                        <div class="color-picker">
                            <input type="color" id="text-color" value="#1e293b" onchange="updateColor('text', this.value)">
                            <input type="text" id="text-color-text" value="#1e293b" onchange="updateColor('text', this.value)">
                        </div>
                    </div>

                    <div class="control-group">
                        <label>Font Family</label>
                        <div class="font-selector">
                            <div class="font-option active" onclick="selectFont('system-ui', this)">
                                <div class="preview" style="font-family: system-ui">Aa</div>
                                <div class="name">System</div>
                            </div>
                            <div class="font-option" onclick="selectFont('Georgia', this)">
                                <div class="preview" style="font-family: Georgia">Aa</div>
                                <div class="name">Serif</div>
                            </div>
                            <div class="font-option" onclick="selectFont('Courier New', this)">
                                <div class="preview" style="font-family: 'Courier New'">Aa</div>
                                <div class="name">Mono</div>
                            </div>
                            <div class="font-option" onclick="selectFont('Inter', this)">
                                <div class="preview" style="font-family: Inter">Aa</div>
                                <div class="name">Modern</div>
                            </div>
                        </div>
                    </div>

                    <div class="control-group">
                        <label>Border Radius</label>
                        <div class="range-control">
                            <input type="range" id="border-radius" min="0" max="24" value="12" oninput="updateRadius(this.value)">
                            <span id="radius-value">12px</span>
                        </div>
                    </div>

                    <div class="control-group">
                        <label>Spacing Scale</label>
                        <div class="range-control">
                            <input type="range" id="spacing-scale" min="0.5" max="2" step="0.125" value="1" oninput="updateSpacing(this.value)">
                            <span id="spacing-value">1x</span>
                        </div>
                    </div>

                    <button class="apply-btn" onclick="applyCustomizations()">Apply Customizations</button>
                </div>

                <div class="customizer-preview">
                    <h3 style="font-size: 1.25rem; font-weight: 700; color: #1e293b; margin: 0 0 1rem;">👁️ Live Preview</h3>
                    <div class="toolbar">
                        <button class="toolbar-btn active">Desktop</button>
                        <button class="toolbar-btn">Tablet</button>
                        <button class="toolbar-btn">Mobile</button>
                    </div>
                    <div class="preview-container">
                        <iframe class="preview-frame" srcdoc="<html><body style='padding: 2rem; font-family: system-ui;'><h1 style='color: #6366f1;'>Your Design</h1><p style='color: #64748b;'>Customize using the panel on the left</p></body></html>" sandbox="allow-scripts"></iframe>
                    </div>
                </div>
            </div>

            <script>
                let currentCustomizations = {{
                    primary: '#6366f1',
                    secondary: '#8b5cf6',
                    bg: '#ffffff',
                    text: '#1e293b',
                    fontFamily: 'system-ui',
                    borderRadius: '12px',
                    spacingScale: '1x'
                }};

                function updateColor(type, value) {{
                    currentCustomizations[type] = value;
                    document.getElementById(type + '-color-text').value = value;
                    document.getElementById(type + '-color').value = value;
                }}

                function selectFont(font, element) {{
                    currentCustomizations.fontFamily = font;
                    document.querySelectorAll('.font-option').forEach(el => el.classList.remove('active'));
                    element.classList.add('active');
                }}

                function updateRadius(value) {{
                    currentCustomizations.borderRadius = value + 'px';
                    document.getElementById('radius-value').textContent = value + 'px';
                }}

                function updateSpacing(value) {{
                    currentCustomizations.spacingScale = value + 'x';
                    document.getElementById('spacing-value').textContent = value + 'x';
                }}

                function applyCustomizations() {{
                    const event = new CustomEvent('applyCustomizations', {{ detail: currentCustomizations }});
                    window.parent.postMessage(event, '*');
                }}
            </script>
        </div>
        """

    def _render_theme_builder(self) -> str:
        """Render theme builder."""
        return """
        <div style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .theme-builder {{ max-width: 1000px; }}
                .theme-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; }}
                .theme-card {{ background: white; border: 2px solid #e2e8f0; border-radius: 12px; overflow: hidden; cursor: pointer; transition: all 0.2s; }}
                .theme-card:hover {{ border-color: #6366f1; transform: translateY(-4px); }}
                .theme-preview {{ height: 150px; display: flex; align-items: center; justify-content: center; }}
                .theme-info {{ padding: 1rem; }}
                .theme-info h4 {{ font-size: 1rem; font-weight: 600; color: #1e293b; margin: 0 0 0.5rem; }}
                .theme-info p {{ font-size: 0.875rem; color: #64748b; margin: 0; }}
                .theme-colors {{ display: flex; gap: 0.5rem; margin-top: 0.75rem; }}
                .theme-color {{ width: 24px; height: 24px; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgb(0 0 0 / 0.1); }}
                .create-theme {{ background: #f8fafc; border: 2px dashed #e2e8f0; border-radius: 12px; padding: 2rem; text-align: center; cursor: pointer; }}
                .create-theme:hover {{ border-color: #6366f1; background: #f1f5f9; }}
            </style>

            <div class="theme-builder">
                <h3 style="margin-bottom: 1.5rem;">🎨 Theme Builder</h3>

                <div class="theme-grid">
                    <div class="theme-card" onclick="selectTheme('light')">
                        <div class="theme-preview" style="background: #ffffff;">
                            <span style="font-size: 2rem;">☀️</span>
                        </div>
                        <div class="theme-info">
                            <h4>Light Theme</h4>
                            <p>Clean, bright, professional</p>
                            <div class="theme-colors">
                                <div class="theme-color" style="background: #6366f1;"></div>
                                <div class="theme-color" style="background: #1e293b;"></div>
                                <div class="theme-color" style="background: #ffffff;"></div>
                            </div>
                        </div>
                    </div>

                    <div class="theme-card" onclick="selectTheme('dark')">
                        <div class="theme-preview" style="background: #0f172a;">
                            <span style="font-size: 2rem;">🌙</span>
                        </div>
                        <div class="theme-info">
                            <h4>Dark Theme</h4>
                            <p>Deep, modern, elegant</p>
                            <div class="theme-colors">
                                <div class="theme-color" style="background: #818cf8;"></div>
                                <div class="theme-color" style="background: #e2e8f0;"></div>
                                <div class="theme-color" style="background: #0f172a;"></div>
                            </div>
                        </div>
                    </div>

                    <div class="theme-card" onclick="selectTheme('ocean')">
                        <div class="theme-preview" style="background: linear-gradient(135deg, #0ea5e9, #6366f1);">
                            <span style="font-size: 2rem;">🌊</span>
                        </div>
                        <div class="theme-info">
                            <h4>Ocean Theme</h4>
                            <p>Calm, professional, trustworthy</p>
                            <div class="theme-colors">
                                <div class="theme-color" style="background: #0ea5e9;"></div>
                                <div class="theme-color" style="background: #0f172a;"></div>
                                <div class="theme-color" style="background: #ffffff;"></div>
                            </div>
                        </div>
                    </div>

                    <div class="create-theme" onclick="createCustomTheme()">
                        <span style="font-size: 3rem;">➕</span>
                        <h4 style="margin: 1rem 0 0.5rem; color: #1e293b;">Create Custom Theme</h4>
                        <p style="color: #64748b;">Design your own unique theme</p>
                    </div>
                </div>
            </div>

            <script>
                function selectTheme(theme) {{
                    const event = new CustomEvent('selectTheme', {{ detail: {{ theme: theme }} }});
                    window.parent.postMessage(event, '*');
                }}

                function createCustomTheme() {{
                    const event = new CustomEvent('createTheme', {{}});
                    window.parent.postMessage(event, '*');
                }}
            </script>
        </div>
        """

    def _render_layout_editor(self) -> str:
        """Render layout editor."""
        return """
        <div style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .layout-editor {{ max-width: 1000px; }}
                .layout-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; }}
                .layout-option {{ background: white; border: 2px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; cursor: pointer; text-align: center; transition: all 0.2s; }}
                .layout-option:hover {{ border-color: #6366f1; transform: translateY(-2px); }}
                .layout-preview {{ width: 100%; height: 120px; margin-bottom: 1rem; }}
                .layout-option h4 {{ font-size: 0.875rem; font-weight: 600; color: #1e293b; margin: 0; }}
            </style>

            <div class="layout-editor">
                <h3 style="margin-bottom: 1.5rem;">📐 Layout Editor</h3>

                <div class="layout-grid">
                    <div class="layout-option" onclick="selectLayout('single-column')">
                        <svg class="layout-preview" viewBox="0 0 200 120">
                            <rect x="40" y="20" width="120" height="80" rx="8" fill="#e2e8f0"/>
                        </svg>
                        <h4>Single Column</h4>
                    </div>

                    <div class="layout-option" onclick="selectLayout('two-column')">
                        <svg class="layout-preview" viewBox="0 0 200 120">
                            <rect x="20" y="20" width="70" height="80" rx="8" fill="#e2e8f0"/>
                            <rect x="110" y="20" width="70" height="80" rx="8" fill="#e2e8f0"/>
                        </svg>
                        <h4>Two Column</h4>
                    </div>

                    <div class="layout-option" onclick="selectLayout('three-column')">
                        <svg class="layout-preview" viewBox="0 0 200 120">
                            <rect x="15" y="20" width="50" height="80" rx="8" fill="#e2e8f0"/>
                            <rect x="75" y="20" width="50" height="80" rx="8" fill="#e2e8f0"/>
                            <rect x="135" y="20" width="50" height="80" rx="8" fill="#e2e8f0"/>
                        </svg>
                        <h4>Three Column</h4>
                    </div>

                    <div class="layout-option" onclick="selectLayout('hero-sidebar')">
                        <svg class="layout-preview" viewBox="0 0 200 120">
                            <rect x="20" y="20" width="120" height="80" rx="8" fill="#e2e8f0"/>
                            <rect x="150" y="20" width="30" height="80" rx="8" fill="#cbd5e1"/>
                        </svg>
                        <h4>Hero + Sidebar</h4>
                    </div>
                </div>
            </div>

            <script>
                function selectLayout(layout) {{
                    const event = new CustomEvent('selectLayout', {{ detail: {{ layout: layout }} }});
                    window.parent.postMessage(event, '*');
                }}
            </script>
        </div>
        """
