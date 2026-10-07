"""
title: Framework Export
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesigner
version: 1.0.0
required_open_webui_version: 0.10.0
"""

from typing import Any


class FrameworkExport:
    """Framework Export — Export designs as React, Vue, or Next.js code."""

    def __init__(self):
        self.type = "action"

    def actions(self) -> list[dict[str, str]]:
        """Return available actions."""
        return [
            {
                "name": "Export to React",
                "description": "Export as React component with JSX",
                "icon": "react",
            },
            {
                "name": "Export to Vue",
                "description": "Export as Vue component",
                "icon": "vue",
            },
            {
                "name": "Export to Next.js",
                "description": "Export as Next.js page with TypeScript",
                "icon": "nextjs",
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
        """Handle export action."""
        if action == "Export to React":
            return self._render_export_ui("react", body)
        elif action == "Export to Vue":
            return self._render_export_ui("vue", body)
        elif action == "Export to Next.js":
            return self._render_export_ui("nextjs", body)

        return f"Unknown action: {action}"

    def _render_export_ui(self, framework: str, body: dict) -> str:
        """Render export interface."""
        framework_labels = {
            "react": "React",
            "vue": "Vue",
            "nextjs": "Next.js",
        }

        framework_extensions = {
            "react": ".jsx",
            "vue": ".vue",
            "nextjs": ".tsx",
        }

        label = framework_labels.get(framework, "React")
        extension = framework_extensions.get(framework, ".jsx")

        return f"""
        <div class="export-panel" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .export-panel {{ max-width: 1200px; }}
                .export-header {{ text-align: center; margin-bottom: 2rem; }}
                .export-header h3 {{ font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0 0 0.5rem; }}
                .export-header p {{ color: #64748b; }}
                .framework-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; margin-bottom: 2rem; }}
                .framework-card {{ background: white; border: 2px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; text-align: center; cursor: pointer; transition: all 0.2s; }}
                .framework-card:hover {{ border-color: #6366f1; transform: translateY(-4px); }}
                .framework-card.active {{ border-color: #6366f1; background: #f8fafc; }}
                .framework-icon {{ font-size: 3rem; margin-bottom: 1rem; }}
                .framework-name {{ font-size: 1.125rem; font-weight: 600; color: #1e293b; margin: 0 0 0.5rem; }}
                .framework-desc {{ font-size: 0.875rem; color: #64748b; margin: 0; }}
                .export-options {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; }}
                .export-options h4 {{ font-size: 1.125rem; font-weight: 600; color: #1e293b; margin: 0 0 1rem; }}
                .option-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; }}
                .option-item {{ padding: 1rem; background: #f8fafc; border-radius: 8px; }}
                .option-item label {{ display: flex; align-items: center; gap: 0.5rem; cursor: pointer; }}
                .option-item input[type="checkbox"] {{ width: 18px; height: 18px; }}
                .option-item span {{ font-size: 0.875rem; color: #1e293b; }}
                .code-output {{ background: #1e293b; color: #e2e8f0; border-radius: 12px; padding: 1.5rem; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; line-height: 1.6; overflow-x: auto; max-height: 500px; overflow-y: auto; }}
                .export-btn {{ padding: 1rem 2rem; background: #6366f1; color: white; border: none; border-radius: 12px; font-weight: 600; cursor: pointer; font-size: 1rem; }}
                .export-btn:hover {{ background: #4f46e5; }}
                .copy-btn {{ padding: 0.75rem 1.5rem; background: #475569; color: white; border: none; border-radius: 8px; cursor: pointer; margin-bottom: 1rem; }}
            </style>

            <div class="export-header">
                <h3>🚀 Export to {label}</h3>
                <p>Convert your design to production-ready {label} code</p>
            </div>

            <div class="framework-grid">
                <div class="framework-card {{ 'active' if framework == 'react' else '' }}" onclick="selectFramework('react')">
                    <div class="framework-icon">⚛️</div>
                    <div class="framework-name">React</div>
                    <p class="framework-desc">Component-based UI library</p>
                </div>
                <div class="framework-card {{ 'active' if framework == 'vue' else '' }}" onclick="selectFramework('vue')">
                    <div class="framework-icon">💚</div>
                    <div class="framework-name">Vue</div>
                    <p class="framework-desc">Progressive JavaScript framework</p>
                </div>
                <div class="framework-card {{ 'active' if framework == 'nextjs' else '' }}" onclick="selectFramework('nextjs')">
                    <div class="framework-icon">▲</div>
                    <div class="framework-name">Next.js</div>
                    <p class="framework-desc">React framework for production</p>
                </div>
            </div>

            <div class="export-options">
                <h4>Export Options</h4>
                <div class="option-grid">
                    <div class="option-item">
                        <label>
                            <input type="checkbox" checked>
                            <span>Include CSS modules</span>
                        </label>
                    </div>
                    <div class="option-item">
                        <label>
                            <input type="checkbox" checked>
                            <span>Responsive design</span>
                        </label>
                    </div>
                    <div class="option-item">
                        <label>
                            <input type="checkbox">
                            <span>Include animations</span>
                        </label>
                    </div>
                    <div class="option-item">
                        <label>
                            <input type="checkbox">
                            <span>Accessibility attributes</span>
                        </label>
                    </div>
                </div>
            </div>

            <button class="export-btn" onclick="generateCode()">Generate {label} Code</button>

            <div id="code-output" class="code-output" style="display: none;"></div>
            <button class="copy-btn" id="copy-btn" style="display: none;" onclick="copyCode()">📋 Copy to Clipboard</button>

            <script>
                let currentFramework = '{framework}';

                function selectFramework(fw) {{
                    currentFramework = fw;
                    document.querySelectorAll('.framework-card').forEach(card => card.classList.remove('active'));
                    event.target.closest('.framework-card').classList.add('active');
                }}

                function generateCode() {{
                    const code = `// ${label} Component
// Generated by OpenDesigner
// Framework: ${label}
// Extension: ${extension}

import React from 'react';

export default function DesignComponent() {{
    return (
        <div className="design-container">
            <h1>Your Design</h1>
            <p>Exported from OpenDesigner</p>
        </div>
    );
}}`;

                    const output = document.getElementById('code-output');
                    output.textContent = code;
                    output.style.display = 'block';
                    document.getElementById('copy-btn').style.display = 'inline-block';
                }}

                function copyCode() {{
                    const code = document.getElementById('code-output').textContent;
                    navigator.clipboard.writeText(code).then(() => {{
                        alert('Code copied to clipboard!');
                    }});
                }}
            </script>
        </div>
        """
