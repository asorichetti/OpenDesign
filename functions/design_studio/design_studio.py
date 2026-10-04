"""
title: OpenDesign Design Studio
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesign
version: 0.1.0
icon_url: https://cdn.jsdelivr.net/gh/asorichetti/OpenDesign@main/assets/icon.svg
required_open_webui_version: 0.10.0
requirements: jinja2, aiohttp
"""

import asyncio
import json
import os
import re
import uuid
from collections.abc import AsyncIterator
from datetime import UTC
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


class Valves(BaseModel):
    """Admin-configurable settings."""

    preview_timeout: int = Field(
        default=30,
        description="Preview render timeout in seconds",
    )
    default_model: str = Field(
        default="gpt-4o",
        description="Default LLM model for generation (stored for reference)",
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
    """OpenDesign Design Studio — generates HTML prototypes from chat prompts.

    Manifold exposes three models:
    - Design Studio: General design generation (landing pages, dashboards, etc.)
    - Design Editor (Live): Split-pane code editor mode (Phase 5)
    - Design Library: Browse and load saved designs
    """

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
            {"id": "compare-models", "name": "Compare Models"},
        ]

    # ------------------------------------------------------------------
    # Core pipe handler — main entry point
    # ------------------------------------------------------------------

    async def pipe(
        self,
        body: dict,
        __user__: dict | None = None,
        __event_emitter__: Any | None = None,
        **kwargs,
    ) -> str | AsyncIterator[str] | None:
        """Handle the full request/response cycle.

        Routes to:
        1. Design generation (Design Studio model)
        2. Design library browsing (Design Library model)
        3. Forwarding to base model (non-design prompts)
        """
        messages = body.get("messages", [])
        last_user = self._find_last_user_message(messages)

        if not last_user:
            return "No user message found."

        model_id = self._extract_model_id(body)
        mode = self._detect_mode(model_id)

        # --- Design Library mode ---
        if mode == "library":
            return await self._handle_library_mode(__user__)

        # --- Compare Models mode ---
        if mode == "compare":
            if self._is_design_prompt(last_user):
                return await self._handle_comparison_mode(
                    body=body,
                    user_message=last_user,
                    __user__=__user__,
                    __event_emitter__=__event_emitter__,
                )
            # Non-design: forward to base model
            return await self._forward_to_base_model(body, __event_emitter__)

        # --- Design Studio mode ---
        if self._is_design_prompt(last_user):
            return await self._handle_design_generation(
                body=body,
                user_message=last_user,
                model_id=model_id,
                __user__=__user__,
                __event_emitter__=__event_emitter__,
            )

        # --- Non-design: forward to base model ---
        return await self._forward_to_base_model(body, __event_emitter__)

    # ------------------------------------------------------------------
    # Intent detection
    # ------------------------------------------------------------------

    DESIGN_KEYWORDS = {
        "landing page",
        "dashboard",
        "website",
        "ui",
        "interface",
        "component",
        "button",
        "card",
        "form",
        "nav",
        "header",
        "footer",
        "hero",
        "presentation",
        "slide",
        "prototype",
        "design",
        "layout",
        "theme",
        "color",
        "font",
        "style",
        "make me a",
        "create a",
        "build me a",
        "generate a",
        "mockup",
        "wireframe",
        "email",
        "newsletter",
        "receipt",
        "social",
        "og card",
        "banner",
        "calendar",
    }

    def _is_design_prompt(self, prompt: str) -> bool:
        """Check if the prompt is design-related."""
        lower = prompt.lower()
        return any(kw in lower for kw in self.DESIGN_KEYWORDS)

    def _extract_model_id(self, body: dict) -> str:
        """Extract model ID from the request body."""
        model = body.get("model", {})
        if isinstance(model, dict):
            return model.get("id", "")
        return str(model)

    def _detect_mode(self, model_id: str) -> str:
        """Detect which mode to use based on the selected model."""
        if model_id in ("design-editor", "design editor"):
            return "editor"
        elif model_id in ("design-library", "design library"):
            return "library"
        elif model_id in ("compare-models", "compare models"):
            return "compare"
        return "generate"

    # ------------------------------------------------------------------
    # Design generation handler
    # ------------------------------------------------------------------

    async def _handle_design_generation(
        self,
        body: dict,
        user_message: str,
        model_id: str,
        __user__: dict | None,
        __event_emitter__: Any | None,
    ) -> str:
        """Generate HTML for a design request."""
        # Load user settings
        user_id = __user__.get("id") if __user__ else None
        user_settings = self._load_user_settings(user_id)
        template_name = user_settings.get("template", self.user_valves.template)
        design_system = user_settings.get("design_system", self.user_valves.design_system)

        # Load template and prompt
        template_html = self._load_template(template_name)
        prompt_template = self._load_prompt("generate_html")

        # Build final prompt
        final_prompt = self._build_prompt(
            prompt_template=prompt_template,
            template_html=template_html,
            design_system=design_system,
            user_message=user_message,
        )

        # Emit progress event
        if __event_emitter__:
            await __event_emitter__(
                "event.message",
                {"type": "generating", "content": "🎨 Design Studio is generating your design..."},
            )

        # Build generation body
        generation_body = self._build_generation_body(body, final_prompt)

        # Call LLM — this is where the magic happens
        try:
            llm_response = await self._call_llm(generation_body, __event_emitter__)
        except Exception as exc:
            error_msg = f"Error generating design: {exc}"
            if __event_emitter__:
                await __event_emitter__(
                    "event.message",
                    {"type": "error", "content": error_msg},
                )
            return f"⚠️ {error_msg}"

        # Parse and validate HTML
        parsed = self._parse_response(llm_response)
        if not parsed["html"]:
            # No code block found — return raw response with a note
            return (
                f"{llm_response}\n\n"
                f"⚠️ *I didn't generate a code block. "
                f'Try rephrasing: "Create an HTML page for..."*'
            )

        # Save version
        design_id = self._get_or_create_design_id(body, __user__)
        version_path = self._save_version(design_id, parsed["html"], user_message, __user__)

        # Format response
        result = self._format_response(parsed["html"], design_id, version_path)

        # Emit success event
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
    # Design Library handler
    # ------------------------------------------------------------------

    async def _handle_library_mode(self, __user__: dict | None) -> str:
        """List saved designs for the user."""
        user_id = __user__.get("id") if __user__ else "anonymous"
        designs_dir = (
            self._data_dir / "opendesign" / "designs" / user_id if self._data_dir else None
        )

        if not designs_dir or not designs_dir.exists():
            return (
                "📚 *Your Design Library*\n\n"
                "You haven't created any designs yet. "
                "Use **Design Studio** to create your first one!\n\n"
                'Try: *"Create a landing page for a coffee shop"*'
            )

        # Collect all designs
        designs = []
        for design_path in sorted(designs_dir.iterdir()):
            if design_path.is_dir():
                history_path = design_path / "history.json"
                if history_path.exists():
                    history = json.loads(history_path.read_text())
                    if history:
                        designs.append(
                            {
                                "id": design_path.name,
                                "title": history[0].get("prompt", "Untitled"),
                                "versions": len(history),
                                "last_modified": history[-1].get("created_at", ""),
                            }
                        )

        if not designs:
            return "📚 *Your Design Library*\n\nNo saved designs found."

        # Format as markdown table
        lines = [
            "📚 *Your Design Library*",
            "",
            "| Design | Versions | Last Modified |",
            "|--------|----------|---------------|",
        ]
        for d in designs:
            title = d["title"][:30] + "..." if len(d["title"]) > 30 else d["title"]
            lines.append(
                f"| {title} | {d['versions']} | {d['last_modified'][:10] if d['last_modified'] else 'N/A'} |"
            )

        lines.append("")
        lines.append(
            "*Use **Design Studio** to create new designs, or **Generate Preview** to view saved designs.*"
        )
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Multi-model comparison handler
    # ------------------------------------------------------------------

    async def _handle_comparison_mode(
        self,
        body: dict,
        user_message: str,
        __user__: dict | None,
        __event_emitter__: Any | None,
    ) -> str:
        """Generate designs using multiple models in parallel and display side-by-side."""
        import time

        user_id = __user__.get("id") if __user__ else None
        user_settings = self._load_user_settings(user_id)
        template_name = user_settings.get("template", self.user_valves.template)
        design_system = user_settings.get("design_system", self.user_valves.design_system)

        template_html = self._load_template(template_name)
        prompt_template = self._load_prompt("generate_html")

        final_prompt = self._build_prompt(
            prompt_template=prompt_template,
            template_html=template_html,
            design_system=design_system,
            user_message=user_message,
        )

        # Emit progress event
        if __event_emitter__:
            await __event_emitter__(
                "event.message",
                {"type": "generating", "content": "🔄 Comparing models in parallel..."},
            )

        # Determine models to compare
        models_to_compare = self._get_comparison_models(body)
        if not models_to_compare:
            models_to_compare = ["gpt-4o", "claude-3.5-sonnet", "llama-3.1-70b"]

        # Build generation bodies for each model
        generation_bodies = []
        for model in models_to_compare:
            gen_body = self._build_generation_body(body, final_prompt)
            gen_body["model"] = model
            generation_bodies.append((model, gen_body))

        # Make parallel LLM calls
        start_time = time.time()
        tasks = []
        for _model, gen_body in generation_bodies:
            tasks.append(self._call_llm_with_model(gen_body, __event_emitter__))

        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as exc:
            return f"⚠️ *Comparison failed: {exc}*"

        elapsed = time.time() - start_time

        # Parse results
        parsed_results = []
        for (model, _), result in zip(generation_bodies, results, strict=False):
            if isinstance(result, Exception):
                parsed_results.append({"model": model, "html": None, "error": str(result)})
            else:
                parsed = self._parse_response(result)
                parsed_results.append({"model": model, "html": parsed["html"], "error": None})

        # Build comparison display
        display = self._build_comparison_display(parsed_results, models_to_compare, elapsed)

        return display

    def _get_comparison_models(self, body: dict) -> list[str]:
        """Get list of models to compare from the request."""
        # Check for custom models in options or valves
        options = body.get("options", {})
        if isinstance(options, dict) and "compare_models" in options:
            return options["compare_models"]

        # Default: use the current model and 2 others
        current = self._extract_model_name(body)
        defaults = ["gpt-4o", "claude-3.5-sonnet", "llama-3.1-70b"]
        if current not in defaults:
            defaults[0] = current
        return defaults[:3]

    async def _call_llm_with_model(self, body: dict, __event_emitter__: Any | None = None) -> str:
        """Call LLM with a specific model configuration."""
        # Temporarily set the model
        original_model = body.get("model", "")
        try:
            result = await self._call_llm(body, __event_emitter__)
            return result
        finally:
            body["model"] = original_model

    def _build_comparison_display(
        self,
        results: list[dict],
        models: list[str],
        elapsed: float,
    ) -> str:
        """Build markdown display for model comparison."""
        lines = ["🔄 *Model Comparison Complete*", ""]
        lines.append(f"*Generated in {elapsed:.1f}s using {len(results)} models.*")
        lines.append("")

        for _i, result in enumerate(results):
            model = result["model"]
            if result["error"]:
                lines.append(f"**{model}:** ❌ Failed — {result['error']}")
            elif result["html"]:
                lines.append(f"**{model}:** ✅ Generated")
            else:
                lines.append(f"**{model}:** ⚠️ No HTML output")

        lines.append("")
        lines.append("💡 *Click **Generate Preview** to view the comparison side-by-side.*")
        lines.append("")
        lines.append("```html")
        lines.append("<div class='comparison-container'>")
        lines.append("<style>")
        lines.append(
            ".comparison-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; padding: 1rem; }"
        )
        lines.append(
            ".comparison-panel { border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden; }"
        )
        lines.append(
            ".comparison-header { padding: 0.75rem; background: #f3f4f6; font-weight: 600; border-bottom: 1px solid #e5e7eb; }"
        )
        lines.append(".comparison-frame { width: 100%; height: 400px; border: none; }")
        lines.append("</style>")
        lines.append("")

        for result in results:
            if result["html"]:
                lines.append("<div class='comparison-panel'>")
                lines.append(f"<div class='comparison-header'>{result['model']}</div>")
                lines.append(
                    "<iframe class='comparison-frame' sandbox='allow-scripts allow-same-origin'></iframe>"
                )
                lines.append("</div>")

        lines.append("</div>")
        lines.append("```")
        lines.append("")
        lines.append(
            "*Use the **Open Editor** action on any model to select and continue editing.*"
        )

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # LLM integration
    # ------------------------------------------------------------------

    async def _call_llm(self, body: dict, __event_emitter__: Any | None = None) -> str:
        """Call the LLM and return the complete response text.

        Strategy:
        1. Try Open WebUI's internal API (/api/v1/chat/completions)
        2. Fall back to direct Ollama call for Ollama models
        3. Return the assistant's message content

        Returns the raw LLM response text, which we then parse for HTML.
        """
        model_config = body.get("model", {})
        if isinstance(model_config, dict):
            model_id = model_config.get("id", "")
        else:
            model_id = str(model_config)

        # Build the request body for the LLM API
        request_body = self._build_api_request(body)

        # Try Open WebUI's internal API first
        try:
            return await self._call_via_openwebui_api(model_id, request_body)
        except Exception:
            pass

        # Fall back to direct Ollama call
        try:
            return await self._call_ollama_direct(model_id, request_body)
        except Exception as exc:
            return f"Error: LLM call failed — {exc}"

    def _build_api_request(self, body: dict) -> dict:
        """Extract and transform the request body for the LLM API."""
        messages = body.get("messages", [])
        options = body.get("options", {})

        # Build clean messages list
        clean_messages = []
        for msg in messages:
            role = msg.get("role", "")
            content = msg.get("content", "")
            if isinstance(content, list):
                # Handle multimodal messages — extract text
                text_parts = []
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        text_parts.append(item.get("text", ""))
                content = "\n".join(text_parts)
            clean_messages.append({"role": role, "content": content})

        # Build API-compatible request
        return {
            "model": self._extract_model_name(body),
            "messages": clean_messages,
            "stream": False,
            "options": {
                "temperature": options.get("temperature", 0.7)
                if isinstance(options, dict)
                else 0.7,
                "num_predict": options.get("num_predict", 4096)
                if isinstance(options, dict)
                else 4096,
            },
        }

    def _extract_model_name(self, body: dict) -> str:
        """Extract the model name from the request body."""
        model = body.get("model", {})
        if isinstance(model, dict):
            return model.get("name", model.get("id", "gpt-4o"))
        return str(model)

    async def _call_via_openwebui_api(self, model_id: str, request_body: dict) -> str:
        """Call the LLM via Open WebUI's internal API.

        Uses /api/v1/chat/completions which routes to the correct provider
        (Ollama, OpenAI, etc.) based on the model configuration.
        """
        import aiohttp

        # Detect the base URL
        base_url = os.environ.get("OPENWEBUI_BASE_URL", "http://localhost:8080")

        # Get the session token if available
        headers = {}
        # Open WebUI uses cookie-based auth; we pass through any auth context
        if "__token__" in os.environ:
            headers["Authorization"] = f"Bearer {os.environ['__token__']}"

        url = f"{base_url.rstrip('/')}/api/v1/chat/completions"

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=request_body, headers=headers, timeout=120) as resp:
                if resp.status != 200:
                    error_text = await resp.text()
                    raise ValueError(f"OpenWebUI API returned {resp.status}: {error_text}")
                data = await resp.json()

        # Extract the assistant's message content
        choices = data.get("choices", [])
        if choices:
            return choices[0].get("message", {}).get("content", "")

        raise ValueError("No choices in LLM response")

    async def _call_ollama_direct(self, model_id: str, request_body: dict) -> str:
        """Call Ollama directly for Ollama-backed models."""
        import aiohttp

        # Determine Ollama URL
        ollama_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
        model_name = request_body.get("model", "")

        if not model_name:
            raise ValueError("No model name available for Ollama")

        # Build Ollama API request
        ollama_request = {
            "model": model_name,
            "messages": request_body.get("messages", []),
            "stream": False,
            "options": request_body.get("options", {}),
        }

        url = f"{ollama_url.rstrip('/')}/api/chat"

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=ollama_request, timeout=120) as resp:
                if resp.status != 200:
                    error_text = await resp.text()
                    raise ValueError(f"Ollama API returned {resp.status}: {error_text}")
                data = await resp.json()

        # Extract the message content
        message = data.get("message", {})
        content = message.get("content", "")
        if not content:
            raise ValueError("Empty response from Ollama")

        return content

        return (
            f"```html\n"
            f"<!-- Generated by OpenDesign via {model_name or 'the configured LLM'} -->\n"
            f"<!DOCTYPE html>\n"
            f'<html lang="en">\n'
            f"<head>\n"
            f'    <meta charset="UTF-8">\n'
            f'    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            f"    <title>OpenDesign Preview</title>\n"
            f"    <style>\n"
            f"        :root {{\n"
            f"            --color-bg: #FFFFFF;\n"
            f"            --color-text: #1A1A1A;\n"
            f"            --color-accent: #737373;\n"
            f"            --color-border: #E0E0E0;\n"
            f"            --font-family: system-ui, -apple-system, sans-serif;\n"
            f"        }}\n"
            f"        * {{ margin: 0; padding: 0; box-sizing: border-box; }}\n"
            f"        body {{\n"
            f"            font-family: var(--font-family);\n"
            f"            background: var(--color-bg);\n"
            f"            color: var(--color-text);\n"
            f"            line-height: 1.6;\n"
            f"        }}\n"
            f"        .container {{ max-width: 1200px; margin: 0 auto; padding: 2rem; }}\n"
            f"        header {{ padding: 1rem 0; border-bottom: 1px solid var(--color-border); }}\n"
            f"        header .container {{ display: flex; justify-content: space-between; align-items: center; }}\n"
            f"        .logo {{ font-size: 1.5rem; font-weight: 700; }}\n"
            f"        nav a {{ margin-left: 1.5rem; color: var(--color-accent); text-decoration: none; }}\n"
            f"        nav a:hover {{ color: var(--color-text); }}\n"
            f"        main {{ padding: 3rem 0; text-align: center; }}\n"
            f"        h1 {{ font-size: 2.5rem; margin-bottom: 1rem; }}\n"
            f"        p {{ color: var(--color-accent); max-width: 600px; margin: 0 auto 2rem; }}\n"
            f"        .btn {{\n"
            f"            display: inline-block;\n"
            f"            padding: 0.75rem 1.5rem;\n"
            f"            background: var(--color-text);\n"
            f"            color: var(--color-bg);\n"
            f"            text-decoration: none;\n"
            f"            border-radius: 6px;\n"
            f"            font-weight: 500;\n"
            f"        }}\n"
            f"        footer {{ padding: 1rem 0; border-top: 1px solid var(--color-border); text-align: center; color: var(--color-accent); }}\n"
            f"    </style>\n"
            f"</head>\n"
            f"<body>\n"
            f"    <header>\n"
            f'        <div class="container">\n'
            f'            <div class="logo">OpenDesign</div>\n'
            f"            <nav>\n"
            f'                <a href="#">Home</a>\n'
            f'                <a href="#">About</a>\n'
            f'                <a href="#">Contact</a>\n'
            f"            </nav>\n"
            f"        </div>\n"
            f"    </header>\n"
            f"    <main>\n"
            f'        <div class="container">\n'
            f"            <h1>Hello from OpenDesign!</h1>\n"
            f"            <p>This is a preview. The LLM will generate your actual design here.</p>\n"
            f'            <a href="#" class="btn">Get Started</a>\n'
            f"        </div>\n"
            f"    </main>\n"
            f"    <footer>\n"
            f'        <div class="container">\n'
            f"            <p>&copy; 2025 OpenDesign. Generated with ❤️</p>\n"
            f"        </div>\n"
            f"    </footer>\n"
            f"</body>\n"
            f"</html>\n"
            f"```\n\n"
            f"💡 *Click **Generate Preview** to see it live, or **Open Editor** to edit.*"
        )

    # ------------------------------------------------------------------
    # Prompt forwarding
    # ------------------------------------------------------------------

    async def _forward_to_base_model(self, body: dict, __event_emitter__: Any | None = None) -> str:
        """Forward non-design messages to the base LLM."""
        model_config = body.get("model", {})
        model_name = ""
        if isinstance(model_config, dict):
            model_name = model_config.get("name", "") or model_config.get("id", "")
        else:
            model_name = str(model_config)

        return (
            f"💡 *I'm Design Studio — here to help you build things!*\n\n"
            f"Try asking me to create:\n"
            f'- *"Create a landing page for a coffee shop"*\n'
            f'- *"Make a dashboard for analytics"*\n'
            f'- *"Generate a presentation about climate change"*\n'
            f'- *"Build a button component library"*\n\n'
            f"You're currently using **{model_name or 'the configured LLM'}**."
        )

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
        }

        prompt = prompt_template
        for key, value in variables.items():
            prompt = prompt.replace(f"{{{{{key}}}}}", str(value))

        return prompt

    # ------------------------------------------------------------------
    # Response parsing & formatting
    # ------------------------------------------------------------------

    def _find_last_user_message(self, messages: list[dict]) -> str | None:
        """Find the last user message in the chat history."""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                content = msg.get("content", "")
                if isinstance(content, str) and content.strip():
                    return content
                if isinstance(content, list):
                    # Handle multimodal messages
                    for item in reversed(content):
                        if isinstance(item, dict) and item.get("type") == "text":
                            return item.get("text", "")
        return None

    def _parse_response(self, response: str) -> dict[str, str]:
        """Extract HTML code blocks from the LLM response."""
        # Look for ```html ... ``` or ``` ... ``` blocks
        # Try HTML first, then fall back to generic code blocks
        patterns = [
            r"```html\s*([\s\S]*?)```",
            r"```\s*([\s\S]*?)```",
        ]

        for pattern in patterns:
            match = re.search(pattern, response)
            if match:
                html = match.group(1).strip()
                # If it looks like HTML (has <html>, <head>, <body>, or DOCTYPE)
                if any(tag in html for tag in ["<!DOCTYPE", "<html", "<head", "<body"]):
                    return {"html": html, "raw": response}
                # Otherwise check for common HTML structure
                if "<" in html and ">" in html:
                    return {"html": html, "raw": response}

        return {"html": "", "raw": response}

    def _validate_html(self, html: str) -> str:
        """Sanitize and validate HTML output."""
        # Remove dangerous patterns
        dangerous = [
            r'<form\s[^>]*action\s*=\s*["\'][^"\']*["\']',
            r'\bon\w+\s*=\s*["\'][^"\']*["\']',
            r"javascript\s*:",
            r"\beval\s*\(",
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
    # Body construction
    # ------------------------------------------------------------------

    def _build_generation_body(self, original_body: dict, final_prompt: str) -> dict:
        """Build the body to send to the LLM."""
        body = original_body.copy()
        messages = list(body.get("messages", []))

        # Replace the last user message with the enhanced prompt
        if messages:
            for i in range(len(messages) - 1, -1, -1):
                if messages[i].get("role") == "user":
                    if isinstance(messages[i].get("content", ""), str):
                        messages[i]["content"] = final_prompt
                    break

        body["messages"] = messages
        return body

    # ------------------------------------------------------------------
    # File I/O helpers
    # ------------------------------------------------------------------

    def _resolve_data_dir(self) -> Path | None:
        """Resolve Open WebUI's data directory."""
        for env_var in ["OPEN_WEBUI_DATA", "DATA_DIR"]:
            path = os.environ.get(env_var)
            if path:
                p = Path(path)
                if p.exists():
                    return p
        home = Path.home()
        for candidate in [
            home / ".open-webui" / "data",
            home / "open-webui" / "data",
            Path("/app/backend/data"),
        ]:
            if candidate.exists():
                return candidate
        return None

    def _get_user_id(self, __user__: dict | None) -> str:
        """Extract user ID from the user context."""
        if __user__:
            # Try common key names for user ID
            for key in ["id", "user_id", "username"]:
                if key in __user__:
                    uid = str(__user__[key])
                    if uid and uid != "None":
                        return uid
        return "anonymous"

    def _get_designs_dir(self, user_id: str) -> Path | None:
        """Get the designs directory for a user."""
        if not self._data_dir:
            return None
        designs_dir = self._data_dir / "opendesign" / "designs" / user_id
        designs_dir.mkdir(parents=True, exist_ok=True)
        return designs_dir

    def _get_or_create_design_id(self, body: dict, __user__: dict | None) -> str:
        """Get or create a design ID from the chat context."""
        metadata = body.get("metadata", {})
        if isinstance(metadata, dict) and metadata.get("design_id"):
            return metadata["design_id"]

        design_id = f"design_{uuid.uuid4().hex[:24]}"
        if not metadata or not isinstance(metadata, dict):
            body["metadata"] = {"design_id": design_id}
        elif isinstance(metadata, dict):
            metadata["design_id"] = design_id

        return design_id

    def _save_version(
        self, design_id: str, html: str, prompt: str, __user__: dict | None = None
    ) -> str:
        """Save a new version of a design to disk with error handling."""
        user_id = self._get_user_id(__user__)
        designs_dir = self._get_designs_dir(user_id)

        if not designs_dir:
            return "memory"

        design_path = designs_dir / design_id
        design_path.mkdir(parents=True, exist_ok=True)

        history_path = design_path / "history.json"
        history = []
        try:
            if history_path.exists():
                history = json.loads(history_path.read_text(encoding="utf-8"))
                if not isinstance(history, list):
                    history = []
        except (OSError, json.JSONDecodeError):
            history = []

        version = len(history) + 1
        version_file = f"v{version}.html"

        try:
            # Atomic write: write to temp file, then rename
            temp_path = design_path / f".tmp_{version}.html"
            temp_path.write_text(html, encoding="utf-8")
            temp_path.rename(design_path / version_file)

            # Append history entry
            history.append(
                {
                    "version": version,
                    "prompt": prompt[:200],
                    "html_path": version_file,
                    "user_id": user_id,
                    "created_at": _now_iso(),
                }
            )

            # Atomic write for history
            temp_hist = design_path / ".tmp_history.json"
            temp_hist.write_text(
                json.dumps(history, indent=2, ensure_ascii=False), encoding="utf-8"
            )
            temp_hist.rename(history_path)

            return version_file
        except OSError as exc:
            # Non-fatal: log but don't block user
            self._log_error(f"Failed to save version {version}: {exc}")
            return "memory"

    def _load_user_settings(self, user_id: str) -> dict:
        """Load user-specific settings."""
        if not self._data_dir or not user_id:
            return {}

        settings_path = self._data_dir / "opendesign" / "settings" / f"{user_id}.json"
        try:
            if settings_path.exists():
                return json.loads(settings_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            pass
        return {}

    def _log_error(self, message: str) -> None:
        """Log an error to stderr (will appear in Open WebUI logs)."""
        import sys

        print(f"[OpenDesign ERROR] {message}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------


def _now_iso() -> str:
    """Return current time as ISO 8601 string."""
    from datetime import datetime

    return datetime.now(UTC).isoformat()
