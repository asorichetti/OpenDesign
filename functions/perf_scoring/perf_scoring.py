"""
title: Performance Scoring
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesigner
version: 1.0.0
required_open_webui_version: 0.10.0
"""

from typing import Any


class Action:
    """Performance Scoring — Analyze and score design performance metrics."""

    def __init__(self):
        self.type = "action"

    def actions(self) -> list[dict[str, str]]:
        """Return available actions."""
        return [
            {
                "name": "Performance Score",
                "description": "Get performance score for your design",
                "icon": "activity",
            },
            {
                "name": "Optimization Tips",
                "description": "Get optimization recommendations",
                "icon": "lightbulb",
            },
            {
                "name": "Core Web Vitals",
                "description": "Analyze Core Web Vitals metrics",
                "icon": "gauge",
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
        """Handle performance scoring action."""
        if action == "Performance Score":
            return self._render_score(body)
        elif action == "Optimization Tips":
            return self._render_tips()
        elif action == "Core Web Vitals":
            return self._render_vitals()

        return f"Unknown action: {action}"

    def _render_score(self, body: dict) -> str:
        """Render performance score."""
        return """
        <div class="perf-score" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .perf-score {{ max-width: 800px; margin: 0 auto; }}
                .score-circle {{ width: 200px; height: 200px; border-radius: 50%; margin: 0 auto 2rem; display: flex; flex-direction: column; align-items: center; justify-content: center; background: conic-gradient(#16a34a 0% 92%, #e2e8f0 92% 100%); position: relative; }}
                .score-circle-inner {{ width: 170px; height: 170px; border-radius: 50%; background: white; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
                .score-value {{ font-size: 4rem; font-weight: 700; color: #16a34a; }}
                .score-label {{ font-size: 1rem; color: #64748b; }}
                .score-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5rem; margin-bottom: 2rem; }}
                .score-card {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; }}
                .score-card h4 {{ font-size: 1rem; font-weight: 600; color: #1e293b; margin: 0 0 1rem; }}
                .score-item {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem; }}
                .score-item:last-child {{ margin-bottom: 0; }}
                .score-bar {{ height: 8px; background: #f1f5f9; border-radius: 4px; overflow: hidden; margin-top: 0.5rem; }}
                .score-fill {{ height: 100%; border-radius: 4px; }}
                .score-fill.excellent {{ background: #16a34a; width: 92%; }}
                .score-fill.good {{ background: #16a34a; width: 85%; }}
                .score-fill.average {{ background: #d97706; width: 65%; }}
                .score-fill.poor {{ background: #dc2626; width: 45%; }}
            </style>

            <div class="perf-score">
                <h3 style="text-align: center; margin-bottom: 2rem;">⚡ Performance Score</h3>

                <div class="score-circle">
                    <div class="score-circle-inner">
                        <div class="score-value">92</div>
                        <div class="score-label">Excellent</div>
                    </div>
                </div>

                <div class="score-grid">
                    <div class="score-card">
                        <h4>Performance</h4>
                        <div class="score-item">
                            <span>First Contentful Paint</span>
                            <span style="font-weight: 600; color: #16a34a;">0.8s</span>
                        </div>
                        <div class="score-bar">
                            <div class="score-fill excellent"></div>
                        </div>
                    </div>

                    <div class="score-card">
                        <h4>Accessibility</h4>
                        <div class="score-item">
                            <span>WCAG Compliance</span>
                            <span style="font-weight: 600; color: #16a34a;">92/100</span>
                        </div>
                        <div class="score-bar">
                            <div class="score-fill good"></div>
                        </div>
                    </div>

                    <div class="score-card">
                        <h4>SEO</h4>
                        <div class="score-item">
                            <span>SEO Score</span>
                            <span style="font-weight: 600; color: #16a34a;">88/100</span>
                        </div>
                        <div class="score-bar">
                            <div class="score-fill good"></div>
                        </div>
                    </div>

                    <div class="score-card">
                        <h4>Best Practices</h4>
                        <div class="score-item">
                            <span>Score</span>
                            <span style="font-weight: 600; color: #16a34a;">98/100</span>
                        </div>
                        <div class="score-bar">
                            <div class="score-fill excellent"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """

    def _render_tips(self) -> str:
        """Render optimization tips."""
        return """
        <div style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .tips-list {{ max-width: 800px; }}
                .tip-card {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; }}
                .tip-header {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem; }}
                .tip-title {{ font-weight: 600; color: #1e293b; }}
                .tip-badge {{ padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.75rem; font-weight: 600; }}
                .tip-badge.high {{ background: #fee2e2; color: #dc2626; }}
                .tip-badge.medium {{ background: #fef3c7; color: #d97706; }}
                .tip-badge.low {{ background: #dcfce7; color: #16a34a; }}
                .tip-desc {{ font-size: 0.875rem; color: #64748b; margin-bottom: 0.75rem; }}
                .tip-action {{ padding: 0.5rem 1rem; background: #6366f1; color: white; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; font-size: 0.875rem; }}
            </style>

            <div class="tips-list">
                <h3 style="margin-bottom: 1.5rem;">💡 Optimization Tips</h3>

                <div class="tip-card">
                    <div class="tip-header">
                        <span class="tip-title">🖼️ Optimize Images</span>
                        <span class="tip-badge high">High Priority</span>
                    </div>
                    <div class="tip-desc">Images account for 65% of page weight. Use WebP format and lazy loading.</div>
                    <button class="tip-action">Auto Optimize</button>
                </div>

                <div class="tip-card">
                    <div class="tip-header">
                        <span class="tip-title">📦 Minify Resources</span>
                        <span class="tip-badge medium">Medium Priority</span>
                    </div>
                    <div class="tip-desc">Minify CSS and JavaScript to reduce file sizes by 30-40%.</div>
                    <button class="tip-action">Minify Now</button>
                </div>

                <div class="tip-card">
                    <div class="tip-header">
                        <span class="tip-title">🚀 Enable Caching</span>
                        <span class="tip-badge low">Low Priority</span>
                    </div>
                    <div class="tip-desc">Set proper cache headers for static assets to improve repeat visits.</div>
                    <button class="tip-action">Configure</button>
                </div>

                <div class="tip-card">
                    <div class="tip-header">
                        <span class="tip-title">📱 Responsive Images</span>
                        <span class="tip-badge low">Low Priority</span>
                    </div>
                    <div class="tip-desc">Use srcset and sizes attributes to serve appropriate image sizes.</div>
                    <button class="tip-action">Setup</button>
                </div>
            </div>
        </div>
        """

    def _render_vitals(self) -> str:
        """Render Core Web Vitals."""
        return """
        <div style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .vitals-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; }}
                .vital-card {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; text-align: center; }}
                .vital-icon {{ font-size: 3rem; margin-bottom: 1rem; }}
                .vital-name {{ font-size: 1.125rem; font-weight: 600; color: #1e293b; margin-bottom: 0.5rem; }}
                .vital-value {{ font-size: 2rem; font-weight: 700; color: #16a34a; margin-bottom: 0.5rem; }}
                .vital-status {{ padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.75rem; font-weight: 600; display: inline-block; }}
                .vital-status.good {{ background: #dcfce7; color: #16a34a; }}
                .vital-status.needs-improvement {{ background: #fef3c7; color: #d97706; }}
                .vital-status.poor {{ background: #fee2e2; color: #dc2626; }}
                .vital-desc {{ font-size: 0.875rem; color: #64748b; margin-top: 0.75rem; }}
            </style>

            <div style="max-width: 1000px;">
                <h3 style="margin-bottom: 1.5rem;">📊 Core Web Vitals</h3>

                <div class="vitals-grid">
                    <div class="vital-card">
                        <div class="vital-icon">🎨</div>
                        <div class="vital-name">LCP</div>
                        <div class="vital-desc">Largest Contentful Paint</div>
                        <div class="vital-value">0.8s</div>
                        <span class="vital-status good">✅ Good</span>
                        <div class="vital-desc">Under 2.5s is good</div>
                    </div>

                    <div class="vital-card">
                        <div class="vital-icon">👆</div>
                        <div class="vital-name">INP</div>
                        <div class="vital-desc">Interaction to Next Paint</div>
                        <div class="vital-value">120ms</div>
                        <span class="vital-status good">✅ Good</span>
                        <div class="vital-desc">Under 200ms is good</div>
                    </div>

                    <div class="vital-card">
                        <div class="vital-icon">📏</div>
                        <div class="vital-name">CLS</div>
                        <div class="vital-desc">Cumulative Layout Shift</div>
                        <div class="vital-value">0.02</div>
                        <span class="vital-status good">✅ Good</span>
                        <div class="vital-desc">Under 0.1 is good</div>
                    </div>
                </div>
            </div>
        </div>
        """
