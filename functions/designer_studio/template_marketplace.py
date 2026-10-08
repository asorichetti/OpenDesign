"""
title: OpenDesigner Template Marketplace
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesigner
version: 0.1.0
required_open_webui_version: 0.10.0
"""

import hashlib
import json
import re
from datetime import UTC
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Template Validation
# ---------------------------------------------------------------------------

DANGEROUS_PATTERNS = [
    r"\bimport\s+",
    r"\bfrom\s+import\s+",
    r"\beval\s*\(",
    r"\bexec\s*\(",
    r"\bcompile\s*\(",
    r"__import__",
    r"os\.system",
    r"subprocess\.",
    r"socket\.",
    r"http://(?!localhost|127\.0\.0\.1)[^\s'\"]+",
    r"javascript\s*:",
    r"\bon\w+\s*=\s*['\"]",
]


class Action:
    """Validate user-submitted templates for security."""

    @staticmethod
    def validate_template(html_content: str) -> tuple[bool, list[str]]:
        """Validate template HTML for dangerous patterns.

        Returns:
            (is_valid, list_of_errors)
        """
        errors = []

        if not html_content or not html_content.strip():
            return False, ["Template content is empty"]

        # Check for dangerous patterns
        for pattern in DANGEROUS_PATTERNS:
            if re.search(pattern, html_content, re.IGNORECASE):
                errors.append(f"Contains dangerous pattern: {pattern}")

        # Check for external script/style sources
        if re.search(r'<script\s+src\s*=\s*["\']https?://', html_content):
            errors.append("Contains external script source")
        if re.search(r'<link\s+rel=["\']stylesheet["\']\s+href\s*=\s*["\']https?://', html_content):
            errors.append("Contains external stylesheet source")

        # Check for form actions to external URLs
        if re.search(
            r'<form\s+[^>]*action\s*=\s*["\']https?://(?!localhost|127\.0\.0\.1)', html_content
        ):
            errors.append("Form submits to external URL")

        # Check for iframes to external URLs
        if re.search(
            r'<iframe[^>]*src\s*=\s*["\']https?://(?!localhost|127\.0\.0\.1)', html_content
        ):
            errors.append("Iframe loads from external URL")

        return (len(errors) == 0, errors)


# ---------------------------------------------------------------------------
# Template Store
# ---------------------------------------------------------------------------


class TemplateStore:
    """Manage user templates with versioning."""

    def __init__(self, data_dir: Path | None = None):
        self._data_dir = data_dir
        self._templates_dir = (
            data_dir / "opendesigner" / "community_templates" if data_dir else None
        )

    def get_user_templates(self, user_id: str) -> list[dict]:
        """Get all templates for a user."""
        if not self._templates_dir:
            return []

        user_dir = self._templates_dir / user_id
        if not user_dir.exists():
            return []

        templates = []
        for template_dir in sorted(user_dir.iterdir()):
            if template_dir.is_dir():
                manifest = template_dir / "manifest.json"
                if manifest.exists():
                    templates.append(json.loads(manifest.read_text()))

        return templates

    def save_template(
        self,
        user_id: str,
        title: str,
        description: str,
        html: str,
        template_type: str = "custom",
        version: str = "1.0.0",
        author: str = "",
    ) -> dict | None:
        """Save a user template with versioning."""
        if not self._templates_dir:
            return None

        # Create user directory
        user_dir = self._templates_dir / user_id
        user_dir.mkdir(parents=True, exist_ok=True)

        # Generate slug from title
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        template_dir = user_dir / slug

        # Check if template exists, increment version if so
        if template_dir.exists():
            existing = self._get_template_metadata(slug, user_id)
            if existing:
                version = self._increment_version(existing.get("version", "1.0.0"))

        # Generate content hash
        content_hash = hashlib.sha256(html.encode()).hexdigest()[:16]

        # Create template directory
        template_dir.mkdir(parents=True, exist_ok=True)

        # Save HTML
        html_path = template_dir / f"v{version.replace('.', '_')}.html"
        html_path.write_text(html, encoding="utf-8")

        # Save manifest
        manifest = {
            "slug": slug,
            "title": title,
            "description": description,
            "template_type": template_type,
            "version": version,
            "author": author,
            "content_hash": content_hash,
            "created_at": self._now_iso(),
            "updated_at": self._now_iso(),
            "html_path": str(html_path),
        }

        manifest_path = template_dir / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

        return manifest

    def load_template(self, slug: str, user_id: str) -> dict | None:
        """Load a template's HTML content."""
        template_dir = self._templates_dir / user_id / slug
        manifest_path = template_dir / "manifest.json"

        if not manifest_path.exists():
            return None

        manifest = json.loads(manifest_path.read_text())

        # Find the latest HTML file
        html_files = sorted(
            [f for f in template_dir.glob("v*.html")],
            key=lambda x: x.name,
            reverse=True,
        )

        if not html_files:
            return None

        manifest["html"] = html_files[0].read_text()
        return manifest

    def _get_template_metadata(self, slug: str, user_id: str) -> dict | None:
        """Get template metadata without loading HTML."""
        template_dir = self._templates_dir / user_id / slug
        manifest_path = template_dir / "manifest.json"

        if not manifest_path.exists():
            return None

        return json.loads(manifest_path.read_text())

    @staticmethod
    def _increment_version(version: str) -> str:
        """Increment the patch version."""
        parts = version.split(".")
        if len(parts) >= 3:
            parts[2] = str(int(parts[2]) + 1)
        return ".".join(parts)

    @staticmethod
    def _now_iso() -> str:
        """Return current time as ISO 8601 string."""
        from datetime import datetime

        return datetime.now(UTC).isoformat()


