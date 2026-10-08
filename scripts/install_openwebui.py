#!/usr/bin/env python3
"""
OpenDesigner Plugin Install Script for Open WebUI

This script programmatically imports all OpenDesigner functions into
an Open WebUI instance via the API. It is idempotent - safe to re-run.

Usage:
    export OPENWEBUI_URL="http://localhost:3000"
    export OPENWEBUI_API_KEY="xxx"
    python3 scripts/install_openwebui.py

Or with explicit arguments:
    python3 scripts/install_openwebui.py --url http://localhost:3000 --api-key your-key
"""

import argparse
import asyncio
import json
import os
import re
import sys
import time
from pathlib import Path

import aiohttp

BASE_DIR = Path(__file__).resolve().parent.parent
PLUGIN_JSON = BASE_DIR / "plugin" / "plugin.json"
FUNCTIONS_DIR = BASE_DIR / "functions"

# Open WebUI API endpoints
API_CREATE = "/api/v1/functions/create"
API_UPDATE = "/api/v1/functions/id/{id}/update"
API_TOGGLE = "/api/v1/functions/id/{id}/toggle"
API_TOGGLE_GLOBAL = "/api/v1/functions/id/{id}/toggle/global"
API_GET = "/api/v1/functions/id/{id}"
API_LIST = "/api/v1/functions/"


