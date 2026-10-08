"""
title: OpenDesigner Authentication & Authorization
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesigner
version: 0.1.0
required_open_webui_version: 0.10.0
"""

import time
from typing import Any


class Action:
    """OpenDesigner Authentication — secure access control and user management."""

    def __init__(self):
        self.type = "action"
        self.sessions = {}
        self.users = {}

    def actions(self) -> list[dict[str, str]]:
        """Return available actions."""
        return [
            {
                "name": "User Settings",
                "description": "Configure user preferences and account settings",
                "icon": "user",
            },
            {
                "name": "Security Settings",
                "description": "Manage authentication and security preferences",
                "icon": "shield",
            },
            {
                "name": "Team Management",
                "description": "Manage team members and permissions",
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
        """Handle action click."""
        if action == "User Settings":
            return self._render_user_settings(__user__)
        elif action == "Security Settings":
            return self._render_security_settings()
        elif action == "Team Management":
            return self._render_team_management()

        return f"Unknown action: {action}"

    def _render_user_settings(self, __user__: dict | None = None) -> str:
        """Render user settings UI."""
        return """
        <div class="auth-settings" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .auth-settings {{ max-width: 800px; margin: 0 auto; }}
                .settings-header {{ text-align: center; margin-bottom: 2rem; }}
                .settings-header h3 {{ font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0 0 0.5rem; }}
                .settings-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }}
                .settings-card {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; }}
                .settings-card h4 {{ font-size: 1.125rem; font-weight: 600; color: #1e293b; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; }}
                .setting-item {{ display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 0; border-bottom: 1px solid #f1f5f9; }}
                .setting-item:last-child {{ border-bottom: none; }}
                .setting-label {{ font-size: 0.875rem; color: #64748b; }}
                .setting-value {{ font-size: 0.875rem; font-weight: 600; color: #1e293b; }}
                .toggle {{ position: relative; width: 48px; height: 24px; background: #e2e8f0; border-radius: 12px; cursor: pointer; transition: all 0.3s; }}
                .toggle.active {{ background: #6366f1; }}
                .toggle::after {{ content: ''; position: absolute; top: 2px; left: 2px; width: 20px; height: 20px; background: white; border-radius: 50%; transition: all 0.3s; }}
                .toggle.active::after {{ left: 26px; }}
                .form-group {{ margin-bottom: 1rem; }}
                .form-group label {{ display: block; font-size: 0.875rem; font-weight: 600; color: #1e293b; margin-bottom: 0.5rem; }}
                .form-group input {{ width: 100%; padding: 0.75rem; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 0.875rem; }}
                .save-btn {{ width: 100%; padding: 0.75rem; background: #6366f1; color: white; border: none; border-radius: 8px; font-size: 0.875rem; font-weight: 600; cursor: pointer; }}
                @media (max-width: 768px) {{ .settings-grid {{ grid-template-columns: 1fr; }} }}
            </style>

            <div class="settings-header">
                <h3>👤 User Settings</h3>
                <p style="color: #64748b;">Manage your account preferences</p>
            </div>

            <div class="settings-grid">
                <div class="settings-card">
                    <h4>📝 Profile</h4>
                    <div class="form-group">
                        <label>Username</label>
                        <input type="text" value="{{ __user__.get('name', 'Anonymous') if __user__ else 'Anonymous' }}" readonly>
                    </div>
                    <div class="form-group">
                        <label>User ID</label>
                        <input type="text" value="{{ __user__.get('_id', 'anonymous') if __user__ else 'anonymous' }}" readonly>
                    </div>
                    <div class="form-group">
                        <label>Email</label>
                        <input type="email" value="user@example.com" placeholder="your@email.com">
                    </div>
                </div>

                <div class="settings-card">
                    <h4>🎨 Appearance</h4>
                    <div class="setting-item">
                        <span class="setting-label">Dark Mode</span>
                        <div class="toggle active"></div>
                    </div>
                    <div class="setting-item">
                        <span class="setting-label">Compact View</span>
                        <div class="toggle"></div>
                    </div>
                    <div class="setting-item">
                        <span class="setting-label">Animations</span>
                        <div class="toggle active"></div>
                    </div>
                </div>
            </div>

            <div class="settings-card" style="margin-top: 1.5rem;">
                <h4>💾 Data Preferences</h4>
                <div class="form-group">
                    <label>Auto-save Interval</label>
                    <select style="width: 100%; padding: 0.75rem; border: 1px solid #e2e8f0; border-radius: 8px;">
                        <option>Every 30 seconds</option>
                        <option selected>Every 1 minute</option>
                        <option>Every 5 minutes</option>
                        <option>Manual only</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Default Template</label>
                    <select style="width: 100%; padding: 0.75rem; border: 1px solid #e2e8f0; border-radius: 8px;">
                        <option>Blank</option>
                        <option selected>Landing Page - Hero</option>
                        <option>Email - Newsletter</option>
                        <option>Component - Button</option>
                    </select>
                </div>
                <button class="save-btn">💾 Save Settings</button>
            </div>
        </div>
        """

    def _render_security_settings(self) -> str:
        """Render security settings UI."""
        return """
        <div class="security-settings" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .security-settings {{ max-width: 800px; margin: 0 auto; }}
                .settings-header {{ text-align: center; margin-bottom: 2rem; }}
                .settings-header h3 {{ font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0 0 0.5rem; }}
                .settings-card {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; }}
                .settings-card h4 {{ font-size: 1.125rem; font-weight: 600; color: #1e293b; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; }}
                .security-item {{ display: flex; justify-content: space-between; align-items: center; padding: 1rem; background: #f8fafc; border-radius: 8px; margin-bottom: 0.75rem; }}
                .security-info {{ flex: 1; }}
                .security-title {{ font-weight: 600; color: #1e293b; margin-bottom: 0.25rem; }}
                .security-desc {{ font-size: 0.875rem; color: #64748b; }}
                .security-badge {{ padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.75rem; font-weight: 600; }}
                .security-badge.enabled {{ background: #dcfce7; color: #16a34a; }}
                .security-badge.disabled {{ background: #fee2e2; color: #dc2626; }}
                .action-btn {{ padding: 0.5rem 1rem; background: #6366f1; color: white; border: none; border-radius: 6px; font-size: 0.875rem; font-weight: 600; cursor: pointer; }}
            </style>

            <div class="settings-header">
                <h3>🔒 Security Settings</h3>
                <p style="color: #64748b;">Manage authentication and security</p>
            </div>

            <div class="settings-card">
                <h4>🔐 Authentication</h4>
                <div class="security-item">
                    <div class="security-info">
                        <div class="security-title">Two-Factor Authentication</div>
                        <div class="security-desc">Add an extra layer of security to your account</div>
                    </div>
                    <span class="security-badge enabled">Enabled</span>
                </div>
                <div class="security-item">
                    <div class="security-info">
                        <div class="security-title">Session Timeout</div>
                        <div class="security-desc">Automatically log out after inactivity</div>
                    </div>
                    <select style="padding: 0.5rem; border: 1px solid #e2e8f0; border-radius: 6px;">
                        <option>15 minutes</option>
                        <option selected>1 hour</option>
                        <option>4 hours</option>
                        <option>Never</option>
                    </select>
                </div>
            </div>

            <div class="settings-card">
                <h4>🛡️ API Security</h4>
                <div class="security-item">
                    <div class="security-info">
                        <div class="security-title">API Key Rotation</div>
                        <div class="security-desc">Regularly rotate API keys for security</div>
                    </div>
                    <button class="action-btn">Rotate Key</button>
                </div>
                <div class="security-item">
                    <div class="security-info">
                        <div class="security-title">Rate Limiting</div>
                        <div class="security-desc">Prevent abuse with request rate limits</div>
                    </div>
                    <span class="security-badge enabled">Active</span>
                </div>
            </div>

            <div class="settings-card">
                <h4>📋 Audit Log</h4>
                <div class="security-item">
                    <div class="security-info">
                        <div class="security-title">Login Activity</div>
                        <div class="security-desc">Last login: Today at 10:30 AM from San Francisco, CA</div>
                    </div>
                    <button class="action-btn">View Details</button>
                </div>
                <div class="security-item">
                    <div class="security-info">
                        <div class="security-title">Active Sessions</div>
                        <div class="security-desc">2 active sessions on 2 devices</div>
                    </div>
                    <button class="action-btn">Manage</button>
                </div>
            </div>
        </div>
        """

    def _render_team_management(self) -> str:
        """Render team management UI."""
        return """
        <div class="team-management" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .team-management {{ max-width: 900px; margin: 0 auto; }}
                .settings-header {{ text-align: center; margin-bottom: 2rem; }}
                .settings-header h3 {{ font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0 0 0.5rem; }}
                .team-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-bottom: 2rem; }}
                .member-card {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; }}
                .member-header {{ display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem; }}
                .member-avatar {{ width: 48px; height: 48px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; color: white; }}
                .member-info h4 {{ font-size: 1rem; margin-bottom: 0.25rem; }}
                .member-info p {{ font-size: 0.875rem; color: #64748b; }}
                .role-badge {{ display: inline-block; padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.75rem; font-weight: 600; margin-top: 0.5rem; }}
                .role-badge.owner {{ background: #fef3c7; color: #92400e; }}
                .role-badge.admin {{ background: #dbeafe; color: #1e40af; }}
                .role-badge.editor {{ background: #dcfce7; color: #16a34a; }}
                .invite-section {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; }}
                .invite-section h4 {{ font-size: 1.125rem; font-weight: 600; color: #1e293b; margin-bottom: 1rem; }}
                .invite-form {{ display: flex; gap: 0.75rem; }}
                .invite-input {{ flex: 1; padding: 0.75rem; border: 1px solid #e2e8f0; border-radius: 8px; }}
                .invite-btn {{ padding: 0.75rem 1.5rem; background: #6366f1; color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; }}
            </style>

            <div class="settings-header">
                <h3>👥 Team Management</h3>
                <p style="color: #64748b;">Manage team members and permissions</p>
            </div>

            <div class="team-grid">
                <div class="member-card">
                    <div class="member-header">
                        <div class="member-avatar" style="background: #6366f1;">YO</div>
                        <div class="member-info">
                            <h4>You</h4>
                            <p>you@example.com</p>
                            <span class="role-badge owner">Owner</span>
                        </div>
                    </div>
                </div>

                <div class="member-card">
                    <div class="member-header">
                        <div class="member-avatar" style="background: #22c55e;">AS</div>
                        <div class="member-info">
                            <h4>Alice Smith</h4>
                            <p>alice@example.com</p>
                            <span class="role-badge admin">Admin</span>
                        </div>
                    </div>
                </div>

                <div class="member-card">
                    <div class="member-header">
                        <div class="member-avatar" style="background: #f59e0b;">BJ</div>
                        <div class="member-info">
                            <h4>Bob Johnson</h4>
                            <p>bob@example.com</p>
                            <span class="role-badge editor">Editor</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="invite-section">
                <h4>📧 Invite Team Members</h4>
                <div class="invite-form">
                    <input type="email" class="invite-input" placeholder="Enter email address">
                    <select style="padding: 0.75rem; border: 1px solid #e2e8f0; border-radius: 8px;">
                        <option>Editor</option>
                        <option>Admin</option>
                    </select>
                    <button class="invite-btn">Invite</button>
                </div>
            </div>
        </div>
        """

    def create_session(self, user_id: str, expires_in: int = 3600) -> str:
        """Create a new session."""
        import hashlib
        import time

        session_id = hashlib.sha256(f"{user_id}{time.time()}".encode()).hexdigest()[:32]
        self.sessions[session_id] = {
            "user_id": user_id,
            "created_at": time.time(),
            "expires_at": time.time() + expires_in,
        }
        return session_id

    def verify_session(self, session_id: str) -> bool:
        """Verify if a session is valid."""
        if session_id not in self.sessions:
            return False
        session = self.sessions[session_id]
        if session["expires_at"] < time.time():
            del self.sessions[session_id]
            return False
        return True

    def hash_password(self, password: str, salt: str = "") -> str:
        """Hash a password securely."""
        import hashlib

        salted_password = f"{salt}{password}"
        return hashlib.sha256(salted_password.encode()).hexdigest()
