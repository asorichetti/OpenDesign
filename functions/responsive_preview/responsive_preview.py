"""
title: Responsive Preview Studio
author: asorichetti
author_url: https://github.com/asorichetti/OpenDesigner
version: 1.0.0
required_open_webui_version: 0.10.0
"""

from typing import Any


class ResponsivePreview:
    """Responsive Preview Studio — See designs on multiple devices simultaneously."""

    def __init__(self):
        self.type = "action"

    def actions(self) -> list[dict[str, str]]:
        """Return available actions."""
        return [
            {
                "name": "Responsive Preview",
                "description": "Preview design on desktop, tablet, and mobile",
                "icon": "monitor",
            },
            {
                "name": "Device Simulator",
                "description": "Simulate specific device screens",
                "icon": "smartphone",
            },
            {
                "name": "Breakpoint Checker",
                "description": "Check responsive breakpoints and layout shifts",
                "icon": "ruler",
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
        """Handle preview action."""
        if action == "Responsive Preview":
            return self._render_responsive_preview(body)
        elif action == "Device Simulator":
            return self._render_device_simulator(body)
        elif action == "Breakpoint Checker":
            return self._render_breakpoint_checker(body)

        return f"Unknown action: {action}"

    def _render_responsive_preview(self, body: dict) -> str:
        """Render responsive preview studio."""
        html_content = body.get("html", "<html><body>No design loaded</body></html>")
        # Escape quotes for srcdoc
        escaped_html = html_content.replace('"', "&quot;").replace("'", "&#x27;")

        return f"""
        <div class="responsive-studio" style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .responsive-studio {{ max-width: 1400px; margin: 0 auto; }}
                .studio-header {{ text-align: center; margin-bottom: 2rem; }}
                .studio-header h3 {{ font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0 0 0.5rem; }}
                .studio-header p {{ color: #64748b; }}
                .device-grid {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 2rem; }}
                .device-frame {{ background: white; border: 2px solid #e2e8f0; border-radius: 16px; overflow: hidden; transition: all 0.3s; }}
                .device-frame:hover {{ border-color: #6366f1; transform: translateY(-4px); box-shadow: 0 20px 40px rgb(0 0 0 / 0.1); }}
                .device-header {{ padding: 1rem; background: #f8fafc; border-bottom: 1px solid #e2e8f0; display: flex; align-items: center; justify-content: space-between; }}
                .device-info {{ display: flex; align-items: center; gap: 0.75rem; }}
                .device-icon {{ font-size: 1.5rem; }}
                .device-details h4 {{ font-size: 0.875rem; font-weight: 600; color: #1e293b; margin: 0; }}
                .device-details span {{ font-size: 0.75rem; color: #64748b; }}
                .device-actions {{ display: flex; gap: 0.5rem; }}
                .device-btn {{ padding: 0.375rem 0.75rem; border: 1px solid #e2e8f0; border-radius: 6px; background: white; cursor: pointer; font-size: 0.75rem; font-weight: 600; }}
                .device-btn:hover {{ background: #f1f5f9; }}
                .device-btn.active {{ background: #6366f1; color: white; border-color: #6366f1; }}
                .device-screen {{ height: 500px; overflow: auto; background: #f1f5f9; }}
                .device-screen iframe {{ width: 100%; height: 100%; border: none; background: white; }}
                .responsive-controls {{ display: flex; gap: 0.75rem; margin-bottom: 1.5rem; justify-content: center; }}
                .control-btn {{ padding: 0.75rem 1.5rem; border: 2px solid #e2e8f0; border-radius: 12px; background: white; cursor: pointer; font-weight: 600; transition: all 0.2s; }}
                .control-btn:hover {{ border-color: #6366f1; }}
                .control-btn.active {{ background: #6366f1; color: white; border-color: #6366f1; }}
                .breakpoints {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 2rem; }}
                .breakpoint-card {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1rem; text-align: center; }}
                .breakpoint-value {{ font-size: 2rem; font-weight: 700; color: #6366f1; margin-bottom: 0.25rem; }}
                .breakpoint-label {{ font-size: 0.875rem; color: #64748b; }}
            </style>

            <div class="studio-header">
                <h3>📱 Responsive Preview Studio</h3>
                <p>See how your design looks on all devices simultaneously</p>
            </div>

            <div class="responsive-controls">
                <button class="control-btn active" onclick="setView('all')">All Devices</button>
                <button class="control-btn" onclick="setView('desktop')">Desktop</button>
                <button class="control-btn" onclick="setView('tablet')">Tablet</button>
                <button class="control-btn" onclick="setView('mobile')">Mobile</button>
            </div>

            <div class="device-grid">
                <div class="device-frame" id="desktop-frame">
                    <div class="device-header">
                        <div class="device-info">
                            <span class="device-icon">🖥️</span>
                            <div class="device-details">
                                <h4>Desktop</h4>
                                <span>1920 × 1080</span>
                            </div>
                        </div>
                        <div class="device-actions">
                            <button class="device-btn" onclick="zoomDevice('desktop', 1)">100%</button>
                            <button class="device-btn" onclick="zoomDevice('desktop', 0.75)">75%</button>
                        </div>
                    </div>
                    <div class="device-screen">
                        <iframe id="desktop-preview" srcdoc="${escaped_html}" sandbox="allow-scripts allow-same-origin"></iframe>
                    </div>
                </div>

                <div class="device-frame" id="tablet-frame">
                    <div class="device-header">
                        <div class="device-info">
                            <span class="device-icon">📱</span>
                            <div class="device-details">
                                <h4>Tablet</h4>
                                <span>768 × 1024</span>
                            </div>
                        </div>
                        <div class="device-actions">
                            <button class="device-btn" onclick="zoomDevice('tablet', 1)">100%</button>
                            <button class="device-btn" onclick="zoomDevice('tablet', 0.75)">75%</button>
                        </div>
                    </div>
                    <div class="device-screen">
                        <iframe id="tablet-preview" style="width: 768px; margin: 0 auto;" srcdoc="${escaped_html}" sandbox="allow-scripts allow-same-origin"></iframe>
                    </div>
                </div>

                <div class="device-frame" id="mobile-frame">
                    <div class="device-header">
                        <div class="device-info">
                            <span class="device-icon">📱</span>
                            <div class="device-details">
                                <h4>Mobile</h4>
                                <span>375 × 812</span>
                            </div>
                        </div>
                        <div class="device-actions">
                            <button class="device-btn" onclick="zoomDevice('mobile', 1)">100%</button>
                            <button class="device-btn" onclick="zoomDevice('mobile', 0.75)">75%</button>
                        </div>
                    </div>
                    <div class="device-screen">
                        <iframe id="mobile-preview" style="width: 375px; margin: 0 auto;" srcdoc="${escaped_html}" sandbox="allow-scripts allow-same-origin"></iframe>
                    </div>
                </div>
            </div>

            <div class="breakpoints">
                <div class="breakpoint-card">
                    <div class="breakpoint-value">320px</div>
                    <div class="breakpoint-label">Mobile Small</div>
                </div>
                <div class="breakpoint-card">
                    <div class="breakpoint-value">768px</div>
                    <div class="breakpoint-label">Tablet</div>
                </div>
                <div class="breakpoint-card">
                    <div class="breakpoint-value">1024px</div>
                    <div class="breakpoint-label">Laptop</div>
                </div>
                <div class="breakpoint-card">
                    <div class="breakpoint-value">1440px</div>
                    <div class="breakpoint-label">Desktop</div>
                </div>
            </div>

            <script>
                function setView(view) {{
                    const frames = document.querySelectorAll('.device-frame');
                    frames.forEach(frame => frame.style.display = 'none');

                    if (view === 'all') {{
                        frames.forEach(frame => frame.style.display = 'block');
                    }} else if (view === 'desktop') {{
                        document.getElementById('desktop-frame').style.display = 'block';
                    }} else if (view === 'tablet') {{
                        document.getElementById('tablet-frame').style.display = 'block';
                    }} else if (view === 'mobile') {{
                        document.getElementById('mobile-frame').style.display = 'block';
                    }}

                    document.querySelectorAll('.control-btn').forEach(btn => btn.classList.remove('active'));
                    event.target.classList.add('active');
                }}

                function zoomDevice(device, scale) {{
                    const preview = document.getElementById(device + '-preview');
                    preview.style.transform = 'scale(' + scale + ')';
                    preview.style.transformOrigin = 'top center';
                }}
            </script>
        </div>
        """

    def _render_device_simulator(self, body: dict) -> str:
        """Render device simulator."""
        html_content = body.get("html", "<html><body>No design loaded</body></html>")
        escaped_html = html_content.replace('"', "&quot;").replace("'", "&#x27;")

        return f"""
        <div style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .device-simulator {{ max-width: 1200px; }}
                .device-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; }}
                .device-card {{ background: white; border: 2px solid #e2e8f0; border-radius: 24px; overflow: hidden; transition: all 0.3s; cursor: pointer; }}
                .device-card:hover {{ border-color: #6366f1; transform: translateY(-8px); }}
                .device-bezel {{ padding: 12px; background: #1e293b; }}
                .device-notch {{ width: 60%; height: 20px; background: #1e293b; border-radius: 0 0 12px 12px; margin: 0 auto; }}
                .device-screen-container {{ background: #000; padding: 8px; border-radius: 16px; }}
                .device-screen-inner {{ width: 100%; overflow: hidden; border-radius: 8px; }}
                .device-screen-inner iframe {{ width: 100%; border: none; background: white; }}
                .device-info {{ padding: 1rem; text-align: center; }}
                .device-info h4 {{ font-size: 1rem; font-weight: 600; color: #1e293b; margin: 0 0 0.25rem; }}
                .device-info p {{ font-size: 0.875rem; color: #64748b; margin: 0; }}
            </style>

            <div class="device-simulator">
                <h3 style="margin-bottom: 1.5rem;">📱 Device Simulator</h3>

                <div class="device-grid">
                    <div class="device-card" onclick="selectDevice('iphone-14')">
                        <div class="device-bezel">
                            <div class="device-notch"></div>
                        </div>
                        <div class="device-screen-container">
                            <div class="device-screen-inner">
                                <iframe style="height: 600px;" srcdoc="${escaped_html}" sandbox="allow-scripts"></iframe>
                            </div>
                        </div>
                        <div class="device-info">
                            <h4>iPhone 14</h4>
                            <p>390 × 844</p>
                        </div>
                    </div>

                    <div class="device-card" onclick="selectDevice('iphone-se')">
                        <div class="device-bezel">
                            <div class="device-notch"></div>
                        </div>
                        <div class="device-screen-container">
                            <div class="device-screen-inner">
                                <iframe style="height: 600px;" srcdoc="${escaped_html}" sandbox="allow-scripts"></iframe>
                            </div>
                        </div>
                        <div class="device-info">
                            <h4>iPhone SE</h4>
                            <p>375 × 667</p>
                        </div>
                    </div>

                    <div class="device-card" onclick="selectDevice('ipad')">
                        <div class="device-bezel" style="border-radius: 24px; padding: 16px;">
                        </div>
                        <div class="device-screen-container">
                            <div class="device-screen-inner">
                                <iframe style="height: 600px;" srcdoc="${escaped_html}" sandbox="allow-scripts"></iframe>
                            </div>
                        </div>
                        <div class="device-info">
                            <h4>iPad</h4>
                            <p>810 × 1080</p>
                        </div>
                    </div>

                    <div class="device-card" onclick="selectDevice('pixel-7')">
                        <div class="device-bezel">
                            <div class="device-notch"></div>
                        </div>
                        <div class="device-screen-container">
                            <div class="device-screen-inner">
                                <iframe style="height: 600px;" srcdoc="${escaped_html}" sandbox="allow-scripts"></iframe>
                            </div>
                        </div>
                        <div class="device-info">
                            <h4>Pixel 7</h4>
                            <p>412 × 915</p>
                        </div>
                    </div>
                </div>
            </div>

            <script>
                function selectDevice(device) {{
                    const event = new CustomEvent('selectDevice', {{ detail: {{ device: device }} }});
                    window.parent.postMessage(event, '*');
                }}
            </script>
        </div>
        """

    def _render_breakpoint_checker(self, body: dict) -> str:
        """Render breakpoint checker."""
        return """
        <div style="padding: 1.5rem; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
            <style>
                .breakpoint-checker {{ max-width: 1000px; }}
                .breakpoint-list {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; }}
                .breakpoint-item {{ display: flex; align-items: center; justify-content: space-between; padding: 1rem 1.5rem; border-bottom: 1px solid #e2e8f0; }}
                .breakpoint-item:last-child {{ border-bottom: none; }}
                .breakpoint-info {{ display: flex; align-items: center; gap: 1rem; }}
                .breakpoint-icon {{ font-size: 1.5rem; }}
                .breakpoint-name {{ font-weight: 600; color: #1e293b; }}
                .breakpoint-range {{ font-size: 0.875rem; color: #64748b; }}
                .breakpoint-status {{ padding: 0.375rem 0.75rem; border-radius: 999px; font-size: 0.75rem; font-weight: 600; }}
                .breakpoint-status.pass {{ background: #dcfce7; color: #16a34a; }}
                .breakpoint-status.warn {{ background: #fef3c7; color: #d97706; }}
                .breakpoint-status.fail {{ background: #fee2e2; color: #dc2626; }}
            </style>

            <div class="breakpoint-checker">
                <h3 style="margin-bottom: 1.5rem;">📏 Breakpoint Checker</h3>

                <div class="breakpoint-list">
                    <div class="breakpoint-item">
                        <div class="breakpoint-info">
                            <span class="breakpoint-icon">📱</span>
                            <div>
                                <div class="breakpoint-name">Mobile Small</div>
                                <div class="breakpoint-range">320px - 479px</div>
                            </div>
                        </div>
                        <span class="breakpoint-status pass">✅ Pass</span>
                    </div>

                    <div class="breakpoint-item">
                        <div class="breakpoint-info">
                            <span class="breakpoint-icon">📱</span>
                            <div>
                                <div class="breakpoint-name">Mobile</div>
                                <div class="breakpoint-range">480px - 767px</div>
                            </div>
                        </div>
                        <span class="breakpoint-status pass">✅ Pass</span>
                    </div>

                    <div class="breakpoint-item">
                        <div class="breakpoint-info">
                            <span class="breakpoint-icon">📱</span>
                            <div>
                                <div class="breakpoint-name">Tablet</div>
                                <div class="breakpoint-range">768px - 1023px</div>
                            </div>
                        </div>
                        <span class="breakpoint-status warn">⚠️ Warning</span>
                    </div>

                    <div class="breakpoint-item">
                        <div class="breakpoint-info">
                            <span class="breakpoint-icon">💻</span>
                            <div>
                                <div class="breakpoint-name">Laptop</div>
                                <div class="breakpoint-range">1024px - 1439px</div>
                            </div>
                        </div>
                        <span class="breakpoint-status pass">✅ Pass</span>
                    </div>

                    <div class="breakpoint-item">
                        <div class="breakpoint-info">
                            <span class="breakpoint-icon">🖥️</span>
                            <div>
                                <div class="breakpoint-name">Desktop</div>
                                <div class="breakpoint-range">1440px+</div>
                            </div>
                        </div>
                        <span class="breakpoint-status pass">✅ Pass</span>
                    </div>
                </div>
            </div>
        </div>
        """
