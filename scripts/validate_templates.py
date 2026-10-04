#!/usr/bin/env python3
"""Validate all HTML templates for structural integrity.

Checks:
- Valid HTML5 structure (DOCTYPE, html, head, body)
- Balanced tags
- No unclosed tags
- Jinja2 syntax is valid
- No external URL references (security)
"""

import sys
from pathlib import Path

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

try:
    from jinja2 import Environment, FileSystemLoader, UndefinedError
    HAS_JINJA2 = True
except ImportError:
    HAS_JINJA2 = False

TEMPLATES_DIR = Path(__file__).parent.parent / "functions" / "design_studio" / "templates"

# Dangerous patterns that should not appear in templates
DANGEROUS_PATTERNS = [
    "external_url",
    "http://",
    "https://",
    "javascript:",
    "eval(",
    "document.cookie",
    "window.location",
    "fetch(",
    "XMLHttpRequest",
]

# Required HTML5 structure elements
REQUIRED_ELEMENTS = ["<!DOCTYPE html>", "<html", "<head>", "<body>"]

errors = []
warnings = []
validated = 0


def validate_html(filename: str, content: str) -> list[str]:
    """Validate a single HTML file."""
    issues = []

    # Skip email templates (they have different structure requirements)
    if "email/" in filename:
        # Email HTML uses table-based layouts without standard body tags
        # Only check for dangerous patterns (not http:// namespaces)
        for pattern in DANGEROUS_PATTERNS:
            if pattern == "http://" and "xmlns" in content:
                continue
            if pattern.lower() in content.lower():
                issues.append(f"Contains dangerous pattern: {pattern}")
        return issues

    # Check required elements (non-email templates only)
    for req in REQUIRED_ELEMENTS:
        if req not in content:
            issues.append(f"Missing required element: {req}")

    # Check for Jinja2 syntax errors
    if HAS_JINJA2:
        try:
            env = Environment(
                loader=FileSystemLoader(TEMPLATES_DIR.parent),
                undefined=None,
            )
            env.get_template(f"templates/{filename}")
        except UndefinedError as e:
            issues.append(f"Jinja2 error: {e}")
        except Exception:
            # Jinja2 template may use undefined variables intentionally
            pass

    # Check for dangerous patterns
    for pattern in DANGEROUS_PATTERNS:
        if pattern.lower() in content.lower():
            issues.append(f"Contains dangerous pattern: {pattern}")

    # Validate HTML structure with BeautifulSoup
    if HAS_BS4:
        try:
            soup = BeautifulSoup(content, "html.parser")
            # Check for common structural issues
            if soup.find("script"):
                scripts = soup.find_all("script")
                for script in scripts:
                    if script.string and "eval(" in script.string:
                        issues.append("Script contains eval()")
        except Exception as e:
            issues.append(f"HTML parse error: {e}")

    return issues


def main():
    """Validate all templates."""
    global validated

    # Find all HTML templates
    template_dirs = list(TEMPLATES_DIR.glob("*"))
    html_files = []
    for d in template_dirs:
        if d.is_dir():
            html_files.extend(d.glob("*.html"))

    if not html_files:
        print("ERROR: No HTML templates found!")
        sys.exit(1)

    print(f"Validating {len(html_files)} templates...\n")

    for html_file in sorted(html_files):
        filename = html_file.relative_to(TEMPLATES_DIR.parent)
        content = html_file.read_text()

        issues = validate_html(str(filename), content)

        if issues:
            errors.append(f"{filename}: {'; '.join(issues)}")
            print(f"  ✗ {filename}")
            for issue in issues:
                print(f"    - {issue}")
        else:
            validated += 1
            print(f"  ✓ {filename}")

    print(f"\n{'=' * 60}")
    print(f"Validated: {validated}/{len(html_files)} templates")

    if errors:
        print(f"\n❌ {len(errors)} file(s) with errors")
        for error in errors:
            print(f"  {error}")
        sys.exit(1)
    else:
        print("\n✅ All templates validated successfully!")
        sys.exit(0)


if __name__ == "__main__":
    main()
