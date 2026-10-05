# Troubleshooting FAQ

## Installation Issues

### "OpenWebUI data directory not found"

**Cause**: OpenDesigner can't find the OpenWebUI data directory.

**Solution**:

1. Find your data directory:
   ```bash
   # Docker
   docker inspect openwebui | grep -A 5 Mounts
   
   # Native install
   echo $OPENWEBUI_DATA_DIR
   # or check your config
   cat /path/to/openwebui/config.json
   ```

2. Set the data directory in valves:
   ```python
   pipe.valves.data_directory = "/path/to/your/openwebui/data"
   ```

3. Or use the installer script:
   ```bash
   ./install-opendesigner.sh /path/to/openwebui/data
   ```

### "Plugin not appearing in OpenWebUI"

**Cause**: Plugin not properly registered or OpenWebUI not restarted.

**Solution**:

1. Check plugin structure:
   ```
   plugins/opendesigner/
   ├── plugin.json
   ├── functions/
   │   ├── design_studio.py
   │   ├── preview_generator.py
   │   └── prompt_enhancer.py
   └── assets/
   ```

2. Verify plugin.json:
   ```json
   {
     "name": "OpenDesigner Studio",
     "slug": "opendesigner",
     "version": "0.2.0",
     "functions": [...]
   }
   ```

3. Restart OpenWebUI:
   ```bash
   docker restart openwebui
   # or
   systemctl restart openwebui
   ```

### Docker Container Won't Start

**Cause**: Port conflict or volume permission issues.

**Solution**:

1. Check ports:
   ```bash
   lsof -i :3000  # OpenWebUI default port
   ```

2. Fix permissions:
   ```bash
   mkdir -p /path/to/openwebui/data
   chmod 755 /path/to/openwebui/data
   ```

3. Rebuild:
   ```bash
   cd docker
   docker-compose down
   docker-compose up --build
   ```

## Generation Issues

### "LLM API timeout"

**Cause**: Model taking too long to generate.

**Solution**:

1. Use a faster model:
   ```python
   # In OpenWebUI settings
   # Switch from "claude-3.5-sonnet" to "gpt-4o-mini"
   ```

2. Simplify your prompt:
   - Be specific about scope
   - Use smaller templates
   - Avoid "create everything" requests

3. Check API connectivity:
   ```bash
   curl -X POST http://localhost:11434/api/chat \
     -H "Content-Type: application/json" \
     -d '{"model": "llama3", "messages": [{"role": "user", "content": "hi"}]}'
   ```

### "No HTML code block found"

**Cause**: LLM didn't include HTML in its response.

**Solution**:

1. Be explicit:
   ```
   Instead of: "Create a landing page"
   Use: "Create a landing page. Include the full HTML in a ```html code block."
   ```

2. Check LLM model:
   - Some models are better at code generation
   - Try gpt-4o or claude-3.5-sonnet

3. Use templates:
   ```
   Use the hero template to create a landing page
   ```

### "HTML sanitization removed my code"

**Cause**: Your HTML contains patterns flagged as dangerous.

**Solution**:

1. Avoid these patterns:
   ```html
   <!-- BAD -->
   <div onclick="alert('hi')">Click me</div>
   <a href="javascript:void(0)">Link</a>
   <form action="https://evil.com">...</form>
   
   <!-- GOOD -->
   <div id="my-button">Click me</div>
   <a href="/page">Link</a>
   <form action="/submit">...</form>
   ```

2. Use event delegation:
   ```html
   <!-- Instead of onclick, use ID and handle in JS -->
   <script>
   document.getElementById('my-button').addEventListener('click', () => {
     alert('hi');
   });
   </script>
   ```

### "Preview not rendering"

**Cause**: Sandbox blocking content or invalid HTML.

**Solution**:

1. Check browser console for errors
2. Validate HTML:
   ```bash
   python -c "from html.parser import HTMLParser; HTMLParser().feed(open('template.html').read())"
   ```
3. Ensure no external resources
4. Check iframe sandbox settings

## Template Issues

### "Template not found"

**Cause**: Template path incorrect or file missing.

**Solution**:

1. List available templates:
   ```python
   from functions.design_studio.design_studio import Pipe

   pipe = Pipe()
   print(pipe.list_templates())
   ```

2. Check template exists:
   ```bash
   ls functions/design_studio/templates/
   ```

3. Use correct path format:
   ```
   Correct: "landing/hero"
   Wrong:   "templates/landing/hero"
   ```

### "Template validation failed"

**Cause**: Template contains forbidden patterns.

**Solution**:

1. Run validation:
   ```bash
   python scripts/check_security.py functions/design_studio/templates/your-template.html
   ```

2. Common issues:
   - External script sources
   - Inline event handlers
   - eval/exec calls
   - Form actions to external URLs

3. Fix and re-test:
   ```bash
   python scripts/check_security.py functions/design_studio/templates/your-template.html
   ```

## Marketplace Issues

### "Can't import template from URL"

**Cause**: URL unreachable or invalid content type.

**Solution**:

1. Check URL accessibility:
   ```bash
   curl -I https://example.com/template.html
   ```

2. Ensure content type is text/html

3. Try raw URL:
   ```
   https://raw.githubusercontent.com/...
   ```

### "Template submission rejected"

**Cause**: Template failed validation.

**Solution**:

1. Check error message from rejection
2. Common issues:
   - Contains `import` or `from import`
   - Contains `eval` or `exec`
   - External resource references
3. Remove dangerous patterns and resubmit

## Performance Issues

### "Slow generation"

**Cause**: LLM model performance or large templates.

**Solution**:

1. Use faster models:
   ```
   gpt-4o-mini > gpt-4o > claude-3.5-sonnet
   ```

2. Use smaller templates:
   - Component templates > Full page templates
   - Reuse existing templates

3. Cache templates:
   ```python
   # Templates are cached automatically
   # Check cache hits in logs
   ```

### "Memory issues"

**Cause**: Large HTML responses or many concurrent requests.

**Solution**:

1. Limit template size:
   ```python
   pipe.valves.max_template_size = 50000  # 50KB
   ```

2. Reduce concurrent requests
3. Use streaming mode
4. Monitor memory usage:
   ```bash
   htop
   docker stats
   ```

## Debug Mode

### Enable Debug Logging

```python
import logging

