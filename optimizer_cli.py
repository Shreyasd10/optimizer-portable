#!/usr/bin/env python3
"""
Optimizer CLI - Unified interface for local optimizer + optional ruflo integration

Usage:
    python3 optimizer_cli.py status              # Check system status
    python3 optimizer_cli.py store <key> <value> # Store a pattern
    python3 optimizer_cli.py recall <query>       # Recall patterns
    python3 optimizer_cli.py list                 # List all patterns
    python3 optimizer_cli.py doctor               # Run health checks
    python3 optimizer_cli.py install              # Show ruflo install info

PORTABLE: Works from any directory, auto-detects paths
"""

import argparse
import json
import sys
from pathlib import Path

# Add optimizer directory to path for imports
OPTIMIZER_DIR = Path(__file__).parent
sys.path.insert(0, str(OPTIMIZER_DIR))

from paths import get_optimizer_home, detect_agent_platform
from ruflo_bridge import RufloBridge

# Use portable path
BASE_DIR = get_optimizer_home()


def cmd_status(bridge: RufloBridge):
    """Show optimizer and ruflo status."""
    status = bridge.status()
    
    print("=" * 50)
    print("Optimizer Status")
    print("=" * 50)
    print(f"Ruflo available: {status['available']}")
    print(f"Ruflo enabled: {status['enabled']}")
    print(f"Ruflo path: {status['ruflo_path'] or 'npx (will use npx)'}")
    
    # Check disable file
    disabled_file = BASE_DIR / ".ruflo_disabled"
    if disabled_file.exists():
        print("\n[ruflo is DISABLED - using local fallback]")
        print("  To enable: optimizer ruflo-enable")
    elif status['available'] and status['enabled']:
        print("\n[Ruflo is ready for enhanced capabilities]")
        print("  - Vector memory search")
        print("  - Swarm coordination")
        print("  - Neural pattern training")
        print("  To disable: optimizer ruflo-disable")
    else:
        print("\n[Using local fallback]")
        print("  - JSON-based pattern storage")
        print("  - Simple keyword search")
        print("\nTo enable ruflo: npm install -g ruflo")
    
    # Show local memory stats
    memory_dir = BASE_DIR / "memory"
    if memory_dir.exists():
        files = list(memory_dir.glob("*.json"))
        print(f"\nLocal patterns: {len(files)} namespace(s)")
        for f in files:
            with f.open() as fp:
                data = json.load(fp)
                print(f"  - {f.stem}: {len(data)} pattern(s)")
    
    # Show platform info
    platform = detect_agent_platform()
    print(f"\nDetected platform: {platform}")
    
    print()


def cmd_store(bridge: RufloBridge, key: str, value: str, namespace: str = "patterns"):
    """Store a pattern."""
    result = bridge.memory_store(key, value, namespace)
    
    if result.success:
        mode = "ruflo" if result.using_ruflo else "local"
        print(f"[Stored] {key} ({mode} mode)")
    else:
        print(f"[Error] {result.error}")
        sys.exit(1)


def cmd_recall(bridge: RufloBridge, query: str, namespace: str = "patterns", limit: int = 5):
    """Recall patterns matching query."""
    result = bridge.memory_search(query, namespace=namespace, limit=limit)
    
    if result.success and result.output:
        mode = "ruflo" if result.using_ruflo else "local"
        print(f"Found {len(result.output)} pattern(s) ({mode} mode):")
        print()
        
        if isinstance(result.output, list):
            for item in result.output:
                if isinstance(item, dict):
                    print(f"  Key: {item.get('key', 'unknown')}")
                    print(f"  Value: {item.get('value', '')[:100]}...")
                    print()
        else:
            print(json.dumps(result.output, indent=2))
    else:
        print("[No patterns found]")
    
    # Try local fallback if ruflo failed
    if not result.success or not result.output:
        bridge.config.enabled = False
        result = bridge.memory_search(query, namespace=namespace, limit=limit)
        if result.success and result.output:
            print("\n[Fell back to local search]")
            for item in result.output:
                print(f"  - {item.get('key')}: {item.get('value', '')[:60]}...")


def cmd_list(bridge: RufloBridge, namespace: str = None):
    """List all patterns."""
    result = bridge.memory_list(namespace=namespace)
    
    if result.success and result.output:
        mode = "ruflo" if result.using_ruflo else "local"
        print(f"Patterns ({mode} mode):")
        print()
        
        if isinstance(result.output, dict):
            for ns, patterns in result.output.items():
                print(f"  Namespace: {ns}")
                for key, entry in patterns.items():
                    val = entry.get('value', '')[:60]
                    print(f"    - {key}: {val}...")
                print()
        else:
            print(json.dumps(result.output, indent=2))
    else:
        print("[No patterns stored]")


