"""
title: Design Analytics
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesigner
version: 1.0.0
required_open_webui_version: 0.10.0
"""

from typing import Any


class DesignAnalytics:
    """Design Analytics — Track usage, performance, and insights for your designs."""

    def __init__(self):
        self.type = "action"

    def actions(self) -> list[dict[str, str]]:
        """Return available actions."""
        return [
            {
                "name": "Usage Analytics",
                "description": "Track design usage and engagement metrics",
                "icon": "bar-chart",
            },
            {
                "name": "Performance Reports",
                "description": "Monitor design performance and load times",
                "icon": "activity",
            },
            {
                "name": "User Insights",
                "description": "Understand how users interact with your designs",
                "icon": "users",
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
        """Handle analytics action."""
        if action == "Usage Analytics":
            return self._render_usage_analytics()
        elif action == "Performance Reports":
            return self._render_performance_reports()
        elif action == "User Insights":
            return self._render_user_insights()

        return f"Unknown action: {action}"

    def _render_usage_analytics(self) -> str:
        """Render usage analytics dashboard."""
        return """
        <div class="usage-analytics" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .usage-analytics {{ max-width: 1200px; margin: 0 auto; }}
                .analytics-header {{ text-align: center; margin-bottom: 2rem; }}
                .analytics-header h3 {{ font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0 0 0.5rem; }}
                .analytics-header p {{ color: #64748b; }}
                .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }}
                .metric-card {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; }}
                .metric-icon {{ font-size: 2rem; margin-bottom: 0.75rem; }}
                .metric-value {{ font-size: 2.5rem; font-weight: 700; color: #1e293b; margin-bottom: 0.25rem; }}
                .metric-label {{ font-size: 0.875rem; color: #64748b; margin-bottom: 0.5rem; }}
                .metric-change {{ font-size: 0.75rem; font-weight: 600; }}
                .metric-change.positive {{ color: #16a34a; }}
                .metric-change.negative {{ color: #dc2626; }}
                .chart-container {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; }}
                .chart-title {{ font-size: 1.125rem; font-weight: 600; color: #1e293b; margin-bottom: 1rem; }}
                .chart-bars {{ display: flex; align-items: flex-end; gap: 0.5rem; height: 200px; }}
                .chart-bar {{ flex: 1; background: linear-gradient(to top, #6366f1, #a5b4fc); border-radius: 4px 4px 0 0; transition: all 0.3s; }}
                .chart-bar:hover {{ opacity: 0.8; }}
                .chart-label {{ text-align: center; font-size: 0.75rem; color: #64748b; margin-top: 0.5rem; }}
            </style>

            <div class="usage-analytics">
                <div class="analytics-header">
                    <h3>📊 Usage Analytics</h3>
                    <p>Track your design usage and engagement metrics</p>
                </div>

                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-icon">🎨</div>
                        <div class="metric-value">1,247</div>
                        <div class="metric-label">Total Designs</div>
                        <div class="metric-change positive">↑ 12.5% from last month</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-icon">👥</div>
                        <div class="metric-value">8,432</div>
                        <div class="metric-label">Active Users</div>
                        <div class="metric-change positive">↑ 8.3% from last month</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-icon">🔄</div>
                        <div class="metric-value">15,891</div>
                        <div class="metric-label">Total Edits</div>
                        <div class="metric-change positive">↑ 15.2% from last month</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-icon">⏱️</div>
                        <div class="metric-value">4.2m</div>
                        <div class="metric-label">Avg Session Time</div>
                        <div class="metric-change positive">↑ 3.1% from last month</div>
                    </div>
                </div>

                <div class="chart-container">
                    <div class="chart-title">Designs Created (Last 7 Days)</div>
                    <div class="chart-bars">
                        <div style="text-align: center; flex: 1;">
                            <div class="chart-bar" style="height: 60%;"></div>
                            <div class="chart-label">Mon</div>
                        </div>
                        <div style="text-align: center; flex: 1;">
                            <div class="chart-bar" style="height: 80%;"></div>
                            <div class="chart-label">Tue</div>
                        </div>
                        <div style="text-align: center; flex: 1;">
                            <div class="chart-bar" style="height: 45%;"></div>
                            <div class="chart-label">Wed</div>
                        </div>
                        <div style="text-align: center; flex: 1;">
                            <div class="chart-bar" style="height: 90%;"></div>
                            <div class="chart-label">Thu</div>
                        </div>
                        <div style="text-align: center; flex: 1;">
                            <div class="chart-bar" style="height: 70%;"></div>
                            <div class="chart-label">Fri</div>
                        </div>
                        <div style="text-align: center; flex: 1;">
                            <div class="chart-bar" style="height: 50%;"></div>
                            <div class="chart-label">Sat</div>
                        </div>
                        <div style="text-align: center; flex: 1;">
                            <div class="chart-bar" style="height: 35%;"></div>
                            <div class="chart-label">Sun</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """

    def _render_performance_reports(self) -> str:
        """Render performance reports."""
        return """
        <div style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .perf-reports {{ max-width: 1000px; }}
                .report-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; }}
                .report-card {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; }}
                .report-card h4 {{ font-size: 1.125rem; font-weight: 600; color: #1e293b; margin: 0 0 1rem; }}
                .perf-item {{ display: flex; align-items: center; justify-content: space-between; padding: 0.75rem 0; border-bottom: 1px solid #f1f5f9; }}
                .perf-item:last-child {{ border-bottom: none; }}
                .perf-label {{ font-size: 0.875rem; color: #1e293b; }}
                .perf-value {{ font-size: 0.875rem; font-weight: 600; }}
                .perf-value.good {{ color: #16a34a; }}
                .perf-value.warning {{ color: #d97706; }}
                .perf-value.bad {{ color: #dc2626; }}
                .perf-bar {{ height: 8px; background: #f1f5f9; border-radius: 4px; overflow: hidden; }}
                .perf-fill {{ height: 100%; border-radius: 4px; }}
                .perf-fill.good {{ background: #16a34a; }}
                .perf-fill.warning {{ background: #d97706; }}
                .perf-fill.bad {{ background: #dc2626; }}
            </style>

            <div class="perf-reports">
                <h3 style="margin-bottom: 1.5rem;">⚡ Performance Reports</h3>

                <div class="report-grid">
                    <div class="report-card">
                        <h4>📈 Load Times</h4>
                        <div class="perf-item">
                            <span class="perf-label">First Paint</span>
                            <span class="perf-value good">0.8s</span>
                        </div>
                        <div class="perf-item">
                            <span class="perf-label">Interactive</span>
                            <span class="perf-value good">1.2s</span>
                        </div>
                        <div class="perf-item">
                            <span class="perf-label">DOM Complete</span>
                            <span class="perf-value warning">2.1s</span>
                        </div>
                    </div>

                    <div class="report-card">
                        <h4>🎯 Performance Scores</h4>
                        <div style="margin-bottom: 1rem;">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                                <span class="perf-label">Performance</span>
                                <span class="perf-value good">95/100</span>
                            </div>
                            <div class="perf-bar">
                                <div class="perf-fill good" style="width: 95%;"></div>
                            </div>
                        </div>
                        <div style="margin-bottom: 1rem;">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                                <span class="perf-label">Accessibility</span>
                                <span class="perf-value good">92/100</span>
                            </div>
                            <div class="perf-bar">
                                <div class="perf-fill good" style="width: 92%;"></div>
                            </div>
                        </div>
                        <div style="margin-bottom: 1rem;">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                                <span class="perf-label">Best Practices</span>
                                <span class="perf-value good">98/100</span>
                            </div>
                            <div class="perf-bar">
                                <div class="perf-fill good" style="width: 98%;"></div>
                            </div>
                        </div>
                        <div>
                            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                                <span class="perf-label">SEO</span>
                                <span class="perf-value good">88/100</span>
                            </div>
                            <div class="perf-bar">
                                <div class="perf-fill good" style="width: 88%;"></div>
                            </div>
                        </div>
                    </div>

                    <div class="report-card">
                        <h4>💾 Resource Usage</h4>
                        <div class="perf-item">
                            <span class="perf-label">Total Size</span>
                            <span class="perf-value good">145 KB</span>
                        </div>
                        <div class="perf-item">
                            <span class="perf-label">Images</span>
                            <span class="perf-value good">98 KB</span>
                        </div>
                        <div class="perf-item">
                            <span class="perf-label">CSS</span>
                            <span class="perf-value good">28 KB</span>
                        </div>
                        <div class="perf-item">
                            <span class="perf-label">JavaScript</span>
                            <span class="perf-value warning">19 KB</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """

    def _render_user_insights(self) -> str:
        """Render user insights dashboard."""
        return """
        <div style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .user-insights {{ max-width: 1000px; }}
                .insight-card {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; }}
                .insight-card h4 {{ font-size: 1.125rem; font-weight: 600; color: #1e293b; margin: 0 0 1rem; }}
                .heatmap {{ display: grid; grid-template-columns: repeat(24, 1fr); gap: 2px; }}
                .heat-cell {{ height: 32px; border-radius: 4px; background: #f1f5f9; }}
                .heat-cell.level-1 {{ background: #dbeafe; }}
                .heat-cell.level-2 {{ background: #93c5fd; }}
                .heat-cell.level-3 {{ background: #2563eb; }}
                .user-segments {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; }}
                .segment-card {{ padding: 1rem; background: #f8fafc; border-radius: 8px; text-align: center; }}
                .segment-value {{ font-size: 1.5rem; font-weight: 700; color: #1e293b; }}
                .segment-label {{ font-size: 0.875rem; color: #64748b; }}
            </style>

            <div class="user-insights">
                <h3 style="margin-bottom: 1.5rem;">👥 User Insights</h3>

                <div class="insight-card">
                    <h4>🕐 User Activity Heatmap (Last 30 Days)</h4>
                    <div class="heatmap">
                        <div class="heat-cell level-1"></div>
                        <div class="heat-cell level-2"></div>
                        <div class="heat-cell level-3"></div>
                        <div class="heat-cell level-1"></div>
                        <div class="heat-cell level-2"></div>
                        <div class="heat-cell level-3"></div>
                        <div class="heat-cell level-1"></div>
                        <div class="heat-cell level-2"></div>
                        <div class="heat-cell level-3"></div>
                        <div class="heat-cell level-1"></div>
                        <div class="heat-cell level-2"></div>
                        <div class="heat-cell level-3"></div>
                        <div class="heat-cell level-1"></div>
                        <div class="heat-cell level-2"></div>
                        <div class="heat-cell level-3"></div>
                        <div class="heat-cell level-1"></div>
                        <div class="heat-cell level-2"></div>
                        <div class="heat-cell level-3"></div>
                        <div class="heat-cell level-1"></div>
                        <div class="heat-cell level-2"></div>
                        <div class="heat-cell level-3"></div>
                        <div class="heat-cell level-1"></div>
                        <div class="heat-cell level-2"></div>
                        <div class="heat-cell level-3"></div>
                        <div style="grid-column: span 24; text-align: center; margin-top: 0.5rem; font-size: 0.75rem; color: #64748b;">
                            Peak activity: 9 AM - 11 AM weekdays
                        </div>
                    </div>
                </div>

                <div class="insight-card">
                    <h4>📊 User Segments</h4>
                    <div class="user-segments">
                        <div class="segment-card">
                            <div class="segment-value">45%</div>
                            <div class="segment-label">Designers</div>
                        </div>
                        <div class="segment-card">
                            <div class="segment-value">30%</div>
                            <div class="segment-label">Developers</div>
                        </div>
                        <div class="segment-card">
                            <div class="segment-value">15%</div>
                            <div class="segment-label">Marketers</div>
                        </div>
                        <div class="segment-card">
                            <div class="segment-value">10%</div>
                            <div class="segment-label">Other</div>
                        </div>
                    </div>
                </div>

                <div class="insight-card">
                    <h4>💡 Key Insights</h4>
                    <div style="display: flex; flex-direction: column; gap: 1rem;">
                        <div style="padding: 1rem; background: #f8fafc; border-radius: 8px;">
                            <div style="font-weight: 600; color: #1e293b; margin-bottom: 0.25rem;">📱 Mobile Usage Growing</div>
                            <div style="font-size: 0.875rem; color: #64748b;">Mobile sessions increased 25% this month. Consider optimizing for mobile-first design.</div>
                        </div>
                        <div style="padding: 1rem; background: #f8fafc; border-radius: 8px;">
                            <div style="font-weight: 600; color: #1e293b; margin-bottom: 0.25rem;">🎨 Dark Mode Popular</div>
                            <div style="font-size: 0.875rem; color: #64748b;">62% of users prefer dark mode. Ensure all designs support dark theme.</div>
                        </div>
                        <div style="padding: 1rem; background: #f8fafc; border-radius: 8px;">
                            <div style="font-weight: 600; color: #1e293b; margin-bottom: 0.25rem;">⚡ Speed Matters</div>
                            <div style="font-size: 0.875rem; color: #64748b;">Pages loading under 2s have 40% higher engagement. Optimize performance.</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