class OpenDesignerInstaller:
    """Install OpenDesigner plugin functions into Open WebUI."""

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.session: aiohttp.ClientSession | None = None
        self.functions_config = {}

    async def __aenter__(self):
        # Use generous timeouts — some functions are large (~46KB)
        timeout = aiohttp.ClientTimeout(total=120, connect=30, sock_read=60)
        self.session = aiohttp.ClientSession(
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            timeout=timeout,
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

        print(
            f"📦 Loaded plugin: {self.functions_config['name']} v{self.functions_config['version']}"
        )
        print(f"   Functions: {len(self.functions_config['functions'])}")
        return self.functions_config

    def get_function_path(self, func_path: str) -> Path:
        """Get absolute path to a function file."""
        return FUNCTIONS_DIR / func_path

    @staticmethod
    def detect_class_type(content: str) -> str:
        """Detect the function type (Action/Pipe/Filter/Tools) from class definition."""
        match = re.search(r"class\s+(Action|Pipe|Filter|Tools)\s*[\(:]", content)
        return match.group(1) if match else "UNKNOWN"

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

        # Check for valid class type
        class_type = self.detect_class_type(content)
        if class_type == "UNKNOWN":
            return False, "No Open WebUI Function class (Action/Pipe/Filter/Tools) found"

        # Check for relative imports
        for line in content.split("\n"):
            if line.strip().startswith("from . "):
                return False, f"Relative import found: {line.strip()}"

        return True, f"OK (type: {class_type})"

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

        # Build payload - Open WebUI extracts type from content (Pipe/Filter/Action/Event)
        payload: dict = {
            "id": func_id,
            "name": frontmatter.get("title", func_name),
            "content": content,
            "meta": {
                "author": frontmatter.get("author", "Unknown"),
                "version": frontmatter.get("version", "0.1.0"),
                "description": frontmatter.get("title", func_name),
            },
        }

        # Note: Open WebUI extracts requirements from frontmatter in content,
        # so we do NOT send it in the payload (FunctionForm doesn't have that field)

        try:
            async with self.session.post(f"{self.base_url}{API_CREATE}", json=payload) as resp:
                if resp.status in (200, 201):
                    return True, "Created"
                error = await resp.text()
                # Try update if create fails (function already exists)
                if resp.status == 409 or "already exists" in error.lower():
                    return await self.update_function(func_id, content, frontmatter)
                return False, f"HTTP {resp.status}: {error[:200]}"
        except asyncio.TimeoutError:
            return False, "Request timeout (function content is large, try again)"
        except aiohttp.ClientError as e:
            return False, f"Network error: {e}"
        except Exception as e:
            return False, str(e)

    async def update_function(
        self, func_id: str, content: str, frontmatter: dict
    ) -> tuple[bool, str]:
        """Update an existing function."""
        payload: dict = {
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
        except asyncio.TimeoutError:
            return False, "Request timeout during update"
        except aiohttp.ClientError as e:
            return False, f"Network error: {e}"
        except Exception as e:
            return False, str(e)

    async def get_function(self, func_id: str) -> dict | None:
        """Fetch a single function by ID to check its current state."""
        try:
            url = f"{self.base_url}{API_GET.format(id=func_id)}"
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    return await resp.json()
                return None
        except Exception:
            return None

    async def _request_with_retry(
        self, method: str, url: str, json_data: dict | None = None, max_retries: int = 3
    ) -> aiohttp.ClientResponse | None:
        """Make an HTTP request with retry logic for transient failures."""
        last_exception = None
        for attempt in range(max_retries):
            try:
                if method == "GET":
                    return await self.session.get(url)
                elif method == "POST":
                    return await self.session.post(url, json=json_data)
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                last_exception = e
                if attempt < max_retries - 1:
                    wait = 2 ** attempt  # 1s, 2s, 4s
                    print(f"   ⏳ Retry {attempt + 1}/{max_retries} after {wait}s: {e}")
                    await asyncio.sleep(wait)
        if last_exception:
            raise last_exception
        return None

    async def toggle_function(self, func_id: str, enable: bool = True) -> tuple[bool, str]:
        """Enable or disable a function — safely idempotent.

        The toggle endpoint FLIPS the current state, so we fetch the
        current state first and only call toggle when necessary.
        """
        try:
            # Fetch current state
            func = await self.get_function(func_id)
            if func is None:
                return False, "Could not fetch function state"

            current_active = func.get("is_active", False)

            if current_active == enable:
                # Already in desired state — nothing to do
                return True, "Already set" if enable else "Already disabled"

            # Only toggle when state differs (with retry)
            url = f"{self.base_url}{API_TOGGLE.format(id=func_id)}"
            resp = await self._request_with_retry("POST", url)
            if resp is None:
                return False, "Could not connect to server"
            if resp.status in (200, 201):
                return True, "Enabled" if enable else "Disabled"
            return False, f"HTTP {resp.status}"
        except Exception as e:
            return False, str(e)

    async def toggle_global(self, func_id: str, make_global: bool = True) -> tuple[bool, str]:
        """Set/clear the global flag — safely idempotent.

        The toggle global endpoint FLIPS the current state, so we
        fetch the current state first and only call toggle when necessary.
        """
        try:
            # Fetch current state
            func = await self.get_function(func_id)
            if func is None:
                return False, "Could not fetch function state"

            current_global = func.get("is_global", False)

            if current_global == make_global:
                # Already in desired state — nothing to do
                return True, "Already global" if make_global else "Already not global"

            # Only toggle when state differs (with retry)
            url = f"{self.base_url}{API_TOGGLE_GLOBAL.format(id=func_id)}"
            resp = await self._request_with_retry("POST", url)
            if resp is None:
                return False, "Could not connect to server"
            if resp.status in (200, 201):
                return True, "Set as global" if make_global else "Cleared global"
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

    async def smoke_test(
        self, expected_count: int, expected_ids: list[str], global_ids: set[str] | None = None
    ) -> tuple[bool, list[str]]:
        """Run a smoke test to verify installation.

        Checks:
        1. The expected function IDs are all present (not just a count)
        2. Each expected function is active (is_active == True)
        3. Functions in global_ids are also global (is_global == True)

        Returns (passed, list_of_failure_messages).
        """
        functions = await self.list_functions()
        func_map = {f["id"]: f for f in functions}

        failures = []
        expected_ids_set = set(expected_ids)

        # Check 1: All expected IDs are present
        missing = expected_ids_set - set(func_map.keys())
        if missing:
            failures.append(f"Missing functions: {', '.join(sorted(missing))}")

        # Check 2: All expected functions are active
        inactive = []
        for fid in expected_ids:
            if fid in func_map and not func_map[fid].get("is_active", False):
                inactive.append(fid)
        if inactive:
            failures.append(f"Inactive functions: {', '.join(sorted(inactive))}")

        # Check 3: Global functions must also be global
        if global_ids:
            not_global = []
            for fid in global_ids:
                if fid in func_map and not func_map[fid].get("is_global", False):
                    not_global.append(fid)
            if not_global:
                failures.append(f"Functions not global (need global): {', '.join(sorted(not_global))}")

        # Count active functions for display
        active_count = sum(1 for f in functions if f.get("is_active", False))

        print("\n🔍 Smoke Test Results:")
        print(f"   Expected functions: {expected_count}")
        print(f"   Active: {active_count}/{len(functions)}")

        if not failures:
            print("   Status: ✅ PASS")
            return True, []
        else:
            print(f"   Status: ❌ FAIL")
            for failure in failures:
                print(f"      ⚠️  {failure}")
            return False, failures


async def main():
    parser = argparse.ArgumentParser(description="Install OpenDesigner plugin into Open WebUI")
    parser.add_argument(
        "--url",
        default=os.environ.get("OPENWEBUI_URL", "http://localhost:3000"),
        help="Open WebUI URL",
    )
    parser.add_argument(
        "--api-key", default=os.environ.get("OPENWEBUI_API_KEY", ""), help="Open WebUI API key"
    )
    parser.add_argument(
        "--enable-all",
        action="store_true",
        default=True,
        help="Enable all functions after installation",
    )
    parser.add_argument(
        "--global-funcs",
        nargs="*",
        default=[],
        help="Function IDs that should be set as global (filters/actions). "
        "Default: all functions are global.",
    )
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

        # Create missing __init__.py files (needed for proper module resolution)
        print("\n📦 Ensuring __init__.py files...")
        init_dirs = set()
        for func_path in valid_funcs:
            init_dirs.add(str(installer.get_function_path(func_path).parent))

        for dir_path in sorted(init_dirs):
            init_file = Path(dir_path) / "__init__.py"
            if not init_file.exists():
                init_file.write_text("# Open WebUI function module\n")
                print(f"   ✓ Created: {dir_path}/__init__.py")
            else:
                print(f"   ✓ Exists: {dir_path}/__init__.py")

        # Determine which functions should be global
        # Default: all functions are global (needed for filters/actions to apply per-user)
        global_func_ids = set(args.global_funcs) if args.global_funcs else None
        if global_func_ids is None:
            global_func_ids = {installer.get_function_path(fp).stem for fp in valid_funcs}

        # Install each function
        print(f"\n📦 Installing {len(valid_funcs)} functions...")
        results = []
        any_failure = False
        for func_path in valid_funcs:
            success, msg = await installer.create_function(func_path)
            status = "✓" if success else "✗"
            print(f"   {status} {func_path}: {msg}")
            if not success:
                any_failure = True
            results.append((func_path, success))

        # Enable all functions (idempotently)
        if args.enable_all:
            print("\n🔓 Enabling functions...")
            for func_path, _ in results:
                if func_path:
                    func_id = installer.get_function_path(func_path).stem
                    success, msg = await installer.toggle_function(func_id, enable=True)
                    status = "✓" if success else "✗"
                    print(f"   {status} {func_id}: {msg}")
                    if not success:
                        any_failure = True

        # Set global flag (idempotently)
        if global_func_ids:
            print("\n🌍 Setting global functions...")
            for func_path, _ in results:
                if func_path:
                    func_id = installer.get_function_path(func_path).stem
                    if func_id in global_func_ids:
                        success, msg = await installer.toggle_global(func_id, make_global=True)
                        status = "✓" if success else "✗"
                        print(f"   {status} {func_id}: {msg}")
                        if not success:
                            any_failure = True

        # Run smoke test
        expected_ids = [installer.get_function_path(fp).stem for fp in valid_funcs]
        success_count = sum(1 for _, s in results if s)
        smoke_passed, smoke_failures = await installer.smoke_test(
            success_count, expected_ids, global_func_ids
        )
        if not smoke_passed:
            any_failure = True

        # Summary
        print("\n" + "=" * 50)
        if any_failure:
            print("❌ Installation completed with errors")
        else:
            print("✅ Installation complete: all functions installed, enabled, and global")
        print(f"   Successful: {success_count}/{len(valid_funcs)} functions")
        print("-" * 50)

        if any_failure or smoke_failures:
            print("\n❌ Some operations failed. Please check the errors above.")
            print("   - Run the installer again — it is safely idempotent.")
            print("   - Check that your OPENWEBUI_URL and OPENWEBUI_API_KEY are correct.")
            sys.exit(1)

        print("\nNext steps:")
        print("  1. Open Open WebUI in your browser")
        print("  2. Go to Admin → Functions")
        print("  3. Verify all functions are enabled")
        print("  4. Start using OpenDesigner in your chats!")
        sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
