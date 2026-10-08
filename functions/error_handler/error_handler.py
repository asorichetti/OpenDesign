"""
title: OpenDesigner Error Handler
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesigner
version: 0.1.0
required_open_webui_version: 0.10.0
"""

from typing import Any


class Action:
    """OpenDesigner Error Handler — provides graceful error recovery and suggestions."""

    def __init__(self):
        self.type = "filter"
        self.error_patterns = self._load_error_patterns()

    def _load_error_patterns(self) -> dict:
        """Load error pattern mappings."""
        return {
            "llm_timeout": {
                "pattern": "timeout|timed out|deadline exceeded",
                "title": "⏰ Generation Timed Out",
                "message": "The AI model took too long to respond. This can happen with complex designs or slow models.",
                "suggestions": [
                    "Try a simpler prompt (e.g., 'Create a button' instead of 'Create a full dashboard')",
                    "Switch to a faster AI model",
                    "Try again in a moment",
                ],
            },
            "llm_error": {
                "pattern": "error|failed|exception|traceback",
                "title": "❌ Generation Failed",
                "message": "The AI model encountered an error while generating your design.",
                "suggestions": [
                    "Check your AI model is running and accessible",
                    "Try rephrasing your prompt",
                    "Restart Open WebUI if the issue persists",
                ],
            },
            "no_html": {
                "pattern": "no code block|didn't generate|no html",
                "title": "⚠️ No HTML Generated",
                "message": "The AI didn't produce a code block. This usually means the prompt needs to be more specific.",
                "suggestions": [
                    'Try: "Create an HTML page that shows..."',
                    'Try: "Generate a landing page with..."',
                    "Make sure to ask for HTML/code output",
                ],
            },
            "template_error": {
                "pattern": "template not found|invalid template",
                "title": "📄 Template Error",
                "message": "The selected template couldn't be loaded.",
                "suggestions": [
                    "Try a different template from the dropdown",
                    "Check that templates are installed correctly",
                    "Restart Open WebUI",
                ],
            },
            "general": {
                "pattern": ".*",
                "title": "⚠️ Something Went Wrong",
                "message": "An unexpected error occurred.",
                "suggestions": [
                    "Check the browser console for detailed errors",
                    "Try refreshing the page",
                    "Report this issue on GitHub",
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
        """Process response and inject error handling if needed."""
        response = body.get("response", "")

        if not response:
            return body

        # Check for error patterns
        import re

        for _pattern_name, error_info in self.error_patterns.items():
            if re.search(error_info["pattern"], response, re.IGNORECASE):
                return await self._handle_error(error_info, __event_emitter__, response)

        return body

    async def _handle_error(
        self, error_info: dict, __event_emitter__: Any | None = None, original: str = ""
    ) -> dict:
        """Handle error with suggestions."""
        error_html = self._render_error(error_info)

        if __event_emitter__:
            await __event_emitter__(
                "event.message", {"type": "error", "content": error_info["title"]}
            )

        return error_html

    def _render_error(self, error_info: dict) -> str:
        """Render error message with suggestions."""
        suggestions_html = "".join(
            f'<li style="margin-bottom: 0.5rem;">{suggestion}</li>'
            for suggestion in error_info["suggestions"]
        )

        return f"""
        <div class="error-container" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .error-container {{
                    max-width: 800px;
                    margin: 0 auto;
                }}
                .error-card {{
                    background: #fef2f2;
                    border: 1px solid #fecaca;
                    border-radius: 12px;
                    padding: 1.5rem;
                }}
                .error-title {{
                    font-size: 1.25rem;
                    font-weight: 600;
                    color: #991b1b;
                    margin: 0 0 0.75rem;
                }}
                .error-message {{
                    color: #7f1d1d;
                    margin: 0 0 1rem;
                    line-height: 1.6;
                }}
                .error-suggestions {{
                    background: white;
                    border-radius: 8px;
                    padding: 1rem;
                }}
                .error-suggestions h4 {{
                    margin: 0 0 0.75rem;
                    color: #991b1b;
                    font-size: 0.875rem;
                }}
                .error-suggestions ul {{
                    margin: 0;
                    padding-left: 1.5rem;
                    color: #7f1d1d;
                }}
                .retry-btn {{
                    display: inline-flex;
                    align-items: center;
                    gap: 0.5rem;
                    padding: 0.75rem 1.5rem;
                    background: #dc2626;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 0.875rem;
                    font-weight: 600;
                    cursor: pointer;
                    margin-top: 1rem;
                    transition: all 0.2s;
                }}
                .retry-btn:hover {{
                    background: #b91c1c;
                    transform: translateY(-1px);
                }}
            </style>

            <div class="error-card">
                <h3 class="error-title">{error_info["title"]}</h3>
                <p class="error-message">{error_info["message"]}</p>

                <div class="error-suggestions">
                    <h4>💡 Suggestions:</h4>
                    <ul>{suggestions_html}</ul>
                </div>

                <button class="retry-btn" onclick="location.reload()">
                    🔄 Retry Generation
                </button>
            </div>
        </div>
        """
