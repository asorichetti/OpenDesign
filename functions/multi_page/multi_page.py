"""
title: Multi-Page Website Generator
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesigner
version: 1.0.0
required_open_webui_version: 0.10.0
"""

from typing import Any


class MultiPageGenerator:
    """Multi-Page Website Generator — Create multi-page websites with consistent design."""

    def __init__(self):
        self.type = "action"

    def actions(self) -> list[dict[str, str]]:
        """Return available actions."""
        return [
            {
                "name": "Multi-Page Generator",
                "description": "Generate a complete multi-page website",
                "icon": "layout",
            },
            {
                "name": "Page Manager",
                "description": "Manage pages, navigation, and site structure",
                "icon": "folder",
            },
            {
                "name": "Site Preview",
                "description": "Preview the entire site with navigation",
                "icon": "globe",
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
        """Handle multi-page action."""
        if action == "Multi-Page Generator":
            return self._render_generator(body)
        elif action == "Page Manager":
            return self._render_page_manager()
        elif action == "Site Preview":
            return self._render_site_preview(body)

        return f"Unknown action: {action}"

    def _render_generator(self, body: dict) -> str:
        """Render multi-page generator."""
        return """
        <div class="multi-page-gen" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .multi-page-gen {{ max-width: 1200px; margin: 0 auto; }}
                .generator-header {{ text-align: center; margin-bottom: 2rem; }}
                .generator-header h3 {{ font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0 0 0.5rem; }}
                .generator-header p {{ color: #64748b; }}
                .page-form {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; }}
                .form-row {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-bottom: 1rem; }}
                .form-group {{ display: flex; flex-direction: column; gap: 0.5rem; }}
                .form-group label {{ font-size: 0.875rem; font-weight: 600; color: #1e293b; }}
                .form-group input, .form-group select, .form-group textarea {{ padding: 0.75rem; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 0.875rem; }}
                .form-group textarea {{ min-height: 100px; resize: vertical; }}
                .generate-btn {{ padding: 1rem 2rem; background: #6366f1; color: white; border: none; border-radius: 12px; font-weight: 600; cursor: pointer; font-size: 1rem; }}
                .page-list {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; }}
                .page-item {{ display: flex; align-items: center; justify-content: space-between; padding: 1rem 1.5rem; border-bottom: 1px solid #e2e8f0; }}
                .page-item:last-child {{ border-bottom: none; }}
                .page-info {{ display: flex; align-items: center; gap: 1rem; }}
                .page-icon {{ font-size: 1.5rem; }}
                .page-details h4 {{ font-size: 0.875rem; font-weight: 600; color: #1e293b; margin: 0; }}
                .page-details span {{ font-size: 0.75rem; color: #64748b; }}
                .page-actions {{ display: flex; gap: 0.5rem; }}
                .page-btn {{ padding: 0.5rem 1rem; border: 1px solid #e2e8f0; border-radius: 6px; background: white; cursor: pointer; font-size: 0.75rem; font-weight: 600; }}
                .page-btn:hover {{ background: #f1f5f9; }}
            </style>

            <div class="multi-page-gen">
                <div class="generator-header">
                    <h3>🌐 Multi-Page Website Generator</h3>
                    <p>Create a complete website with multiple pages and consistent design</p>
                </div>

                <div class="page-form">
                    <h4 style="margin-bottom: 1rem;">➕ Add New Page</h4>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Page Name</label>
                            <input type="text" id="page-name" placeholder="Home, About, Contact, Services...">
                        </div>
                        <div class="form-group">
                            <label>Page URL Slug</label>
                            <input type="text" id="page-url" placeholder="home, about, contact, services...">
                        </div>
                        <div class="form-group">
                            <label>Page Type</label>
                            <select id="page-type">
                                <option value="landing">Landing Page</option>
                                <option value="about">About Page</option>
                                <option value="contact">Contact Page</option>
                                <option value="services">Services Page</option>
                                <option value="blog">Blog</option>
                                <option value="portfolio">Portfolio</option>
                                <option value="pricing">Pricing</option>
                                <option value="faq">FAQ</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-group" style="margin-bottom: 1rem;">
                        <label>Page Description</label>
                        <textarea id="page-desc" placeholder="Describe what this page should contain..."></textarea>
                    </div>
                    <button class="generate-btn" onclick="addPage()">Add Page</button>
                </div>

                <h4 style="margin-bottom: 1rem;">📄 Pages (3)</h4>
                <div class="page-list">
                    <div class="page-item">
                        <div class="page-info">
                            <span class="page-icon">🏠</span>
                            <div class="page-details">
                                <h4>Home</h4>
                                <span>/home - Landing page with hero section</span>
                            </div>
                        </div>
                        <div class="page-actions">
                            <button class="page-btn">Edit</button>
                            <button class="page-btn">Preview</button>
                            <button class="page-btn" style="color: #dc2626;">Delete</button>
                        </div>
                    </div>
                    <div class="page-item">
                        <div class="page-info">
                            <span class="page-icon">👥</span>
                            <div class="page-details">
                                <h4>About</h4>
                                <span>/about - Company information and team</span>
                            </div>
                        </div>
                        <div class="page-actions">
                            <button class="page-btn">Edit</button>
                            <button class="page-btn">Preview</button>
                            <button class="page-btn" style="color: #dc2626;">Delete</button>
                        </div>
                    </div>
                    <div class="page-item">
                        <div class="page-info">
                            <span class="page-icon">✉️</span>
                            <div class="page-details">
                                <h4>Contact</h4>
                                <span>/contact - Contact form and map</span>
                            </div>
                        </div>
                        <div class="page-actions">
                            <button class="page-btn">Edit</button>
                            <button class="page-btn">Preview</button>
                            <button class="page-btn" style="color: #dc2626;">Delete</button>
                        </div>
                    </div>
                </div>

                <div style="margin-top: 1.5rem; text-align: center;">
                    <button class="generate-btn" style="background: #10b981;">🚀 Generate Complete Website</button>
                </div>
            </div>

            <script>
                function addPage() {{
                    const name = document.getElementById('page-name').value;
                    const url = document.getElementById('page-url').value;
                    const type = document.getElementById('page-type').value;
                    const desc = document.getElementById('page-desc').value;

                    if (!name || !url) {{
                        alert('Please fill in page name and URL');
                        return;
                    }}

                    const event = new CustomEvent('addPage', {{
                        detail: {{ name, url, type, desc }}
                    }});
                    window.parent.postMessage(event, '*');
                }}
            </script>
        </div>
        """

    def _render_page_manager(self) -> str:
        """Render page manager."""
        return """
        <div style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .page-manager {{ max-width: 1000px; }}
                .site-tree {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; }}
                .tree-item {{ padding: 0.75rem 0; border-bottom: 1px solid #f1f5f9; }}
                .tree-item:last-child {{ border-bottom: none; }}
                .tree-header {{ display: flex; align-items: center; gap: 0.75rem; }}
                .tree-icon {{ font-size: 1.25rem; }}
                .tree-name {{ font-weight: 600; color: #1e293b; }}
                .tree-path {{ font-size: 0.75rem; color: #64748b; }}
                .tree-children {{ margin-left: 1.5rem; padding-left: 1.5rem; border-left: 2px solid #e2e8f0; }}
                .site-stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1.5rem; }}
                .stat-card {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; text-align: center; }}
                .stat-value {{ font-size: 2rem; font-weight: 700; color: #6366f1; margin-bottom: 0.25rem; }}
                .stat-label {{ font-size: 0.875rem; color: #64748b; }}
            </style>

            <div class="page-manager">
                <h3 style="margin-bottom: 1.5rem;">📁 Site Structure</h3>

                <div class="site-tree">
                    <div class="tree-item">
                        <div class="tree-header">
                            <span class="tree-icon">🏠</span>
                            <div>
                                <div class="tree-name">Home</div>
                                <div class="tree-path">/home - Landing page</div>
                            </div>
                        </div>
                    </div>
                    <div class="tree-item">
                        <div class="tree-header">
                            <span class="tree-icon">👥</span>
                            <div>
                                <div class="tree-name">About</div>
                                <div class="tree-path">/about - Company info</div>
                            </div>
                        </div>
                    </div>
                    <div class="tree-item">
                        <div class="tree-header">
                            <span class="tree-icon">📦</span>
                            <div>
                                <div class="tree-name">Services</div>
                                <div class="tree-path">/services - What we offer</div>
                            </div>
                        </div>
                    </div>
                    <div class="tree-item">
                        <div class="tree-header">
                            <span class="tree-icon">✉️</span>
                            <div>
                                <div class="tree-name">Contact</div>
                                <div class="tree-path">/contact - Get in touch</div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="site-stats">
                    <div class="stat-card">
                        <div class="stat-value">4</div>
                        <div class="stat-label">Total Pages</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">12</div>
                        <div class="stat-label">Components</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">3</div>
                        <div class="stat-label">Templates</div>
                    </div>
                </div>
            </div>
        </div>
        """

    def _render_site_preview(self, body: dict) -> str:
        """Render site preview with navigation."""
        return """
        <div style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .site-preview {{ max-width: 1200px; }}
                .site-nav {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1rem 1.5rem; margin-bottom: 1.5rem; display: flex; align-items: center; justify-content: space-between; }}
                .nav-links {{ display: flex; gap: 1.5rem; }}
                .nav-link {{ font-weight: 600; color: #64748b; cursor: pointer; transition: color 0.2s; }}
                .nav-link:hover, .nav-link.active {{ color: #6366f1; }}
                .nav-cta {{ padding: 0.5rem 1rem; background: #6366f1; color: white; border-radius: 8px; font-weight: 600; }}
                .preview-frame {{ background: white; border: 2px solid #e2e8f0; border-radius: 12px; overflow: hidden; }}
                .preview-toolbar {{ display: flex; gap: 0.5rem; padding: 1rem; background: #f8fafc; border-bottom: 1px solid #e2e8f0; }}
                .toolbar-btn {{ padding: 0.5rem 1rem; border: 1px solid #e2e8f0; border-radius: 6px; background: white; cursor: pointer; font-size: 0.875rem; }}
                .toolbar-btn:hover {{ background: #f1f5f9; }}
                .preview-content {{ padding: 2rem; }}
            </style>

            <div class="site-preview">
                <h3 style="margin-bottom: 1.5rem;">🌐 Site Preview</h3>

                <div class="site-nav">
                    <div style="font-weight: 700; font-size: 1.25rem;">🎨 MyWebsite</div>
                    <div class="nav-links">
                        <span class="nav-link active">Home</span>
                        <span class="nav-link">About</span>
                        <span class="nav-link">Services</span>
                        <span class="nav-link">Contact</span>
                    </div>
                    <div class="nav-cta">Get Started</div>
                </div>

                <div class="preview-frame">
                    <div class="preview-toolbar">
                        <button class="toolbar-btn">🏠 Home</button>
                        <button class="toolbar-btn">👥 About</button>
                        <button class="toolbar-btn">📦 Services</button>
                        <button class="toolbar-btn">✉️ Contact</button>
                    </div>
                    <div class="preview-content">
                        <div style="text-align: center; padding: 4rem 2rem;">
                            <h1 style="font-size: 2.5rem; font-weight: 700; color: #1e293b; margin-bottom: 1rem;">Welcome to Our Website</h1>
                            <p style="font-size: 1.125rem; color: #64748b; max-width: 600px; margin: 0 auto 2rem;">We create beautiful, responsive websites that help businesses grow and succeed in the digital age.</p>
                            <div style="display: flex; gap: 1rem; justify-content: center;">
                                <button style="padding: 0.75rem 1.5rem; background: #6366f1; color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;">Get Started</button>
                                <button style="padding: 0.75rem 1.5rem; background: white; color: #6366f1; border: 2px solid #6366f1; border-radius: 8px; font-weight: 600; cursor: pointer;">Learn More</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