def cmd_doctor(bridge: RufloBridge):
    """Run health checks."""
    print("Running health checks...")
    print()
    
    # Check ruflo
    status = bridge.status()
    print(f"  [{'OK' if status['available'] else 'SKIP'}] Ruflo CLI")
    
    # Check local memory directory
    memory_dir = OPTIMIZER_DIR / "memory"
    print(f"  [{'OK' if memory_dir.exists() else 'WARN'}] Memory directory")
    
    # Check state files
    state_path = OPTIMIZER_DIR / "state.json"
    profile_path = OPTIMIZER_DIR / "profile.json"
    print(f"  [{'OK' if state_path.exists() else 'WARN'}] State file")
    print(f"  [{'OK' if profile_path.exists() else 'ERROR'}] Profile file")
    
    # Check droids directory
    droids_dir = Path.home() / ".factory" / "droids"
    print(f"  [{'OK' if droids_dir.exists() else 'WARN'}] Droids directory")
    
    print()
    print("Run 'ruflo doctor' for ruflo-specific diagnostics")


def cmd_install():
    """Show ruflo installation instructions."""
    print("=" * 50)
    print("Installing Ruflo CLI")
    print("=" * 50)
    print()
    print("Ruflo provides enhanced capabilities:")
    print("  - Vector-based semantic memory search")
    print("  - Multi-agent swarm coordination")
    print("  - Neural pattern learning")
    print("  - 17 learning hooks + 12 background workers")
    print()
    print("Installation options:")
    print()
    print("  Option 1: Global npm install (recommended)")
    print("    $ npm install -g ruflo")
    print()
    print("  Option 2: Use via npx (no install)")
    print("    $ npx ruflo@latest <command>")
    print("    Note: Slower startup, no persistent memory")
    print()
    print("  Option 3: Initialize project with wizard")
    print("    $ npx ruflo@latest init --wizard")
    print()
    print("After installing, run:")
    print("  $ claude mcp add ruflo -- npx -y ruflo@latest")
    print("  # to add ruflo as MCP server for Claude Code")
    print()
    print("Learn more: https://github.com/ruvnet/ruflo")


def cmd_ruflo_enable(bridge: RufloBridge):
    """Enable ruflo integration."""
    bridge.enable()
    print("[Enabled] Ruflo integration is now active")


def cmd_ruflo_disable(bridge: RufloBridge):
    """Disable ruflo integration."""
    bridge.disable()
    print("[Disabled] Using local fallback only")


def main():
    parser = argparse.ArgumentParser(
        description="Optimizer CLI - Local + ruflo integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s status              # Check system status
  %(prog)s store auth-pattern "JWT with refresh tokens"  
  %(prog)s recall authentication
  %(prog)s list
  %(prog)s doctor
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Status command
    subparsers.add_parser("status", help="Show optimizer and ruflo status")
    
    # Store command
    store_parser = subparsers.add_parser("store", help="Store a pattern")
    store_parser.add_argument("key", help="Pattern key")
    store_parser.add_argument("value", help="Pattern value")
    store_parser.add_argument("-n", "--namespace", default="patterns", help="Namespace (default: patterns)")
    
    # Recall command
    recall_parser = subparsers.add_parser("recall", help="Recall patterns")
    recall_parser.add_argument("query", help="Search query")
    recall_parser.add_argument("-n", "--namespace", default="patterns", help="Namespace (default: patterns)")
    recall_parser.add_argument("-l", "--limit", type=int, default=5, help="Max results (default: 5)")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all patterns")
    list_parser.add_argument("-n", "--namespace", help="Filter by namespace")
    
    # Doctor command
    subparsers.add_parser("doctor", help="Run health checks")
    
    # Install command
    subparsers.add_parser("install", help="Show ruflo installation instructions")
    
    # Ruflo enable/disable commands
    subparsers.add_parser("ruflo-enable", help="Enable ruflo integration")
    subparsers.add_parser("ruflo-disable", help="Disable ruflo integration (use local only)")
    
    args = parser.parse_args()
    
    # Initialize bridge
    bridge = RufloBridge()
    
    # Dispatch
    if args.command == "status":
        cmd_status(bridge)
    elif args.command == "store":
        cmd_store(bridge, args.key, args.value, args.namespace)
    elif args.command == "recall":
        cmd_recall(bridge, args.query, args.namespace, args.limit)
    elif args.command == "list":
        cmd_list(bridge, args.namespace)
    elif args.command == "doctor":
        cmd_doctor(bridge)
    elif args.command == "install":
        cmd_install()
    elif args.command == "ruflo-enable":
        cmd_ruflo_enable(bridge)
    elif args.command == "ruflo-disable":
        cmd_ruflo_disable(bridge)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
