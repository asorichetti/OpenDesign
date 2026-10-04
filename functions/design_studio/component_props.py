"""
title: OpenDesign Component Props
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesign
version: 0.1.0
"""



# ---------------------------------------------------------------------------
# Props Definition Schema
# ---------------------------------------------------------------------------

# Each template can define props that users can configure
# Props schema: {name: {type, label, default, options, min, max}}

COMPONENT_PROPS = {
    "button": {
        "text": {"type": "string", "label": "Button Text", "default": "Click Me"},
        "variant": {
            "type": "select",
            "label": "Variant",
            "default": "primary",
            "options": ["primary", "secondary", "ghost", "outline"],
        },
        "size": {
            "type": "select",
            "label": "Size",
            "default": "md",
            "options": ["sm", "md", "lg"],
        },
        "disabled": {"type": "boolean", "label": "Disabled", "default": False},
        "icon": {
            "type": "select",
            "label": "Icon",
            "default": "none",
            "options": [
                "none",
                "arrow-right",
                "arrow-left",
                "check",
                "x",
                "download",
                "upload",
                "search",
                "plus",
                "minus",
            ],
        },
    },
    "card": {
        "title": {"type": "string", "label": "Title", "default": "Card Title"},
        "description": {
            "type": "string",
            "label": "Description",
            "default": "Card description goes here.",
        },
        "image_url": {
            "type": "string",
            "label": "Image URL",
            "default": "",
        },
        "button_text": {
            "type": "string",
            "label": "Button Text",
            "default": "Learn More",
        },
        "variant": {
            "type": "select",
            "label": "Style",
            "default": "default",
            "options": ["default", "elevated", "outlined", "ghost"],
        },
    },
    "nav": {
        "brand": {"type": "string", "label": "Brand Name", "default": "Brand"},
        "links": {
            "type": "array",
            "label": "Navigation Links",
            "default": ["Home", "Features", "About", "Contact"],
        },
        "variant": {
            "type": "select",
            "label": "Style",
            "default": "default",
            "options": ["default", "minimal", "glass", "dark"],
        },
        "show_collapse": {
            "type": "boolean",
            "label": "Mobile Menu",
            "default": True,
        },
    },
    "hero": {
        "headline": {
            "type": "string",
            "label": "Headline",
            "default": "Welcome to Our Product",
        },
        "subheadline": {
            "type": "string",
            "label": "Subheadline",
            "default": "Build beautiful products faster than ever.",
        },
        "button_text": {
            "type": "string",
            "label": "Primary Button",
            "default": "Get Started",
        },
        "button_text_secondary": {
            "type": "string",
            "label": "Secondary Button",
            "default": "Learn More",
        },
        "layout": {
            "type": "select",
            "label": "Layout",
            "default": "centered",
            "options": ["centered", "left", "right", "split"],
        },
    },
    "accordion": {
        "items": {
            "type": "array",
            "label": "FAQ Items",
            "default": [
                {"q": "What is this?", "a": "This is a great product."},
                {"q": "How much?", "a": "It's free!"},
                {"q": "How to use?", "a": "Just click around!"},
            ],
        },
        "variant": {
            "type": "select",
            "label": "Style",
            "default": "default",
            "options": ["default", "bordered", "filled"],
        },
    },
    "carousel": {
        "slides": {
            "type": "array",
            "label": "Slides",
            "default": [
                {"title": "Slide 1", "description": "First slide content"},
                {"title": "Slide 2", "description": "Second slide content"},
                {"title": "Slide 3", "description": "Third slide content"},
            ],
        },
        "autoplay": {
            "type": "boolean",
            "label": "Auto-play",
            "default": True,
        },
        "autoplay_interval": {
            "type": "number",
            "label": "Interval (ms)",
            "default": 3000,
            "min": 1000,
            "max": 10000,
        },
        "show_indicators": {
            "type": "boolean",
            "label": "Show Dots",
            "default": True,
        },
    },
    "form": {
        "title": {"type": "string", "label": "Form Title", "default": "Contact Us"},
        "fields": {
            "type": "array",
            "label": "Fields",
            "default": [
                {"name": "name", "label": "Name", "type": "text", "required": True},
                {"name": "email", "label": "Email", "type": "email", "required": True},
                {"name": "message", "label": "Message", "type": "textarea", "required": True},
            ],
        },
        "submit_text": {
            "type": "string",
            "label": "Submit Button",
            "default": "Send Message",
        },
    },
    "tabs": {
        "tabs": {
            "type": "array",
            "label": "Tab Names",
            "default": ["Tab 1", "Tab 2", "Tab 3"],
        },
        "contents": {
            "type": "array",
            "label": "Tab Contents",
            "default": [
                "Content for tab 1",
                "Content for tab 2",
                "Content for tab 3",
            ],
        },
        "variant": {
            "type": "select",
            "label": "Style",
            "default": "default",
            "options": ["default", "underline", "pills", "vertical"],
        },
    },
}


