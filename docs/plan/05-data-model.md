# Data Model

## Storage Strategy

OpenDesigner uses **file-based storage** within Open WebUI's data directory. No separate database required.

## Directory Structure

```
<openwebui_data_dir>/opendesigner/
├── designs/                    # User design files
│   ├── <user_id>/
│   │   ├── <design_id>.json    # Design metadata + history
│   │   └── <design_id>/
│   │       ├── v1.html         # Version 1 HTML
│   │       ├── v2.html         # Version 2 HTML
│   │       └── history.json    # Version metadata
│   └── <user_id_2>/
│       └── ...
├── templates/                  # User custom templates
│   └── <user_id>/
│       └── ...
└── settings/                   # User settings
    └── <user_id>.json
```

## Design JSON Schema

```json
{
  "id": "design_01J8K3M2N4P5Q6R7S8T9U0V1W2",
  "user_id": "user_abc123",
  "title": "Coffee Shop Landing Page",
  "prompt": "Create a landing page for a specialty coffee shop called Bean & Brew...",
  "output_type": "landing",
  "template": "landing/hero",
  "design_system": "light",
  "model": "gpt-4o",
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:45:00Z",
  "versions": [
    {
      "version": 1,
      "prompt": "Create a landing page for a specialty coffee shop...",
      "html_path": "v1.html",
      "created_at": "2025-01-15T10:30:00Z",
      "diff_summary": "Initial generation"
    },
    {
      "version": 2,
      "prompt": "Make the hero section darker and change the button to green",
      "html_path": "v2.html",
      "created_at": "2025-01-15T10:45:00Z",
      "diff_summary": "Changed hero bg to #1a1a2b, button color to #16a34a"
    }
  ],
  "tags": ["landing-page", "food-beverage", "responsive"]
}
```

## Settings JSON Schema

```json
{
  "user_id": "user_abc123",
  "default_template": "landing/hero",
  "default_design_system": "light",
  "auto_preview": true,
  "preferred_model": "gpt-4o",
  "favorite_templates": ["landing/hero", "presentation/blank"],
  "custom_css": "",
  "editor_theme": "light"
}
```

## Design System Presets

Each preset is a CSS file with custom properties:

```css
/* assets/light.css */
:root {
  --od-color-bg-primary: #FFFFFF;
  --od-color-bg-secondary: #F7F7F8;
  --od-color-text-primary: #1A1A1A;
  --od-color-text-secondary: #6B6B6B;
  --od-color-accent: #737373;
  --od-color-border: #E0E0E0;
  --od-font-family: system-ui, -apple-system, sans-serif;
  --od-font-size-base: 16px;
  --od-spacing-unit: 8px;
}
```

## No-DB Fallback

If Open WebUI's data directory is not configured:
- Designs are stored in memory only
- Preview still works
- No version history
- Settings use defaults
- Pipe logs a warning but continues
