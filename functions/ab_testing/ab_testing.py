"""
title: A/B Testing Mode
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesigner
version: 1.0.0
required_open_webui_version: 0.10.0
"""

from typing import Any


class Action:
    """A/B Testing Mode — Create variants and compare design performance."""

    def __init__(self):
        self.type = "action"

    def actions(self) -> list[dict[str, str]]:
        """Return available actions."""
        return [
            {
                "name": "A/B Test",
                "description": "Create and run A/B tests on your designs",
                "icon": "git-branch",
            },
            {
                "name": "Variant Builder",
                "description": "Build design variants with different options",
                "icon": "layers",
            },
            {
                "name": "Results Dashboard",
                "description": "View A/B test results and insights",
                "icon": "bar-chart",
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
        """Handle A/B test action."""
        if action == "A/B Test":
            return self._render_test_dashboard(body)
        elif action == "Variant Builder":
            return self._render_variant_builder()
        elif action == "Results Dashboard":
            return self._render_results_dashboard()

        return f"Unknown action: {action}"

    def _render_test_dashboard(self, body: dict) -> str:
        """Render A/B test dashboard."""
        return """
        <div class="ab-test-dashboard" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .ab-test-dashboard {{ max-width: 1200px; margin: 0 auto; }}
                .dashboard-header {{ text-align: center; margin-bottom: 2rem; }}
                .dashboard-header h3 {{ font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0 0 0.5rem; }}
                .dashboard-header p {{ color: #64748b; }}
                .test-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-bottom: 2rem; }}
                .test-card {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; }}
                .test-header {{ padding: 1rem 1.5rem; background: #f8fafc; border-bottom: 1px solid #e2e8f0; }}
                .test-name {{ font-weight: 600; color: #1e293b; }}
                .test-content {{ padding: 1.5rem; min-height: 300px; display: flex; align-items: center; justify-content: center; }}
                .test-content a {{ background: #f1f5f9; border: 2px dashed #e2e8f0; border-radius: 8px; padding: 2rem; text-align: center; }}
                .test-stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 2rem; }}
                .stat-card {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; text-align: center; }}
                .stat-value {{ font-size: 2rem; font-weight: 700; color: #6366f1; margin-bottom: 0.25rem; }}
                .stat-label {{ font-size: 0.875rem; color: #64748b; }}
                .create-btn {{ padding: 1rem 2rem; background: #6366f1; color: white; border: none; border-radius: 12px; font-weight: 600; cursor: pointer; font-size: 1rem; }}
            </style>

            <div class="ab-test-dashboard">
                <div class="dashboard-header">
                    <h3>🧪 A/B Test Dashboard</h3>
                    <p>Create variants and compare design performance</p>
                </div>

                <div class="test-stats">
                    <div class="stat-card">
                        <div class="stat-value">2</div>
                        <div class="stat-label">Active Tests</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">12.5K</div>
                        <div class="stat-label">Total Visitors</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">8.3%</div>
                        <div class="stat-label">Avg Conversion</div>
                    </div>
                </div>

                <div class="test-grid">
                    <div class="test-card">
                        <div class="test-header">
                            <div class="test-name">🎨 Hero Section Color Test</div>
                        </div>
                        <div class="test-content">
                            <div style="display: flex; gap: 2rem;">
                                <div style="flex: 1; text-align: center;">
                                    <div style="padding: 2rem; background: #6366f1; border-radius: 8px; color: white; font-weight: 600;">Variant A</div>
                                    <div style="margin-top: 1rem;">
                                        <div style="font-size: 1.5rem; font-weight: 700; color: #16a34a;">45%</div>
                                        <div style="font-size: 0.875rem; color: #64748b;">2,340 visitors</div>
                                    </div>
                                </div>
                                <div style="flex: 1; text-align: center;">
                                    <div style="padding: 2rem; background: #10b981; border-radius: 8px; color: white; font-weight: 600;">Variant B</div>
                                    <div style="margin-top: 1rem;">
                                        <div style="font-size: 1.5rem; font-weight: 700; color: #16a34a;">55%</div>
                                        <div style="font-size: 0.875rem; color: #64748b;">2,480 visitors</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="test-card">
                        <div class="test-header">
                            <div class="test-name">📝 CTA Button Test</div>
                        </div>
                        <div class="test-content">
                            <div style="display: flex; gap: 2rem;">
                                <div style="flex: 1; text-align: center;">
                                    <div style="padding: 2rem; background: #f1f5f9; border-radius: 8px; color: #64748b;">Variant A</div>
                                    <div style="margin-top: 1rem;">
                                        <div style="font-size: 1.5rem; font-weight: 700; color: #64748b;">50%</div>
                                        <div style="font-size: 0.875rem; color: #64748b;">Running...</div>
                                    </div>
                                </div>
                                <div style="flex: 1; text-align: center;">
                                    <div style="padding: 2rem; background: #f1f5f9; border-radius: 8px; color: #64748b;">Variant B</div>
                                    <div style="margin-top: 1rem;">
                                        <div style="font-size: 1.5rem; font-weight: 700; color: #64748b;">50%</div>
                                        <div style="font-size: 0.875rem; color: #64748b;">Running...</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div style="text-align: center;">
                    <button class="create-btn">➕ Create New A/B Test</button>
                </div>
            </div>
        </div>
        """

    def _render_variant_builder(self) -> str:
        """Render variant builder."""
        return """
        <div style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .variant-builder {{ max-width: 1200px; }}
                .builder-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }}
                .variant-panel {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; }}
                .variant-panel h4 {{ font-size: 1.125rem; font-weight: 600; color: #1e293b; margin: 0 0 1rem; }}
                .control-group {{ margin-bottom: 1rem; }}
                .control-group label {{ display: block; font-size: 0.875rem; font-weight: 600; color: #1e293b; margin-bottom: 0.5rem; }}
                .control-group select, .control-group input {{ width: 100%; padding: 0.75rem; border: 1px solid #e2e8f0; border-radius: 8px; }}
                .compare-btn {{ padding: 0.75rem 1.5rem; background: #6366f1; color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; width: 100%; }}
            </style>

            <div class="variant-builder">
                <h3 style="margin-bottom: 1.5rem;">🔧 Variant Builder</h3>

                <div class="builder-grid">
                    <div class="variant-panel">
                        <h4>🎨 Variant A (Control)</h4>
                        <div class="control-group">
                            <label>Button Color</label>
                            <select>
                                <option>Blue (#6366f1)</option>
                                <option>Green (#10b981)</option>
                                <option>Orange (#f59e0b)</option>
                            </select>
                        </div>
                        <div class="control-group">
                            <label>Button Text</label>
                            <input type="text" value="Get Started">
                        </div>
                        <div class="control-group">
                            <label>Layout</label>
                            <select>
                                <option>Centered</option>
                                <option>Left-aligned</option>
                                <option>Right-aligned</option>
                            </select>
                        </div>
                    </div>

                    <div class="variant-panel">
                        <h4>🎨 Variant B (Test)</h4>
                        <div class="control-group">
                            <label>Button Color</label>
                            <select>
                                <option>Blue (#6366f1)</option>
                                <option selected>Green (#10b981)</option>
                                <option>Orange (#f59e0b)</option>
                            </select>
                        </div>
                        <div class="control-group">
                            <label>Button Text</label>
                            <input type="text" value="Start Free Trial">
                        </div>
                        <div class="control-group">
                            <label>Layout</label>
                            <select>
                                <option>Centered</option>
                                <option selected>Left-aligned</option>
                                <option>Right-aligned</option>
                            </select>
                        </div>
                        <button class="compare-btn">🔄 Compare Variants</button>
                    </div>
                </div>
            </div>
        </div>
        """

    def _render_results_dashboard(self) -> str:
        """Render results dashboard."""
        return """
        <div style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .results-dashboard {{ max-width: 1000px; }}
                .result-chart {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 2rem; margin-bottom: 1.5rem; }}
                .chart-bar {{ display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem; }}
                .chart-label {{ width: 100px; font-weight: 600; color: #1e293b; }}
                .chart-track {{ flex: 1; height: 32px; background: #f1f5f9; border-radius: 16px; overflow: hidden; }}
                .chart-fill {{ height: 100%; border-radius: 16px; display: flex; align-items: center; padding-left: 1rem; color: white; font-weight: 600; font-size: 0.875rem; }}
                .chart-fill.blue {{ background: #6366f1; }}
                .chart-fill.green {{ background: #10b981; }}
                .insights-card {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; }}
                .insight-item {{ padding: 1rem 0; border-bottom: 1px solid #f1f5f9; }}
                .insight-item:last-child {{ border-bottom: none; }}
                .insight-title {{ font-weight: 600; color: #1e293b; margin-bottom: 0.25rem; }}
                .insight-desc {{ font-size: 0.875rem; color: #64748b; }}
            </style>

            <div class="results-dashboard">
                <h3 style="margin-bottom: 1.5rem;">📊 A/B Test Results</h3>

                <div class="result-chart">
                    <h4 style="margin-bottom: 1rem;">Conversion Rate</h4>
                    <div class="chart-bar">
                        <div class="chart-label">Variant A</div>
                        <div class="chart-track">
                            <div class="chart-fill blue" style="width: 45%;">45%</div>
                        </div>
                    </div>
                    <div class="chart-bar">
                        <div class="chart-label">Variant B</div>
                        <div class="chart-track">
                            <div class="chart-fill green" style="width: 55%;">55%</div>
                        </div>
                    </div>
                </div>

                <div class="insights-card">
                    <h4 style="margin-bottom: 1rem;">🎯 Key Insights</h4>
                    <div class="insight-item">
                        <div class="insight-title">✅ Variant B Wins</div>
                        <div class="insight-desc">Variant B outperformed Variant A by 22.2% in conversion rate</div>
                    </div>
                    <div class="insight-item">
                        <div class="insight-title">💡 Color Matters</div>
                        <div class="insight-desc">Green buttons converted 15% better than blue in this test</div>
                    </div>
                    <div class="insight-item">
                        <div class="insight-title">📈 Statistical Significance</div>
                        <div class="insight-desc">Results reached 95% confidence level after 4,820 visitors</div>
                    </div>
                    <div class="insight-item">
                        <div class="insight-title">🚀 Recommendation</div>
                        <div class="insight-desc">Deploy Variant B to all traffic for optimal conversion</div>
                    </div>
                </div>
            </div>
        </div>
        """