# ---------------------------------------------------------------------------
# Props Renderer
# ---------------------------------------------------------------------------

class PropsRenderer:
    """Render component props configuration UI."""

    @staticmethod
    def render_props_form(template_name: str) -> str:
        """Render props configuration form for a template."""
        props = COMPONENT_PROPS.get(template_name, {})

        if not props:
            return '<div class="od-no-props">No configurable props for this template.</div>'

        # Build form fields
        fields_html = []
        for name, prop in props.items():
            field_html = PropsRenderer._render_field(name, prop)
            fields_html.append(field_html)

        html = f"""<div class="od-props-form">
<style>
.od-props-form {{ padding: 1rem; background: #f8fafc; border-radius: 8px; margin: 1rem 0; }}
.od-props-form h3 {{ margin: 0 0 1rem; font-size: 1rem; color: #1e293b; }}
.od-prop-group {{ margin-bottom: 1rem; }}
.od-prop-label {{ display: block; font-size: 0.875rem; font-weight: 500; color: #475569; margin-bottom: 0.25rem; }}
.od-prop-input {{ width: 100%; padding: 0.5rem; border: 1px solid #e2e8f0; border-radius: 6px; font-size: 0.875rem; }}
.od-prop-input:focus {{ outline: none; border-color: #6366f1; box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1); }}
.od-prop-hint {{ font-size: 0.75rem; color: #94a3b8; margin-top: 0.25rem; }}
.od-apply-btn {{ padding: 0.5rem 1rem; background: #6366f1; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 0.875rem; margin-top: 0.5rem; }}
.od-apply-btn:hover {{ background: #4f46e5; }}
.od-reset-btn {{ padding: 0.5rem 1rem; background: white; color: #475569; border: 1px solid #e2e8f0; border-radius: 6px; cursor: pointer; font-size: 0.875rem; margin-left: 0.5rem; }}
.od-reset-btn:hover {{ background: #f1f5f9; }}
.od-array-item {{ display: flex; gap: 0.5rem; margin-bottom: 0.5rem; align-items: center; }}
.od-array-item input {{ flex: 1; }}
.od-array-item button {{ padding: 0.25rem 0.5rem; background: #ef4444; color: white; border: none; border-radius: 4px; cursor: pointer; }}
.od-add-btn {{ padding: 0.25rem 0.75rem; background: #10b981; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 0.875rem; }}
.od-add-btn:hover {{ background: #059669; }}
</style>
<h3>⚙️ Configure {template_name}</h3>
"""

        for field in fields_html:
            html += field

        html += """
<div style="margin-top: 1rem;">
    <button class="od-apply-btn" onclick="window.parent.postMessage({type: 'od-apply-props', props: getPropsValues()}, '*')">Apply & Preview</button>
    <button class="od-reset-btn" onclick="resetProps()">Reset</button>
</div>
</div>
<script>
function getPropsValues() {
    const values = {};
    document.querySelectorAll('.od-props-form input, .od-props-form select, .od-props-form textarea').forEach(el => {
        if (el.type === 'checkbox') {
            values[el.dataset.prop] = el.checked;
        } else {
            values[el.dataset.prop] = el.value;
        }
    });
    // Collect arrays
    document.querySelectorAll('[data-props-arr]').forEach(container => {
        const propName = container.dataset.propsArr;
        const items = [];
        container.querySelectorAll('.od-array-item input').forEach(input => {
            if (input.value.trim()) items.push(input.value.trim());
        });
        values[propName] = items;
    });
    return values;
}
function resetProps() {
    document.querySelectorAll('.od-props-form input, .od-props-form select, .od-props-form textarea').forEach(el => {
        if (el.type === 'checkbox') {
            el.checked = el.defaultChecked;
        } else {
            el.value = el.defaultValue;
        }
    });
}
</script>
"""

        return html

    @staticmethod
    def _render_field(name: str, prop: dict) -> str:
        """Render a single prop field."""
        prop_type = prop.get("type", "string")
        label = prop.get("label", name)
        default = prop.get("default", "")

        html = f'<div class="od-prop-group" data-prop="{name}">'
        html += f'<label class="od-prop-label">{label}</label>'

        if prop_type == "select":
            options = prop.get("options", [])
            html += '<select class="od-prop-input" data-prop="' + name + '">'
            for opt in options:
                selected = "selected" if opt == default else ""
                html += f'<option value="{opt}" {selected}>{opt}</option>'
            html += "</select>"

        elif prop_type == "boolean":
            checked = "checked" if default else ""
            html += f'<input type="checkbox" class="od-prop-input" data-prop="{name}" {checked}>'

        elif prop_type == "number":
            min_val = prop.get("min", "")
            max_val = prop.get("max", "")
            html += f'<input type="number" class="od-prop-input" data-prop="{name}" value="{default}" {f"min={min_val}" if min_val else ""} {f"max={max_val}" if max_val else ""}>'

        elif prop_type == "array":
            default_items = default if isinstance(default, list) else [default]
            html += '<div class="od-array-container" data-props-arr="' + name + '">'
            for item in default_items:
                if isinstance(item, dict):
                    item_str = item.get("q", item.get("title", ""))
                else:
                    item_str = str(item)
                html += f'<div class="od-array-item"><input type="text" value="{item_str}" placeholder="Item"><button onclick="this.parentElement.remove()">×</button></div>'
            html += '</div><button class="od-add-btn" onclick="this.previousElementSibling.insertAdjacentHTML(\'beforeend\', \'\'\'<div class=\"od-array-item\"><input type=\"text\" placeholder=\"Item\"><button onclick=\"this.parentElement.remove()\">×</button></div>\')">+ Add</button>'

        else:  # string, text
            html_type = "textarea" if len(str(default)) > 50 else "text"
            html += f'<{html_type} class="od-prop-input" data-prop="{name}">{default if html_type == "textarea" else ""}</{html_type}>'

        if prop.get("description"):
            html += f'<div class="od-prop-hint">{prop["description"]}</div>'

        html += "</div>"
        return html

    @staticmethod
    def substitute_props(html: str, props: dict) -> str:
        """Substitute template variables with prop values."""
        result = html

        for name, value in props.items():
            # Convert value to string
            if isinstance(value, bool):
                str_value = "true" if value else "false"
            elif isinstance(value, list):
                str_value = ", ".join(str(v) for v in value)
            else:
                str_value = str(value)

            # Simple substitution patterns
            patterns = [
                (f"{{{{{name}}}}}", str_value),
                (f"{{{{{name.upper()}}}}}", str_value),
                (f'{{{{{name.capitalize()}}}}}', str_value),
            ]

            for pattern, replacement in patterns:
                result = result.replace(pattern, replacement)

        return result

    @staticmethod
    def get_props_for_template(template_name: str) -> dict:
        """Get props definition for a template."""
        return COMPONENT_PROPS.get(template_name, {})
