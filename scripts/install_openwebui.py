#!/usr/bin/env python3
"""
OpenDesigner Plugin Install Script for Open WebUI

This script programmatically imports all OpenDesigner functions into
an Open WebUI instance via the API. It is idempotent - safe to re-run.

Usage:
    export OPENWEBUI_URL="http://localhost:3000"
    export OPENWEBUI_API_KEY="your-api-key-from-settings"
    python3 scripts/install_openwebui.py

Or with explicit arguments:
    python3 scripts/install_openwebui.py --url http://localhost:3000 --api-key your-key
"""

import argparse
import json
import os
import sys
from pathlib import Path

import aiohttp
import asyncio


BASE_DIR = Path(__file__).resolve().parent.parent
PLUGIN_JSON = BASE_DIR / "plugin" / "plugin.json"
FUNCTIONS_DIR = BASE_DIR / "functions"

# Open WebUI API endpoints
API_CREATE = "/api/v1/functions/create"
API_UPDATE = "/api/v1/functions/id/{id}/update"
API_TOGGLE = "/api/v1/functions/id/{id}/toggle"
API_LIST = "/api/v1/functions/"


class OpenDesignerInstaller:
    """Install OpenDesigner plugin functions into Open WebUI."""

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.session: aiohttp.ClientSession | None = None
        self.functions_config = {}

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        )
        return self

    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()

    async def load_plugin_config(self) -> dict:
        """Load plugin.json configuration."""
        if not PLUGIN_JSON.exists():
            print(f"❌ plugin.json not found at {PLUGIN_JSON}")
            sys.exit(1)

        with open(PLUGIN_JSON) as f:
            self.functions_config = json.load(f)

        print(f"📦 Loaded plugin: {self.functions_config['name']} v{self.functions_config['version']}")
        print(f"   Functions: {len(self.functions_config['functions'])}")
        return self.functions_config

    def get_function_path(self, func_path: str) -> Path:
        """Get absolute path to a function file."""
        return FUNCTIONS_DIR / func_path

    def validate_function(self, func_path: str) -> tuple[bool, str]:
        """Validate that a function file is importable."""
        path = self.get_function_path(func_path)
        if not path.exists():
            return False, f"File not found: {path}"

        # Check for required frontmatter
        with open(path) as f:
            content = f.read()

        if '"""' not in content[:200]:
            return False, "Missing frontmatter (triple-quoted docstring)"

        if "title:" not in content:
            return False, "Missing 'title' in frontmatter"

        if "author:" not in content:
            return False, "Missing 'author' in frontmatter"

        # Check for valid class
        if not any(f"class {cls}:" in content for cls in ["Action", "Pipe", "Filter", "Tools"]):
            return False, "No Open WebUI Function class (Action/Pipe/Filter/Tools) found"

        # Check for relative imports
        for line in content.split("\n"):
            if line.strip().startswith("from . "):
                return False, f"Relative import found: {line.strip()}"

        return True, "OK"

    async def create_function(self, func_path: str) -> tuple[bool, str]:
        """Create or update a function via the API."""
        path = self.get_function_path(func_path)
        if not path.exists():
            return False, f"File not found: {path}"

        with open(path) as f:
            content = f.read()

        func_id = path.stem
        func_name = Path(func_path).parent.name.replace("_", " ").title()

        # Extract frontmatter
        frontmatter = self._extract_frontmatter(content)

        payload = {
            "id": func_id,
            "name": frontmatter.get("title", func_name),
            "content": content,
            "meta": {
                "author": frontmatter.get("author", "Unknown"),
                "version": frontmatter.get("version", "0.1.0"),
                "description": frontmatter.get("title", func_name),
            },
        }

        # Add requirements if specified
        if frontmatter.get("requirements"):
            payload["requirements"] = [
                r.strip() for r in frontmatter["requirements"].split(",")
            ]

        try:
            async with self.session.post(f"{self.base_url}{API_CREATE}", json=payload) as resp:
                if resp.status in (200, 201):
                    return True, "Created"
                error = await resp.text()
                # Try update if create fails (function already exists)
                if resp.status == 409 or "already exists" in error.lower():
                    return await self.update_function(func_id, content, frontmatter)
                return False, f"HTTP {resp.status}: {error[:200]}"
        except Exception as e:
            return False, str(e)

    async def update_function(self, func_id: str, content: str, frontmatter: dict) -> tuple[bool, str]:
        """Update an existing function."""
        payload = {
            "content": content,
            "meta": {
                "author": frontmatter.get("author", "Unknown"),
                "version": frontmatter.get("version", "0.1.0"),
            },
        }

        try:
            url = f"{self.base_url}{API_UPDATE.format(id=func_id)}"
            async with self.session.post(url, json=payload) as resp:
                if resp.status in (200, 201):
                    return True, "Updated"
                return False, f"HTTP {resp.status}: {await resp.text()[:200]}"
        except Exception as e:
            return False, str(e)

    async def toggle_function(self, func_id: str, enable: bool = True) -> tuple[bool, str]:
        """Enable or disable a function."""
        try:
            url = f"{self.base_url}{API_TOGGLE.format(id=func_id)}"
            async with self.session.post(url, json={"is_active": enable}) as resp:
                if resp.status in (200, 201):
                    return True, "Enabled" if enable else "Disabled"
                return False, f"HTTP {resp.status}"
        except Exception as e:
            return False, str(e)

    def _extract_frontmatter(self, content: str) -> dict:
        """Extract frontmatter from Open WebUI function file."""
        if not content.startswith('"""'):
            return {}

        # Find closing triple quotes
        end_idx = content.find('"""', 3)
        if end_idx == -1:
            return {}

        fm_text = content[3:end_idx]
        frontmatter = {}
        for line in fm_text.split("\n"):
            line = line.strip()
            if ":" in line and not line.startswith('"'):
                key, _, value = line.partition(":")
                frontmatter[key.strip()] = value.strip()

        return frontmatter

    async def list_functions(self) -> list[dict]:
        """List all current functions."""
        try:
            async with self.session.get(f"{self.base_url}{API_LIST}") as resp:
                if resp.status == 200:
                    return await resp.json()
                return []
        except Exception:
            return []

    async def smoke_test(self, expected_count: int) -> bool:
        """Run a smoke test to verify installation."""
        functions = await self.list_functions()
        installed = len(functions)
        print(f"\n🔍 Smoke Test Results:")
        print(f"   Expected functions: {expected_count}")
        print(f"   Installed: {installed}")

        if installed >= expected_count:
            print(f"   Status: ✅ PASS")
            return True
        else:
            print(f"   Status: ⚠️  Expected at least {expected_count}, found {installed}")
            return False


