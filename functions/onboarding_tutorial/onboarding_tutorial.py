"""
title: OpenDesigner Onboarding Tutorial
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesigner
version: 0.1.0
required_open_webui_version: 0.10.0
"""

from typing import Any


class Filter:
    """OpenDesigner Onboarding — provides interactive tutorials for new users."""

    def __init__(self):
        self.type = "filter"
        self.tutorials = self._load_tutorials()

    def _load_tutorials(self) -> dict:
        """Load tutorial content."""
        return {
            "first_time": {
                "title": "Welcome to OpenDesigner! 🎨",
                "steps": [
                    {
                        "title": "What is OpenDesigner?",
                        "content": "OpenDesigner is an AI-powered design generation tool that lives inside Open WebUI. It transforms your ideas into beautiful, functional HTML prototypes — landing pages, dashboards, components, and more!",
                    },
                    {
                        "title": "How to Generate a Design",
                        "content": "1. Click the **Design Studio** dropdown\n2. Type a prompt like: 'Create a landing page for a coffee shop'\n3. Wait for the AI to generate the design\n4. Click **Generate Preview** to see it in action!",
                    },
                    {
                        "title": "Try These Prompts",
                        "content": "• 'Create a dashboard for analytics'\n• 'Build a pricing page with 3 tiers'\n• 'Make a responsive navigation bar'\n• 'Design an email newsletter template'",
                    },
                    {
                        "title": "Explore Features",
                        "content": "After generating a design, you'll see action buttons:\n• **Generate Preview** — See your design live\n• **Open Editor** — Edit the code directly\n• **Export HTML/PNG/PDF** — Download your work\n• **AI Prompt Generator** — Create prompts for other AI models",
                    },
                    {
                        "title": "You're All Set! 🎉",
                        "content": "Start creating amazing designs! Remember, you can always come back to this tutorial from the help menu.",
                    },
                ],
            },
            "advanced": {
                "title": "Advanced Features Guide ⚡",
                "steps": [
                    {
                        "title": "Multi-Model Comparison",
                        "content": "Select **Compare Models** from the dropdown to generate designs with multiple AI models side-by-side. Perfect for choosing the best output!",
                    },
                    {
                        "title": "Component Props System",
                        "content": "Configure templates with parameters — colors, text, layouts — without touching code. Click on any component to customize it.",
                    },
                    {
                        "title": "Template Marketplace",
                        "content": "Browse, import, and share community templates. Submit your own creations to help other designers!",
                    },
                    {
                        "title": "AI Prompt Generator",
                        "content": "After generating a design, click **AI Prompt Generator** to create detailed prompts for recreating your design in ChatGPT, Claude, Ollama, or any AI model.",
                    },
                    {
                        "title": "Presenter Mode",
                        "content": "For presentation templates, use keyboard shortcuts:\n• **← →** — Navigate slides\n• **P** — Presenter mode\n• **F** — Fullscreen\n• **Ctrl+P** — Export as PDF",
                    },
                ],
            },
            "troubleshooting": {
                "title": "Troubleshooting Guide 🔧",
                "steps": [
                    {
                        "title": "Design Not Generating?",
                        "content": "1. Check your AI model connection\n2. Try a simpler prompt\n3. Restart Open WebUI\n4. Check browser console for errors",
                    },
                    {
                        "title": "Preview Not Showing?",
                        "content": "1. Click 'Generate Preview' again\n2. Refresh the page\n3. Check that the code block contains HTML\n4. Try a different template",
                    },
                    {
                        "title": "Export Issues?",
                        "content": "1. Make sure the design generated successfully\n2. Try exporting as HTML first\n3. Use browser's native 'Save Page As' as backup\n4. Check file permissions",
                    },
                    {
                        "title": "Need More Help?",
                        "content": "• Check the documentation: /docs\n• Report issues: GitHub Issues\n• Join the community: Discord/Forum\n• Email support: support@opendesigner.dev",
                    },
                ],
            },
        }

    async def process(
        self,
        body: dict,
        __user__: dict | None = None,
        __event_emitter__: Any | None = None,
        **kwargs,
    ) -> dict:
        """Process messages and inject tutorial if needed."""
        messages = body.get("messages", [])
        last_user = messages[-1]["content"] if messages else ""

        # Check if this is a help/tutorial request
        if any(
            phrase in last_user.lower()
            for phrase in ["help", "tutorial", "how to", "beginner", "welcome"]
        ):
            return await self._provide_help(last_user, __event_emitter__)

        return body

    async def _provide_help(self, prompt: str, __event_emitter__: Any | None = None) -> dict:
        """Provide help/tutorial based on user request."""
        help_responses = {
            "first time": self.tutorials["first_time"],
            "beginner": self.tutorials["first_time"],
            "new user": self.tutorials["first_time"],
            "advanced": self.tutorials["advanced"],
            "tips": self.tutorials["advanced"],
            "troubleshoot": self.tutorials["troubleshooting"],
            "fix": self.tutorials["troubleshooting"],
            "error": self.tutorials["troubleshooting"],
        }

        tutorial = None
        for key, content in help_responses.items():
            if key in prompt:
                tutorial = content
                break

        if not tutorial:
            tutorial = self.tutorials["first_time"]

        if __event_emitter__:
            await __event_emitter__(
                "event.message",
                {
                    "type": "generating",
                    "content": f"📚 Showing tutorial: {tutorial['title']}",
                },
            )

        tutorial_html = self._render_tutorial(tutorial)

        if __event_emitter__:
            await __event_emitter__(
                "event.message",
                {"type": "generating", "content": "✅ Tutorial loaded!"},
            )

        return tutorial_html

    def _render_tutorial(self, tutorial: dict) -> str:
        """Render tutorial as HTML."""
        steps_html = ""
        for i, step in enumerate(tutorial["steps"], 1):
            steps_html += f"""
            <div class="tutorial-step" style="margin-bottom: 1.5rem; padding: 1rem; background: #f8fafc; border-radius: 8px; border-left: 3px solid #6366f1;">
                <h4 style="margin: 0 0 0.5rem; color: #1e293b;">
                    <span style="background: #6366f1; color: white; width: 24px; height: 24px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 0.75rem; margin-right: 0.5rem;">{i}</span>
                    {step["title"]}
                </h4>
                <p style="margin: 0; color: #64748b; line-height: 1.6;">{step["content"]}</p>
            </div>
            """

        return f"""
        <div class="tutorial-container" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .tutorial-container {{
                    max-width: 800px;
                    margin: 0 auto;
                }}
                .tutorial-header {{
                    text-align: center;
                    margin-bottom: 2rem;
                    padding: 2rem;
                    background: linear-gradient(135deg, #6366f1, #8b5cf6);
                    border-radius: 12px;
                    color: white;
                }}
                .tutorial-header h2 {{
                    margin: 0 0 0.5rem;
                    font-size: 1.75rem;
                }}
                .tutorial-header p {{
                    margin: 0;
                    opacity: 0.9;
                }}
                .tutorial-footer {{
                    text-align: center;
                    margin-top: 2rem;
                    padding: 1rem;
                    background: #f0fdf4;
                    border-radius: 8px;
                    color: #16a34a;
                    font-weight: 600;
                }}
            </style>

            <div class="tutorial-header">
                <h2>{tutorial["title"]}</h2>
                <p>{len(tutorial["steps"])} steps to get started</p>
            </div>

            {steps_html}

            <div class="tutorial-footer">
                🎉 Ready to start creating amazing designs!
            </div>
        </div>
        """
