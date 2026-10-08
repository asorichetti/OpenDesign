"""
title: OpenDesigner API & Integrations
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesigner
version: 0.1.0
required_open_webui_version: 0.10.0
"""

from typing import Any


class Action:
    """OpenDesigner API — external integrations and programmatic access."""

    def __init__(self):
        self.type = "action"

    def actions(self) -> list[dict[str, str]]:
        """Return available actions."""
        return [
            {
                "name": "API Documentation",
                "description": "View API documentation and available endpoints",
                "icon": "book-open",
            },
            {
                "name": "API Keys",
                "description": "Manage API keys and access tokens",
                "icon": "key",
            },
            {
                "name": "Webhooks",
                "description": "Configure webhooks for event notifications",
                "icon": "webhook",
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
        if action == "API Documentation":
            return self._render_api_docs()
        elif action == "API Keys":
            return self._render_api_keys()
        elif action == "Webhooks":
            return self._render_webhooks()

        return f"Unknown action: {action}"

    def _render_api_docs(self) -> str:
        """Render API documentation."""
        return """
        <div class="api-docs" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .api-docs { max-width: 1000px; margin: 0 auto; }
                .docs-header { text-align: center; margin-bottom: 2rem; }
                .docs-header h3 { font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0 0 0.5rem; }
                .endpoint-card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; }
                .endpoint-header { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem; }
                .method-badge { padding: 0.25rem 0.75rem; border-radius: 6px; font-size: 0.75rem; font-weight: 700; }
                .method-badge.get { background: #dcfce7; color: #16a34a; }
                .method-badge.post { background: #dbeafe; color: #1e40af; }
                .method-badge.put { background: #fef3c7; color: #92400e; }
                .method-badge.delete { background: #fee2e2; color: #dc2626; }
                .endpoint-path { font-family: 'JetBrains Mono', monospace; font-size: 0.875rem; color: #1e293b; }
                .endpoint-desc { font-size: 0.875rem; color: #64748b; margin-bottom: 1rem; }
                .code-block { background: #1e293b; color: #e2e8f0; padding: 1rem; border-radius: 8px; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; line-height: 1.6; overflow-x: auto; }
                .section { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; }
                .section h4 { font-size: 1.125rem; font-weight: 600; color: #1e293b; margin-bottom: 1rem; }
            </style>

            <div class="docs-header">
                <h3>📚 API Documentation</h3>
                <p style="color: #64748b;">Integrate OpenDesigner with your applications</p>
            </div>

            <div class="section">
                <h4>🔑 Authentication</h4>
                <div class="code-block">
{ "Authorization": "Bearer YOUR_API_KEY" }
                </div>
            </div>

            <div class="section">
                <h4>🎨 Templates API</h4>
                <div class="endpoint-card">
                    <div class="endpoint-header">
                        <span class="method-badge get">GET</span>
                        <span class="endpoint-path">/api/v1/templates</span>
                    </div>
                    <p class="endpoint-desc">List all available templates</p>
                    <div class="code-block">{
  "templates": [
    { "id": "landing/hero", "name": "Hero Landing Page" },
    { "id": "email/newsletter", "name": "Newsletter Email" }
  ]
}</div>
                </div>

                <div class="endpoint-card">
                    <div class="endpoint-header">
                        <span class="method-badge post">POST</span>
                        <span class="endpoint-path">/api/v1/generate</span>
                    </div>
                    <p class="endpoint-desc">Generate design from template</p>
                    <div class="code-block">{
  "template": "landing/hero",
  "variables": {
    "title": "My Product",
    "description": "Best product ever"
  }
}</div>
                </div>
            </div>

            <div class="section">
                <h4>📊 Designs API</h4>
                <div class="endpoint-card">
                    <div class="endpoint-header">
                        <span class="method-badge get">GET</span>
                        <span class="endpoint-path">/api/v1/designs</span>
                    </div>
                    <p class="endpoint-desc">List all user designs</p>
                </div>

                <div class="endpoint-card">
                    <div class="endpoint-header">
                        <span class="method-badge post">POST</span>
                        <span class="endpoint-path">/api/v1/designs</span>
                    </div>
                    <p class="endpoint-desc">Create new design</p>
                </div>
            </div>
        </div>
        """

    def _render_api_keys(self) -> str:
        """Render API keys management."""
        return """
        <div style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .api-keys { max-width: 800px; }
                .key-card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; }
                .key-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
                .key-label { font-weight: 600; color: #1e293b; }
                .key-status { padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.75rem; font-weight: 600; }
                .key-status.active { background: #dcfce7; color: #16a34a; }
                .key-value { background: #1e293b; color: #e2e8f0; padding: 0.75rem; border-radius: 8px; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; word-break: break-all; }
                .key-actions { display: flex; gap: 0.5rem; margin-top: 1rem; }
                .key-btn { padding: 0.5rem 1rem; border-radius: 6px; font-size: 0.875rem; font-weight: 600; cursor: pointer; border: none; }
                .key-btn.primary { background: #6366f1; color: white; }
                .key-btn.secondary { background: #f1f5f9; color: #1e293b; }
                .create-key { background: #f0fdf4; border: 1px solid #86efac; border-radius: 12px; padding: 1.5rem; margin-top: 1.5rem; }
                .create-key h4 { color: #16a34a; margin-bottom: 1rem; }
            </style>

            <div class="api-keys">
                <h3 style="margin-bottom: 1.5rem;">🔑 API Keys</h3>

                <div class="key-card">
                    <div class="key-header">
                        <span class="key-label">Production Key</span>
                        <span class="key-status active">Active</span>
                    </div>
                    <div class="key-value">sk_live_••••••••••••1234</div>
                    <div class="key-actions">
                        <button class="key-btn secondary">Copy</button>
                        <button class="key-btn secondary">Rotate</button>
                        <button class="key-btn secondary">Revoke</button>
                    </div>
                </div>

                <div class="create-key">
                    <h4>➕ Create New Key</h4>
                    <div style="display: flex; gap: 0.75rem;">
                        <input type="text" placeholder="Key name" style="flex: 1; padding: 0.75rem; border: 1px solid #86efac; border-radius: 8px;">
                        <button class="key-btn primary">Create</button>
                    </div>
                </div>
            </div>
        </div>
        """

    def _render_webhooks(self) -> str:
        """Render webhooks configuration."""
        return """
        <div style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .webhooks { max-width: 800px; }
                .webhook-card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; }
                .webhook-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
                .webhook-url { font-family: 'JetBrains Mono', monospace; font-size: 0.875rem; color: #6366f1; }
                .webhook-events { display: flex; gap: 0.5rem; flex-wrap: wrap; margin: 1rem 0; }
                .event-tag { padding: 0.25rem 0.75rem; background: #f1f5f9; border-radius: 999px; font-size: 0.75rem; font-weight: 600; }
                .create-webhook { background: #f0fdf4; border: 1px solid #86efac; border-radius: 12px; padding: 1.5rem; }
                .create-webhook h4 { color: #16a34a; margin-bottom: 1rem; }
            </style>

            <div class="webhooks">
                <h3 style="margin-bottom: 1.5rem;">🪝 Webhooks</h3>

                <div class="webhook-card">
                    <div class="webhook-header">
                        <span class="key-label">Slack Notifications</span>
                        <span class="key-status active">Active</span>
                    </div>
                    <div class="webhook-url">https://hooks.slack.com/services/••••••••••••</div>
                    <div class="webhook-events">
                        <span class="event-tag">design.created</span>
                        <span class="event-tag">design.published</span>
                        <span class="event-tag">error</span>
                    </div>
                </div>

                <div class="create-webhook">
                    <h4>➕ Add New Webhook</h4>
                    <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                        <input type="text" placeholder="Webhook URL" style="padding: 0.75rem; border: 1px solid #86efac; border-radius: 8px;">
                        <select style="padding: 0.75rem; border: 1px solid #86efac; border-radius: 8px;">
                            <option>design.created</option>
                            <option>design.published</option>
                            <option>design.updated</option>
                            <option>error</option>
                        </select>
                        <button class="key-btn primary">Create Webhook</button>
                    </div>
                </div>
            </div>
        </div>
        """
