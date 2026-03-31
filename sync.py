#!/usr/bin/env python3
"""
Sync/Export script for Factory Optimizer

This script helps you:
1. Export your optimizer setup to a portable directory
2. Import from another machine
3. Sync between machines using git

Usage:
    python3 sync.py export [path]     # Export to portable format
    python3 sync.py import [path]    # Import from exported format
    python3 sync.py init             # Initialize in current factory home
    python3 sync.py status            # Show sync status
"""

import argparse
import json
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, List


# Core files that form the portable core
PORTABLE_CORE_FILES = [
    "profile.json",
    "state.json",
    "write_state.py",
    "ruflo_bridge.py",
    "paths.py",
    "optimizer_cli.py",
]

# Optional files
OPTIONAL_FILES = [
    "memory/*.json",  # Stored patterns
]

# Droids and skills (usually user-specific)
PERSONAL_FILES = [
    "droids/*.md",
]

# Skills folder has subdirectories
SKILLS_FILES = "skills"

# Bin scripts for easy access
BIN_FILES = [
    "bin/optimizer",
    "bin/ruflo-enable",
    "bin/ruflo-disable",
]


def get_factory_home() -> Path:
    """Get Factory home directory."""
    if factory := os.environ.get("FACTORY_HOME"):
        return Path(factory)
    home = Path(os.path.expanduser("~"))
    for name in [".factory", ".droid"]:
        path = home / name
        if path.exists():
            return path
    return home / ".factory"


def get_optimizer_home() -> Path:
    """Get optimizer directory."""
    return get_factory_home() / "optimizer"


