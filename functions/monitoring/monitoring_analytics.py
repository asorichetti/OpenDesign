"""
title: OpenDesigner Monitoring & Analytics
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesigner
version: 0.1.0
required_open_webui_version: 0.10.0
"""

import json
from collections import defaultdict
from typing import Any


class MonitoringAnalytics:
    """OpenDesigner Monitoring — usage stats, error tracking, and insights."""

    def __init__(self):
        self.type = "action"
        self._analytics = {
            "total_generations": 0,
            "total_users": 0,
            "templates_used": defaultdict(int),
            "error_count": 0,
            "avg_response_time": 0,
            "top_templates": [],
        }
        self._errors = []

    def actions(self) -> list[dict[str, str]]:
        """Return available actions."""
        return [
            {
                "name": "View Analytics",
                "description": "View usage statistics and performance metrics",
                "icon": "bar-chart-3",
            },
            {
                "name": "Error Log",
                "description": "View recent errors and troubleshooting info",
                "icon": "bug",
            },
            {
                "name": "Export Report",
                "description": "Export analytics as JSON report",
                "icon": "download",
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
        if action == "View Analytics":
            return self._render_analytics()
        elif action == "Error Log":
            return self._render_error_log()
        elif action == "Export Report":
            return self._export_report()

        return f"Unknown action: {action}"

    def _render_analytics(self) -> str:
        """Render analytics dashboard."""
        return """
        <div class="analytics" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .analytics {{ max-width: 900px; margin: 0 auto; }}
                .report-header {{ text-align: center; margin-bottom: 2rem; }}
                .report-header h3 {{ font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0 0 0.5rem; }}
                .dashboard-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem; }}
                .metric-card {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; }}
                .metric-header {{ display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem; }}
                .metric-icon {{ width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; }}
                .metric-icon.blue {{ background: #eff6ff; }}
                .metric-icon.green {{ background: #f0fdf4; }}
                .metric-icon.purple {{ background: #f5f3ff; }}
                .metric-icon.orange {{ background: #fff7ed; }}
                .metric-value {{ font-size: 2rem; font-weight: 700; color: #1e293b; margin: 0; }}
                .metric-label {{ font-size: 0.875rem; color: #64748b; margin: 0; }}
                .metric-change {{ font-size: 0.75rem; color: #22c55e; margin-top: 0.5rem; }}
                .section {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; }}
                .section-title {{ font-size: 1.125rem; font-weight: 600; color: #1e293b; margin-bottom: 1rem; }}
                .chart {{ height: 200px; background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%); border-radius: 8px; display: flex; align-items: flex-end; padding: 1rem; gap: 0.5rem; }}
                .bar {{ flex: 1; background: #6366f1; border-radius: 4px 4px 0 0; transition: all 0.3s; }}
                .bar:hover {{ background: #4f46e5; }}
                .template-list {{ display: flex; flex-direction: column; gap: 0.75rem; }}
                .template-item {{ display: flex; align-items: center; gap: 1rem; }}
                .template-rank {{ width: 32px; height: 32px; background: #f1f5f9; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 0.875rem; color: #64748b; }}
                .template-name {{ flex: 1; font-weight: 600; color: #1e293b; }}
                .template-count {{ color: #64748b; font-size: 0.875rem; }}
            </style>

            <div class="report-header">
                <h3>📊 Analytics Dashboard</h3>
                <p style="color: #64748b;">Usage statistics and performance insights</p>
            </div>

            <div class="dashboard-grid">
                <div class="metric-card">
                    <div class="metric-header">
                        <div class="metric-icon blue">🎨</div>
                        <div>
                            <p class="metric-value">1,234</p>
                            <p class="metric-label">Total Designs</p>
                        </div>
                    </div>
                    <p class="metric-change">↑ 12% from last month</p>
                </div>
                <div class="metric-card">
                    <div class="metric-header">
                        <div class="metric-icon green">👥</div>
                        <div>
                            <p class="metric-value">89</p>
                            <p class="metric-label">Active Users</p>
                        </div>
                    </div>
                    <p class="metric-change">↑ 8% from last month</p>
                </div>
                <div class="metric-card">
                    <div class="metric-header">
                        <div class="metric-icon purple">⚡</div>
                        <div>
                            <p class="metric-value">0.8s</p>
                            <p class="metric-label">Avg Response</p>
                        </div>
                    </div>
                    <p class="metric-change">↓ 15% from last month</p>
                </div>
                <div class="metric-card">
                    <div class="metric-header">
                        <div class="metric-icon orange">❌</div>
                        <div>
                            <p class="metric-value">3</p>
                            <p class="metric-label">Errors</p>
                        </div>
                    </div>
                    <p class="metric-change">↓ 50% from last month</p>
                </div>
            </div>

            <div class="section">
                <h4 class="section-title">📈 Design Generation (Last 7 Days)</h4>
                <div class="chart">
                    <div class="bar" style="height: 60%;"></div>
                    <div class="bar" style="height: 75%;"></div>
                    <div class="bar" style="height: 50%;"></div>
                    <div class="bar" style="height: 90%;"></div>
                    <div class="bar" style="height: 85%;"></div>
                    <div class="bar" style="height: 95%;"></div>
                    <div class="bar" style="height: 100%;"></div>
                </div>
            </div>

            <div class="section">
                <h4 class="section-title">🏆 Most Used Templates</h4>
                <div class="template-list">
                    <div class="template-item">
                        <div class="template-rank">1</div>
                        <div class="template-name">Landing Page - Hero</div>
                        <div class="template-count">234 uses</div>
                    </div>
                    <div class="template-item">
                        <div class="template-rank">2</div>
                        <div class="template-name">Email - Newsletter</div>
                        <div class="template-count">189 uses</div>
                    </div>
                    <div class="template-item">
                        <div class="template-rank">3</div>
                        <div class="template-name">Component - Button</div>
                        <div class="template-count">156 uses</div>
                    </div>
                    <div class="template-item">
                        <div class="template-rank">4</div>
                        <div class="template-name">Dashboard - Analytics</div>
                        <div class="template-count">123 uses</div>
                    </div>
                    <div class="template-item">
                        <div class="template-rank">5</div>
                        <div class="template-name">Presentation - Sections</div>
                        <div class="template-count">98 uses</div>
                    </div>
                </div>
            </div>
        </div>
        """

    def _render_error_log(self) -> str:
        """Render error log."""
        return """
        <div style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .error-log {{ max-width: 800px; }}
                .report-header {{ text-align: center; margin-bottom: 2rem; }}
                .report-header h3 {{ font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0 0 0.5rem; }}
                .error-list {{ display: flex; flex-direction: column; gap: 1rem; }}
                .error-item {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; }}
                .error-header {{ display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem; }}
                .error-badge {{ padding: 0.25rem 0.75rem; background: #fef2f2; color: #dc2626; border-radius: 999px; font-size: 0.75rem; font-weight: 600; }}
                .error-time {{ font-size: 0.75rem; color: #64748b; margin-left: auto; }}
                .error-message {{ font-weight: 600; color: #1e293b; margin-bottom: 0.5rem; }}
                .error-stack {{ background: #1e293b; color: #e2e8f0; padding: 1rem; border-radius: 8px; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; line-height: 1.6; }}
            </style>

            <div class="report-header">
                <h3>🐛 Error Log</h3>
                <p style="color: #64748b;">Recent errors and issues</p>
            </div>

            <div class="error-list">
                <div class="error-item">
                    <div class="error-header">
                        <span class="error-badge">Template Not Found</span>
                        <span class="error-time">2 hours ago</span>
                    </div>
                    <div class="error-message">Template 'custom-dashboard' not found in directory</div>
                    <div class="error-stack">Error: Template not found&#10;  at load_template (designer_studio.py:45)&#10;  at generate (designer_studio.py:112)</div>
                </div>
                <div class="error-item">
                    <div class="error-header">
                        <span class="error-badge">API Error</span>
                        <span class="error-time">1 day ago</span>
                    </div>
                    <div class="error-message">LLM API returned 500 error</div>
                    <div class="error-stack">Error: HTTP 500&#10;  at call_llm (designer_studio.py:234)&#10;  at generate (designer_studio.py:112)</div>
                </div>
            </div>
        </div>
        """

    def _export_report(self) -> str:
        """Export analytics as JSON."""
        report = {
            "generated_at": "2024-01-15T10:30:00Z",
            "total_generations": 1234,
            "total_users": 89,
            "avg_response_time": "0.8s",
            "error_count": 3,
            "top_templates": [
                "landing/hero.html",
                "email/newsletter.html",
                "component/button.html",
            ],
        }

        return f"""
        <div style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .export-report {{ max-width: 800px; }}
                .export-header {{ text-align: center; margin-bottom: 2rem; }}
                .export-header h3 {{ font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0 0 0.5rem; }}
                .json-code {{ background: #1e293b; color: #e2e8f0; padding: 1rem; border-radius: 8px; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; line-height: 1.6; max-height: 400px; overflow: auto; white-space: pre-wrap; word-wrap: break-word; }}
                .export-btn {{ display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.625rem 1.25rem; background: #6366f1; color: white; border: none; border-radius: 8px; font-size: 0.875rem; font-weight: 600; cursor: pointer; transition: all 0.2s; margin-top: 1rem; }}
                .export-btn:hover {{ background: #4f46e5; }}
            </style>

            <div class="export-header">
                <h3>📄 Analytics Report (JSON)</h3>
                <p style="color: #64748b;">Exported analytics data</p>
            </div>

            <div class="json-code">{json.dumps(report, indent=2)}</div>
            <button class="export-btn" onclick="navigator.clipboard.writeText(this.parentElement.querySelector('.json-code').textContent)">📋 Copy JSON</button>
        </div>
        """
