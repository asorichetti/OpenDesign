"""
title: AI Image Generation Integration
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesigner
version: 1.0.0
required_open_webui_version: 0.10.0
"""

from typing import Any


class Action:
    """AI Image Generation Integration — Generate images for your designs using AI."""

    def __init__(self):
        self.type = "action"

    def actions(self) -> list[dict[str, str]]:
        """Return available actions."""
        return [
            {
                "name": "Generate Image",
                "description": "Generate images using AI (DALL-E, Stable Diffusion, etc.)",
                "icon": "image",
            },
            {
                "name": "Image Styles",
                "description": "Browse AI image styles and presets",
                "icon": "palette",
            },
            {
                "name": "Image Library",
                "description": "Manage and organize your generated images",
                "icon": "folder",
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
        """Handle AI image action."""
        if action == "Generate Image":
            return self._render_generator(body)
        elif action == "Image Styles":
            return self._render_styles()
        elif action == "Image Library":
            return self._render_library()

        return f"Unknown action: {action}"

    def _render_generator(self, body: dict) -> str:
        """Render AI image generator."""
        return """
        <div class="ai-image-gen" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .ai-image-gen {{ max-width: 1200px; margin: 0 auto; }}
                .generator-header {{ text-align: center; margin-bottom: 2rem; }}
                .generator-header h3 {{ font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0 0 0.5rem; }}
                .generator-header p {{ color: #64748b; }}
                .input-form {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; }}
                .prompt-input {{ width: 100%; padding: 1rem; border: 2px solid #e2e8f0; border-radius: 12px; font-size: 1rem; margin-bottom: 1rem; }}
                .prompt-input:focus {{ outline: none; border-color: #6366f1; }}
                .generate-btn {{ padding: 1rem 2rem; background: #6366f1; color: white; border: none; border-radius: 12px; font-weight: 600; cursor: pointer; font-size: 1rem; }}
                .style-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1rem; }}
                .style-card {{ padding: 1rem; border: 2px solid #e2e8f0; border-radius: 12px; text-align: center; cursor: pointer; transition: all 0.2s; }}
                .style-card:hover {{ border-color: #6366f1; }}
                .style-card.selected {{ border-color: #6366f1; background: #f8fafc; }}
                .style-icon {{ font-size: 2rem; margin-bottom: 0.5rem; }}
                .style-name {{ font-weight: 600; color: #1e293b; }}
                .generated-images {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin-top: 1.5rem; }}
                .image-card {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; }}
                .image-placeholder {{ height: 200px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; align-items: center; justify-content: center; color: white; font-size: 3rem; }}
                .image-actions {{ padding: 1rem; display: flex; gap: 0.5rem; }}
                .image-action {{ flex: 1; padding: 0.5rem; border: 1px solid #e2e8f0; border-radius: 6px; background: white; cursor: pointer; font-size: 0.75rem; font-weight: 600; }}
                .image-action:hover {{ background: #f1f5f9; }}
            </style>

            <div class="ai-image-gen">
                <div class="generator-header">
                    <h3>🎨 AI Image Generator</h3>
                    <p>Generate beautiful images for your designs using AI</p>
                </div>

                <div class="input-form">
                    <label style="display: block; font-weight: 600; color: #1e293b; margin-bottom: 0.5rem;">Describe your image</label>
                    <textarea class="prompt-input" id="image-prompt" rows="3" placeholder="A modern hero section for a SaaS landing page with gradients and abstract shapes..."></textarea>

                    <label style="display: block; font-weight: 600; color: #1e293b; margin-bottom: 0.5rem;">Select Style</label>
                    <div class="style-grid">
                        <div class="style-card selected" onclick="selectStyle(this)">
                            <div class="style-icon">🎨</div>
                            <div class="style-name">Modern</div>
                        </div>
                        <div class="style-card" onclick="selectStyle(this)">
                            <div class="style-icon">🌈</div>
                            <div class="style-name">Colorful</div>
                        </div>
                        <div class="style-card" onclick="selectStyle(this)">
                            <div class="style-icon">⚫</div>
                            <div class="style-name">Minimal</div>
                        </div>
                        <div class="style-card" onclick="selectStyle(this)">
                            <div class="style-icon">🎭</div>
                            <div class="style-name">Artistic</div>
                        </div>
                        <div class="style-card" onclick="selectStyle(this)">
                            <div class="style-icon">📸</div>
                            <div class="style-name">Photorealistic</div>
                        </div>
                        <div class="style-card" onclick="selectStyle(this)">
                            <div class="style-icon">✏️</div>
                            <div class="style-name">Illustration</div>
                        </div>
                    </div>

                    <div style="margin-top: 1.5rem; text-align: center;">
                        <button class="generate-btn" onclick="generateImage()">🚀 Generate Image</button>
                    </div>
                </div>

                <h4 style="margin-bottom: 1rem;">Generated Images</h4>
                <div class="generated-images">
                    <div class="image-card">
                        <div class="image-placeholder">🖼️</div>
                        <div class="image-actions">
                            <button class="image-action">Download</button>
                            <button class="image-action">Use</button>
                            <button class="image-action">Regenerate</button>
                        </div>
                    </div>
                    <div class="image-card">
                        <div class="image-placeholder">🖼️</div>
                        <div class="image-actions">
                            <button class="image-action">Download</button>
                            <button class="image-action">Use</button>
                            <button class="image-action">Regenerate</button>
                        </div>
                    </div>
                    <div class="image-card">
                        <div class="image-placeholder">🖼️</div>
                        <div class="image-actions">
                            <button class="image-action">Download</button>
                            <button class="image-action">Use</button>
                            <button class="image-action">Regenerate</button>
                        </div>
                    </div>
                    <div class="image-card">
                        <div class="image-placeholder">🖼️</div>
                        <div class="image-actions">
                            <button class="image-action">Download</button>
                            <button class="image-action">Use</button>
                            <button class="image-action">Regenerate</button>
                        </div>
                    </div>
                </div>
            </div>

            <script>
                function selectStyle(card) {{
                    document.querySelectorAll('.style-card').forEach(c => c.classList.remove('selected'));
                    card.classList.add('selected');
                }}

                function generateImage() {{
                    const prompt = document.getElementById('image-prompt').value;
                    if (!prompt) {{
                        alert('Please enter a description');
                        return;
                    }}

                    const event = new CustomEvent('generateImage', {{
                        detail: {{ prompt: prompt }}
                    }});
                    window.parent.postMessage(event, '*');
                }}
            </script>
        </div>
        """

    def _render_styles(self) -> str:
        """Render AI image styles."""
        return """
        <div style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .styles-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; }}
                .style-card {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; }}
                .style-preview {{ height: 150px; border-radius: 8px; margin-bottom: 1rem; }}
                .style-name {{ font-size: 1.125rem; font-weight: 600; color: #1e293b; margin-bottom: 0.5rem; }}
                .style-desc {{ font-size: 0.875rem; color: #64748b; margin-bottom: 1rem; }}
                .use-btn {{ padding: 0.75rem 1.5rem; background: #6366f1; color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; }}
            </style>

            <h3 style="margin-bottom: 1.5rem;">🎨 AI Image Styles</h3>

            <div class="styles-grid">
                <div class="style-card">
                    <div class="style-preview" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);"></div>
                    <div class="style-name">Modern Gradient</div>
                    <div class="style-desc">Vibrant gradients with modern aesthetics</div>
                    <button class="use-btn">Use This Style</button>
                </div>

                <div class="style-card">
                    <div class="style-preview" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);"></div>
                    <div class="style-name">Colorful Burst</div>
                    <div class="style-desc">Bold and energetic color combinations</div>
                    <button class="use-btn">Use This Style</button>
                </div>

                <div class="style-card">
                    <div class="style-preview" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);"></div>
                    <div class="style-name">Ocean Blue</div>
                    <div class="style-desc">Cool blue tones for professional designs</div>
                    <button class="use-btn">Use This Style</button>
                </div>

                <div class="style-card">
                    <div class="style-preview" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);"></div>
                    <div class="style-name">Nature Fresh</div>
                    <div class="style-desc">Fresh green tones inspired by nature</div>
                    <button class="use-btn">Use This Style</button>
                </div>

                <div class="style-card">
                    <div class="style-preview" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);"></div>
                    <div class="style-name">Sunset Warm</div>
                    <div class="style-desc">Warm sunset tones for inviting designs</div>
                    <button class="use-btn">Use This Style</button>
                </div>

                <div class="style-card">
                    <div class="style-preview" style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);"></div>
                    <div class="style-name">Pastel Soft</div>
                    <div class="style-desc">Soft pastel colors for elegant designs</div>
                    <button class="use-btn">Use This Style</button>
                </div>
            </div>
        </div>
        """

    def _render_library(self) -> str:
        """Render image library."""
        return """
        <div style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .image-library {{ max-width: 1200px; }}
                .library-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1.5rem; }}
                .library-item {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; }}
                .library-image {{ height: 150px; display: flex; align-items: center; justify-content: center; color: white; font-size: 2rem; }}
                .library-info {{ padding: 1rem; }}
                .library-name {{ font-weight: 600; color: #1e293b; margin-bottom: 0.25rem; }}
                .library-meta {{ font-size: 0.75rem; color: #64748b; margin-bottom: 0.75rem; }}
                .library-actions {{ display: flex; gap: 0.5rem; }}
                .library-action {{ flex: 1; padding: 0.375rem; border: 1px solid #e2e8f0; border-radius: 6px; background: white; cursor: pointer; font-size: 0.75rem; }}
                .library-action:hover {{ background: #f1f5f9; }}
            </style>

            <div class="image-library">
                <h3 style="margin-bottom: 1.5rem;">📸 Image Library</h3>

                <div class="library-grid">
                    <div class="library-item">
                        <div class="library-image" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">🖼️</div>
                        <div class="library-info">
                            <div class="library-name">Hero Background</div>
                            <div class="library-meta">Generated 2 hours ago</div>
                            <div class="library-actions">
                                <button class="library-action">Use</button>
                                <button class="library-action">Download</button>
                            </div>
                        </div>
                    </div>
                    <div class="library-item">
                        <div class="library-image" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">🖼️</div>
                        <div class="library-info">
                            <div class="library-name">Card Image</div>
                            <div class="library-meta">Generated 5 hours ago</div>
                            <div class="library-actions">
                                <button class="library-action">Use</button>
                                <button class="library-action">Download</button>
                            </div>
                        </div>
                    </div>
                    <div class="library-item">
                        <div class="library-image" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">🖼️</div>
                        <div class="library-info">
                            <div class="library-name">Feature Banner</div>
                            <div class="library-meta">Generated 1 day ago</div>
                            <div class="library-actions">
                                <button class="library-action">Use</button>
                                <button class="library-action">Download</button>
                            </div>
                        </div>
                    </div>
                    <div class="library-item">
                        <div class="library-image" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">🖼️</div>
                        <div class="library-info">
                            <div class="library-name">Social Post</div>
                            <div class="library-meta">Generated 2 days ago</div>
                            <div class="library-actions">
                                <button class="library-action">Use</button>
                                <button class="library-action">Download</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
