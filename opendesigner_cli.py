#!/usr/bin/env python3
"""
OpenDesigner CLI — Standalone test runner for the generation pipeline.

Run all tests:
    python opendesigner_cli.py

Run a specific test:
    python opendesigner_cli.py intent
    python opendesigner_cli.py templates
    python opendesigner_cli.py generate

Shows the generation pipeline working end-to-end without needing OpenWebUI.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from functions.designer_studio.designer_studio import Pipe
from functions.preview_generator.preview_generator import Action as PreviewGenerator
from functions.prompt_enhancer.prompt_enhancer import Filter as PromptEnhancer


# ANSI colors
class Colors:
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    CYAN = "\033[0;36m"
    BOLD = "\033[1m"
    NC = "\033[0m"  # No Color


def print_header(title):
    print(f"\n{Colors.BLUE}{'=' * 60}{Colors.NC}")
    print(f"{Colors.BLUE}{Colors.BOLD}  {title}{Colors.NC}")
    print(f"{Colors.BLUE}{'=' * 60}{Colors.NC}\n")


def print_test(name):
    print(f"{Colors.CYAN}▶{Colors.NC} {name}")


def print_pass(message="Passed"):
    print(f"  {Colors.GREEN}✓{Colors.NC} {message}")


def print_fail(message="Failed"):
    print(f"  {Colors.RED}✗{Colors.NC} {message}")


def print_info(message):
    print(f"  {Colors.YELLOW}ℹ{Colors.NC} {message}")


class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def run_test(self, name, func):
        print_test(name)
        try:
            result = func()
            if result:
                print_pass()
                self.passed += 1
            else:
                print_fail()
                self.failed += 1
        except Exception as e:
            print_fail(f"Error: {str(e)}")
            self.failed += 1


def test_intent_detection():
    """Test that design intent is correctly detected from chat messages."""
    pipe = Pipe()

    # Test 1: Design keyword detected
    messages = [{"role": "user", "content": "Create a landing page for my startup"}]
    assert pipe.detect_intent(messages), "Should detect design intent"

    # Test 2: Non-design message ignored
    messages = [{"role": "user", "content": "What's the weather today?"}]
    assert not pipe.detect_intent(messages), "Should not detect design intent"

    # Test 3: Multiple messages - last one counts
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"},
        {"role": "user", "content": "Generate a dashboard"},
    ]
    assert pipe.detect_intent(messages), "Should detect in last message"

    return True


def test_template_loading():
    """Test that templates load correctly from the templates directory."""
    pipe = Pipe()

    # Test 1: Load existing template
    template = pipe.load_template("landing/hero.html")
    assert template is not None, "Should load template"
    assert "HTML" in template or "<html" in template.lower(), "Should contain HTML"

    # Test 2: Load nonexistent template (should fall back)
    template = pipe.load_template("nonexistent/template.html")
    assert template is not None, "Should return fallback template"
    assert len(template) > 100, "Fallback should have content"

    # Test 3: Template caching works
    template1 = pipe.load_template("landing/hero.html")
    template2 = pipe.load_template("landing/hero.html")
    assert template1 == template2, "Cached templates should match"

    return True


def test_prompt_construction():
    """Test that prompts are constructed with correct variables and context."""
    pipe = Pipe()

    # Test 1: Load prompt template
    prompt_text = pipe.load_prompt_template("generate_html.md")
    assert prompt_text is not None, "Should load prompt template"
    assert "{{" in prompt_text, "Should contain Jinja2 variables"

    # Test 2: Variable substitution works
    variables = {
        "page_type": "landing page",
        "page_title": "My Startup",
        "page_description": "The best startup ever",
        "template": "<html><body>Hello</body></html>",
        "css_theme": "light",
        "color_scheme": "blue",
        "font_family": "sans-serif",
        "include_logo": "false",
        "include_navigation": "true",
        "include_hero": "true",
        "include_features": "true",
        "include_cta": "true",
        "include_footer": "true",
        "include_testimonials": "false",
        "include_pricing": "false",
    }
    prompt = pipe._build_prompt("Create a landing page", variables, "landing/hero.html")
    assert "My Startup" in prompt, "Should substitute page_title"
    assert "The best startup ever" in prompt, "Should substitute page_description"

    return True


def test_html_extraction():
    """Test that HTML is correctly extracted from LLM response."""
    pipe = Pipe()

    # Test 1: Extract from code block
    response = """
    Here's your landing page:

    ```html
    <!DOCTYPE html>
    <html>
    <head><title>Test</title></head>
    <body><h1>Hello World</h1></body>
    </html>
    ```

    Let me know if you need changes!
    """
    html = pipe.extract_html_from_response(response)
    assert "<html" in html.lower(), "Should extract HTML"
    assert "Hello World" in html, "Should preserve content"

    # Test 2: No code block returns empty
    response = "I can't help with that."
    html = pipe.extract_html_from_response(response)
    assert html is not None, "Should return something"

    return True


def test_html_sanitization():
    """Test that HTML is sanitized to remove dangerous code."""
    pipe = Pipe()

    # Test 1: Sanitize script tags
    html = '<html><body><script>alert("XSS")</script></body></html>'
    sanitized = pipe.sanitize_html(html)
    assert "<script>" not in sanitized.lower(), "Should remove script tags"

    # Test 2: Sanitize onerror attributes
    html = '<img src="x" onerror="alert(1)">'
    sanitized = pipe.sanitize_html(html)
    assert "onerror" not in sanitized.lower(), "Should remove onerror"

    # Test 3: Preserve safe HTML
    html = '<div class="container"><h1>Safe Content</h1></div>'
    sanitized = pipe.sanitize_html(html)
    assert "Safe Content" in sanitized, "Should preserve safe content"

    return True


def test_preview_generation():
    """Test that preview generation works correctly."""
    preview = PreviewGenerator()

    # Test 1: Extract code blocks
    response = "Here's the HTML:\n```html\n<div>Test</div>\n```"
    blocks = preview.extract_code_blocks(response)
    assert len(blocks) > 0, "Should extract code blocks"

    # Test 2: Render preview
    html = "<html><body><h1>Preview</h1></body></html>"
    preview_html = preview.render_preview(html)
    assert "iframe" in preview_html.lower(), "Should create iframe"
    assert "Preview" in preview_html, "Should preserve content"

    # Test 3: Render editor
    editor_html = preview.render_editor(html)
    assert "textarea" in editor_html.lower() or "code" in editor_html.lower(), (
        "Should create editor"
    )

    return True


def test_prompt_enhancement():
    """Test that prompts are enhanced with design context."""
    enhancer = PromptEnhancer()

    # Test 1: Enhance design prompt
    messages = [{"role": "user", "content": "Create a landing page"}]
    enhanced = enhancer.outlet(messages)
    assert enhanced is not None, "Should return enhanced messages"

    # Test 2: Skip non-design prompt
    messages = [{"role": "user", "content": "What's 2+2?"}]
    enhanced = enhancer.outlet(messages)
    assert enhanced is not None, "Should return messages even if not enhanced"

    return True


def test_all_templates_loadable():
    """Test that all templates can be loaded without errors."""
    pipe = Pipe()
    templates_dir = Path("functions/designer_studio/templates")

    if not templates_dir.exists():
        print_info("Templates directory not found")
        return True

    total = 0
    failed = 0

    for template_file in templates_dir.rglob("*.html"):
        rel_path = template_file.relative_to(templates_dir)
        template_str = str(rel_path).replace(os.sep, "/")
        total += 1

        try:
            template = pipe.load_template(template_str)
            if template and len(template) > 50:
                pass  # Success
            else:
                failed += 1
                print(f"  {Colors.RED}✗{Colors.NC} {template_str} (empty or too short)")
        except Exception as e:
            failed += 1
            print(f"  {Colors.RED}✗{Colors.NC} {template_str} ({e})")

    print(f"  Loaded {total - failed}/{total} templates successfully")
    return failed == 0


def test_end_to_end_generation():
    """Test complete generation pipeline (without actual LLM call)."""
    pipe = Pipe()

    # Step 1: Detect intent
    messages = [{"role": "user", "content": "Generate a dashboard"}]
    assert pipe.detect_intent(messages), "Intent detection should work"

    # Step 2: Load template
    template = pipe.load_template("dashboard/analytics.html")
    assert template is not None, "Template should load"

    # Step 3: Build variables
    variables = {
        "page_type": "dashboard",
        "page_title": "Analytics",
        "page_description": "Analytics dashboard",
        "template": template,
        "css_theme": "light",
        "color_scheme": "blue",
        "font_family": "sans-serif",
        "include_logo": "false",
        "include_navigation": "true",
        "include_hero": "false",
        "include_features": "true",
        "include_cta": "false",
        "include_footer": "true",
        "include_testimonials": "false",
        "include_pricing": "false",
    }

    # Step 4: Build prompt
    prompt = pipe._build_prompt("Generate a dashboard", variables, "dashboard/analytics.html")
    assert "Analytics" in prompt, "Prompt should contain variables"

    print_info("Pipeline works end-to-end (LLM call skipped)")
    return True


def main():
    """Run all tests."""
    print_header("OPENDESIGNER COMPREHENSIVE TEST SUITE")

    runner = TestRunner()

    # Test Suite 1: Core Functions
    print_header("📦 TEST SUITE 1: Core Functions")
    runner.run_test("Intent detection", test_intent_detection)
    runner.run_test("Template loading", test_template_loading)
    runner.run_test("Prompt construction", test_prompt_construction)
    runner.run_test("HTML extraction", test_html_extraction)
    runner.run_test("HTML sanitization", test_html_sanitization)

    # Test Suite 2: Preview & Enhancement
    print_header("📦 TEST SUITE 2: Preview & Enhancement")
    runner.run_test("Preview generation", test_preview_generation)
    runner.run_test("Prompt enhancement", test_prompt_enhancement)

    # Test Suite 3: Template Validation
    print_header("📦 TEST SUITE 3: Template Validation")
    runner.run_test("All templates loadable", test_all_templates_loadable)
    runner.run_test("End-to-end pipeline", test_end_to_end_generation)

    # Summary
    print_header("📊 TEST RESULTS")
    print(f"  {Colors.GREEN}Passed: {Colors.BOLD}{runner.passed}{Colors.NC}")
    print(
        f"  {Colors.RED if runner.failed > 0 else Colors.GREEN}Failed: {Colors.BOLD}{runner.failed}{Colors.NC}"
    )
    print(f"  Total:  {runner.passed + runner.failed}")

    if runner.failed == 0:
        print(f"\n  {Colors.GREEN}{Colors.BOLD}✅ ALL TESTS PASSED!{Colors.NC}")
    else:
        print(f"\n  {Colors.RED}{Colors.BOLD}❌ SOME TESTS FAILED{Colors.NC}")

    print()
    return runner.failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
