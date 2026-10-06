"""
title: OpenDesigner AI Prompt Generator
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesigner
version: 0.1.0
required_open_webui_version: 0.10.0
"""

from typing import Any


class PromptGenerator:
    """OpenDesigner AI Prompt Generator — creates prompts for any AI model."""

    def __init__(self):
        self.type = "action"

    def actions(self) -> list[dict[str, str]]:
        """Return available actions."""
        return [
            {
                "name": "Generate AI Prompt",
                "description": "Create a detailed prompt to recreate this design in any AI model (ChatGPT, Claude, Ollama, etc.)",
                "icon": "message-circle",
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
        if action == "Generate AI Prompt":
            content = body.get("message", {}).get("content", "")
            return self._generate_prompt(content)

        return f"Unknown action: {action}"

    def _generate_prompt(self, content: str) -> str:
        """Generate AI prompt from design content."""
        return f"""
        <div class="prompt-generator" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .prompt-generator {{
                    max-width: 800px;
                    margin: 0 auto;
                }}
                .prompt-header {{
                    text-align: center;
                    margin-bottom: 2rem;
                }}
                .prompt-header h3 {{
                    font-size: 1.5rem;
                    font-weight: 700;
                    color: #1e293b;
                    margin: 0 0 0.5rem;
                }}
                .prompt-header p {{
                    color: #64748b;
                    margin: 0;
                }}
                .prompt-card {{
                    background: #f8fafc;
                    border: 1px solid #e2e8f0;
                    border-radius: 12px;
                    padding: 1.5rem;
                    margin-bottom: 1.5rem;
                }}
                .prompt-label {{
                    font-size: 0.875rem;
                    font-weight: 600;
                    color: #475569;
                    margin-bottom: 0.75rem;
                }}
                .prompt-text {{
                    background: white;
                    border: 1px solid #e2e8f0;
                    border-radius: 8px;
                    padding: 1rem;
                    font-family: 'JetBrains Mono', 'Fira Code', monospace;
                    font-size: 0.8125rem;
                    line-height: 1.7;
                    color: #334155;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                    max-height: 400px;
                    overflow-y: auto;
                }}
                .model-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 0.75rem;
                    margin-top: 1rem;
                }}
                .model-card {{
                    padding: 1rem;
                    background: white;
                    border: 2px solid #e2e8f0;
                    border-radius: 10px;
                    cursor: pointer;
                    transition: all 0.2s ease;
                    text-align: center;
                }}
                .model-card:hover {{
                    border-color: #6366f1;
                    background: #f0f0ff;
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15);
                }}
                .model-icon {{
                    font-size: 1.75rem;
                    margin-bottom: 0.5rem;
                }}
                .model-name {{
                    font-weight: 600;
                    color: #1e293b;
                    margin-bottom: 0.25rem;
                }}
                .model-desc {{
                    font-size: 0.75rem;
                    color: #64748b;
                }}
                .copy-btn {{
                    display: inline-flex;
                    align-items: center;
                    gap: 0.5rem;
                    padding: 0.625rem 1.25rem;
                    background: #6366f1;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 0.875rem;
                    font-weight: 600;
                    cursor: pointer;
                    margin-top: 1rem;
                    transition: all 0.2s;
                }}
                .copy-btn:hover {{
                    background: #4f46e5;
                    transform: translateY(-1px);
                }}
            </style>

            <div class="prompt-header">
                <h3>🤖 Generate AI Prompt</h3>
                <p>Create a prompt to recreate this design in any AI model</p>
            </div>

            <div class="prompt-card">
                <div class="prompt-label">✨ Generated Prompt</div>
                <div class="prompt-text" id="generated-prompt">Create a modern, responsive landing page with the following specifications:

## Page Type
Landing Page

## Required Components
• Navigation bar with menu items
• Hero section with call-to-action
• Features section with icons
• Footer with links and copyright

## Design Requirements
- Modern, clean aesthetic
- Medium complexity level
- Professional typography
- Cohesive color scheme (indigo/violet gradient)
- Accessible (WCAG 2.1 AA compliant)
- Mobile-first responsive design

## Technical Requirements
- Single HTML file with inline CSS
- No external dependencies
- Semantic HTML5 elements
- CSS custom properties for theming
- Smooth transitions and micro-interactions

Generate the complete, production-ready HTML code.</div>
                <button class="copy-btn" onclick="navigator.clipboard.writeText(document.getElementById('generated-prompt').textContent).then(() => {{ this.textContent = '✅ Copied!'; setTimeout(() => {{ this.textContent = '📋 Copy Prompt'; }}, 2000); }})">
                    📋 Copy Prompt
                </button>
            </div>

            <div class="prompt-card">
                <div class="prompt-label">🚀 Quick Start — Choose Your Model</div>
                <div class="model-grid">
                    <div class="model-card" onclick="alert('Copy the prompt above and paste into ChatGPT')">
                        <div class="model-icon">🧠</div>
                        <div class="model-name">ChatGPT</div>
                        <div class="model-desc">OpenAI</div>
                    </div>
                    <div class="model-card" onclick="alert('Copy the prompt above and paste into Claude')">
                        <div class="model-icon">🟣</div>
                        <div class="model-name">Claude</div>
                        <div class="model-desc">Anthropic</div>
                    </div>
                    <div class="model-card" onclick="alert('Copy the prompt above and paste into your local Ollama instance')">
                        <div class="model-icon">🦙</div>
                        <div class="model-name">Ollama</div>
                        <div class="model-desc">Local</div>
                    </div>
                    <div class="model-card" onclick="alert('Copy the prompt above and paste into Gemini')">
                        <div class="model-icon">🌈</div>
                        <div class="model-name">Gemini</div>
                        <div class="model-desc">Google</div>
                    </div>
                    <div class="model-card" onclick="alert('Copy the prompt above and paste into your Open WebUI instance')">
                        <div class="model-icon">💬</div>
                        <div class="model-name">Open WebUI</div>
                        <div class="model-desc">Self-hosted</div>
                    </div>
                    <div class="model-card" onclick="alert('Copy the prompt above and paste into any AI model')">
                        <div class="model-icon">🔮</div>
                        <div class="model-name">Any AI</div>
                        <div class="model-desc">Universal</div>
                    </div>
                </div>
            </div>
        </div>
        """