def export_to_directory(target_path: Path, include_personal: bool = True):
    """Export optimizer setup to a directory."""
    source = get_optimizer_home()
    target = Path(target_path).expanduser()
    
    print(f"Exporting from: {source}")
    print(f"Exporting to:   {target}")
    
    # Create target directory
    target.mkdir(parents=True, exist_ok=True)
    
    # Export core files
    print("\n[1/3] Exporting core files...")
    for filename in PORTABLE_CORE_FILES:
        src = source / filename
        dst = target / filename
        if src.exists():
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
            print(f"  + {filename}")
        else:
            print(f"  - {filename} (not found)")
    
    # Export memory patterns
    print("\n[2/3] Exporting memory patterns...")
    memory_dir = source / "memory"
    if memory_dir.exists():
        target_memory = target / "memory"
        target_memory.mkdir(exist_ok=True)
        for json_file in memory_dir.glob("*.json"):
            shutil.copy2(json_file, target_memory / json_file.name)
            print(f"  + memory/{json_file.name}")
    
    # Optionally export personal files (droids, skills)
    if include_personal:
        print("\n[3/3] Exporting personal files (droids, skills)...")
        factory = get_factory_home()
        
        # Export droids
        for pattern in PERSONAL_FILES:
            if "*" in pattern:
                base, glob = pattern.split("/")
                src_dir = factory / base
                if src_dir.exists():
                    for f in src_dir.glob(glob):
                        dst = target / base / f.name
                        dst.parent.mkdir(exist_ok=True)
                        shutil.copy2(f, dst)
                        print(f"  + {base}/{f.name}")
        
        # Export skills (subdirectories)
        skills_src = factory / "skills"
        skills_dst = target / "skills"
        if skills_src.exists():
            skills_dst.mkdir(exist_ok=True)
            for skill_dir in skills_src.iterdir():
                if skill_dir.is_dir():
                    dst_dir = skills_dst / skill_dir.name
                    shutil.copytree(skill_dir, dst_dir, dirs_exist_ok=True)
                    print(f"  + skills/{skill_dir.name}/")
    
    # Create manifest
    manifest = {
        "exported_at": datetime.now().isoformat(),
        "source": str(source),
        "version": 2,
        "includes_personal": include_personal,
        "files": {
            "core": PORTABLE_CORE_FILES,
            "memory": [str(f.name) for f in (memory_dir.glob("*.json"))] if memory_dir.exists() else [],
        }
    }
    
    with open(target / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\n[Done] Export complete!")
    print(f"\nTo import on another machine:")
    print(f"  1. Copy the '{target.name}' folder to the machine")
    print(f"  2. Run: python3 sync.py init")
    print(f"  3. Run: python3 sync.py import .")
    
    return target


def import_from_directory(source_path: Path, target_home: Optional[Path] = None):
    """Import optimizer setup from a directory."""
    source = Path(source_path).expanduser()
    
    if not source.exists():
        print(f"[Error] Source directory not found: {source}")
        return False
    
    manifest_path = source / "manifest.json"
    if not manifest_path.exists():
        print(f"[Error] Not a valid export (no manifest.json)")
        return False
    
    with open(manifest_path) as f:
        manifest = json.load(f)
    
    print(f"Importing export from: {manifest.get('exported_at', 'unknown date')}")
    
    # Determine target
    target = target_home or get_optimizer_home()
    print(f"Importing to: {target}")
    
    # Create directory structure
    target.mkdir(parents=True, exist_ok=True)
    (target / "memory").mkdir(parents=True, exist_ok=True)
    
    # Import core files
    print("\n[1/2] Importing core files...")
    for filename in PORTABLE_CORE_FILES:
        src = source / filename
        dst = target / filename
        if src.exists():
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
            print(f"  + {filename}")
    
    # Import memory files
    print("\n[2/2] Importing memory patterns...")
    memory_dir = source / "memory"
    if memory_dir.exists():
        for json_file in memory_dir.glob("*.json"):
            shutil.copy2(json_file, target / "memory" / json_file.name)
            print(f"  + memory/{json_file.name}")
    
    # Optionally import personal files
    if manifest.get("includes_personal"):
        factory = target.parent
        print("\n[+] Importing personal files (droids, skills)...")
        
        # Import droids
        for pattern in PERSONAL_FILES:
            if "*" in pattern:
                base, glob = pattern.split("/")
                src_dir = source / base
                if src_dir.exists():
                    for f in src_dir.glob(glob):
                        dst = factory / base / f.name
                        dst.parent.mkdir(exist_ok=True)
                        shutil.copy2(f, dst)
                        print(f"  + {base}/{f.name}")
        
        # Import skills (subdirectories)
        skills_src = source / "skills"
        skills_dst = factory / "skills"
        if skills_src.exists():
            skills_dst.mkdir(exist_ok=True)
            for skill_dir in skills_src.iterdir():
                if skill_dir.is_dir():
                    dst_dir = skills_dst / skill_dir.name
                    shutil.copytree(skill_dir, dst_dir, dirs_exist_ok=True)
                    print(f"  + skills/{skill_dir.name}/")
    
    print(f"\n[Done] Import complete!")
    return True


def init_in_current_home():
    """Initialize optimizer in current factory home."""
    optimizer = get_optimizer_home()
    
    print(f"Factory home: {get_factory_home()}")
    print(f"Optimizer dir: {optimizer}")
    
    if optimizer.exists():
        print("\n[Skipping] Optimizer already initialized")
        return
    
    # Create directories
    optimizer.mkdir(parents=True, exist_ok=True)
    (optimizer / "memory").mkdir(exist_ok=True)
    
    # Create default profile
    default_profile = {
        "version": 2,
        "modeSupport": {
            "manualAnalysis": True,
            "sessionStartAdvisor": True
        },
        "policy": {
            "recommendOnly": True,
            "autoModifyConfig": False,
            "autoModifyPlugins": False,
            "autoModifyDroids": False
        },
        "memoryFormat": {
            "type": "json-snapshots",
            "humanInspectable": True,
            "rufloIntegration": {
                "enabled": True,
                "fallbackToLocal": True
            }
        },
        "retentionPolicy": {
            "maxRecentRecommendations": 20,
            "maxSessionIds": 50,
            "preferenceTtlDays": 30
        },
        "recommendationThemes": [
            "routing",
            "validation",
            "model-selection",
            "workflow-habits",
            "skill-usage"
        ]
    }
    
    with open(optimizer / "profile.json", "w") as f:
        json.dump(default_profile, f, indent=2)
    
    # Create default state
    default_state = {
        "version": 1,
        "lastUpdated": None,
        "observedPreferences": [],
        "recentRecommendations": [],
        "evidenceSnapshot": {
            "sessionIds": [],
            "notes": []
        }
    }
    
    with open(optimizer / "state.json", "w") as f:
        json.dump(default_state, f, indent=2)
    
    print("\n[Done] Initialized!")
    
    # Create symlinks for scripts if we're in the right place
    src_scripts = Path(__file__).parent
    if src_scripts.name == "optimizer":
        print("\n[+] Setting up bin scripts...")
        
        bin_dir = get_factory_home() / "bin"
        bin_dir.mkdir(exist_ok=True)
        
        for script in ["optimizer", "ruflo-enable", "ruflo-disable"]:
            src = src_scripts.parent / "bin" / script
            dst = bin_dir / script
            if src.exists():
                print(f"  + {script} (already exists)")
            else:
                # Create simple wrapper
                dst.write_text(f"""#!/bin/bash
cd ~/.factory/optimizer && python3 {script}.py "$@"
""")
                dst.chmod(0o755)
                print(f"  + {script} (created)")


def show_status():
    """Show sync status."""
    optimizer = get_optimizer_home()
    factory = get_factory_home()
    
    print("=" * 50)
    print("Sync Status")
    print("=" * 50)
    print(f"Factory home: {factory}")
    print(f"Optimizer dir: {optimizer}")
    print(f"Exists: {optimizer.exists()}")
    
    if optimizer.exists():
        files = list(optimizer.glob("*.py")) + list(optimizer.glob("*.json"))
        print(f"Core files: {len(files)}")
        
        memory = optimizer / "memory"
        if memory.exists():
            memory_files = list(memory.glob("*.json"))
            print(f"Memory files: {len(memory_files)}")
    
    # Check for droids
    droids = factory / "droids"
    if droids.exists():
        droid_files = list(droids.glob("*.md"))
        print(f"Droid files: {len(droid_files)}")
    
    print()
    
    # Check for portable export
    portable = Path("~/optimizer-portable").expanduser()
    if portable.exists():
        manifest = portable / "manifest.json"
        if manifest.exists():
            print(f"[+] Portable export found at: {portable}")
    
    print()
    print("Commands:")
    print("  sync.py export [path]   - Export to portable format")
    print("  sync.py import [path]    - Import from portable format")
    print("  sync.py init             - Initialize in current home")


def main():
    parser = argparse.ArgumentParser(description="Factory Optimizer Sync Tool")
    subparsers = parser.add_subparsers(dest="command")
    
    subparsers.add_parser("init", help="Initialize optimizer in current factory home")
    subparsers.add_parser("status", help="Show sync status")
    
    export_parser = subparsers.add_parser("export", help="Export to portable format")
    export_parser.add_argument("path", nargs="?", default="~/optimizer-portable", help="Export path")
    export_parser.add_argument("--no-personal", action="store_true", help="Exclude droids/skills")
    
    import_parser = subparsers.add_parser("import", help="Import from portable format")
    import_parser.add_argument("path", help="Import source path")
    
    args = parser.parse_args()
    
    if args.command == "export":
        export_to_directory(args.path, include_personal=not args.no_personal)
    elif args.command == "import":
        import_from_directory(args.path)
    elif args.command == "init":
        init_in_current_home()
    elif args.command == "status":
        show_status()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
