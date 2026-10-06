"""
title: OpenDesigner Export Formats
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesigner
version: 0.1.0
required_open_webui_version: 0.10.0
"""

import json
import re
from typing import Any


class ExportFormats:
    """OpenDesigner Export — export designs to multiple formats."""

    def __init__(self):
        self.type = "action"

    def actions(self) -> list[dict[str, str]]:
        """Return available actions."""
        return [
            {
                "name": "Export SVG",
                "description": "Export design as SVG vector graphics",
                "icon": "image",
            },
            {
                "name": "Export JSON",
                "description": "Export design data as JSON",
                "icon": "code",
            },
            {
                "name": "Export HTML",
                "description": "Export design as standalone HTML file",
                "icon": "file-text",
            },
            {
                "name": "Export PNG",
                "description": "Export design preview as PNG image",
                "icon": "camera",
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
        """Handle action click."""
        if action == "Export SVG":
            return self._export_svg(body)
        elif action == "Export JSON":
            return self._export_json(body)
        elif action == "Export HTML":
            return self._export_html(body)
        elif action == "Export PNG":
            return self._export_png(body)

        return f"Unknown action: {action}"

    def _export_svg(self, body: dict) -> str:
        """Generate SVG export UI."""
        html_content = body.get("message", {}).get("content", "")

        # Extract simple shapes from HTML for SVG conversion
        svg_content = self._html_to_svg(html_content)

        return f"""
        <div class="export-svg" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .export-svg {{ max-width: 800px; margin: 0 auto; }}
                .export-header {{ text-align: center; margin-bottom: 2rem; }}
                .export-header h3 {{ font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0 0 0.5rem; }}
                .export-header p {{ color: #64748b; margin: 0; }}
                .export-card {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; }}
                .export-label {{ font-size: 0.875rem; font-weight: 600; color: #475569; margin-bottom: 0.75rem; }}
                .svg-preview {{ background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 1rem; margin-bottom: 1rem; min-height: 200px; display: flex; align-items: center; justify-content: center; }}
                .svg-code {{ background: #1e293b; color: #e2e8f0; padding: 1rem; border-radius: 8px; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; line-height: 1.6; max-height: 300px; overflow: auto; white-space: pre-wrap; word-wrap: break-word; }}
                .export-btn {{ display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.625rem 1.25rem; background: #6366f1; color: white; border: none; border-radius: 8px; font-size: 0.875rem; font-weight: 600; cursor: pointer; transition: all 0.2s; }}
                .export-btn:hover {{ background: #4f46e5; }}
            </style>

            <div class="export-header">
                <h3>🎨 Export as SVG</h3>
                <p>Vector graphics format for scalable design assets</p>
            </div>

            <div class="export-card">
                <div class="export-label">Preview</div>
                <div class="svg-preview">
                    {svg_content}
                </div>
                <div class="export-label">SVG Code</div>
                <div class="svg-code">{svg_content}</div>
                <button class="export-btn" onclick="navigator.clipboard.writeText(this.parentElement.querySelector('.svg-code').textContent)">📋 Copy SVG Code</button>
            </div>
        </div>
        """

    def _html_to_svg(self, html: str) -> str:
        """Convert HTML content to SVG representation."""
        # Extract title or create default
        title_match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE)
        title = title_match.group(1) if title_match else "Design"

        return f"""<svg width="400" height="300" viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
    <rect width="400" height="300" fill="#f8fafc"/>
    <rect x="50" y="50" width="300" height="40" fill="#6366f1" rx="8"/>
    <text x="200" y="75" text-anchor="middle" fill="white" font-family="system-ui" font-size="16" font-weight="600">{title}</text>
    <rect x="50" y="110" width="130" height="140" fill="white" stroke="#e2e8f0" rx="8"/>
    <rect x="220" y="110" width="130" height="140" fill="white" stroke="#e2e8f0" rx="8"/>
    <text x="200" y="280" text-anchor="middle" fill="#64748b" font-family="system-ui" font-size="12">SVG Export Preview</text>
</svg>"""

    def _export_json(self, body: dict) -> str:
        """Generate JSON export UI."""
        html_content = body.get("message", {}).get("content", "")

        # Parse HTML structure to JSON
        export_data = self._html_to_json(html_content)

        json_str = json.dumps(export_data, indent=2)

        return f"""
        <div class="export-json" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .export-json {{ max-width: 800px; margin: 0 auto; }}
                .export-header {{ text-align: center; margin-bottom: 2rem; }}
                .export-header h3 {{ font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0 0 0.5rem; }}
                .export-header p {{ color: #64748b; margin: 0; }}
                .export-card {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; }}
                .export-label {{ font-size: 0.875rem; font-weight: 600; color: #475569; margin-bottom: 0.75rem; }}
                .json-code {{ background: #1e293b; color: #e2e8f0; padding: 1rem; border-radius: 8px; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; line-height: 1.6; max-height: 400px; overflow: auto; white-space: pre-wrap; word-wrap: break-word; }}
                .export-btn {{ display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.625rem 1.25rem; background: #6366f1; color: white; border: none; border-radius: 8px; font-size: 0.875rem; font-weight: 600; cursor: pointer; transition: all 0.2s; margin-top: 1rem; }}
                .export-btn:hover {{ background: #4f46e5; }}
            </style>

            <div class="export-header">
                <h3>📄 Export as JSON</h3>
                <p>Structured data format for programmatic use</p>
            </div>

            <div class="export-card">
                <div class="export-label">Export Data</div>
                <div class="json-code">{json_str}</div>
                <button class="export-btn" onclick="navigator.clipboard.writeText(this.parentElement.querySelector('.json-code').textContent)">📋 Copy JSON</button>
            </div>
        </div>
        """

    def _html_to_json(self, html: str) -> dict:
        """Convert HTML content to JSON structure."""
        import re

        # Extract basic structure
        title_match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE)
        meta_matches = re.findall(r'<meta\s+name="(.*?)"\s+content="(.*?)"', html, re.IGNORECASE)

        return {
            "type": "html-design",
            "version": "1.0.0",
            "title": title_match.group(1) if title_match else "Untitled Design",
            "meta": dict(meta_matches),
            "structure": {
                "doctype": "html5",
                "lang": "en",
                "head": {"title": title_match.group(1) if title_match else "Untitled"},
                "body": "Contains HTML elements and styling",
            },
            "metadata": {
                "exported_at": "2024",
                "exporter": "OpenDesigner",
                "format": "json",
            },
        }

    def _export_html(self, body: dict) -> str:
        """Generate HTML export UI."""
        html_content = body.get("message", {}).get("content", "")

        return f"""
        <div class="export-html" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .export-html {{ max-width: 800px; margin: 0 auto; }}
                .export-header {{ text-align: center; margin-bottom: 2rem; }}
                .export-header h3 {{ font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0 0 0.5rem; }}
                .export-header p {{ color: #64748b; margin: 0; }}
                .export-card {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; }}
                .export-label {{ font-size: 0.875rem; font-weight: 600; color: #475569; margin-bottom: 0.75rem; }}
                .html-code {{ background: #1e293b; color: #e2e8f0; padding: 1rem; border-radius: 8px; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; line-height: 1.6; max-height: 400px; overflow: auto; white-space: pre-wrap; word-wrap: break-word; }}
                .export-btn {{ display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.625rem 1.25rem; background: #6366f1; color: white; border: none; border-radius: 8px; font-size: 0.875rem; font-weight: 600; cursor: pointer; transition: all 0.2s; margin-top: 1rem; }}
                .export-btn:hover {{ background: #4f46e5; }}
            </style>

            <div class="export-header">
                <h3>🌐 Export as HTML</h3>
                <p>Standalone HTML file ready for deployment</p>
            </div>

            <div class="export-card">
                <div class="export-label">HTML Code</div>
                <div class="html-code">{html_content}</div>
                <button class="export-btn" onclick="navigator.clipboard.writeText(this.parentElement.querySelector('.html-code').textContent)">📋 Copy HTML</button>
                <button class="export-btn" style="margin-left: 0.5rem; background: #10b981;" onclick="window.open('data:text/html;charset=utf-8,' + encodeURIComponent(this.parentElement.querySelector('.html-code').textContent))">💾 Download HTML</button>
            </div>
        </div>
        """

    def _export_png(self, body: dict) -> str:
        """Generate PNG export UI."""
        html_content = body.get("message", {}).get("content", "")

        # Create a data URL for preview
        escaped_html = html_content.replace('"', '\\"').replace("\n", "\\n")

        return f"""
        <div class="export-png" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .export-png {{ max-width: 800px; margin: 0 auto; }}
                .export-header {{ text-align: center; margin-bottom: 2rem; }}
                .export-header h3 {{ font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0 0 0.5rem; }}
                .export-header p {{ color: #64748b; margin: 0; }}
                .export-card {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; text-align: center; }}
                .preview-frame {{ width: 100%; height: 400px; border: 1px solid #e2e8f0; border-radius: 8px; margin-bottom: 1rem; }}
                .export-btn {{ display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.625rem 1.25rem; background: #6366f1; color: white; border: none; border-radius: 8px; font-size: 0.875rem; font-weight: 600; cursor: pointer; transition: all 0.2s; margin: 0.25rem; }}
                .export-btn:hover {{ background: #4f46e5; }}
                .note {{ margin-top: 1rem; padding: 1rem; background: #fef3c7; border-radius: 8px; color: #92400e; font-size: 0.875rem; }}
            </style>

            <div class="export-header">
                <h3>📸 Export as PNG</h3>
                <p>Raster image format for presentations and sharing</p>
            </div>

            <div class="export-card">
                <iframe class="preview-frame" srcdoc="{escaped_html}" sandbox="allow-scripts"></iframe>
                <button class="export-btn">📸 Screenshot & Download PNG</button>
                <div class="note">
                    💡 <strong>Note:</strong> For best results, use your browser's native screenshot tool (Cmd+Shift+4 on Mac, Win+Shift+S on Windows)
                </div>
            </div>
        </div>
        """
