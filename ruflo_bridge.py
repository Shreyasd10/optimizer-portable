#!/usr/bin/env python3
"""
Ruflo Bridge - Optional integration layer for ruflo CLI

This module detects ruflo availability and provides a unified interface
for memory, swarm, and hooks operations. Falls back gracefully when
ruflo is not installed.

PORTABLE: Uses paths.py for dynamic path detection
"""

import json
import subprocess
import shutil
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List, Dict, Any
from enum import Enum

# Import portable path utilities
import sys
_optimizer_dir = Path(__file__).parent
sys.path.insert(0, str(_optimizer_dir))
from paths import get_optimizer_home

# Use portable BASE_DIR
BASE_DIR = get_optimizer_home()


class Availability(Enum):
    AVAILABLE = "available"
    NOT_INSTALLED = "not_installed"
    ERROR = "error"


@dataclass
class RufloConfig:
    enabled: bool = True
    auto_init_memory: bool = True
    use_swarm_for_complex_tasks: bool = False
    cache_results: bool = True
    timeout_seconds: int = 30


@dataclass
class MemoryEntry:
    key: str
    value: str
    namespace: str = "patterns"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SwarmTask:
    task: str
    topology: str = "hierarchical"
    max_agents: int = 4
    strategy: str = "specialized"


@dataclass
class HookResult:
    success: bool
    output: Any = None
    error: Optional[str] = None
    using_ruflo: bool = False