async def main():
    parser = argparse.ArgumentParser(description="Install OpenDesigner plugin into Open WebUI")
    parser.add_argument("--url", default=os.environ.get("OPENWEBUI_URL", "http://localhost:3000"),
                        help="Open WebUI URL")
    parser.add_argument("--api-key", default=os.environ.get("OPENWEBUI_API_KEY", ""),
                        help="Open WebUI API key")
    parser.add_argument("--enable-all", action="store_true", default=True,
                        help="Enable all functions after installation")
    args = parser.parse_args()

    if not args.api_key:
        print("❌ OPENWEBUI_API_KEY environment variable is required")
        print("   Get it from: Settings → Account → API Keys")
        sys.exit(1)

    print(f"🚀 Installing OpenDesigner into {args.url}")
    print("-" * 50)

    async with OpenDesignerInstaller(args.url, args.api_key) as installer:
        # Load plugin config
        config = await installer.load_plugin_config()
        func_paths = config.get("functions", [])

        # Validate all functions first
        print("\n📋 Validating functions...")
        valid_funcs = []
        for func_path in func_paths:
            is_valid, msg = installer.validate_function(func_path)
            status = "✓" if is_valid else "✗"
            print(f"   {status} {func_path}: {msg}")
            if is_valid:
                valid_funcs.append(func_path)

        if not valid_funcs:
            print("\n❌ No valid functions to install!")
            sys.exit(1)

        # Install each function
        print(f"\n📦 Installing {len(valid_funcs)} functions...")
        results = []
        for func_path in valid_funcs:
            success, msg = await installer.create_function(func_path)
            status = "✓" if success else "✗"
            print(f"   {status} {func_path}: {msg}")
            results.append((func_path, success))

        # Enable all functions
        if args.enable_all:
            print("\n🔓 Enabling functions...")
            for func_path, _ in results:
                if func_path:
                    func_id = installer.get_function_path(func_path).stem
                    await installer.toggle_function(func_id, enable=True)

        # Run smoke test
        success_count = sum(1 for _, s in results if s)
        await installer.smoke_test(success_count)

        # Summary
        print("\n" + "=" * 50)
        print(f"✅ Installation complete: {success_count}/{len(valid_funcs)} functions")
        print("-" * 50)
        print("\nNext steps:")
        print("  1. Open Open WebUI in your browser")
        print("  2. Go to Admin → Functions")
        print("  3. Verify all functions are enabled")
        print("  4. Start using OpenDesigner in your chats!")


if __name__ == "__main__":
    asyncio.run(main())
