#!/usr/bin/env python3
"""
Portable path utilities for Factory Optimizer
Automatically detects home directory and agent platform
"""

import os
import socket
from pathlib import Path
from typing import Optional


def get_home() -> Path:
    """Get home directory, works on any platform."""
    return Path(os.path.expanduser("~"))


def get_factory_home() -> Path:
    """Get Factory home directory.
    
    Checks in order:
    1. FACTORY_HOME env var
    2. ~/.factory
    3. ~/.droid
    """
    if factory := os.environ.get("FACTORY_HOME"):
        return Path(factory)
    
    factory = get_home() / ".factory"
    if factory.exists():
        return factory
    
    droid = get_home() / ".droid"
    if droid.exists():
        return droid
    
    return factory  # Default even if doesn't exist


def get_optimizer_home() -> Path:
    """Get optimizer directory within Factory."""
    return get_factory_home() / "optimizer"


def get_droids_home() -> Path:
    """Get droids directory within Factory."""
    return get_factory_home() / "droids"


def get_skills_home() -> Path:
    """Get skills directory within Factory."""
    return get_factory_home() / "skills"


def detect_agent_platform() -> str:
    """Detect which agent platform is running.
    
    Returns:
        - 'factory' for Factory/Droid
        - 'codex' for OpenAI Codex
        - 'forge' for Forge
        - 'claude' for Claude Code
        - 'hermes' for Hermes
        - 'unknown' if detection fails
    """
    # Check environment variables first
    env_markers = {
        "FACTORY": "factory",
        "CLAUDE_CODE": "claude",
        "OPENAI_API_KEY": "codex",
        "FORGE_HOME": "forge",
        "HERMES_HOME": "hermes",
    }
    
    for env_var, platform in env_markers.items():
        if os.environ.get(env_var):
            return platform
    
    # Check hostname patterns (common conventions)
    hostname = socket.gethostname().lower()
    
    if "factory" in hostname:
        return "factory"
    elif "codex" in hostname:
        return "codex"
    elif "forge" in hostname:
        return "forge"
    elif "claude" in hostname:
        return "claude"
    elif "hermes" in hostname:
        return "hermes"
    
    # Check parent process name
    try:
        import psutil
        parent = psutil.Process().parent()
        if parent:
            name = parent.name().lower()
            if "factory" in name or "droid" in name:
                return "factory"
            elif "codex" in name:
                return "codex"
            elif "forge" in name:
                return "forge"
    except (ImportError, Exception):
        pass
    
    return "unknown"


def get_platform_config_dir() -> Path:
    """Get platform-specific config directory.
    
    Factory: ~/.factory
    Claude Code: ~/.claude
    Codex: ~/.codex
    Forge: ~/.forge
    Hermes: ~/.hermes
    """
    platform = detect_agent_platform()
    
    dirs = {
        "factory": get_home() / ".factory",
        "claude": get_home() / ".claude",
        "codex": get_home() / ".codex",
        "forge": get_home() / ".forge",
        "hermes": get_home() / ".hermes",
    }
    
    return dirs.get(platform, get_factory_home())


def ensure_directories():
    """Ensure all required directories exist."""
    for path in [
        get_optimizer_home(),
        get_optimizer_home() / "memory",
        get_droids_home(),
        get_skills_home(),
    ]:
        path.mkdir(parents=True, exist_ok=True)


# Quick test
if __name__ == "__main__":
    print(f"Home: {get_home()}")
    print(f"Factory: {get_factory_home()}")
    print(f"Optimizer: {get_optimizer_home()}")
    print(f"Platform: {detect_agent_platform()}")
    print(f"Config dir: {get_platform_config_dir()}")
