"""
title: OpenDesign Design Studio
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesign
version: 0.1.0
icon_url: https://cdn.jsdelivr.net/gh/asorichetti/OpenDesign@main/assets/icon.svg
required_open_webui_version: 0.10.0
requirements: jinja2, beautifulsoup4
"""

import json
import os
import re
import uuid
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

class Valves(BaseModel):
    """Admin-configurable settings."""

    base_model: str = Field(
        default="gpt-4o",
        description="Base LLM model to use for generation",
    )
    api_key: Optional[str] = Field(
        default=None,
        description="API key for the base model (if not using Ollama)",
    )
    preview_timeout: int = Field(
        default=10,
        description="Preview render timeout in seconds",
    )


class UserValves(BaseModel):
    """User-configurable settings."""

    template: str = Field(
        default="landing/minimal",
        description="Default template to use for generation",
    )
    design_system: str = Field(
        default="light",
        description="Design system preset (light/dark)",
    )
    auto_preview: bool = Field(
        default=True,
        description="Automatically generate preview when a design is created",
    )


# ---------------------------------------------------------------------------
# Pipe Class
# ---------------------------------------------------------------------------


class Pipe:
    """OpenDesign Design Studio — generates HTML prototypes from chat prompts."""

    def __init__(self):
        self.type = "pipe"
        self.name = "Design Studio"
        self.valves = Valves()
        self.user_valves = UserValves()
        self._templates_cache: dict[str, str] = {}
        self._prompts_cache: dict[str, str] = {}
        self._data_dir = self._resolve_data_dir()

    # ------------------------------------------------------------------
    # Manifold — exposes multiple models
    # ------------------------------------------------------------------

    def pipes(self) -> list[dict[str, str]]:
        """Return the manifold of available models."""
        return [
            {"id": "design-studio", "name": "Design Studio"},
            {"id": "design-editor", "name": "Design Editor (Live)"},
            {"id": "design-library", "name": "Design Library"},
        ]

    # ------------------------------------------------------------------
    # Core pipe handler
    # ------------------------------------------------------------------

    async def pipe(
        self,
        body: dict,
        __user__: dict | None = None,
        __event_emitter__: Any | None = None,
        **kwargs,
    ) -> str:
        """Handle the full request/response cycle.

        If the user's message is not design-related, forward to the base
        model.  If it is design-related, generate an HTML prototype.
        """

        # Detect design intent from the last user message
        messages = body.get("messages", [])
        last_user = None
        for msg in reversed(messages):
            if msg.get("role") == "user":
                last_user = msg.get("content", "")
                break

        if not last_user:
            return await self._forward_to_base_model(body, __user__, __event_emitter__, **kwargs)

        if not self._is_design_prompt(last_user):
            return await self._forward_to_base_model(body, __user__, __event_emitter__, **kwargs)

        # --- Design generation path ---
        model_id = body.get("model", {}).get("id", "")
        mode = self._detect_mode(model_id)

        # Load user settings
        user_settings = self._load_user_settings(__user__["id"] if __user__ else None)
        template_name = user_settings.get("template", self.user_valves.template)
        design_system = user_settings.get("design_system", self.user_valves.design_system)

        # Load template and prompt
        template_html = self._load_template(template_name)
        prompt_template = self._load_prompt(mode)

        # Build final prompt
        final_prompt = self._build_prompt(
            prompt_template=prompt_template,
            template_html=template_html,
            design_system=design_system,
            user_message=last_user,
            mode=mode,
        )

        # Call LLM
        generation_body = self._build_generation_body(body, final_prompt)

        try:
            response = await self._call_llm(generation_body, __event_emitter__, __user__)
        except Exception as exc:
            return f"Error generating design: {exc}"

        # Parse and validate HTML
        parsed = self._parse_response(response)
        if not parsed["html"]:
            return response  # No code block found, return raw response

        # Save version
        design_id = self._get_or_create_design_id(body, __user__)
        version_path = self._save_version(design_id, parsed["html"], last_user)

        # Format response
        result = self._format_response(parsed["html"], design_id, version_path)

        # Emit event if auto_preview is enabled
        if user_settings.get("auto_preview", True) and __event_emitter__:
            await __event_emitter__(
                "event.message",
                {
                    "type": "design_generated",
                    "design_id": design_id,
                    "version": version_path,
                },
            )

        return result

    # ------------------------------------------------------------------
    # Intent detection
    # ------------------------------------------------------------------

    def _is_design_prompt(self, prompt: str) -> bool:
        """Check if the prompt is design-related."""
        keywords = [
            "landing page", "dashboard", "website", "ui", "interface",
            "component", "button", "card", "form", "nav", "header",
            "footer", "hero", "presentation", "slide", "prototype",
            "design", "layout", "theme", "color", "font", "style",
            "make me a", "create a", "build me a", "generate a",
            "mockup", "wireframe", "prototype",
        ]
        lower = prompt.lower()
        return any(kw in lower for kw in keywords)

    def _detect_mode(self, model_id: str) -> str:
        """Detect which mode to use based on the selected model."""
        if "presentation" in model_id:
            return "present"
        elif "component" in model_id:
            return "component"
        return "generate_html"

    # ------------------------------------------------------------------
    # Template & prompt loading
    # ------------------------------------------------------------------

    def _load_template(self, template_name: str) -> str:
        """Load a template HTML file from disk (cached)."""
        if template_name in self._templates_cache:
            return self._templates_cache[template_name]

        base = Path(__file__).parent / "templates"
        template_path = base / f"{template_name}.html"

        if not template_path.exists():
            # Fallback to minimal
            template_path = base / "landing/minimal.html"

        html = template_path.read_text(encoding="utf-8")
        self._templates_cache[template_name] = html
        return html

    def _load_prompt(self, mode: str) -> str:
        """Load a prompt template from disk (cached)."""
        if mode in self._prompts_cache:
            return self._prompts_cache[mode]

        base = Path(__file__).parent / "prompts"
        prompt_path = base / f"{mode}.md"

        if not prompt_path.exists():
            prompt_path = base / "generate_html.md"

        prompt = prompt_path.read_text(encoding="utf-8")
        self._prompts_cache[mode] = prompt
        return prompt

    # ------------------------------------------------------------------
    # Prompt construction
    # ------------------------------------------------------------------

    def _build_prompt(
        self,
        prompt_template: str,
        template_html: str,
        design_system: str,
        user_message: str,
        mode: str,
    ) -> str:
        """Build the final prompt for the LLM using Jinja2-style substitution."""

        # Load design system CSS
        assets_dir = Path(__file__).parent / "assets"
        css_path = assets_dir / f"{design_system}.css"
        design_css = css_path.read_text(encoding="utf-8") if css_path.exists() else ""

        # Simple template substitution (Jinja2-style {{ variable }})
        variables = {
            "design_system": design_system,
            "design_css": design_css,
            "template_html": template_html,
            "user_message": user_message,
            "mode": mode,
        }

        prompt = prompt_template
        for key, value in variables.items():
            prompt = prompt.replace(f"{{{{{key}}}}}", str(value))

        return prompt

    # ------------------------------------------------------------------
    # LLM call
    # ------------------------------------------------------------------

    async def _call_llm(
        self,
        body: dict,
        __event_emitter__: Any | None,
        __user__: dict | None,
    ) -> str:
        """Call the underlying LLM via Open WebUI's mechanism."""

        # We use the events to stream the response back
        if __event_emitter__:
            await __event_emitter__(
                "event.message",
                {"type": "generating", "content": "Generating design..."},
            )

        # For now, we forward to the base model and capture the response.
        # In a real implementation, this would use Open WebUI's internal
        # API to call the model directly.
        #
        # The Pipe receives the full `body` dict which includes the model
        # configuration. We modify it and let Open WebUI handle the rest.
        #
        # IMPORTANT: In the final implementation, use Open WebUI's internal
        # model calling mechanism. For now, this is a placeholder.
        #
        # The correct approach is:
        #   1. Use __metadata__ to get the model
        #   2. Call the model's stream() method directly
        #   3. Collect the streamed chunks
        #   4. Return the combined response

        # Placeholder: in a real implementation this would call the LLM
        # and return the generated HTML. For development, we return a
        # placeholder that the user can test the preview with.
        return self._placeholder_html()

    def _placeholder_html(self) -> str:
        """Return a minimal HTML placeholder for testing the preview."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenDesign Preview</title>
    <style>
        :root {
            --color-bg: #FFFFFF;
            --color-text: #1A1A1A;
            --color-accent: #737373;
            --color-border: #E0E0E0;
            --font-family: system-ui, -apple-system, sans-serif;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: var(--font-family);
            background: var(--color-bg);
            color: var(--color-text);
            line-height: 1.6;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
        header {
            padding: 1rem 0;
            border-bottom: 1px solid var(--color-border);
        }
        header .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo { font-size: 1.5rem; font-weight: 700; }
        nav a { margin-left: 1.5rem; color: var(--color-accent); text-decoration: none; }
        nav a:hover { color: var(--color-text); }
        main { padding: 3rem 0; text-align: center; }
        h1 { font-size: 2.5rem; margin-bottom: 1rem; }
        p { color: var(--color-accent); max-width: 600px; margin: 0 auto 2rem; }
        .btn {
            display: inline-block;
            padding: 0.75rem 1.5rem;
            background: var(--color-text);
            color: var(--color-bg);
            text-decoration: none;
            border-radius: 6px;
            font-weight: 500;
        }
        .placeholder {
            margin-top: 2rem;
            padding: 2rem;
            border: 2px dashed var(--color-border);
            border-radius: 8px;
            color: var(--color-accent);
        }
        footer {
            padding: 1rem 0;
            border-top: 1px solid var(--color-border);
            text-align: center;
            color: var(--color-accent);
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div class="logo">OpenDesign</div>
            <nav>
                <a href="#">Home</a>
                <a href="#">About</a>
                <a href="#">Contact</a>
            </nav>
        </div>
    </header>
    <main>
        <div class="container">
            <h1>{{ user_message }}</h1>
            <p>This is a generated design. The full HTML will be returned by the LLM.</p>
            <a href="#" class="btn">Get Started</a>
            <div class="placeholder">
                <p>🎨 Design generated by OpenDesign</p>
                <p>Click "Generate Preview" to see the result</p>
            </div>
        </div>
    </main>
    <footer>
        <div class="container">
            <p>&copy; 2025 OpenDesign. Generated with ❤️</p>
        </div>
    </footer>
</body>
</html>"""

    def _build_generation_body(self, original_body: dict, final_prompt: str) -> dict:
        """Build the body to send to the LLM."""
        body = original_body.copy()
        messages = list(body.get("messages", []))

        # Replace the last user message with the enhanced prompt
        if messages:
            for i in range(len(messages) - 1, -1, -1):
                if messages[i].get("role") == "user":
                    messages[i]["content"] = final_prompt
                    break

        body["messages"] = messages
        return body

    async def _forward_to_base_model(
        self,
        body: dict,
        __user__: dict | None,
        __event_emitter__: Any | None,
        **kwargs,
    ) -> str:
        """Forward non-design messages to the configured base model."""
        # In a real implementation, this would call the base model.
        # For now, return a message indicating this is the design pipe.
        return "This is the OpenDesign Design Agent. Describe what you'd like to build and I'll generate the code for you."

    # ------------------------------------------------------------------
    # Response parsing & formatting
    # ------------------------------------------------------------------

    def _parse_response(self, response: str) -> dict[str, str]:
        """Extract HTML code blocks from the LLM response."""
        # Look for ```html ... ``` blocks
        pattern = r"```html\s*([\s\S]*?)```"
        match = re.search(pattern, response)

        if match:
            return {"html": match.group(1).strip(), "raw": response}
        return {"html": "", "raw": response}

    def _validate_html(self, html: str) -> str:
        """Sanitize and validate HTML output."""
        # Remove dangerous patterns
        dangerous = [
            r'<form\s[^>]*action\s*=',
            r'[\s\S]*\bon\w+\s*=\s*["\'][^"\']*["\'][\s\S]*',
            r'javascript\s*:',
            r'\beval\s*\(',
        ]
        for pattern in dangerous:
            html = re.sub(pattern, "", html, flags=re.IGNORECASE)

        return html

    def _format_response(self, html: str, design_id: str, version_path: str) -> str:
        """Format the response for display in Open WebUI."""
        safe_html = self._validate_html(html)
        return (
            f"```\n<!-- Generated by OpenDesign | Design: {design_id} | Version: {version_path} -->\n"
            f"{safe_html}\n```\n\n"
            f"💡 *Click **Generate Preview** to see it live, or **Open Editor** to edit.*"
        )

    # ------------------------------------------------------------------
    # File I/O helpers
    # ------------------------------------------------------------------

    def _resolve_data_dir(self) -> Path | None:
        """Resolve Open WebUI's data directory."""
        # Check common locations
        for env_var in ["OPEN_WEBUI_DATA", "DATA_DIR"]:
            path = os.environ.get(env_var)
            if path:
                return Path(path)
        # Try the default Open WebUI data directory
        home = Path.home()
        for candidate in [
            home / ".open-webui" / "data",
            home / "open-webui" / "data",
            Path("/app/backend/data"),
        ]:
            if candidate.exists():
                return candidate
        return None

    def _get_designs_dir(self, user_id: str) -> Path | None:
        """Get the designs directory for a user."""
        if not self._data_dir:
            return None
        designs_dir = self._data_dir / "opendesign" / "designs" / user_id
        designs_dir.mkdir(parents=True, exist_ok=True)
        return designs_dir

    def _get_or_create_design_id(self, body: dict, __user__: dict | None) -> str:
        """Get or create a design ID from the chat context."""
        # Try to extract from existing messages or metadata
        metadata = body.get("metadata", {})
        if metadata.get("design_id"):
            return metadata["design_id"]

        # Create new design ID
        design_id = f"design_{uuid.uuid4().hex[:24]}"

        # Store in the next message's metadata if possible
        if not metadata:
            body["metadata"] = {"design_id": design_id}

        return design_id

    def _save_version(self, design_id: str, html: str, prompt: str) -> str:
        """Save a new version of a design to disk."""
        user_id = "anonymous"  # In practice, get from __user__
        designs_dir = self._get_designs_dir(user_id)

        if not designs_dir:
            return "memory"  # No disk, return placeholder

        design_path = designs_dir / design_id
        design_path.mkdir(parents=True, exist_ok=True)

        # Determine version number
        history_path = design_path / "history.json"
        history = []
        if history_path.exists():
            history = json.loads(history_path.read_text())

        version = len(history) + 1
        version_file = f"v{version}.html"

        # Save HTML
        (design_path / version_file).write_text(html, encoding="utf-8")

        # Save history entry
        history.append({
            "version": version,
            "prompt": prompt[:200],  # Truncate long prompts
            "html_path": version_file,
            "created_at": _now_iso(),
        })
        history_path.write_text(json.dumps(history, indent=2))

        return version_file

    def _load_user_settings(self, user_id: str) -> dict:
        """Load user-specific settings."""
        if not self._data_dir or not user_id:
            return {}

        settings_path = self._data_dir / "opendesign" / "settings" / f"{user_id}.json"
        if settings_path.exists():
            return json.loads(settings_path.read_text())
        return {}


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def _now_iso() -> str:
    """Return current time as ISO 8601 string."""
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()
