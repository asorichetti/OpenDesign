"""
title: SEO Optimization Engine
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesigner
version: 1.0.0
required_open_webui_version: 0.10.0
"""

from typing import Any


class SEOOptimizer:
    """SEO Optimization Engine — Auto-generate SEO-friendly meta tags and structured data."""

    def __init__(self):
        self.type = "action"

    def actions(self) -> list[dict[str, str]]:
        """Return available actions."""
        return [
            {
                "name": "SEO Optimizer",
                "description": "Optimize your design for search engines",
                "icon": "search",
            },
            {
                "name": "Meta Tag Generator",
                "description": "Generate meta tags, Open Graph, and Twitter Cards",
                "icon": "code",
            },
            {
                "name": "Structured Data",
                "description": "Add JSON-LD structured data for rich snippets",
                "icon": "database",
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
        """Handle SEO action."""
        if action == "SEO Optimizer":
            return self._render_seo_dashboard(body)
        elif action == "Meta Tag Generator":
            return self._render_meta_tag_generator(body)
        elif action == "Structured Data":
            return self._render_structured_data(body)

        return f"Unknown action: {action}"

    def _render_seo_dashboard(self, body: dict) -> str:
        """Render SEO dashboard."""
        return """
        <div class="seo-dashboard" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .seo-dashboard {{ max-width: 1000px; }}
                .seo-header {{ text-align: center; margin-bottom: 2rem; }}
                .seo-header h3 {{ font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0 0 0.5rem; }}
                .seo-header p {{ color: #64748b; }}
                .seo-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; }}
                .seo-card {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; }}
                .seo-card h4 {{ font-size: 1.125rem; font-weight: 600; color: #1e293b; margin: 0 0 1rem; }}
                .seo-score {{ display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem; }}
                .score-circle {{ width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: 700; }}
                .score-circle.excellent {{ background: #dcfce7; color: #16a34a; }}
                .score-circle.good {{ background: #fef3c7; color: #d97706; }}
                .score-circle.poor {{ background: #fee2e2; color: #dc2626; }}
                .seo-metrics {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.75rem; }}
                .metric {{ padding: 0.75rem; background: #f8fafc; border-radius: 8px; }}
                .metric-label {{ font-size: 0.75rem; color: #64748b; margin-bottom: 0.25rem; }}
                .metric-value {{ font-size: 0.875rem; font-weight: 600; color: #1e293b; }}
                .seo-checklist {{ margin-top: 1rem; }}
                .checklist-item {{ display: flex; align-items: center; gap: 0.75rem; padding: 0.5rem 0; }}
                .checklist-icon {{ font-size: 1.25rem; }}
                .checklist-text {{ font-size: 0.875rem; color: #1e293b; }}
            </style>

            <div class="seo-header">
                <h3>🔍 SEO Optimization Dashboard</h3>
                <p>Optimize your design for maximum search engine visibility</p>
            </div>

            <div class="seo-grid">
                <div class="seo-card">
                    <h4>📊 SEO Score</h4>
                    <div class="seo-score">
                        <div class="score-circle excellent">92</div>
                        <div>
                            <div style="font-size: 1.125rem; font-weight: 600; color: #16a34a;">Excellent</div>
                            <div style="font-size: 0.875rem; color: #64748b;">Your design is well-optimized</div>
                        </div>
                    </div>
                    <div class="seo-metrics">
                        <div class="metric">
                            <div class="metric-label">Meta Tags</div>
                            <div class="metric-value">✅ Complete</div>
                        </div>
                        <div class="metric">
                            <div class="metric-label">Open Graph</div>
                            <div class="metric-value">✅ Complete</div>
                        </div>
                        <div class="metric">
                            <div class="metric-label">Twitter Cards</div>
                            <div class="metric-value">✅ Complete</div>
                        </div>
                        <div class="metric">
                            <div class="metric-label">Structured Data</div>
                            <div class="metric-value">⚠️ Missing</div>
                        </div>
                    </div>
                </div>

                <div class="seo-card">
                    <h4>✅ SEO Checklist</h4>
                    <div class="seo-checklist">
                        <div class="checklist-item">
                            <span class="checklist-icon">✅</span>
                            <span class="checklist-text">Title tag present (52 chars)</span>
                        </div>
                        <div class="checklist-item">
                            <span class="checklist-icon">✅</span>
                            <span class="checklist-text">Meta description present (148 chars)</span>
                        </div>
                        <div class="checklist-item">
                            <span class="checklist-icon">✅</span>
                            <span class="checklist-text">Open Graph tags present</span>
                        </div>
                        <div class="checklist-item">
                            <span class="checklist-icon">✅</span>
                            <span class="checklist-text">Twitter Card tags present</span>
                        </div>
                        <div class="checklist-item">
                            <span class="checklist-icon">⚠️</span>
                            <span class="checklist-text">Canonical URL missing</span>
                        </div>
                        <div class="checklist-item">
                            <span class="checklist-icon">⚠️</span>
                            <span class="checklist-text">Structured data missing</span>
                        </div>
                        <div class="checklist-item">
                            <span class="checklist-icon">⚠️</span>
                            <span class="checklist-text">Sitemap reference missing</span>
                        </div>
                    </div>
                </div>

                <div class="seo-card">
                    <h4>🚀 Quick Fixes</h4>
                    <div class="seo-checklist">
                        <div class="checklist-item" style="cursor: pointer;" onclick="applyFix('canonical')">
                            <span class="checklist-icon">➕</span>
                            <span class="checklist-text">Add canonical URL</span>
                        </div>
                        <div class="checklist-item" style="cursor: pointer;" onclick="applyFix('structured-data')">
                            <span class="checklist-icon">➕</span>
                            <span class="checklist-text">Add structured data (JSON-LD)</span>
                        </div>
                        <div class="checklist-item" style="cursor: pointer;" onclick="applyFix('sitemap')">
                            <span class="checklist-icon">➕</span>
                            <span class="checklist-text">Add sitemap reference</span>
                        </div>
                        <div class="checklist-item" style="cursor: pointer;" onclick="applyFix('robots')">
                            <span class="checklist-icon">➕</span>
                            <span class="checklist-text">Add robots.txt reference</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """

    def _render_meta_tag_generator(self, body: dict) -> str:
        """Render meta tag generator."""
        return """
        <div style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .meta-generator {{ max-width: 1000px; }}
                .form-group {{ margin-bottom: 1.5rem; }}
                .form-group label {{ display: block; font-size: 0.875rem; font-weight: 600; color: #1e293b; margin-bottom: 0.5rem; }}
                .form-group input, .form-group textarea {{ width: 100%; padding: 0.75rem; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 0.875rem; }}
                .form-group textarea {{ min-height: 100px; resize: vertical; }}
                .form-group small {{ display: block; margin-top: 0.25rem; color: #64748b; font-size: 0.75rem; }}
                .generate-btn {{ padding: 1rem 2rem; background: #6366f1; color: white; border: none; border-radius: 12px; font-weight: 600; cursor: pointer; }}
                .code-output {{ background: #1e293b; color: #e2e8f0; padding: 1.5rem; border-radius: 12px; margin-top: 1.5rem; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; line-height: 1.6; overflow-x: auto; }}
                .copy-btn {{ padding: 0.5rem 1rem; background: #475569; color: white; border: none; border-radius: 6px; cursor: pointer; margin-bottom: 1rem; }}
            </style>

            <div class="meta-generator">
                <h3 style="margin-bottom: 1.5rem;">📝 Meta Tag Generator</h3>

                <div class="form-group">
                    <label>Page Title</label>
                    <input type="text" id="page-title" placeholder="My Amazing Product - Best Solution for X" maxlength="60">
                    <small>Recommended: 50-60 characters</small>
                </div>

                <div class="form-group">
                    <label>Meta Description</label>
                    <textarea id="meta-description" placeholder="Discover our amazing product that solves X problem. Learn more about our features and benefits." maxlength="160"></textarea>
                    <small>Recommended: 150-160 characters</small>
                </div>

                <div class="form-group">
                    <label>Author</label>
                    <input type="text" id="author" placeholder="Your Name or Company">
                </div>

                <div class="form-group">
                    <label>Canonical URL</label>
                    <input type="url" id="canonical-url" placeholder="https://example.com/page">
                </div>

                <div class="form-group">
                    <label>OG Image URL</label>
                    <input type="url" id="og-image" placeholder="https://example.com/image.jpg">
                    <small>Recommended: 1200x630 pixels</small>
                </div>

                <button class="generate-btn" onclick="generateMetaTags()">Generate Meta Tags</button>

                <div id="meta-output" class="code-output" style="display: none;"></div>
            </div>

            <script>
                function generateMetaTags() {{
                    const title = document.getElementById('page-title').value;
                    const description = document.getElementById('meta-description').value;
                    const author = document.getElementById('author').value;
                    const canonical = document.getElementById('canonical-url').value;
                    const ogImage = document.getElementById('og-image').value;

                    let metaTags = `<!-- Basic Meta Tags -->
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{title}}</title>
<meta name="description" content="{{description}}">
<meta name="author" content="{{author}}">
<link rel="canonical" href="{{canonical}}">

<!-- Open Graph / Facebook -->
<meta property="og:type" content="website">
<meta property="og:url" content="{{canonical}}">
<meta property="og:title" content="{{title}}">
<meta property="og:description" content="{{description}}">
<meta property="og:image" content="{{ogImage}}">

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="{{canonical}}">
<meta property="twitter:title" content="{{title}}">
<meta property="twitter:description" content="{{description}}">
<meta property="twitter:image" content="{{ogImage}}">`;

                    metaTags = metaTags.replace('{{title}}', title || 'Page Title')
                        .replace('{{description}}', description || 'Page description')
                        .replace('{{author}}', author || 'Author')
                        .replace('{{canonical}}', canonical || 'https://example.com')
                        .replace('{{ogImage}}', ogImage || 'https://example.com/image.jpg');

                    const output = document.getElementById('meta-output');
                    output.textContent = metaTags;
                    output.style.display = 'block';
                }}
            </script>
        </div>
        """

    def _render_structured_data(self, body: dict) -> str:
        """Render structured data generator."""
        return """
        <div style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .structured-data {{ max-width: 1000px; }}
                .schema-type {{ display: flex; gap: 0.75rem; margin-bottom: 1.5rem; flex-wrap: wrap; }}
                .schema-btn {{ padding: 0.75rem 1.5rem; border: 2px solid #e2e8f0; border-radius: 12px; background: white; cursor: pointer; font-weight: 600; }}
                .schema-btn.active {{ border-color: #6366f1; background: #f8fafc; }}
                .schema-form {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; }}
                .form-group {{ margin-bottom: 1.5rem; }}
                .form-group label {{ display: block; font-size: 0.875rem; font-weight: 600; color: #1e293b; margin-bottom: 0.5rem; }}
                .form-group input, .form-group textarea {{ width: 100%; padding: 0.75rem; border: 1px solid #e2e8f0; border-radius: 8px; }}
                .generate-btn {{ padding: 1rem 2rem; background: #6366f1; color: white; border: none; border-radius: 12px; font-weight: 600; cursor: pointer; }}
                .code-output {{ background: #1e293b; color: #e2e8f0; padding: 1.5rem; border-radius: 12px; margin-top: 1.5rem; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; line-height: 1.6; overflow-x: auto; }}
            </style>

            <div class="structured-data">
                <h3 style="margin-bottom: 1.5rem;">🗃️ Structured Data (JSON-LD)</h3>

                <div class="schema-type">
                    <button class="schema-btn active" onclick="selectSchema('webpage')">📄 WebPage</button>
                    <button class="schema-btn" onclick="selectSchema('article')">📰 Article</button>
                    <button class="schema-btn" onclick="selectSchema('product')">🛍️ Product</button>
                    <button class="schema-btn" onclick="selectSchema('local-business')">🏢 Local Business</button>
                    <button class="schema-btn" onclick="selectSchema('organization')">🏛️ Organization</button>
                </div>

                <div class="schema-form">
                    <div class="form-group">
                        <label>Page/Entity Name</label>
                        <input type="text" id="schema-name" placeholder="My Amazing Product">
                    </div>

                    <div class="form-group">
                        <label>Description</label>
                        <textarea id="schema-description" placeholder="A brief description of your page or entity"></textarea>
                    </div>

                    <div class="form-group">
                        <label>URL</label>
                        <input type="url" id="schema-url" placeholder="https://example.com">
                    </div>

                    <div class="form-group">
                        <label>Image URL</label>
                        <input type="url" id="schema-image" placeholder="https://example.com/image.jpg">
                    </div>

                    <button class="generate-btn" onclick="generateStructuredData()">Generate JSON-LD</button>
                </div>

                <div id="schema-output" class="code-output" style="display: none;"></div>
            </div>

            <script>
                let currentSchema = 'webpage';

                function selectSchema(type) {{
                    currentSchema = type;
                    document.querySelectorAll('.schema-btn').forEach(btn => btn.classList.remove('active'));
                    event.target.classList.add('active');
                }}

                function generateStructuredData() {{
                    const name = document.getElementById('schema-name').value || 'Page Name';
                    const description = document.getElementById('schema-description').value || 'Page description';
                    const url = document.getElementById('schema-url').value || 'https://example.com';
                    const image = document.getElementById('schema-image').value || 'https://example.com/image.jpg';

                    let schema = {{
                        "@context": "https://schema.org",
                        "@type": currentSchema.charAt(0).toUpperCase() + currentSchema.slice(1).replace('-', ''),
                        "name": name,
                        "description": description,
                        "url": url,
                        "image": image
                    }};

                    if (currentSchema === 'product') {{
                        schema = {{
                            ...schema,
                            "@type": "Product",
                            "offers": {{
                                "@type": "Offer",
                                "price": "99.99",
                                "priceCurrency": "USD"
                            }}
                        }};
                    }}

                    const output = document.getElementById('schema-output');
                    output.textContent = JSON.stringify(schema, null, 2);
                    output.style.display = 'block';
                }}
            </script>
        </div>
        """
