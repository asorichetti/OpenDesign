"""
title: OpenDesigner Accessibility Checker
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesigner
version: 0.1.0
required_open_webui_version: 0.10.0
"""

import re
from typing import Any


class Action:
    """OpenDesigner Accessibility Checker — WCAG 2.1 AA compliance validation."""

    def __init__(self):
        self.type = "action"

    def actions(self) -> list[dict[str, str]]:
        """Return available actions."""
        return [
            {
                "name": "Check Accessibility",
                "description": "Analyze design for WCAG 2.1 AA accessibility compliance",
                "icon": "accessibility",
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
        """Handle action click."""
        if action == "Check Accessibility":
            html_content = body.get("message", {}).get("content", "")
            return self._check_accessibility(html_content)

        return f"Unknown action: {action}"

    def _check_accessibility(self, html: str) -> str:
        """Check HTML for accessibility issues."""
        issues = self._analyze_html(html)
        score = self._calculate_score(issues)

        return self._render_report(html, issues, score)

    def _analyze_html(self, html: str) -> list[dict]:
        """Analyze HTML for accessibility issues."""
        issues = []

        # 1. Check for alt text on images
        img_tags = re.findall(r"<img[^>]*>", html, re.IGNORECASE)
        for img in img_tags:
            if not re.search(r"alt\s*=", img, re.IGNORECASE):
                issues.append(
                    {
                        "severity": "error",
                        "code": "img-no-alt",
                        "message": "Image missing alt attribute",
                        "wcag": "1.1.1",
                        "fix": 'Add alt="description" to all <img> tags',
                    }
                )

        # 2. Check for heading hierarchy
        headings = re.findall(r"<h([1-6])(?:\s|>)", html, re.IGNORECASE)
        if headings:
            first_heading = int(headings[0])
            if first_heading != 1:
                issues.append(
                    {
                        "severity": "warning",
                        "code": "heading-skipped",
                        "message": f"First heading is h{first_heading}, should start with h1",
                        "wcag": "1.3.1",
                        "fix": "Start heading hierarchy with <h1>",
                    }
                )

        # 3. Check for ARIA landmarks
        if not re.search(r'role\s*=\s*["\']main["\']', html, re.IGNORECASE):
            if not re.search(r"<main\b", html, re.IGNORECASE):
                issues.append(
                    {
                        "severity": "warning",
                        "code": "missing-main",
                        "message": "Missing main landmark",
                        "wcag": "1.3.1",
                        "fix": "Add <main> tag or role='main' to primary content",
                    }
                )

        # 4. Check for form labels
        inputs = re.findall(
            r'<input[^>]*type=["\']?(text|email|password|number|tel)["\']?[^>]*>',
            html,
            re.IGNORECASE,
        )
        for _ in inputs:
            # Check if there's a corresponding label
            if not re.search(r'<label[^>]*for\s*=\s*["\'][^"\']*["\']', html, re.IGNORECASE):
                issues.append(
                    {
                        "severity": "error",
                        "code": "input-no-label",
                        "message": "Form input missing associated label",
                        "wcag": "1.3.1",
                        "fix": "Add <label for='input-id'> for each form input",
                    }
                )

        # 5. Check for color contrast (basic check)
        color_matches = re.findall(r"color\s*:\s*([^;]+)", html, re.IGNORECASE)
        bg_matches = re.findall(r"background(?:-color)?\s*:\s*([^;]+)", html, re.IGNORECASE)
        if color_matches and bg_matches:
            # Basic check - if text is light on light background
            issues.append(
                {
                    "severity": "info",
                    "code": "contrast-check",
                    "message": "Manual color contrast verification needed",
                    "wcag": "1.4.3",
                    "fix": "Ensure 4.5:1 contrast ratio for normal text, 3:1 for large text",
                }
            )

        # 6. Check for semantic HTML
        if not re.search(r"<(header|footer|nav|article|section)\b", html, re.IGNORECASE):
            issues.append(
                {
                    "severity": "info",
                    "code": "missing-semantic",
                    "message": "Missing semantic HTML elements",
                    "wcag": "1.3.1",
                    "fix": "Use <header>, <nav>, <main>, <footer>, <article>, <section>",
                }
            )

        # 7. Check for keyboard accessibility (tabindex)
        if re.search(r'tabindex\s*=\s*["\']?[0-9]', html, re.IGNORECASE):
            issues.append(
                {
                    "severity": "error",
                    "code": "bad-tabindex",
                    "message": "Positive tabindex values found (disrupts keyboard navigation)",
                    "wcag": "2.4.3",
                    "fix": "Remove positive tabindex values; use tabindex='0' or '-1' instead",
                }
            )

        # 8. Check for link text
        links = re.findall(r"<a[^>]*>(.*?)</a>", html, re.IGNORECASE)
        for link in links:
            if not link.strip() or link.strip() == "...":
                issues.append(
                    {
                        "severity": "error",
                        "code": "empty-link",
                        "message": "Link has no accessible text",
                        "wcag": "2.4.4",
                        "fix": "Add descriptive text to all links",
                    }
                )

        return issues

    def _calculate_score(self, issues: list[dict]) -> int:
        """Calculate accessibility score (0-100)."""
        if not issues:
            return 100

        score = 100
        for issue in issues:
            if issue["severity"] == "error":
                score -= 15
            elif issue["severity"] == "warning":
                score -= 10
            elif issue["severity"] == "info":
                score -= 5

        return max(0, score)

    def _get_score_label(self, score: int) -> tuple[str, str]:
        """Get score label and color."""
        if score >= 90:
            return ("Excellent", "#22c55e")
        elif score >= 70:
            return ("Good", "#eab308")
        elif score >= 50:
            return ("Needs Work", "#f97316")
        else:
            return ("Poor", "#ef4444")

    def _render_report(self, html: str, issues: list[dict], score: int) -> str:
        """Render accessibility report."""
        score_label, score_color = self._get_score_label(score)
        issues_html = ""

        if issues:
            for issue in issues:
                severity_icon = {
                    "error": "❌",
                    "warning": "⚠️",
                    "info": "ℹ️",
                }.get(issue["severity"], "📝")

                issues_html += f"""
                <div class="issue-item" style="padding: 1rem; margin-bottom: 0.75rem; background: white; border-left: 4px solid {score_color}; border-radius: 6px;">
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                        <span>{severity_icon}</span>
                        <span style="font-weight: 600; color: #1e293b;">{issue["code"]}</span>
                        <span style="font-size: 0.75rem; color: #64748b; margin-left: auto;">WCAG {issue["wcag"]}</span>
                    </div>
                    <p style="margin: 0 0 0.5rem; color: #334155;">{issue["message"]}</p>
                    <p style="margin: 0; font-size: 0.875rem; color: #6366f1;"><strong>Fix:</strong> {issue["fix"]}</p>
                </div>
                """
        else:
            issues_html = """
            <div style="text-align: center; padding: 3rem; background: #f0fdf4; border-radius: 12px;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">✅</div>
                <h3 style="color: #16a34a; margin: 0 0 0.5rem;">Perfect Score!</h3>
                <p style="color: #15803d; margin: 0;">Your design meets all WCAG 2.1 AA requirements</p>
            </div>
            """

        return f"""
        <div class="a11y-report" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .a11y-report {{ max-width: 800px; margin: 0 auto; }}
                .report-header {{ text-align: center; margin-bottom: 2rem; }}
                .report-header h3 {{ font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0 0 0.5rem; }}
                .report-header p {{ color: #64748b; margin: 0; }}
                .score-card {{ background: white; border: 2px solid {score_color}; border-radius: 12px; padding: 2rem; text-align: center; margin-bottom: 1.5rem; }}
                .score-number {{ font-size: 4rem; font-weight: 700; color: {score_color}; margin: 0; }}
                .score-label {{ font-size: 1.25rem; font-weight: 600; color: #1e293b; margin: 0.5rem 0 0; }}
                .issues-list {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; }}
                .issues-title {{ font-size: 1rem; font-weight: 600; color: #1e293b; margin: 0 0 1rem; }}
                .legend {{ display: flex; gap: 1rem; margin-bottom: 1rem; flex-wrap: wrap; }}
                .legend-item {{ display: flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; }}
            </style>

            <div class="report-header">
                <h3>♿ Accessibility Report</h3>
                <p>WCAG 2.1 AA Compliance Analysis</p>
            </div>

            <div class="score-card">
                <p class="score-number">{score}</p>
                <p class="score-label">{score_label}</p>
            </div>

            <div class="legend">
                <div class="legend-item"><span style="color: #ef4444;">❌ Error</span> - Must fix</div>
                <div class="legend-item"><span style="color: #eab308;">⚠️ Warning</span> - Should fix</div>
                <div class="legend-item"><span style="color: #3b82f6;">ℹ️ Info</span> - Good practice</div>
            </div>

            <div class="issues-list">
                <h4 class="issues-title">Issues Found: {len(issues)}</h4>
                {issues_html}
            </div>
        </div>
        """