# ---------------------------------------------------------------------------
# Template Importer
# ---------------------------------------------------------------------------


class TemplateImporter:
    """Import templates from URLs."""

    @staticmethod
    async def import_from_url(url: str) -> tuple[str | None, list[str]]:
        """Import a template from a raw URL.

        Returns:
            (html_content, list_of_errors)
        """
        import aiohttp

        errors = []
        html = None

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=30) as resp:
                    if resp.status != 200:
                        errors.append(f"HTTP {resp.status}: Failed to fetch template")
                        return None, errors

                    content_type = resp.headers.get("Content-Type", "")
                    if "text/html" not in content_type and "text/plain" not in content_type:
                        errors.append(f"Unexpected content type: {content_type}")
                        return None, errors

                    html = await resp.text()

        except Exception as exc:
            errors.append(f"Network error: {exc}")

        return html, errors


# ---------------------------------------------------------------------------
# Marketplace UI Builder
# ---------------------------------------------------------------------------


class MarketplaceUI:
    """Build the marketplace UI for browsing and installing templates."""

    @staticmethod
    def render_marketplace(
        user_templates: list[dict],
        featured_templates: list[dict] | None = None,
    ) -> str:
        """Render the template marketplace UI."""
        templates = user_templates or []

        # Group by type
        by_type = {}
        for t in templates:
            ttype = t.get("template_type", "custom")
            by_type.setdefault(ttype, []).append(t)

        # Build HTML
        html = """<div class="opendesigner-marketplace">
<style>
.opendesigner-marketplace { padding: 1rem; }
.template-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; margin: 1rem 0; }
.template-card { border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; background: white; transition: all 0.2s; }
.template-card:hover { border-color: #6366f1; box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15); }
.template-card.selected { border-color: #10b981; box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2); }
.template-header { padding: 1rem; background: #f8fafc; border-bottom: 1px solid #e2e8f0; }
.template-title { font-weight: 600; font-size: 1rem; margin: 0; }
.template-version { font-size: 0.75rem; color: #64748b; margin-top: 0.25rem; }
.template-body { padding: 1rem; }
.template-description { font-size: 0.875rem; color: #475569; margin: 0 0 0.75rem; }
.template-meta { font-size: 0.75rem; color: #94a3b8; }
.template-actions { padding: 0.75rem 1rem; background: #f8fafc; border-top: 1px solid #e2e8f0; display: flex; gap: 0.5rem; }
.template-actions button { flex: 1; padding: 0.5rem; border: 1px solid #e2e8f0; border-radius: 6px; cursor: pointer; font-size: 0.875rem; background: white; transition: all 0.2s; }
.template-actions button:hover { background: #f1f5f9; border-color: #cbd5e1; }
.template-actions button.primary { background: #6366f1; color: white; border-color: #6366f1; }
.template-actions button.primary:hover { background: #4f46e5; }
.section-title { font-size: 1.125rem; font-weight: 600; margin: 1.5rem 0 0.75rem; color: #1e293b; }
.import-section { padding: 1rem; background: #f8fafc; border-radius: 8px; margin: 1rem 0; }
.import-section h3 { margin: 0 0 0.75rem; }
.import-section input { width: 100%; padding: 0.5rem; border: 1px solid #e2e8f0; border-radius: 6px; margin-bottom: 0.5rem; }
.import-section button { padding: 0.5rem 1rem; background: #6366f1; color: white; border: none; border-radius: 6px; cursor: pointer; }
.badge { display: inline-block; padding: 0.125rem 0.5rem; border-radius: 999px; font-size: 0.75rem; font-weight: 500; }
.badge-custom { background: #dbeafe; color: #1d4ed8; }
.badge-component { background: #dcfce7; color: #15803d; }
.badge-landing { background: #fef3c7; color: #b45309; }
</style>

"""
        # Featured templates section
        if featured_templates:
            html += '<div class="section-title">🌟 Featured Templates</div>\n'
            html += '<div class="template-grid">\n'
            for t in featured_templates:
                html += MarketplaceUI._render_template_card(t)
            html += "</div>\n"

        # User templates section
        html += '<div class="section-title">📦 Your Templates</div>\n'
        if templates:
            html += '<div class="template-grid">\n'
            for t in templates:
                html += MarketplaceUI._render_template_card(t)
            html += "</div>\n"
        else:
            html += '<p style="color: #64748b; margin: 0.5rem 0;">No templates yet. Create one or import from a URL!</p>\n'

        # Import section
        html += """
<div class="import-section">
    <h3>📥 Import from URL</h3>
    <input type="text" placeholder="https://example.com/template.html" id="od-import-url">
    <button onclick="window.parent.postMessage({type: 'od-import-template', url: document.getElementById('od-import-url').value}, '*')">Import</button>
</div>

<script>
(function() {
    const cards = document.querySelectorAll('.template-card');
    cards.forEach(card => {
        card.addEventListener('click', (e) => {
            if (e.target.tagName === 'BUTTON') return;
            cards.forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');
            const slug = card.dataset.slug;
            window.parent.postMessage({type: 'od-template-select', slug: slug}, '*');
        });
    });
})();
</script>
</div>
"""

        return html

    @staticmethod
    def _render_template_card(template: dict) -> str:
        """Render a single template card."""
        title = template.get("title", "Untitled")
        description = template.get("description", "")[:100]
        version = template.get("version", "1.0.0")
        template_type = template.get("template_type", "custom")
        slug = template.get("slug", "")

        type_badge = f'<span class="badge badge-{template_type}">{template_type}</span>'
        post_preview = (
            "window.parent.postMessage({type: 'od-template-preview', slug: '" + slug + "'}, '*')"
        )
        post_use = "window.parent.postMessage({type: 'od-template-use', slug: '" + slug + "'}, '*')"

        html_parts = []
        html_parts.append('<div class="template-card" data-slug="' + slug + '">')
        html_parts.append('<div class="template-header">')
        html_parts.append('    <h4 class="template-title">' + title + "</h4>")
        html_parts.append(
            '    <div class="template-version">v' + version + " " + type_badge + "</div>"
        )
        html_parts.append("</div>")
        html_parts.append('<div class="template-body">')
        html_parts.append('    <p class="template-description">' + description + "</p>")
        html_parts.append(
            '    <div class="template-meta">Author: '
            + template.get("author", "Anonymous")
            + "</div>"
        )
        html_parts.append("</div>")
        html_parts.append('<div class="template-actions">')
        html_parts.append(
            '    <button onclick="event.stopPropagation(); ' + post_preview + '" >Preview</button>'
        )
        html_parts.append(
            '    <button class="primary" onclick="event.stopPropagation(); '
            + post_use
            + '" >Use</button>'
        )
        html_parts.append("</div>")
        html_parts.append("</div>")
        return "\n".join(html_parts)


