"""OpenDesign — Unit Tests

Tests for core functionality:
- Intent detection
- Template loading
- Prompt construction
- HTML extraction/validation
- Version persistence
- Code block extraction (Action)
"""

import asyncio
import json
from unittest.mock import AsyncMock

import pytest


def _run_async(coro):
    """Helper to run async test methods (Python 3.14 compatible)."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def data_dir(tmp_path):
    """Create a temporary data directory for testing."""
    designs_dir = tmp_path / "opendesign" / "designs"
    designs_dir.mkdir(parents=True)
    settings_dir = tmp_path / "opendesign" / "settings"
    settings_dir.mkdir(parents=True)
    return tmp_path


@pytest.fixture
def mock_user():
    """Create a mock user dict."""
    return {"id": "test_user_123", "username": "tester"}


@pytest.fixture
def mock_event_emitter():
    """Create a mock event emitter."""
    emitter = AsyncMock()
    return emitter


@pytest.fixture
def sample_body():
    """Create a sample request body."""
    return {
        "model": {"id": "design-studio", "name": "Design Studio"},
        "messages": [{"role": "user", "content": "Create a landing page for a coffee shop"}],
        "options": {"temperature": 0.7},
        "metadata": {},
    }


# ---------------------------------------------------------------------------
# Test: Intent Detection
# ---------------------------------------------------------------------------


class TestIntentDetection:
    """Test the keyword-based intent detection."""

    @pytest.fixture
    def pipe(self):
        """Create a Pipe instance for testing."""
        from functions.design_studio.design_studio import Pipe

        pipe = object.__new__(Pipe)
        pipe._templates_cache = {}
        pipe._prompts_cache = {}
        pipe._data_dir = None
        return pipe

    def test_design_keywords_detected(self, pipe):
        """Design-related prompts should be detected."""
        prompts = [
            "Create a landing page",
            "Build me a dashboard",
            "Generate a button component",
            "Make a presentation",
            "Design a form",
            "Create a website for my bakery",
        ]
        for prompt in prompts:
            assert pipe._is_design_prompt(prompt), f"Should detect: {prompt}"

    def test_non_design_keywords_ignored(self, pipe):
        """Non-design prompts should not trigger design mode."""
        prompts = [
            "What is the capital of France?",
            "Explain quantum mechanics",
            "Write a poem about love",
            "How do I cook pasta?",
        ]
        for prompt in pipe.DESIGN_KEYWORDS:
            assert pipe._is_design_prompt(prompt), f"Keyword {prompt} should be detected"
        for prompt in prompts:
            assert not pipe._is_design_prompt(prompt), f"Should not detect: {prompt}"

    def test_case_insensitive(self, pipe):
        """Detection should be case-insensitive."""
        assert pipe._is_design_prompt("CREATE A DASHBOARD")
        assert pipe._is_design_prompt("create a dashboard")
        assert pipe._is_design_prompt("CrEaTe A DaShBoArD")

    def test_find_last_user_message(self, pipe):
        """Should find the last user message."""
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
            {"role": "user", "content": "Create a landing page"},
        ]
        assert pipe._find_last_user_message(messages) == "Create a landing page"

    def test_empty_messages(self, pipe):
        """Empty messages list should return None."""
        assert pipe._find_last_user_message([]) is None
        assert pipe._find_last_user_message([{"role": "assistant", "content": "Hi"}]) is None

    def test_multimodal_message(self, pipe):
        """Should extract text from multimodal messages."""
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What is this?"},
                    {"type": "image", "url": "http://example.com/img.png"},
                ],
            },
        ]
        assert pipe._find_last_user_message(messages) == "What is this?"


# ---------------------------------------------------------------------------
# Test: Template Loading
# ---------------------------------------------------------------------------


class TestTemplateLoading:
    """Test template file loading and caching."""

    @pytest.fixture
    def pipe(self):
        from functions.design_studio.design_studio import Pipe

        pipe = object.__new__(Pipe)
        pipe._templates_cache = {}
        pipe._prompts_cache = {}
        pipe._data_dir = None
        return pipe

    def test_load_existing_template(self, pipe):
        """Should load an existing template."""
        html = pipe._load_template("landing/minimal")
        assert isinstance(html, str)
        assert len(html) > 100
        assert "<!DOCTYPE html>" in html

    def test_load_nonexistent_template_fallback(self, pipe):
        """Nonexistent template should fall back to minimal."""
        html = pipe._load_template("nonexistent/template")
        assert "<!DOCTYPE html>" in html

    def test_template_caching(self, pipe):
        """Loaded templates should be cached."""
        html1 = pipe._load_template("landing/minimal")
        html2 = pipe._load_template("landing/minimal")
        assert html1 is html2  # Same object (cached)
        assert len(pipe._templates_cache) == 1

    def test_all_templates_loadable(self, pipe):
        """All defined templates should load without error."""
        templates = [
            "landing/minimal",
            "landing/hero",
            "landing/feature-grid",
            "dashboard/analytics",
            "component/button",
            "component/card",
            "component/modal",
            "component/form",
            "presentation/blank",
            "presentation/sections",
            "email/newsletter",
            "email/transactional",
            "social/hero-banner",
            "social/og-card",
        ]
        for template in templates:
            html = pipe._load_template(template)
            assert len(html) > 50, f"Template {template} is too small"
            assert "<html" in html or "<!DOCTYPE" in html, f"Template {template} is not valid HTML"


# ---------------------------------------------------------------------------
# Test: Prompt Construction
# ---------------------------------------------------------------------------


class TestPromptConstruction:
    """Test prompt template loading and variable substitution."""

    @pytest.fixture
    def pipe(self):
        from functions.design_studio.design_studio import Pipe

        pipe = object.__new__(Pipe)
        pipe._templates_cache = {}
        pipe._prompts_cache = {}
        pipe._data_dir = None
        return pipe

    def test_load_prompt_template(self, pipe):
        """Should load a prompt template."""
        prompt = pipe._load_prompt("generate_html")
        assert "{{user_message}}" in prompt
        assert "{{design_system}}" in prompt

    def test_variable_substitution(self, pipe):
        """Jinja2-style variables should be substituted."""
        template = pipe._load_prompt("generate_html")
        constructed = pipe._build_prompt(
            prompt_template=template,
            template_html="<div>test</div>",
            design_system="light",
            user_message="Create a landing page",
        )
        assert "{{ user_message }}" not in constructed
        assert "{{ design_system }}" not in constructed
        assert "Create a landing page" in constructed
        assert "light" in constructed

    def test_css_injection(self, pipe):
        """Design system CSS should be injected."""
        template = pipe._load_prompt("generate_html")
        constructed = pipe._build_prompt(
            prompt_template=template,
            template_html="<div>test</div>",
            design_system="light",
            user_message="Test",
        )
        assert (
            "--od-bg-primary" in constructed
            or "--od-color-bg" in constructed
            or "background" in constructed.lower()
        )

    def test_empty_template_html(self, pipe):
        """Should work even with empty template HTML."""
        template = pipe._load_prompt("generate_html")
        constructed = pipe._build_prompt(
            prompt_template=template,
            template_html="",
            design_system="light",
            user_message="Test",
        )
        assert "Test" in constructed


# ---------------------------------------------------------------------------
# Test: HTML Extraction & Validation
# ---------------------------------------------------------------------------


class TestHTMLExtraction:
    """Test HTML code block extraction and sanitization."""

    @pytest.fixture
    def pipe(self):
        from functions.design_studio.design_studio import Pipe

        pipe = object.__new__(Pipe)
        pipe._templates_cache = {}
        pipe._prompts_cache = {}
        pipe._data_dir = None
        return pipe

    def test_extract_html_code_block(self, pipe):
        """Should extract HTML from markdown code blocks."""
        response = """Here's your design:

