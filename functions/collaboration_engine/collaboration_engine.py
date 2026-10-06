"""
title: OpenDesigner Real-time Collaboration Engine
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesigner
version: 0.2.0
required_open_webui_version: 0.10.0
"""

import time
from collections import defaultdict
from typing import Any


class CollaborationEngine:
    """OpenDesigner Real-time Collaboration — WebSocket-based collaborative editing."""

    def __init__(self):
        self.type = "filter"
        self.sessions = {}
        self.cursors = defaultdict(dict)

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
            last_content = messages[-1].get("content", "").lower()

            # Detect collaboration requests
            if any(
                phrase in last_content for phrase in ["collaborate", "share", "co-edit", "invite"]
            ):
                return await self._start_session(last_content, __event_emitter__)

            # Detect cursor movements (simulated)
            if "move cursor" in last_content or "select" in last_content:
                return await self._handle_cursor(__user__, last_content, __event_emitter__)

        return body

    async def _start_session(self, prompt: str, __event_emitter__: Any | None = None) -> dict:
        """Start a collaboration session."""
        session_id = f"session_{int(time.time())}"
        self.sessions[session_id] = {
            "created_at": time.time(),
            "users": [],
            "document": None,
        }

        if __event_emitter__:
            await __event_emitter__(
                "event.message",
                {"type": "generating", "content": "👥 Creating collaboration session..."},
            )

        session_html = self._render_session_ui(session_id)

        if __event_emitter__:
            await __event_emitter__(
                "event.message",
                {"type": "generating", "content": "✅ Collaboration session ready!"},
            )

        return session_html

    def _render_session_ui(self, session_id: str) -> str:
        """Render collaboration session UI."""
        return """
        <div class="collab-engine" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .collab-engine { max-width: 900px; margin: 0 auto; }
                .session-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem; }
                .session-title { font-size: 1.5rem; font-weight: 700; color: #1e293b; }
                .session-badge { padding: 0.5rem 1rem; background: #22c55e; color: white; border-radius: 999px; font-size: 0.875rem; font-weight: 600; }
                .collab-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 1.5rem; }
                .editor-panel { background: #1e293b; border-radius: 12px; padding: 1.5rem; min-height: 400px; color: #e2e8f0; font-family: 'JetBrains Mono', monospace; font-size: 0.875rem; line-height: 1.6; position: relative; }
                .cursor { position: absolute; width: 2px; height: 20px; background: #6366f1; animation: blink 1s infinite; }
                .cursor-label { position: absolute; top: -20px; left: 0; background: #6366f1; color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.625rem; }
                @keyframes blink { 0%, 50% { opacity: 1; } 51%, 100% { opacity: 0; } }
                .sidebar { display: flex; flex-direction: column; gap: 1rem; }
                .user-card { padding: 1rem; background: white; border: 1px solid #e2e8f0; border-radius: 8px; }
                .user-card h4 { font-size: 0.875rem; margin-bottom: 0.75rem; color: #1e293b; }
                .user-item { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem; }
                .user-avatar { width: 32px; height: 32px; border-radius: 50%; background: #6366f1; color: white; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 600; }
                .user-name { font-size: 0.875rem; font-weight: 600; color: #1e293b; }
                .invite-box { padding: 1rem; background: #f0fdf4; border-radius: 8px; }
                .invite-box h4 { font-size: 0.875rem; margin-bottom: 0.75rem; color: #16a34a; }
                .invite-input { width: 100%; padding: 0.5rem; border: 1px solid #e2e8f0; border-radius: 6px; margin-bottom: 0.5rem; }
                .invite-btn { width: 100%; padding: 0.5rem; background: #6366f1; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: 600; }
                .share-link { display: flex; gap: 0.5rem; }
                .share-link input { flex: 1; padding: 0.5rem; border: 1px solid #e2e8f0; border-radius: 6px; font-size: 0.75rem; }
                .copy-btn { padding: 0.5rem 0.75rem; background: #10b981; color: white; border: none; border-radius: 6px; cursor: pointer; }
            </style>

            <div class="session-header">
                <h3 class="session-title">👥 Live Collaboration</h3>
                <span class="session-badge">● Live</span>
            </div>

            <div class="collab-grid">
                <div class="editor-panel">
                    <div style="position: relative;">
                        <div class="cursor" style="top: 40px; left: 120px;">
                            <div class="cursor-label">Alice</div>
                        </div>
                        <div class="cursor" style="top: 80px; left: 200px; background: #f59e0b;">
                            <div class="cursor-label" style="background: #f59e0b;">Bob</div>
                        </div>
                        <p style="margin-bottom: 1rem;"><code>&lt;!DOCTYPE html&gt;</code></p>
                        <p style="margin-bottom: 1rem;"><code>&lt;html&gt;</code></p>
                        <p style="margin-bottom: 1rem;"><code>&lt;head&gt;</code></p>
                        <p style="margin-bottom: 1rem;"><code>&lt;title&gt;Collaborative Document&lt;/title&gt;</code></p>
                        <p style="margin-bottom: 1rem;"><code>&lt;/head&gt;</code></p>
                        <p style="margin-bottom: 1rem;"><code>&lt;body&gt;</code></p>
                        <p style="margin-bottom: 1rem;"><code>&lt;h1&gt;Editing together...&lt;/h1&gt;</code></p>
                        <p><code>&lt;/body&gt;</code></p>
                    </div>
                </div>

                <div class="sidebar">
                    <div class="user-card">
                        <h4>👤 Active Users (3)</h4>
                        <div class="user-item">
                            <div class="user-avatar">YO</div>
                            <span class="user-name">You (Owner)</span>
                        </div>
                        <div class="user-item">
                            <div class="user-avatar" style="background: #f59e0b;">AL</div>
                            <span class="user-name">Alice</span>
                        </div>
                        <div class="user-item">
                            <div class="user-avatar" style="background: #22c55e;">BO</div>
                            <span class="user-name">Bob</span>
                        </div>
                    </div>

                    <div class="invite-box">
                        <h4>📧 Invite Others</h4>
                        <input type="email" class="invite-input" placeholder="Email address">
                        <button class="invite-btn">Send Invite</button>
                    </div>

                    <div class="invite-box">
                        <h4>🔗 Share Link</h4>
                        <div class="share-link">
                            <input type="text" value="https://opendesigner.app/share/{{ session_id }}" readonly>
                            <button class="copy-btn">Copy</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """

    async def _handle_cursor(
        self,
        __user__: dict | None = None,
        content: str = "",
        __event_emitter__: Any | None = None,
    ) -> dict:
        """Handle cursor movements."""
        if __event_emitter__:
            user_name = __user__["name"] if __user__ else "Unknown"
            await __event_emitter__(
                "event.message",
                {
                    "type": "system",
                    "content": f"👀 {user_name} is viewing the document",
                },
            )

        return {"type": "cursor_update"}