# ---------------------------------------------------------------------------
# Template Actions
# ---------------------------------------------------------------------------


class TemplateActions:
    """Handle template-related actions."""

    def __init__(self):
        self.type = "action"
        self.validator = TemplateValidator()
        self.store = None  # Will be set by parent

    def actions(self) -> list[dict[str, str]]:
        """Return available actions."""
        return [
            {
                "name": "Submit Template",
                "description": "Submit your design as a community template",
                "icon": "upload",
            },
            {
                "name": "Import Template",
                "description": "Import a template from a URL",
                "icon": "download",
            },
            {
                "name": "View Marketplace",
                "description": "Browse community templates",
                "icon": "store",
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
        """Handle a template action."""
        message = body.get("message", {})
        content = message.get("content", "")

        if action == "Submit Template":
            return await self._handle_submit(content, __user__, __event_emitter__)
        elif action == "Import Template":
            return await self._handle_import(content, __user__, __event_emitter__)
        elif action == "View Marketplace":
            return self._handle_marketplace(__user__)

        return f"Unknown template action: {action}"

    async def _handle_submit(
        self, content: str, __user__: dict | None, __event_emitter__: Any | None
    ) -> str:
        """Handle template submission."""
        # Extract HTML from message
        html = self._extract_html(content)
        if not html:
            return "No HTML code block found. Please include your design in a ```html code block."

        # Validate
        is_valid, errors = self.validator.validate_template(html)
        if not is_valid:
            error_list = "\n".join(f"- {e}" for e in errors)
            return f"❌ *Template Validation Failed*\n\n{error_list}\n\nPlease remove the dangerous patterns and try again."

        # Get metadata
        user_id = __user__.get("id") if __user__ else "anonymous"
        user_settings = {}
        if self.store:
            user_settings = self._load_user_settings(user_id)

        title = user_settings.get("template_title", "Untitled Template")
        description = user_settings.get("template_description", "Community template")
        template_type = user_settings.get("template_type", "custom")

        # Save
        if self.store:
            result = self.store.save_template(
                user_id=user_id,
                title=title,
                description=description,
                html=html,
                template_type=template_type,
            )
            if result:
                return f"✅ *Template Submitted*\n\n**{title}** (v{result['version']}) has been saved to your templates.\n\nUse **View Marketplace** to browse all your templates."

        return "⚠️ Template saved (no persistent storage available)"

    async def _handle_import(
        self, content: str, __user__: dict | None, __event_emitter__: Any | None
    ) -> str:
        """Handle template import from URL."""
        # Extract URL from message
        url_match = re.search(r"(https?://[^\s]+)", content)
        if not url_match:
            return "Please provide a URL to import from.\n\nExample: `Import https://example.com/template.html`"

        url = url_match.group(1)

        # Import
        html, errors = await TemplateImporter.import_from_url(url)
        if errors:
            return "❌ *Import Failed*\n\n" + "\n".join(errors)

        if not html:
            return "⚠️ No HTML content found at the provided URL."

        # Validate imported template
        is_valid, validation_errors = self.validator.validate_template(html)
        if not is_valid:
            error_list = "\n".join(f"- {e}" for e in validation_errors)
            return f"❌ *Import Rejected (Security)*\n\n{error_list}"

        # Save
        user_id = __user__.get("id") if __user__ else "anonymous"
        if self.store:
            result = self.store.save_template(
                user_id=user_id,
                title=f"Imported from {url}",
                description=f"Imported from {url}",
                html=html,
                template_type="imported",
            )
            if result:
                return f"✅ *Template Imported*\n\n**{result['title']}** (v{result['version']}) has been saved.\n\nUse **View Marketplace** to browse."

        return "⚠️ Template imported (no persistent storage available)"

    def _handle_marketplace(self, __user__: dict | None) -> str:
        """Handle marketplace view."""
        user_id = __user__.get("id") if __user__ else "anonymous"

        user_templates = []
        if self.store:
            user_templates = self.store.get_user_templates(user_id)

        # Load featured templates from file
        featured = self._load_featured_templates()

        return MarketplaceUI.render_marketplace(user_templates, featured)

    def _extract_html(self, content: str) -> str | None:
        """Extract HTML code block from content."""
        match = re.search(r"```(?:html)?\s*([\s\S]*?)```", content)
        if match:
            return match.group(1).strip()
        return None

    def _load_user_settings(self, user_id: str) -> dict:
        """Load user settings (stub)."""
        return {}

    def _load_featured_templates(self) -> list[dict]:
        """Load featured templates from file."""
        # This would load from a community templates registry
        # For now, return empty list
        return []


# Aliases for backward compatibility
class TemplateValidator:  # pragma: no cover
    """Alias for Action — supports existing imports of TemplateValidator."""

    @staticmethod
    def validate_template(html_content: str) -> tuple[bool, list[str]]:
        return Action.validate_template(html_content)