logging.getLogger("opendesigner").setLevel(logging.DEBUG)
```

### Check Valves Configuration

```python
from functions.design_studio.design_studio import Pipe

pipe = Pipe()
print(vars(pipe.valves))
```

### Test Template Loading

```python
from functions.design_studio.design_studio import Pipe

pipe = Pipe()
template = pipe.load_template("landing/hero")
print(template[:200])  # First 200 chars
```

### Validate HTML Output

```python
from html.parser import HTMLParser


class HTMLValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []

    def error(self, message):
        self.errors.append(message)


validator = HTMLValidator()
try:
    validator.feed(your_html)
    print("HTML is valid!")
except Exception as e:
    print(f"HTML error: {e}")
```

## Common Error Messages

### "ModuleNotFoundError: No module named 'jinja2'"

**Solution**:
```bash
pip install jinja2 aiohttp pydantic
```

### "Permission denied: /path/to/data"

**Solution**:
```bash
sudo chown -R $(whoami) /path/to/data
chmod -R u+rwX /path/to/data
```

### "Connection refused: localhost:11434"

**Solution**:
```bash
# Check Ollama is running
ollama serve

# Or restart
systemctl restart ollama
```

### "Template syntax error"

**Solution**:
- Check Jinja2 syntax: `{{ variable }}`
- No Python expressions allowed
- Only simple variable substitution

## Getting Help

### Before Asking for Help

1. **Check logs**: Look for error messages
2. **Verify versions**: Use latest OpenDesigner version
3. **Test basic case**: Try "Create a button"
4. **Read docs**: Check API.md and INSTALL.md

### Where to Get Help

- **GitHub Issues**: [opendesigner/issues](https://github.com/asorichetti/OpenDesigner/issues)
- **GitHub Discussions**: [opendesigner/discussions](https://github.com/asorichetti/OpenDesigner/discussions)
- **Email**: support@opendesigner.dev

### What to Include

```markdown
## Environment
- OpenDesigner version: 0.2.0
- OpenWebUI version: 0.5.0
- Python version: 3.12.0
- Deployment: Docker/Native

## Steps to Reproduce
1. ...
2. ...
3. ...

## Expected Behavior
...

## Actual Behavior
...

## Error Message
...

## Screenshots
...
```

## Quick Fixes

| Issue | Quick Fix |
|-------|----------|
| Plugin not showing | Restart OpenWebUI |
| Generation slow | Switch to faster model |
| Template validation failed | Remove inline event handlers |
| Docker won't start | Check port conflicts |
| Data directory error | Set `data_directory` in valves |
| HTML sanitized | Remove dangerous patterns |
| Import failed | Use raw URL |

## Advanced Troubleshooting

### Manual Function Testing

```python
# Test design_studio
python -c "
from functions.design_studio.design_studio import Pipe
pipe = Pipe()
async def test():
    async for msg in pipe.stream([{'role': 'user', 'content': 'Create a button'}]):
        print(msg)
import asyncio
asyncio.run(test())
"
```

### Template Isolation Test

```python
# Test template in isolation
python -c "
from jinja2 import Template
t = Template('{{ title }}')
print(t.render(title='Test'))
"
```

### Security Scan

```bash
# Full security scan
python scripts/check_security.py

# Template validation
python scripts/validate_templates.py

# Run all checks
make check
```

---

**Still having issues?** [Create a GitHub Issue](https://github.com/asorichetti/OpenDesigner/issues) with the troubleshooting template above.
