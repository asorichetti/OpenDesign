"""
title: OpenDesigner Component Library
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesigner
version: 0.1.0
required_open_webui_version: 0.10.0
"""

from typing import Any


class ComponentLibrary:
    """OpenDesigner Component Library — Storybook-like component browser."""

    def __init__(self):
        self.type = "action"

    def actions(self) -> list[dict[str, str]]:
        """Return available actions."""
        return [
            {
                "name": "Component Library",
                "description": "Browse and insert pre-built components",
                "icon": "blocks",
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
        if action == "Component Library":
            return self._render_library()
        return f"Unknown action: {action}"

    def _render_library(self) -> str:
        """Render component library UI."""
        components = [
            {"name": "Button", "icon": "🔘", "categories": ["UI"]},
            {"name": "Card", "icon": "🃏", "categories": ["Layout"]},
            {"name": "Navigation", "icon": "🧭", "categories": ["Navigation"]},
            {"name": "Hero Section", "icon": "🌟", "categories": ["Layout"]},
            {"name": "Pricing Table", "icon": "💰", "categories": ["Business"]},
            {"name": "Form", "icon": "📝", "categories": ["UI"]},
            {"name": "Modal", "icon": "📦", "categories": ["UI"]},
            {"name": "Carousel", "icon": "🎠", "categories": ["Interactive"]},
            {"name": "Accordion", "icon": "🪗", "categories": ["Interactive"]},
            {"name": "Tabs", "icon": "📑", "categories": ["UI"]},
            {"name": "Footer", "icon": "👣", "categories": ["Layout"]},
            {"name": "Alert", "icon": "⚠️", "categories": ["UI"]},
        ]

        components_html = ""
        for comp in components:
            categories_str = ", ".join(comp["categories"])
            components_html += f"""
            <div class="component-card" onclick="alert('Insert {comp["name"]} component')">
                <div class="component-icon">{comp["icon"]}</div>
                <div class="component-name">{comp["name"]}</div>
                <div class="component-categories">{categories_str}</div>
            </div>
            """

        return f"""
        <div class="component-library" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .component-library {{ max-width: 1200px; margin: 0 auto; }}
                .library-header {{ text-align: center; margin-bottom: 2rem; }}
                .library-header h3 {{ font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0 0 0.5rem; }}
                .library-header p {{ color: #64748b; margin: 0; }}
                .search-bar {{ max-width: 400px; margin: 0 auto 2rem; position: relative; }}
                .search-input {{ width: 100%; padding: 0.75rem 1rem 0.75rem 2.5rem; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 0.875rem; outline: none; transition: border-color 0.2s; }}
                .search-input:focus {{ border-color: #6366f1; }}
                .search-icon {{ position: absolute; left: 0.75rem; top: 50%; transform: translateY(-50%); color: #94a3b8; }}
                .components-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem; }}
                .component-card {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; text-align: center; cursor: pointer; transition: all 0.2s ease; }}
                .component-card:hover {{ border-color: #6366f1; background: #f0f0ff; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15); }}
                .component-icon {{ font-size: 2.5rem; margin-bottom: 0.75rem; }}
                .component-name {{ font-weight: 600; color: #1e293b; margin-bottom: 0.25rem; }}
                .component-categories {{ font-size: 0.75rem; color: #64748b; }}
                .library-footer {{ text-align: center; margin-top: 2rem; padding: 1rem; background: #f8fafc; border-radius: 8px; color: #64748b; }}
            </style>
            <div class="library-header">
                <h3>🧩 Component Library</h3>
                <p>Browse and insert pre-built components into your design</p>
            </div>
            <div class="search-bar">
                <span class="search-icon">🔍</span>
                <input type="text" class="search-input" placeholder="Search components..." />
            </div>
            <div class="components-grid">
                {components_html}
            </div>
            <div class="library-footer">💡 Click on any component to insert it into your design</div>
        </div>
        """