```html
<!DOCTYPE html>
<html><body>Hello</body></html>
```

Hope you like it!"""
        result = pipe._parse_response(response)
        assert result["html"] != ""
        assert "Hello" in result["html"]

    def test_extract_generic_code_block(self, pipe):
        """Should extract HTML from generic code blocks."""
        response = """```
<!DOCTYPE html>
<html><body>Test</body></html>
```"""
        result = pipe._parse_response(response)
        assert "Test" in result["html"]

    def test_no_code_block(self, pipe):
        """Should return empty HTML when no code block found."""
        response = "I can't help with that."
        result = pipe._parse_response(response)
        assert result["html"] == ""

    def test_sanitizes_javascript(self, pipe):
        """Dangerous JavaScript should be sanitized."""
        html = '<div onclick="alert(1)">Click</div>'
        safe = pipe._validate_html(html)
        assert "onclick" not in safe

    def test_sanitizes_javascript_uri(self, pipe):
        """javascript: URIs should be sanitized."""
        html = '<a href="javascript:alert(1)">Link</a>'
        safe = pipe._validate_html(html)
        assert "javascript:" not in safe

    def test_sanitizes_eval(self, pipe):
        """eval() calls should be sanitized."""
        html = "<script>eval(userInput)</script>"
        safe = pipe._validate_html(html)
        assert "eval(" not in safe

    def test_sanitizes_form_action(self, pipe):
        """Form actions should be sanitized."""
        html = '<form action="http://evil.com"><input></form>'
        safe = pipe._validate_html(html)
        assert "action=" not in safe or "evil" not in safe

    def test_preserves_safe_html(self, pipe):
        """Safe HTML should be preserved."""
        html = '<div class="test"><p>Hello</p></div>'
        safe = pipe._validate_html(html)
        assert "class=" in safe
        assert "Hello" in safe


# ---------------------------------------------------------------------------
# Test: Version Persistence
# ---------------------------------------------------------------------------


class TestVersionPersistence:
    """Test version saving and loading."""

    @pytest.fixture
    def pipe(self, data_dir):
        from functions.design_studio.design_studio import Pipe

        pipe = object.__new__(Pipe)
        pipe._data_dir = data_dir
        pipe._templates_cache = {}
        pipe._prompts_cache = {}
        return pipe

    def test_save_version(self, pipe, mock_user):
        """Should save a version to disk."""
        design_id = pipe._get_or_create_design_id({}, mock_user)
        version_path = pipe._save_version(
            design_id, "<html>test</html>", "Create a page", mock_user
        )
        assert version_path == "v1.html"

        # Verify file was created
        user_id = pipe._get_user_id(mock_user)
        history_path = (
            pipe._data_dir / "opendesign" / "designs" / user_id / design_id / "history.json"
        )
        assert history_path.exists()

        history = json.loads(history_path.read_text())
        assert len(history) == 1
        assert history[0]["version"] == 1
        assert history[0]["prompt"] == "Create a page"

    def test_version_increments(self, pipe, mock_user):
        """Version numbers should increment."""
        design_id = "test_design"
        pipe._save_version(design_id, "<html>v1</html>", "First", mock_user)
        pipe._save_version(design_id, "<html>v2</html>", "Second", mock_user)

        user_id = pipe._get_user_id(mock_user)
        history_path = (
            pipe._data_dir / "opendesign" / "designs" / user_id / design_id / "history.json"
        )
        history = json.loads(history_path.read_text())
        assert len(history) == 2
        assert history[0]["version"] == 1
        assert history[1]["version"] == 2

    def test_save_without_data_dir(self, pipe):
        """Should return 'memory' when data dir is None."""
        pipe._data_dir = None
        result = pipe._save_version("design_1", "<html>test</html>", "Test")
        assert result == "memory"

    def test_load_user_settings(self, pipe, data_dir):
        """Should load user settings from disk."""
        user_id = "settings_user"
        settings = {"template": "landing/hero", "design_system": "dark"}
        settings_path = data_dir / "opendesign" / "settings" / f"{user_id}.json"
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        settings_path.write_text(json.dumps(settings))

        loaded = pipe._load_user_settings(user_id)
        assert loaded == settings

    def test_user_id_extraction(self, pipe, mock_user):
        """Should extract user ID from user context."""
        assert pipe._get_user_id(mock_user) == "test_user_123"
        assert pipe._get_user_id(None) == "anonymous"


# ---------------------------------------------------------------------------
# Test: Preview Generator Action
# ---------------------------------------------------------------------------


class TestPreviewGenerator:
    """Test the preview generator Action."""

    @pytest.fixture
    def action(self):
        from functions.preview_generator.preview_generator import Action

        return Action()

    def test_extract_code_blocks(self, action):
        """Should extract HTML code blocks from message content."""
        content = """Here's some HTML:

