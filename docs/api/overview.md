# API Overview

Complete API reference for OpenDesigner plugin functions.

---

## 📚 Table of Contents

- [Plugin Functions](#plugin-functions)
- [Pipe Functions](#pipe-functions)
- [Action Functions](#action-functions)
- [Filter Functions](#filter-functions)
- [Custom Events](#custom-events)
- [Example Usage](#example-usage)

---

## Plugin Functions

OpenDesigner provides 35 plugin functions organized into 4 phases:

### Phase 1: Foundation
- `design_iteration.py` — AI Design Iteration Engine
- `customization_panel.py` — Visual Customization Panel
- `seo_optimizer.py` — SEO Optimization Engine

### Phase 2: Polish
- `responsive_preview.py` — Responsive Preview Studio
- `framework_export.py` — Framework Export
- `component_variants.py` — Component Variants & States

### Phase 3: Advanced
- `multi_page.py` — Multi-Page Website Generator
- `design_system.py` — Design System Manager
- `ai_images.py` — AI Image Generation Integration
- `ab_testing.py` — A/B Testing Mode

### Phase 4: Enterprise
- `analytics.py` — Design Analytics
- `figma_export.py` — Export to Figma
- `perf_scoring.py` — Performance Scoring
- `design_to_code.py` — Design-to-Code AI

---

## Pipe Functions

Pipe functions intercept and process chat messages.

### designer_studio.py

**Purpose:** Main design generation pipe function.

**Methods:**
- `__call__()` — Main entry point for design generation
- `_detect_intent()` — Detect design-related prompts
- `_load_template()` — Load design template
- `_construct_prompt()` — Build LLM prompt
- `_generate_html()` — Generate HTML code
- `_sanitize_html()` — Sanitize generated HTML

**Example:**
```python
from designer_studio import DesignStudio

studio = DesignStudio()
result = await studio()
```

---

## Action Functions

Action functions provide interactive UI elements.

### preview_generator.py

**Purpose:** Preview, export, and editor actions.

**Actions:**
- `Preview` — Render design preview
- `Export HTML` — Export as HTML
- `Open Editor` — Open live editor
- `Compare Models` — Compare model outputs
- `AI Prompt Generator` — Generate recreation prompts

**Example:**
```python
from preview_generator import PreviewGenerator

generator = PreviewGenerator()
actions = generator.actions()
```

---

## Filter Functions

Filter functions enhance prompts before processing.

### prompt_enhancer.py

**Purpose:** Enhance design prompts with guidelines and metadata.

**Methods:**
- `__call__()` — Main filter entry point
- `_enhance_prompt()` — Add design guidelines
- `_add_metadata()` — Include design metadata

**Example:**
```python
from prompt_enhancer import PromptEnhancer

enhancer = PromptEnhancer()
enhanced = await enhancer(prompt)
```

---

## Custom Events

OpenDesigner uses custom events for communication.

### Event Types

| Event | Description | Payload |
|-------|-------------|---------|
| `designIteration` | Design iteration request | `{ prompt, changes }` |
| `designAdjustments` | Quick adjustments | `{ type, value }` |
| `applyCustomizations` | Apply customization | `{ colors, fonts, spacing }` |
| `selectTheme` | Theme selection | `{ theme }` |
| `selectLayout` | Layout selection | `{ layout }` |
| `selectDevice` | Device selection | `{ device }` |
| `addPage` | Add new page | `{ name, url, type }` |
| `generateImage` | Image generation | `{ prompt, style }` |
| `exportToFigma` | Figma export | `{ token }` |
| `generateCode` | Design-to-code | `{ framework }` |

### Event Usage

```javascript
// Dispatch custom event
const event = new CustomEvent('designIteration', {
    detail: {
        prompt: "Make it more modern",
        changes: { theme: "dark" }
    }
});
window.parent.postMessage(event, '*');

// Listen for custom event
window.addEventListener('designIteration', (event) => {
    console.log('Design iteration:', event.detail);
});
```

---

## Example Usage

### Basic Design Generation

```python
# Generate a landing page
prompt = "Create a modern landing page for a SaaS product"
result = await designer_studio(prompt)
```

### Customization

```python
# Customize design
customizations = {
    "colors": {"primary": "#6366f1", "secondary": "#10b981"},
    "fonts": {"heading": "Inter, sans-serif", "body": "Inter, sans-serif"},
    "spacing": {"borderRadius": "12px", "padding": "2rem"},
}
await customization_panel(customizations)
```

### Export to Framework

```python
# Export to React
export = await framework_export(
    framework="react", options={"cssModules": True, "responsive": True, "animations": False}
)
```

### SEO Optimization

```python
# Optimize for SEO
seo = await seo_optimizer(
    title="My Product - Best Solution",
    description="Discover our amazing product",
    author="Company Name",
    canonical="https://example.com",
)
```

---

## Security

All actions follow strict security guidelines:

- ✅ **Iframe Sandboxing** — All previews in sandboxed iframes
- ✅ **No External URLs** — Inline CSS/JS only
- ✅ **No eval()** — Code execution blocked
- ✅ **HTML Sanitization** — All generated HTML sanitized
- ✅ **No Credentials** — No hardcoded secrets

---

## Error Handling

All functions include comprehensive error handling:

```python
try:
    result = await action()
except Exception as e:
    # Handle error gracefully
    return f"Error: {str(e)}"
```

---

## Testing

All functions are tested with 52 unit tests:

```bash
# Run all tests
python3 -m pytest tests/test_opendesigner.py

# Run specific test
python3 -m pytest tests/test_opendesigner.py::TestIntentDetection::test_design_keywords_detected

# Run with coverage
python3 -m pytest tests/test_opendesigner.py --cov=functions
```

---

## Additional Resources

- [Plugin Development](./plugin-development.md)
- [Templates](./templates.md)
- [Security Guide](../security/overview.md)
