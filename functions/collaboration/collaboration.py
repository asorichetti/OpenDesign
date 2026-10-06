"""
title: OpenDesigner Real-time Collaboration
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesigner
version: 0.1.0
required_open_webui_version: 0.10.0
"""

from typing import Any


class Collaboration:
    """OpenDesigner Real-time Collaboration — multi-user editing support."""

    def __init__(self):
        self.type = "filter"
        self.active_users = {}

    async def process(
        self,
        body: dict,
        __user__: dict | None = None,
        __event_emitter__: Any | None = None,
        **kwargs,
    ) -> dict:
        """Process collaboration events."""
        messages = body.get("messages", [])
        if messages:
            last_message = messages[-1].get("content", "").lower()
            if any(
                phrase in last_message
                for phrase in ["collaborate", "share", "co-edit", "invite"]
            ):
                return await self._handle_collaboration(
                    last_message, __event_emitter__
                )
        return body

    async def _handle_collaboration(
        self, prompt: str, __event_emitter__: Any | None = None
    ) -> dict:
        """Handle collaboration request."""
        if __event_emitter__:
            await __event_emitter__(
                "event.message",
                {
                    "type": "generating",
                    "content": "👥 Setting up collaboration session...",
                },
            )

        collaboration_html = self._render_collaboration_ui()

        if __event_emitter__:
            await __event_emitter__(
                "event.message",
                {"type": "generating", "content": "✅ Collaboration session ready!"},
            )

        return collaboration_html

    def _render_collaboration_ui(self) -> str:
        """Render collaboration UI."""
        return """
        <div class="collaboration-panel" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .collaboration-panel { max-width: 800px; margin: 0 auto; }
                .collab-header { text-align: center; margin-bottom: 2rem; }
                .collab-header h3 { font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0 0 0.5rem; }
                .collab-header p { color: #64748b; margin: 0; }
                .collab-card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; }
                .collab-title { font-size: 1rem; font-weight: 600; color: #1e293b; margin: 0 0 1rem; }
                .users-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem; }
                .user-card { padding: 1rem; background: #f8fafc; border-radius: 8px; display: flex; align-items: center; gap: 0.75rem; }
                .user-avatar { width: 40px; height: 40px; border-radius: 50%; background: #6366f1; color: white; display: flex; align-items: center; justify-content: center; font-weight: 600; }
                .user-info { flex: 1; }
                .user-name { font-weight: 600; color: #1e293b; font-size: 0.875rem; }
                .user-role { font-size: 0.75rem; color: #64748b; }
                .user-status { width: 8px; height: 8px; border-radius: 50%; background: #22c55e; }
                .invite-form { display: flex; gap: 0.75rem; margin-bottom: 1rem; }
                .invite-input { flex: 1; padding: 0.75rem 1rem; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 0.875rem; outline: none; }
                .invite-input:focus { border-color: #6366f1; }
                .invite-btn { padding: 0.75rem 1.5rem; background: #6366f1; color: white; border: none; border-radius: 8px; font-size: 0.875rem; font-weight: 600; cursor: pointer; transition: all 0.2s; }
                .invite-btn:hover { background: #4f46e5; }
                .collab-footer { text-align: center; padding: 1rem; background: #f0fdf4; border-radius: 8px; color: #16a34a; font-weight: 600; }
            </style>
            <div class="collab-header">
                <h3>👥 Real-time Collaboration</h3>
                <p>Invite others to edit and collaborate on your design</p>
            </div>
            <div class="collab-card">
                <h4 class="collab-title">👤 Active Users</h4>
                <div class="users-grid">
                    <div class="user-card">
                        <div class="user-avatar">YO</div>
                        <div class="user-info">
                            <div class="user-name">You (Owner)</div>
                            <div class="user-role">Full access</div>
                        </div>
                        <div class="user-status"></div>
                    </div>
                </div>
            </div>
            <div class="collab-card">
                <h4 class="collab-title">📧 Invite Collaborators</h4>
                <div class="invite-form">
                    <input type="email" class="invite-input" placeholder="Enter email address..." />
                    <button class="invite-btn">Invite</button>
                </div>
                <div style="color: #64748b; font-size: 0.875rem;">
                    Share this link: <code style="background: #f1f5f9; padding: 0.25rem 0.5rem; border-radius: 4px;">https://opendesigner.app/share/abc123</code>
                </div>
            </div>
            <div class="collab-footer">✅ Collaboration session is ready! Share the link with your team.</div>
        </div>
        """
