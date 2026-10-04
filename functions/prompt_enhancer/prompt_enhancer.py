"""
title: OpenDesign Prompt Enhancer
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesign
version: 0.1.0
required_open_webui_version: 0.10.0
"""

from typing import Any


class Filter:
    """OpenDesign Prompt Enhancer — injects design context into prompts."""

    def __init__(self):
        self.type = "filter"
        self.toggle = True  # User-toggleable

    async def inlet(self, body: dict, __user__: dict | None = None) -> dict:
        """Enhance the request before it reaches the model."""
        messages = body.get("messages", [])
        last_user = None

        for msg in reversed(messages):
            if msg.get("role") == "user":
                last_user = msg.get("content", "")
                break

        if last_user and self._is_design_prompt(last_user):
            body = self._enhance_prompt(body, last_user)

        return body

    async def stream(
        self,
        chunks: list[dict],
        __user__: dict | None = None,
    ) -> list[dict]:
        """Intercept streamed chunks (for token counting)."""
        return chunks

    async def outlet(self, body: dict, __user__: dict | None = None) -> dict:
        """Post-process the response."""
        return body

    def _is_design_prompt(self, prompt: str) -> bool:
        """Check if prompt is design-related."""
        keywords = [
            "landing page", "dashboard", "website", "ui", "interface",
            "component", "button", "card", "form", "nav", "header",
            "footer", "hero", "presentation", "slide", "prototype",
            "design", "layout", "theme", "color", "font", "style",
            "make me a", "create a", "build me a", "generate a",
            "mockup", "wireframe",
        ]
        lower = prompt.lower()
        return any(kw in lower for kw in keywords)

    def _enhance_prompt(self, body: dict, prompt: str) -> dict:
        """Add design context to the prompt."""
        system_prompt = body.get("system_prompt", "")

        enhancement = """

--- Design Context ---
When generating UI code, follow these guidelines:

1. **Accessibility**: Use semantic HTML5 elements. Include ARIA labels on interactive elements. Ensure 4.5:1 minimum contrast ratio.

2. **Responsive Design**: Mobile-first approach. Use CSS Grid and Flexbox. Test at 320px, 768px, 1024px breakpoints.

3. **Performance**: Inline all CSS and JS. No external resources. Keep total size under 50KB.

4. **Design Tokens**: Use CSS custom properties for colors, spacing, and typography:
   - Colors: --color-bg, --color-text, --color-accent, --color-border
   - Typography: --font-family, --font-size-base
   - Spacing: --spacing-unit (8px base)

5. **Structure**: Include header, main, footer. Use nav for navigation. Use article/section for content blocks.

--- End Design Context ---"""

        body["system_prompt"] = system_prompt + enhancement
        return body
