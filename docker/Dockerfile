# syntax=docker/dockerfile:1
# OpenDesign — Production Docker Image
# Bundles Open WebUI with all OpenDesign functions pre-installed

FROM ghcr.io/open-webui/open-webui:latest

# Install Python dependencies for OpenDesign functions
RUN pip install --no-cache-dir \
    jinja2>=3.1 \
    beautifulsoup4>=4.12 \
    aiohttp>=3.9 \
    pydantic>=2.0

# Copy OpenDesign functions into Open WebUI's functions directory
# Open WebUI loads functions from /app/backend/data/functions/
COPY functions/ /app/backend/data/functions/opendesign/

# Copy templates, assets, and prompts
RUN mkdir -p /app/backend/data/opendesign/{templates/{landing,dashboard,component,presentation,email,social},assets,prompts}
COPY functions/design_studio/templates/ /app/backend/data/opendesign/templates/
COPY functions/design_studio/assets/ /app/backend/data/opendesign/assets/
COPY functions/design_studio/prompts/ /app/backend/data/opendesign/prompts/

# Set proper ownership (open-webui runs as UID 1000)
RUN chown -R 1000:1000 /app/backend/data/

# Expose the Open WebUI port (already exposed in base image)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD ["curl", "-f", "http://localhost:8080/health"]

# Default command (already set in base image)
# CMD ["gunicorn", "open_webui.app:app", "--bind", "0.0.0.0:8080", "--workers", "4"]
