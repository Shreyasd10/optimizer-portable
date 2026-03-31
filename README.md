# Factory Optimizer - Portable Setup Guide

Your optimizer is now **portable** and works with any agent platform.

## Supported Platforms

| Platform | Config Location | Auto-Detect |
|----------|------------------|--------------|
| Factory/Droid | `~/.factory` | ✓ |
| Claude Code | `~/.claude` | ✓ |
| OpenAI Codex | `~/.codex` | ✓ |
| Forge | `~/.forge` | ✓ |
| Hermes | `~/.hermes` | ✓ |

## Quick Start on New Machine

### Option 1: Git Sync (Recommended)

```bash
# On your main machine - export
cd ~/.factory/optimizer
python3 sync.py export ~/optimizer-portable

# Push to git
cd ~/optimizer-portable
git init
git add .
git commit -m "Initial optimizer setup"
git remote add origin https://github.com/YOUR/optimizer.git
git push

# On new machine - clone
git clone https://github.com/YOUR/optimizer.git ~/.factory/optimizer

# Setup bin scripts
ln -s ~/.factory/optimizer/optimizer ~/.local/bin/optimizer
ln -s ~/.factory/optimizer/ruflo-enable ~/.local/bin/ruflo-enable
ln -s ~/.factory/optimizer/ruflo-disable ~/.local/bin/ruflo-disable
```

### Option 2: Manual Copy

```bash
# Copy the optimizer folder to new machine
scp -r ~/.factory/optimizer user@new-machine:~/.factory/

# Setup bin scripts
ln -s ~/.factory/optimizer/optimizer ~/.local/bin/optimizer
```

### Option 3: Import from Export

```bash
# Copy export folder
scp -r ~/optimizer-portable user@new-machine:~/

# Import
cd ~/.factory/optimizer
python3 sync.py import ~/optimizer-portable
```

## Commands

```bash
# Core commands
optimizer status          # Check status
optimizer store <key> <val>  # Store pattern
optimizer recall <query>     # Recall patterns
optimizer list            # List all patterns
optimizer doctor          # Health check

# Ruflo toggle
ruflo-enable             # Enable ruflo
ruflo-disable            # Disable ruflo (local only)

# Sync commands
cd ~/.factory/optimizer
python3 sync.py status    # Show sync status
python3 sync.py export    # Export to ~/optimizer-portable
python3 sync.py import    # Import from directory
```

## What Gets Synced

### Core (synced)
- `profile.json` - Configuration
- `state.json` - Learning state
- `*.py` - Python scripts (portable)
- `memory/*.json` - Stored patterns

### Personal (optional)
- `droids/*.md` - Custom droids
- `skills/*.md` - Custom skills

### Not Synced (machine-specific)
- `.ruflo_disabled` - Local ruflo preference
- `.DS_Store` - macOS artifacts
- `__pycache__/` - Python cache

## Per-Platform Notes

### Factory/Droid
Uses `~/.factory` by default. Set `FACTORY_HOME` env var to override.

### Claude Code
Works with Claude Code's config location. Your patterns and learnings sync across.

### Codex
Works with Codex's config. Note: Some hooks may be Codex-specific.

### Forge
Full compatibility with Forge's agent system.

### Hermes
Full compatibility with Hermes's agent system.

## Environment Variables

```bash
FACTORY_HOME=~/.custom-factory  # Override default factory location
```

## Troubleshooting

### "Optimizer not found"
```bash
cd ~/.factory/optimizer
python3 sync.py init
```

### Paths wrong on new machine
The scripts auto-detect paths. If issues occur:
```bash
export FACTORY_HOME=~/.factory
python3 optimizer_cli.py status
```

### Enable ruflo on new machine
```bash
ruflo-enable
npm install -g ruflo  # if not installed
```
