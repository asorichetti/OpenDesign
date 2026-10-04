# Contributing to OpenDesign

Thank you for your interest in contributing to OpenDesign! This guide will help you get started.

## Code of Conduct

Be respectful, inclusive, and constructive. Harassment of any kind will not be tolerated.

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+ (for template development)
- Open WebUI instance (for testing)

### Development Setup

```bash
# Clone the repository
git clone https://github.com/asorichetti/OpenDesign.git
cd OpenDesign

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .[dev]

# Run tests
pytest tests/ -v

# Run linting
ruff check .
ruff format --check .
```

## Project Structure

```
OpenDesign/
├── functions/
│   ├── design_studio/           # Core generation engine
│   │   ├── design_studio.py     # Pipe function
│   │   ├── template_marketplace.py  # Template management
│   │   ├── templates/           # HTML templates
│   │   ├── prompts/             # Prompt templates
│   │   └── assets/              # CSS, images, etc.
│   ├── preview_generator/       # Preview/rendering
│   └── prompt_enhancer/         # Prompt enhancement
├── tests/                       # Test suite
├── docs/                        # Documentation
├── docker/                      # Docker deployment
├── plugins/                     # Plugin distribution
├── scripts/                     # CI/CD scripts
└── demo/                        # Interactive demo
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout main
git pull origin main
git checkout -b feat/your-feature-name
```

### 2. Make Your Changes

Follow the existing code style:
- Use type hints
- Write docstrings for all functions
- Keep functions small and focused
- Add tests for new functionality

### 3. Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_opendesign.py -v

# Run with coverage
pytest tests/ --cov=functions --cov-report=html
```

### 4. Check Code Quality

```bash
# Linting
ruff check .

# Formatting
ruff format .

# Security scan
python scripts/check_security.py

# Template validation
python scripts/validate_templates.py
```

### 5. Commit and Push

```bash
git add .
git commit -m "feat: add your feature description"
git push origin feat/your-feature-name
```

### 6. Create a Pull Request

```bash
gh pr create --base main --head feat/your-feature-name
```

## Template Development

### Template Guidelines

1. **Use Design Tokens** - Reference CSS variables from `design-tokens.css`
2. **Responsive Design** - Use flexbox/grid, media queries
3. **Accessibility** - Include ARIA labels, semantic HTML
4. **No External Dependencies** - All CSS/JS must be inline
5. **No eval() or Dangerous Patterns** - Security first
6. **Use {{ variables }}** - For dynamic content

### Template Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        /* Use design tokens */
        :root {
            --color-primary: var(--od-color-primary);
        }
        /* Your styles here */
    </style>
</head>
<body>
    <main>
        {{ content }}
    </main>
    <script>
        // Your JS here
    </script>
</body>
</html>
```

### Testing Templates

```bash
# Validate template syntax
python scripts/validate_templates.py functions/design_studio/templates/your-template.html

# Check for security issues
python scripts/check_security.py functions/design_studio/templates/your-template.html
```

## Adding New Functions

### Creating a Pipe Function

```python
# functions/my_pipe/my_pipe.py
"""
title: My Pipe Function
version: 0.1.0
"""

from collections.abc import AsyncIterator


class Pipe:
    type = "pipe"
    name = "My Pipe"

    def __init__(self):
        self.valves = Valves()

    async def stream(
        self, messages: list, __user__: dict | None = None, **kwargs
    ) -> AsyncIterator[str]:
        # Your logic here
        yield "Hello from My Pipe!"


class Valves:
    # Configuration options
    pass
```

### Creating an Action Function

```python
# functions/my_action/my_action.py
"""
title: My Action Function
version: 0.1.0
"""


class Action:
    type = "action"

    def __init__(self):
        pass

    def actions(self) -> list[dict]:
        return [
            {
                "name": "My Action",
                "description": "Does something cool",
                "icon": "star",
            }
        ]

    async def action(self, action: str, body: dict, __user__: dict | None = None, **kwargs) -> str:
        if action == "My Action":
            return "Action completed!"
        return f"Unknown action: {action}"
```

### Creating a Filter Function

```python
# functions/my_filter/my_filter.py
"""
title: My Filter Function
version: 0.1.0
"""


class Filter:
    type = "filter"

    def inlet(self, body: dict, __user__: dict | None = None, **kwargs) -> dict:
        # Modify messages
        messages = body.get("messages", [])
        # ... your logic ...
        body["messages"] = messages
        return body
```

## Testing Guidelines

### Writing Tests

```python
class TestYourFeature:
    def test_something(self):
        """Test description."""
        from functions.your_module import YourClass
        
        obj = YourClass()
        result = obj.method()
        assert result == expected
```

### Test Categories

- **Unit Tests** - Test individual functions
- **Integration Tests** - Test function interactions
- **Security Tests** - Test sanitization/validation

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific category
pytest tests/ -v -k "test_template"

# With coverage
pytest tests/ --cov=functions
```

## CI/CD Pipeline

The CI pipeline includes:

1. **Lint & Format** - ruff checks
2. **Unit Tests** - pytest on Python 3.11, 3.12, 3.13
3. **Security Scan** - Custom security checker
4. **Template Validation** - Template syntax validation
5. **HTML Sanitization** - XSS pattern detection
6. **Merge Gate** - All checks must pass

## Documentation

### Writing Documentation

- Use Markdown format
- Include code examples
- Add screenshots for UI changes
- Update README for user-facing changes

### Documentation Structure

```
docs/
├── API.md               # API reference
├── INSTALL.md           # Installation guide
├── CONTRIBUTING.md      # This file
├── SECURITY.md          # Security policy
└── plan/                # Project planning docs
```

## Releasing

### Version Bumping

```bash
# Bump version in:
# - pyproject.toml
# - functions/*/plugin.json (if applicable)
# - README.md

git tag v0.2.0
git push origin v0.2.0
```

### Publishing to Open WebUI

1. Create a release on GitHub
2. Upload plugin.zip to the release assets
3. Update the community plugin index

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/asorichetti/OpenDesign/issues)
- **Discussions**: [GitHub Discussions](https://github.com/asorichetti/OpenDesign/discussions)
- **Email**: [OpenDesign Contributors](mailto:contributors@opendesign.dev)

## Thank You!

Every contribution helps make OpenDesign better. We appreciate your time and effort! 🎉