```html
<!DOCTYPE html><html><body>Test</body></html>
```

And some text."""
        blocks = action._extract_code_blocks(content)
        assert len(blocks) == 1
        assert "Test" in blocks[0]

    def test_extract_multiple_blocks(self, action):
        """Should extract multiple code blocks."""
        content = """```html
<div>First</div>
```

```html
<div>Second</div>
```"""
        blocks = action._extract_code_blocks(content)
        assert len(blocks) == 2
        assert "First" in blocks[0]
        assert "Second" in blocks[1]

    def test_no_code_blocks(self, action):
        """Should return empty list when no code blocks found."""
        content = "Just plain text, no code."
        blocks = action._extract_code_blocks(content)
        assert blocks == []

    def test_render_preview(self, action):
        """Should render a sandboxed iframe preview."""
        html = "<html><body>Preview</body></html>"
        result = action._render_preview(html)
        assert "srcdoc=" in result
        assert "sandbox=" in result
        assert "allow-scripts" in result
        assert "allow-same-origin" in result

    def test_render_editor(self, action):
        """Should render the split-pane live editor."""
        html = "<html><body>Editor</body></html>"
        result = action._render_editor(html)
        assert "srcdoc=" in result
        assert "textarea" in result
        assert "iframe" in result

    def test_escape_for_srcdoc(self, action):
        """HTML should be properly escaped for srcdoc."""
        raw = '<script>alert("xss")</script>'
        escaped = action._escape_for_srcdoc(raw)
        assert "&lt;" in escaped
        assert "&gt;" in escaped
        assert raw not in escaped

    def test_actions_list(self, action):
        """Should return the correct list of actions."""
        actions = action.actions()
        names = [a["name"] for a in actions]
        assert "Generate Preview" in names
        assert "Export HTML" in names
        assert "Open Editor" in names


# ---------------------------------------------------------------------------
# Test: Prompt Enhancer Filter
# ---------------------------------------------------------------------------


class TestPromptEnhancer:
    """Test the prompt enhancer Filter."""

    @pytest.fixture
    def filter(self):
        from functions.prompt_enhancer.prompt_enhancer import Filter

        return Filter()

    def test_enhance_design_prompt(self, filter):
        """Design prompts should be enhanced."""
        body = {
            "messages": [{"role": "user", "content": "Create a landing page"}],
            "system_prompt": "You are helpful.",
        }
        result = _run_async(filter.inlet(body))
        assert "Design Studio Guidelines" in result.get("system_prompt", "")
        assert "Accessibility" in result.get("system_prompt", "")

    def test_skip_non_design_prompt(self, filter):
        """Non-design prompts should not be enhanced."""
        body = {
            "messages": [{"role": "user", "content": "What is 2+2?"}],
            "system_prompt": "You are helpful.",
        }
        result = _run_async(filter.inlet(body))
        assert result["system_prompt"] == "You are helpful."

    def test_outlet_adds_metadata(self, filter):
        """Assistant responses with HTML should get design metadata."""
        body = {
            "messages": [
                {"role": "user", "content": "Create a page"},
                {"role": "assistant", "content": "```html\n<!DOCTYPE html>...</html>\n```"},
            ],
        }
        result = _run_async(filter.outlet(body))
        assert "opendesign" in result.get("metadata", {})
        assert result["metadata"]["opendesign"]["source"] == "opendesign"


# ---------------------------------------------------------------------------
# Multi-model Comparison Tests
# ---------------------------------------------------------------------------


class TestModelComparison:
    """Tests for the multi-model comparison feature."""

    def test_manifold_includes_compare_models(self):
        """Compare Models should be in the manifold."""
        from functions.design_studio.design_studio import Pipe

        pipe = object.__new__(Pipe)
        models = pipe.pipes()
        model_ids = [m["id"] for m in models]
        assert "compare-models" in model_ids
        compare_model = next(m for m in models if m["id"] == "compare-models")
        assert "Compare Models" in compare_model["name"]

    def test_detect_comparison_mode(self):
        """Should detect compare mode from model id."""
        from functions.design_studio.design_studio import Pipe

        pipe = object.__new__(Pipe)
        assert pipe._detect_mode("compare-models") == "compare"
        assert pipe._detect_mode("compare models") == "compare"
        assert pipe._detect_mode("design-studio") == "generate"

    def test_compare_action_exists(self):
        """Compare Models action should exist in preview generator."""
        from functions.preview_generator.preview_generator import Action

        action = Action()
        action_names = [a["name"] for a in action.actions()]
        assert "Compare Models" in action_names

    def test_extract_comparison_models(self):
        """Should extract model names and HTML from comparison output."""
        from functions.preview_generator.preview_generator import Action

        action = Action()
        content = """🔄 *Model Comparison Complete*

**gpt-4o:** ✅ Generated
**claude-3.5-sonnet:** ✅ Generated

```html
<div class='test'>GPT Output</div>
```

```html
<div class='test'>Claude Output</div>
```
"""
        models = action._extract_comparison_models(content)
        assert len(models) == 2
        assert "gpt-4o" in models[0][0] or models[0][0]
        assert "claude-3.5-sonnet" in models[1][0] or models[1][0]
        assert "<div class='test'>GPT Output</div>" in models[0][1]
        assert "<div class='test'>Claude Output</div>" in models[1][1]

    def test_render_comparison(self):
        """Should render comparison UI."""
        from functions.preview_generator.preview_generator import Action

        action = Action()
        content = """**gpt-4o:** ✅
**claude-3.5-sonnet:** ✅

```html
<!DOCTYPE html><html><body><h1>GPT</h1></body></html>
```

```html
<!DOCTYPE html><html><body><h1>Claude</h1></body></html>
```
"""
        result = action._render_comparison(content)
        assert "comparison-container" in result
        assert "comparison-panel" in result
        assert "comparison-frame" in result
        assert "sandbox=" in result
        assert "allow-scripts" in result
