#!/usr/bin/env python3
"""Security check for OpenDesigner templates and Python code.

Scans for:
- Hardcoded API keys / secrets
- Dangerous function calls (eval, exec, compile)
- SQL injection patterns
- Insecure HTTP URLs (should use HTTPS)
- External script/style sources
- Form actions pointing to external URLs
"""

import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

# Patterns that indicate potential security issues
SECURITY_PATTERNS = {
    "hardcoded_secret": {
        "pattern": r'(api[_-]?key|secret|token|password)\s*=\s*["\'][^"\']{8,}["\']',
        "severity": "critical",
        "message": "Potential hardcoded secret detected",
    },
    "eval_call": {
        "pattern": r"\beval\s*\(",
        "severity": "critical",
        "message": "eval() call detected - potential code injection",
    },
    "exec_call": {
        "pattern": r"\bexec\s*\(",
        "severity": "critical",
        "message": "exec() call detected - potential code injection",
    },
    "compile_call": {
        "pattern": r"\bcompile\s*\(",
        "severity": "high",
        "message": "compile() call detected - potential code injection",
    },
    "insecure_url": {
        "pattern": r'http://(?!localhost|127\.0\.0\.1)[^\s"\']+\.com',
        "severity": "medium",
        "message": "Insecure HTTP URL detected (should use HTTPS)",
    },
    "external_script": {
        "pattern": r'<script\s+src\s*=\s*["\']https?://[^\s"\']+',
        "severity": "high",
        "message": "External script source detected",
    },
    "external_style": {
        "pattern": r'<link\s+rel\s*=\s*["\']stylesheet["\']\s+href\s*=\s*["\']https?://[^\s"\']+',
        "severity": "high",
        "message": "External stylesheet source detected",
    },
    "sql_injection": {
        "pattern": r"(SELECT|INSERT|UPDATE|DELETE|DROP|UNION)\s+.*\s*(\+|format\(|%s|\.format\()",
        "severity": "critical",
        "message": "Potential SQL injection pattern",
    },
    "innerHTML": {
        "pattern": r"\.innerHTML\s*=",
        "severity": "medium",
        "message": "innerHTML usage - potential XSS vector",
    },
    "document_write": {
        "pattern": r"document\.write\s*\(",
        "severity": "high",
        "message": "document.write() - potential XSS vector",
    },
    "form_action_external": {
        "pattern": r'<form[^>]*action\s*=\s*["\']https?://(?!localhost|127\.0\.0\.1)[^\s"\']+',
        "severity": "high",
        "message": "Form action pointing to external URL",
    },
    "on.*=.*handler": {
        "pattern": r'\bon\w+\s*=\s*["\'][^"\']*["\']',
        "severity": "medium",
        "message": "Inline event handler - consider using addEventListener",
    },
}

# Extensions considered "code" files (where dangerous function calls matter)
CODE_EXTENSIONS = {".py", ".js", ".ts", ".jsx", ".tsx", ".mjs"}

# Patterns for dangerous code functions (eval/exec/compile)
DANGEROUS_CODE_PATTERNS = {"eval_call", "exec_call", "compile_call"}

# Files to exclude from scanning
EXCLUDED_PATTERNS = [
    "__pycache__",
    ".git",
    ".pytest_cache",
    "node_modules",
    "venv",
    ".venv",
    ".cache",
]

# Files/directories to exclude from scanning (exact match or prefix)
EXCLUDED_DIRS = [
    "docs/",
    "tests/",
    "demo/",
    "scripts/check_security.py",
    "scripts/validate_templates.py",
    "opendesigner_cli.py",
    "README.md",
    "plugins/",
]

# Extensions to scan
SCAN_EXTENSIONS = [".py", ".html", ".css", ".js", ".md"]


def scan_file(filepath: Path) -> list[dict]:
    """Scan a single file for security issues."""
    issues = []
    rel_path = str(filepath.relative_to(PROJECT_ROOT))

    # Skip excluded paths
    for excluded in EXCLUDED_PATTERNS:
        if excluded in str(filepath):
            return issues

    # Skip excluded directories and files
    for excluded in EXCLUDED_DIRS:
        if rel_path == excluded or rel_path.startswith(excluded):
            return issues

    try:
        content = filepath.read_text()
    except (UnicodeDecodeError, PermissionError):
        return issues

    lines = content.split("\n")

    for pattern_name, config in SECURITY_PATTERNS.items():
        matches = re.finditer(config["pattern"], content, re.IGNORECASE)
        for match in matches:
            # Get line number
            line_no = content[: match.start()].count("\n") + 1
            line_text = lines[line_no - 1].strip() if line_no <= len(lines) else ""

            # Skip if line has security allow marker
            if "# security:allow" in line_text or "#sec:allow" in line_text:
                continue

            # Skip document.write in preview_generator (intentional for iframe injection)
            if pattern_name == "document_write" and "preview_generator" in rel_path:
                continue

            # Skip re.compile() calls (safe regex compilation, not code compile)
            if pattern_name == "compile_call" and (
                "re.compile" in line_text or "regex" in line_text
            ):
                continue

            # Skip dangerous code patterns (eval/exec/compile) in non-code files
            # These are only security concerns in actual executable code, not docs
            if pattern_name in DANGEROUS_CODE_PATTERNS and filepath.suffix not in CODE_EXTENSIONS:
                continue

            issues.append(
                {
                    "file": str(filepath.relative_to(PROJECT_ROOT)),
                    "line": line_no,
                    "severity": config["severity"],
                    "pattern": pattern_name,
                    "message": config["message"],
                    "match": match.group()[:50],  # Truncate for readability
                }
            )

    return issues


def main():
    """Scan all files for security issues."""
    all_issues = []

    # Collect files to scan
    files_to_scan = []
    for ext in SCAN_EXTENSIONS:
        files_to_scan.extend(PROJECT_ROOT.rglob(f"*{ext}"))

    if not files_to_scan:
        print("ERROR: No files to scan!")
        sys.exit(1)

    print(f"Scanning {len(files_to_scan)} files for security issues...\n")

    for filepath in sorted(files_to_scan):
        issues = scan_file(filepath)
        all_issues.extend(issues)

    # Report results
    critical = [i for i in all_issues if i["severity"] == "critical"]
    high = [i for i in all_issues if i["severity"] == "high"]
    medium = [i for i in all_issues if i["severity"] == "medium"]
    low = [i for i in all_issues if i["severity"] == "low"]

    print(f"{'=' * 60}")
    print(f"Total issues found: {len(all_issues)}")
    if critical:
        print(f"  🔴 Critical: {len(critical)}")
    if high:
        print(f"  🟠 High: {len(high)}")
    if medium:
        print(f"  🟡 Medium: {len(medium)}")
    if low:
        print(f"  🔵 Low: {len(low)}")

    if all_issues:
        print(f"\n{'=' * 60}\nIssues:\n")
        for issue in sorted(
            all_issues,
            key=lambda x: {"critical": 0, "high": 1, "medium": 2, "low": 3}[x["severity"]],
        ):
            print(f"  [{issue['severity'].upper():8s}] {issue['file']}:{issue['line']}")
            print(f"           {issue['message']}")
            print(f"           Match: {issue['match']}\n")

    # Exit with error code based on severity
    if critical:
        print("❌ Critical issues found. PR cannot be merged.")
        sys.exit(1)
    elif high:
        print("⚠️  High severity issues found. Please review.")
        sys.exit(1)
    else:
        print("\n✅ No critical or high severity issues found.")
        sys.exit(0)


if __name__ == "__main__":
    main()
