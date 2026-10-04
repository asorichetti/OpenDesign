"""
title: OpenDesign Prompt Enhancer
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesign
version: 0.1.0
required_open_webui_version: 0.10.0
"""



class Filter:
    """OpenDesign Prompt Enhancer — injects design context into prompts.

    This filter runs in the inlet phase, adding design-specific guidance
    to prompts that are design-related. It also enhances outlet responses
    to include design metadata.
    """

    def __init__(self):
        self.type = "filter"
        self.toggle = True  # User-toggleable

    # Design keywords shared with the Pipe for consistency
    DESIGN_KEYWORDS = {
        "landing page", "dashboard", "website", "ui", "interface",
        "component", "button", "card", "form", "nav", "header",
        "footer", "hero", "presentation", "slide", "prototype",
        "design", "layout", "theme", "color", "font", "style",
        "make me a", "create a", "build me a", "generate a",
        "mockup", "wireframe", "email", "newsletter", "social",
    }

    async def inlet(self, body: dict, __user__: dict | None = None) -> dict:
        """Enhance the request before it reaches the model."""
        messages = body.get("messages", [])
        last_user = self._find_last_user_message(messages)

        if last_user and self._is_design_prompt(last_user):
            body = self._enhance_prompt(body, last_user)

        return body

    async def stream(
        self,
        chunks: list[dict],
        __user__: dict | None = None,
    ) -> list[dict]:
        """Intercept streamed chunks (for token counting and metadata)."""
        return chunks

    async def outlet(self, body: dict, __user__: dict | None = None) -> dict:
        """Post-process the response to add design metadata."""
        messages = body.get("messages", [])
        last_ai = None

        for msg in reversed(messages):
            if msg.get("role") == "assistant":
                last_ai = msg.get("content", "")
                break

        if last_ai and self._has_code_block(last_ai):
            # Add design metadata to assistant message
            metadata = {
                "source": "opendesign",
                "type": "design_generation",
            }

            # Store metadata in the response
            if "metadata" not in body:
                body["metadata"] = {}
            body["metadata"]["opendesign"] = metadata

        return body

    def _find_last_user_message(self, messages: list[dict]) -> str | None:
        """Find the last user message in the chat history."""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                content = msg.get("content", "")
                if isinstance(content, str) and content.strip():
                    return content
                if isinstance(content, list):
                    for item in reversed(content):
                        if isinstance(item, dict) and item.get("type") == "text":
                            return item.get("text", "")
        return None

    def _is_design_prompt(self, prompt: str) -> bool:
        """Check if prompt is design-related."""
        lower = prompt.lower()
        return any(kw in lower for kw in self.DESIGN_KEYWORDS)

    def _has_code_block(self, content: str) -> bool:
        """Check if content contains an HTML code block."""
        return "```html" in content or ("```" in content and "<html" in content)

    def _enhance_prompt(self, body: dict, prompt: str) -> dict:
        """Add design context to the prompt."""
        system_prompt = body.get("system_prompt", "")

        enhancement = """

--- Design Studio Guidelines ---
When generating UI/UX code, follow these principles:

**1. Accessibility First**
- Use semantic HTML5 elements: header, nav, main, section, article, footer
- Include ARIA labels on interactive elements (buttons, forms, links)
- Ensure minimum 4.5:1 contrast ratio for text
- Support keyboard navigation (Tab, Enter, Escape)

**2. Responsive Design**
- Mobile-first approach with progressive enhancement
- Use CSS Grid and Flexbox for layouts
- Test breakpoints: 320px (mobile), 768px (tablet), 1024px (desktop)
- Use relative units (rem, em, %) instead of fixed pixels

**3. Performance**
- Inline all CSS and JavaScript (no external resources)
- Keep total HTML size under 2MB for preview compatibility
- Use efficient CSS selectors (avoid deep nesting)
- Minimize DOM depth and complexity

**4. Design Tokens**
Use CSS custom properties for consistent theming:
- Colors: --color-bg, --color-text, --color-accent, --color-border
- Typography: --font-family, --font-size-base, --line-height
- Spacing: --spacing-unit (8px base), --spacing-md, --spacing-lg
- Radius: --radius-sm (4px), --radius-md (8px), --radius-lg (12px)

**5. Structure**
- Always include a proper HTML5 doctype and meta viewport
- Use nav for navigation, main for primary content
- Include header and footer sections
- Use article/section for content blocks

**6. Self-Contained Output**
- Return ONLY the complete HTML document
- No external CSS/JS files — everything inline
- No external fonts — use system fonts or embedded @font-face
- No image URLs — use CSS gradients, SVGs, or emoji
- Return code in a markdown code block: ```html

--- End Design Studio Guidelines ---"""

        body["system_prompt"] = system_prompt + enhancement
        return body