class RufloBridge:
    """
    Optional bridge to ruflo CLI.
    
    Usage:
        bridge = RufloBridge()
        if bridge.is_available():
            bridge.memory_store("auth-pattern", "JWT with refresh")
            results = bridge.memory_search("authentication best practices")
        else:
            # Fall back to local JSON storage
            pass
    """
    
    def __init__(self, config: Optional[RufloConfig] = None):
        self.config = config or RufloConfig()
        self._available: Optional[Availability] = None
        self._ruflo_path: Optional[Path] = None
        self._disabled_file = BASE_DIR / ".ruflo_disabled"
        
        # Check for disable flag
        if self._disabled_file.exists():
            self.config.enabled = False
    
    def enable(self) -> bool:
        """Enable ruflo integration."""
        self.config.enabled = True
        if self._disabled_file.exists():
            self._disabled_file.unlink()
        return True
    
    def disable(self) -> bool:
        """Disable ruflo integration (use local fallback)."""
        self.config.enabled = False
        self._disabled_file.write_text("# Disabled by user\n")
        return True
    
    def is_enabled(self) -> bool:
        """Check if ruflo integration is explicitly enabled."""
        return self.config.enabled and not self._disabled_file.exists()
    
    def is_available(self) -> bool:
        """Check if ruflo CLI is available."""
        if not self.config.enabled:
            return False
        if self._available is None:
            self._check_availability()
        return self._available == Availability.AVAILABLE
    
    def _check_availability(self) -> None:
        """Detect ruflo installation."""
        # Check common paths
        possible_paths = [
            Path("/usr/local/bin/ruflo"),
            Path.home() / ".local/bin/ruflo",
            Path.home() / "bin/ruflo",
        ]
        
        for path in possible_paths:
            if path.exists():
                self._ruflo_path = path
                self._available = Availability.AVAILABLE
                return
        
        # Check if npx can run it
        if shutil.which("npx"):
            try:
                result = subprocess.run(
                    ["npx", "--yes", "ruflo@latest", "--version"],
                    capture_output=True,
                    timeout=10,
                    cwd="/tmp"
                )
                if result.returncode == 0:
                    self._ruflo_path = Path("npx")
                    self._available = Availability.AVAILABLE
                    return
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
        
        self._available = Availability.NOT_INSTALLED
    
    def _run_command(self, args: List[str], timeout: Optional[int] = None) -> subprocess.CompletedProcess:
        """Run ruflo command."""
        timeout = timeout or self.config.timeout_seconds
        
        if self._ruflo_path == Path("npx"):
            cmd = ["npx", "--yes", "ruflo@latest"] + args
        else:
            cmd = [str(self._ruflo_path)] + args
        
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(BASE_DIR)
        )
    
    # ========== Memory Operations ==========
    
    def memory_store(self, key: str, value: str, namespace: str = "patterns", 
                     metadata: Optional[Dict] = None) -> HookResult:
        """
        Store a pattern in ruflo's vector memory.
        
        Falls back to local JSON if ruflo not available.
        """
        if not self.is_available():
            return self._memory_store_local(key, value, namespace, metadata)
        
        try:
            metadata_args = []
            if metadata:
                metadata_args = ["--metadata", json.dumps(metadata)]
            
            result = self._run_command([
                "memory", "store",
                "--key", key,
                "--value", value,
                "--namespace", namespace,
            ] + metadata_args)
            
            if result.returncode == 0:
                return HookResult(success=True, using_ruflo=True)
            else:
                return HookResult(success=False, error=result.stderr, using_ruflo=True)
        except subprocess.TimeoutExpired:
            return HookResult(success=False, error="Timeout", using_ruflo=True)
        except Exception as e:
            return HookResult(success=False, error=str(e), using_ruflo=True)
    
    def memory_search(self, query: str, limit: int = 5, 
                      namespace: str = "patterns") -> HookResult:
        """
        Search ruflo's vector memory semantically.
        
        Falls back to local JSON search if ruflo not available.
        """
        if not self.is_available():
            return self._memory_search_local(query, limit, namespace)
        
        try:
            result = self._run_command([
                "memory", "search",
                "--query", query,
                "--limit", str(limit),
                "--namespace", namespace,
            ])
            
            if result.returncode == 0:
                try:
                    output = json.loads(result.stdout)
                    return HookResult(success=True, output=output, using_ruflo=True)
                except json.JSONDecodeError:
                    return HookResult(success=True, output=result.stdout, using_ruflo=True)
            else:
                return HookResult(success=False, error=result.stderr, using_ruflo=True)
        except subprocess.TimeoutExpired:
            return HookResult(success=False, error="Timeout", using_ruflo=True)
        except Exception as e:
            return HookResult(success=False, error=str(e), using_ruflo=True)
    
    def memory_list(self, namespace: Optional[str] = None) -> HookResult:
        """List stored patterns."""
        if not self.is_available():
            return self._memory_list_local(namespace)
        
        try:
            args = ["memory", "list"]
            if namespace:
                args.extend(["--namespace", namespace])
            
            result = self._run_command(args)
            
            if result.returncode == 0:
                return HookResult(success=True, output=result.stdout, using_ruflo=True)
            else:
                return HookResult(success=False, error=result.stderr, using_ruflo=True)
        except Exception as e:
            return HookResult(success=False, error=str(e), using_ruflo=True)
    
    # ========== Hook Operations ==========
    
    def hooks_route(self, task: str) -> HookResult:
        """
        Route a task to optimal agent using ruflo's semantic router.
        """
        if not self.is_available():
            return HookResult(success=False, error="ruflo not available", using_ruflo=False)
        
        try:
            result = self._run_command([
                "hooks", "route",
                "--task", task,
            ])
            
            if result.returncode == 0:
                return HookResult(success=True, output=result.stdout, using_ruflo=True)
            else:
                return HookResult(success=False, error=result.stderr, using_ruflo=True)
        except Exception as e:
            return HookResult(success=False, error=str(e), using_ruflo=True)
    
    def hooks_post_task(self, task_id: str, success: bool, 
                        store_results: bool = True) -> HookResult:
        """
        Record task completion for learning.
        """
        if not self.is_available():
            return HookResult(success=False, error="ruflo not available", using_ruflo=False)
        
        try:
            result = self._run_command([
                "hooks", "post-task",
                "--task-id", task_id,
                "--success", str(success).lower(),
                "--store-results", str(store_results).lower(),
            ])
            
            if result.returncode == 0:
                return HookResult(success=True, using_ruflo=True)
            else:
                return HookResult(success=False, error=result.stderr, using_ruflo=True)
        except Exception as e:
            return HookResult(success=False, error=str(e), using_ruflo=True)
    
    # ========== Swarm Operations ==========
    
    def swarm_init(self, topology: str = "hierarchical", 
                   max_agents: int = 4) -> HookResult:
        """Initialize a swarm."""
        if not self.is_available():
            return HookResult(success=False, error="ruflo not available", using_ruflo=False)
        
        try:
            result = self._run_command([
                "swarm", "init",
                "--topology", topology,
                "--max-agents", str(max_agents),
            ])
            
            if result.returncode == 0:
                return HookResult(success=True, output=result.stdout, using_ruflo=True)
            else:
                return HookResult(success=False, error=result.stderr, using_ruflo=True)
        except Exception as e:
            return HookResult(success=False, error=str(e), using_ruflo=True)
    
    def agent_spawn(self, agent_type: str, name: str) -> HookResult:
        """Spawn an agent in the swarm."""
        if not self.is_available():
            return HookResult(success=False, error="ruflo not available", using_ruflo=False)
        
        try:
            result = self._run_command([
                "agent", "spawn",
                "-t", agent_type,
                "--name", name,
            ])
            
            if result.returncode == 0:
                return HookResult(success=True, output=result.stdout, using_ruflo=True)
            else:
                return HookResult(success=False, error=result.stderr, using_ruflo=True)
        except Exception as e:
            return HookResult(success=False, error=str(e), using_ruflo=True)
    
    # ========== System Operations ==========
    
    def doctor(self, auto_fix: bool = False) -> HookResult:
        """Run system health check."""
        if not self.is_available():
            return HookResult(success=False, error="ruflo not available", using_ruflo=False)
        
        try:
            args = ["doctor"]
            if auto_fix:
                args.append("--fix")
            
            result = self._run_command(args, timeout=60)
            
            if result.returncode == 0:
                return HookResult(success=True, output=result.stdout, using_ruflo=True)
            else:
                return HookResult(success=False, error=result.stderr, using_ruflo=True)
        except Exception as e:
            return HookResult(success=False, error=str(e), using_ruflo=True)
    
    def status(self) -> Dict[str, Any]:
        """Get status of ruflo integration."""
        return {
            "enabled": self.config.enabled,
            "available": self.is_available(),
            "status": self._available.value if self._available else "unknown",
            "ruflo_path": str(self._ruflo_path) if self._ruflo_path else None,
        }
    
    # ========== Local Fallback Operations ==========
    # These use local JSON storage when ruflo is unavailable
    
    def _get_local_memory_path(self, namespace: str) -> Path:
        """Get path for local memory storage."""
        memory_dir = BASE_DIR / "memory"
        memory_dir.mkdir(exist_ok=True)
        return memory_dir / f"{namespace}.json"
    
    def _memory_store_local(self, key: str, value: str, namespace: str,
                            metadata: Optional[Dict] = None) -> HookResult:
        """Store in local JSON fallback."""
        try:
            path = self._get_local_memory_path(namespace)
            
            if path.exists():
                with path.open() as f:
                    data = json.load(f)
            else:
                data = {}
            
            data[key] = {
                "value": value,
                "metadata": metadata or {},
                "stored_at": self._iso_now()
            }
            
            with path.open("w") as f:
                json.dump(data, f, indent=2)
            
            return HookResult(success=True, using_ruflo=False)
        except Exception as e:
            return HookResult(success=False, error=str(e), using_ruflo=False)
    
    def _memory_search_local(self, query: str, limit: int,
                             namespace: str) -> HookResult:
        """Simple keyword search fallback."""
        try:
            path = self._get_local_memory_path(namespace)
            
            if not path.exists():
                return HookResult(success=True, output=[], using_ruflo=False)
            
            with path.open() as f:
                data = json.load(f)
            
            # Simple substring match
            query_lower = query.lower()
            results = []
            for key, entry in data.items():
                if query_lower in key.lower() or query_lower in entry.get("value", "").lower():
                    results.append({"key": key, **entry})
                    if len(results) >= limit:
                        break
            
            return HookResult(success=True, output=results, using_ruflo=False)
        except Exception as e:
            return HookResult(success=False, error=str(e), using_ruflo=False)
    
    def _memory_list_local(self, namespace: Optional[str] = None) -> HookResult:
        """List local memory entries."""
        try:
            memory_dir = BASE_DIR / "memory"
            
            if not memory_dir.exists():
                return HookResult(success=True, output={}, using_ruflo=False)
            
            results = {}
            for path in memory_dir.glob("*.json"):
                ns = path.stem
                if namespace and ns != namespace:
                    continue
                with path.open() as f:
                    results[ns] = json.load(f)
            
            return HookResult(success=True, output=results, using_ruflo=False)
        except Exception as e:
            return HookResult(success=False, error=str(e), using_ruflo=False)
    
    @staticmethod
    def _iso_now() -> str:
        """Get current ISO timestamp."""
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


# Convenience function for quick status check
def check_ruflo_status() -> Dict[str, Any]:
    """Quick status check."""
    bridge = RufloBridge()
    return bridge.status()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "status":
            status = check_ruflo_status()
            print(json.dumps(status, indent=2))
        
        elif command == "doctor":
            bridge = RufloBridge()
            result = bridge.doctor(auto_fix="--fix" in sys.argv)
            print(result.output or result.error)
        
        elif command == "install":
            print("To install ruflo CLI:")
            print("  npm install -g ruflo")
            print("  # or")
            print("  npx ruflo@latest doctor")
    
    else:
        print("Ruflo Bridge - Optional ruflo integration")
        print()
        print("Usage:")
        print("  python ruflo_bridge.py status    # Check ruflo availability")
        print("  python ruflo_bridge.py doctor   # Run health check")
        print("  python ruflo_bridge.py install  # Show install instructions")
