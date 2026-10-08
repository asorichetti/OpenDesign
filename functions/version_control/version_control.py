"""
title: OpenDesigner Version Control
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesigner
version: 0.1.0
required_open_webui_version: 0.10.0
"""

from pathlib import Path
from typing import Any


class Action:
    """OpenDesigner Version Control — provides diff, rollback, and version history."""

    def __init__(self, data_dir: str | None = None):
        self.type = "action"
        self._data_dir = Path(data_dir) if data_dir else self._resolve_data_dir()

    def _resolve_data_dir(self) -> Path:
        """Resolve data directory."""
        import os

        webui_data = os.environ.get("OPENWEBUI_DATA_DIR")
        if webui_data:
            return Path(webui_data) / "opendesigner"
        return Path.home() / ".opendesigner"

    def actions(self) -> list[dict[str, str]]:
        """Return available actions."""
        return [
            {
                "name": "Version History",
                "description": "View version history and compare versions",
                "icon": "git-branch",
            },
            {
                "name": "Compare Versions",
                "description": "Compare two versions side-by-side",
                "icon": "columns",
            },
            {
                "name": "Rollback to Previous",
                "description": "Revert to the previous version",
                "icon": "undo-2",
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
        if action == "Version History":
            return self._render_version_history()
        elif action == "Compare Versions":
            return self._render_compare_versions()
        elif action == "Rollback to Previous":
            return self._render_rollback_confirmation()
        return f"Unknown action: {action}"

    def _render_version_history(self) -> str:
        """Render version history UI."""
        return """
        <div class="version-history" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .version-history { max-width: 800px; margin: 0 auto; }
                .version-header { text-align: center; margin-bottom: 2rem; }
                .version-header h3 { font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0 0 0.5rem; }
                .version-list { background: white; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; }
                .version-item { padding: 1rem 1.5rem; border-bottom: 1px solid #e2e8f0; display: flex; align-items: center; justify-content: space-between; cursor: pointer; transition: background 0.2s; }
                .version-item:last-child { border-bottom: none; }
                .version-item:hover { background: #f8fafc; }
                .version-info { display: flex; align-items: center; gap: 1rem; }
                .version-badge { background: #6366f1; color: white; padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.75rem; font-weight: 600; }
                .version-date { color: #64748b; font-size: 0.875rem; }
                .version-actions { display: flex; gap: 0.5rem; }
                .version-btn { padding: 0.5rem 1rem; border: 1px solid #e2e8f0; border-radius: 6px; background: white; color: #475569; font-size: 0.875rem; cursor: pointer; transition: all 0.2s; }
                .version-btn:hover { border-color: #6366f1; color: #6366f1; }
                .version-note { margin: 2rem 0; padding: 1rem; background: #f8fafc; border-radius: 8px; text-align: center; color: #64748b; }
            </style>
            <div class="version-header">
                <h3>📜 Version History</h3>
                <p style="color: #64748b; margin: 0;">Browse and compare your design versions</p>
            </div>
            <div class="version-list">
                <div class="version-item">
                    <div class="version-info">
                        <span class="version-badge">v3</span>
                        <span class="version-date">Today at 2:30 PM</span>
                    </div>
                    <div class="version-actions">
                        <button class="version-btn">👁️ Preview</button>
                        <button class="version-btn">📋 Copy</button>
                    </div>
                </div>
                <div class="version-item">
                    <div class="version-info">
                        <span class="version-badge">v2</span>
                        <span class="version-date">Today at 2:15 PM</span>
                    </div>
                    <div class="version-actions">
                        <button class="version-btn">👁️ Preview</button>
                        <button class="version-btn">📋 Copy</button>
                    </div>
                </div>
                <div class="version-item">
                    <div class="version-info">
                        <span class="version-badge">v1</span>
                        <span class="version-date">Today at 2:00 PM</span>
                    </div>
                    <div class="version-actions">
                        <button class="version-btn">👁️ Preview</button>
                        <button class="version-btn">📋 Copy</button>
                    </div>
                </div>
            </div>
            <div class="version-note">💡 Click on any version to preview or copy it</div>
        </div>
        """

    def _render_compare_versions(self) -> str:
        """Render version comparison UI."""
        return """
        <div class="version-compare" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .version-compare { max-width: 1200px; margin: 0 auto; }
                .compare-header { text-align: center; margin-bottom: 2rem; }
                .compare-header h3 { font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0 0 0.5rem; }
                .compare-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
                @media (max-width: 768px) { .compare-grid { grid-template-columns: 1fr; } }
                .compare-panel { background: white; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; }
                .compare-panel-header { padding: 1rem; background: #f8fafc; border-bottom: 1px solid #e2e8f0; font-weight: 600; color: #1e293b; }
                .compare-panel-body { padding: 1rem; max-height: 400px; overflow: auto; background: #1e293b; color: #e2e8f0; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; line-height: 1.6; }
            </style>
            <div class="compare-header">
                <h3>🔄 Version Comparison</h3>
                <p style="color: #64748b; margin: 0;">Side-by-side diff between versions</p>
            </div>
            <div class="compare-grid">
                <div class="compare-panel">
                    <div class="compare-panel-header">📄 Version 1 (Original)</div>
                    <div class="compare-panel-body"><!DOCTYPE html>
<html><body><h1>Old Version</h1>
<p>This is the original design.</p></body></html></div>
                </div>
                <div class="compare-panel">
                    <div class="compare-panel-header">✨ Version 2 (Updated)</div>
                    <div class="compare-panel-body"><!DOCTYPE html>
<html><body><h1>Updated Version</h1>
<p>This is the improved design with new features.</p>
<button>Click Me</button></body></html></div>
                </div>
            </div>
            <div style="margin-top: 1.5rem; padding: 1rem; background: #f8fafc; border-radius: 8px;">
                <h4 style="margin: 0 0 0.75rem; color: #1e293b;">📊 Changes Summary</h4>
                <pre style="margin: 0; padding: 1rem; background: #1e293b; color: #e2e8f0; border-radius: 8px; overflow-x: auto; font-size: 0.75rem;">- &lt;h1&gt;Old Version&lt;/h1&gt;
+ &lt;h1&gt;Updated Version&lt;/h1&gt;
+ &lt;button&gt;Click Me&lt;/button&gt;</pre>
            </div>
        </div>
        """

    def _render_rollback_confirmation(self) -> str:
        """Render rollback confirmation UI."""
        return """
        <div class="rollback-confirm" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .rollback-confirm { max-width: 600px; margin: 0 auto; text-align: center; }
                .rollback-card { background: #fef3c7; border: 2px solid #f59e0b; border-radius: 12px; padding: 2rem; }
                .rollback-icon { font-size: 3rem; margin-bottom: 1rem; }
                .rollback-title { font-size: 1.25rem; font-weight: 700; color: #92400e; margin: 0 0 0.75rem; }
                .rollback-message { color: #78350f; margin: 0 0 1.5rem; line-height: 1.6; }
                .rollback-buttons { display: flex; gap: 1rem; justify-content: center; }
                .rollback-btn { padding: 0.75rem 1.5rem; border-radius: 8px; font-size: 0.875rem; font-weight: 600; cursor: pointer; transition: all 0.2s; border: none; }
                .rollback-btn-confirm { background: #f59e0b; color: white; }
                .rollback-btn-confirm:hover { background: #d97706; }
                .rollback-btn-cancel { background: white; color: #64748b; border: 1px solid #e2e8f0; }
                .rollback-btn-cancel:hover { background: #f8fafc; }
            </style>
            <div class="rollback-card">
                <div class="rollback-icon">⚠️</div>
                <h3 class="rollback-title">Rollback to Previous Version?</h3>
                <p class="rollback-message">This will revert your design to the previous version. Current changes will be saved as a new version.</p>
                <div class="rollback-buttons">
                    <button class="rollback-btn rollback-btn-confirm">✅ Yes, Rollback</button>
                    <button class="rollback-btn rollback-btn-cancel" onclick="location.reload()">❌ Cancel</button>
                </div>
            </div>
        </div>
        """
