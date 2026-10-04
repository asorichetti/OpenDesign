# Security Policy

## Overview

OpenDesign takes security seriously. This document outlines our security practices, threat model, and how to report vulnerabilities.

## Security Features

### 1. iframe Sandboxing

All user-generated HTML previews render in strictly sandboxed iframes:

```html
<iframe 
  srcdoc="..." 
  sandbox="allow-scripts allow-same-origin allow-forms"
  referrerpolicy="no-referrer"
>
</iframe>
```

**Allowed:**
- `allow-scripts` - JavaScript execution
- `allow-same-origin` - CSS access to parent context
- `allow-forms` - Form submission

**Not Allowed:**
- `allow-popups` - No popups or new windows
- `allow-modals` - No alerts/prompts/confirm
- `allow-top-navigation` - Can't break out of iframe

### 2. HTML Sanitization

Generated HTML is sanitized before rendering. Dangerous patterns are removed:

```python
SANITIZE_PATTERNS = [
    r'form\s+action\s*=\s*["\'][^"\']*["\']',  # Form actions to external URLs
    r'on\w+\s*=\s*["\'][^"\']*["\']',  # Inline event handlers (onclick, etc.)
    r'href\s*=\s*["\']javascript:[^"\']*["\']',  # JavaScript: URIs
    r"\beval\s*\(",  # eval() calls
]
```

### 3. Template Validation

Community templates are validated before storage:

```python
DANGEROUS_PATTERNS = [
    r"\bimport\s+",  # Python imports
    r"\bfrom\s+import\s+",  # Python from imports
    r"\beval\s*\(",  # eval calls
    r"\bexec\s*\(",  # exec calls
    r"\bcompile\s*\(",  # compile calls
    r"__import__",  # Dynamic imports
    r"os\.system",  # System calls
    r"subprocess\.",  # Subprocess execution
    r"socket\.",  # Network sockets
    r'http://(?!localhost|127\.0\.0\.1)[^\s"\']+',  # Insecure HTTP URLs
    r"javascript\s*:",  # JavaScript URIs
    r"\bon\w+\s*=\s*['\"]",  # Inline event handlers
]
```

### 4. No External Resources

Templates cannot load external resources:
- No external script sources (`<script src="...">`)
- No external stylesheets (`<link href="...">`)
- No external iframe sources (`<iframe src="...">`)
- No external form actions (`<form action="...">`)

### 5. File-based Storage

All user data is stored locally:
- Design files: `<data_dir>/opendesign/designs/<user_id>/<design_id>/`
- Templates: `<data_dir>/opendesign/community_templates/<user_id>/<slug>/`
- Metadata: `history.json` and `manifest.json` files

## Threat Model

### Threats We Mitigate

| Threat | Mitigation |
|--------|-----------|
| XSS via generated HTML | iframe sandboxing + HTML sanitization |
| Malicious template injection | Template validation + dangerous pattern scanning |
| Data exfiltration | No external resource loading |
| Privilege escalation | Strict iframe sandbox |
| Stored XSS | Sanitization on both input and output |

### Threats We Don't Mitigate

| Threat | Reason |
|--------|--------|
| LLM prompt injection | Responsibility of LLM provider |
| Open WebUI API security | Handled by Open WebUI |
| Network-level attacks | Responsibility of deployment infrastructure |

## Dependencies

We use minimal dependencies:

```
jinja2        # Template rendering
aiohttp       # Async HTTP client
pydantic      # Configuration validation
```

All dependencies are audited regularly:
```bash
pip audit
```

## Security Configuration

### Valves Configuration

```python
class Valves:
    data_directory: str = "/path/to/data"  # Local storage path
    allowed_origins: list[str] = ["*"]  # CORS origins (default: all)
    max_template_size: int = 50_000  # Max template size in bytes
    sanitize_level: str = "strict"  # Sanitization level
```

### Strict Mode

Enable strict sanitization:
```python
pipe.valves.sanitize_level = "strict"
```

This enables:
- Removal of ALL inline event handlers
- Removal of ALL external resource references
- Removal of ALL iframe elements
- Removal of ALL script tags (CSS-only mode)

### Custom Sanitization Rules

You can add custom sanitization rules:
```python
# Add to SANITIZE_PATTERNS in design_studio.py
CUSTOM_PATTERNS = [
    r"<style[^>]*>.*?</style>",  # Remove all styles
    r"<script[^>]*>.*?</script>",  # Remove all scripts
]
```

## Reporting Vulnerabilities

### How to Report

1. **Email**: security@opendesign.dev
2. **GitHub**: Use GitHub Security Advisories
3. **Discord**: Private message to maintainers

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)
- Your contact information

### What to Expect

- **Acknowledgment**: Within 48 hours
- **Assessment**: Within 1 week
- **Fix**: Within 2 weeks for critical issues
- **Disclosure**: Coordinated with reporter

### Bug Bounty

We currently don't offer a bug bounty program, but we do:
- Credit reporters in release notes
- Provide swag for significant findings
- Prioritize your issues

## Security Updates

### Update Frequency

- **Critical**: Within 24 hours
- **High**: Within 1 week
- **Medium**: Next release
- **Low**: Best effort

### Update Process

1. Vulnerability discovered and assessed
2. Fix developed and tested
3. Security advisory written
4. Update released
5. Notification sent to users

### Checking for Updates

```bash
# Check for dependency updates
pip list --outdated

# Check for security vulnerabilities
pip audit

# Check template security
python scripts/check_security.py
```

## Compliance

### GDPR

OpenDesign is designed to be GDPR-compliant by default:
- All data stored locally
- No data collection or telemetry
- User data easily deletable
- No third-party data sharing

### Privacy

- No analytics or tracking
- No data sent to external servers
- All processing happens locally
- User controls all data

## Audit Log

### Security Events

The following events are logged to stderr:
- Template validation failures
- Sanitization actions
- Storage errors
- Authentication failures (if enabled)

### Log Configuration

```python
import logging

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
```

## Best Practices

### For Users

1. **Keep Updated**: Always use the latest version
2. **Secure Deployment**: Use HTTPS, secure passwords
3. **Trust Templates**: Only use templates from trusted sources
4. **Review Code**: Inspect generated HTML before viewing
5. **Backup Data**: Regular backups of design files

### For Contributors

1. **Code Review**: All changes require review
2. **Security Testing**: Run security scans before committing
3. **Dependencies**: Keep dependencies minimal and updated
4. **Documentation**: Document security decisions
5. **Fail Securely**: Default to denying access

### For Deployers

1. **Isolate**: Run in a container/VM
2. **Firewall**: Limit network access
3. **Update**: Regular security updates
4. **Monitor**: Watch for suspicious activity
5. **Backup**: Regular data backups

## Incident Response

### In Case of a Security Incident

1. **Contain**: Isolate the affected system
2. **Assess**: Determine scope and impact
3. **Notify**: Contact the team and affected users
4. **Fix**: Deploy security patch
5. **Review**: Analyze and improve

### Contact

- **Primary**: security@opendesign.dev
- **Secondary**: GitHub Security Advisories
- **Emergency**: Discord DM to @asorichetti

## License

MIT License - See [LICENSE](../LICENSE) for details.

**Last Updated**: 2024-01-15
