#!/bin/bash
# =============================================================================
# Factory Optimizer - Single-File Installer
# =============================================================================
# Download and setup optimizer, droids, skills, and commands
# Works on any machine with bash + curl
#
# Usage: bash <(curl -fsSL https://raw.githubusercontent.com/Shreyasd10/optimizer-portable/main/setup.sh)
# =============================================================================

set -e

REPO="Shreyasd10/optimizer-portable"
BRANCH="main"
RAW_BASE="https://raw.githubusercontent.com/${REPO}/${BRANCH}"
INSTALL_DIR="${FACTORY_HOME:-$HOME/.factory}"
OPTIMIZER_DIR="$INSTALL_DIR/optimizer"
BIN_DIR="$INSTALL_DIR/bin"
LOCAL_BIN="$HOME/.local/bin"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() { echo -e "${GREEN}[+]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
error() { echo -e "${RED}[x]${NC} $1"; }
info() { echo -e "${BLUE}[i]${NC} $1"; }

echo ""
echo "=============================================="
echo "  Factory Optimizer - Single-File Installer"
echo "=============================================="
echo ""

# Detect existing setup
if [ -d "$OPTIMIZER_DIR" ]; then
    warn "Found existing optimizer at $OPTIMIZER_DIR"
    read -p "Update existing? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        info "Skipping installation"
        exit 0
    fi
fi

# =============================================================================
# Step 1: Create directories
# =============================================================================
log "Creating directory structure..."

mkdir -p "$OPTIMIZER_DIR"
mkdir -p "$OPTIMIZER_DIR/memory"
mkdir -p "$OPTIMIZER_DIR/droids"
mkdir -p "$OPTIMIZER_DIR/skills"
mkdir -p "$BIN_DIR"
mkdir -p "$LOCAL_BIN"

# =============================================================================
# Step 2: Download core files
# =============================================================================
log "Downloading core files..."

download() {
    local url="$1"
    local dest="$2"
    local name=$(basename "$dest")
    
    if curl -fsSL "$url" -o "$dest" 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} $name"
    else
        echo -e "  ${RED}✗${NC} $name (failed)"
        return 1
    fi
}

# Core Python scripts
download "$RAW_BASE/paths.py" "$OPTIMIZER_DIR/paths.py"
download "$RAW_BASE/ruflo_bridge.py" "$OPTIMIZER_DIR/ruflo_bridge.py"
download "$RAW_BASE/optimizer_cli.py" "$OPTIMIZER_DIR/optimizer_cli.py"
download "$RAW_BASE/write_state.py" "$OPTIMIZER_DIR/write_state.py"
download "$RAW_BASE/sync.py" "$OPTIMIZER_DIR/sync.py"

# Config files
download "$RAW_BASE/profile.json" "$OPTIMIZER_DIR/profile.json"
download "$RAW_BASE/state.json" "$OPTIMIZER_DIR/state.json"

# =============================================================================
# Step 3: Download memory patterns
# =============================================================================
log "Downloading memory patterns..."

download "$RAW_BASE/memory/patterns.json" "$OPTIMIZER_DIR/memory/patterns.json" || true
download "$RAW_BASE/memory/test.json" "$OPTIMIZER_DIR/memory/test.json" || true

# =============================================================================
# Step 4: Download droids
# =============================================================================
log "Downloading droids..."

DROIDS=(
    "architect"
    "code-reviewer"
    "coder"
    "debugger"
    "manual-tester"
    "orchestrator"
    "planner"
    "researcher"
    "scrutiny-feature-reviewer"
    "self-optimizer"
    "test-healer"
    "test-implementer"
    "user-testing-flow-validator"
    "worker"
)

for droid in "${DROIDS[@]}"; do
    download "$RAW_BASE/droids/${droid}.md" "$OPTIMIZER_DIR/droids/${droid}.md"
done

# =============================================================================
# Step 5: Download skills
# =============================================================================
log "Downloading skills..."

SKILLS=(
    "adversarial-review"
    "brainstorming"
    "code-review"
    "code-simplify"
    "continuous-learning"
    "create-plan"
    "create-pr"
    "edge-case-hunter"
    "grill-me"
    "manual-test-design"
    "prompt-optimizer"
    "refactor"
    "replanning-changes"
    "search-first"
    "security-review"
    "skill-comply"
    "tdd-driver"
    "test-strategy"
    "verification-loop"
)

for skill in "${SKILLS[@]}"; do
    mkdir -p "$OPTIMIZER_DIR/skills/$skill"
    download "$RAW_BASE/skills/${skill}/SKILL.md" "$OPTIMIZER_DIR/skills/${skill}/SKILL.md"
done

# =============================================================================
# Step 6: Create bin scripts
# =============================================================================
log "Creating command scripts..."

cat > "$BIN_DIR/optimizer" << 'BINEOF'
#!/bin/bash
cd ~/.factory/optimizer 2>/dev/null || cd ~/.droid/optimizer 2>/dev/null
if [ -f "optimizer_cli.py" ]; then
    python3 optimizer_cli.py "$@"
else
    echo "Optimizer not found. Run setup again."
    exit 1
fi
BINEOF

cat > "$BIN_DIR/ruflo-enable" << 'BINEOF'
#!/bin/bash
cd ~/.factory/optimizer && python3 optimizer_cli.py ruflo-enable
BINEOF

cat > "$BIN_DIR/ruflo-disable" << 'BINEOF'
#!/bin/bash
cd ~/.factory/optimizer && python3 optimizer_cli.py ruflo-disable
BINEOF

chmod +x "$BIN_DIR/optimizer"
chmod +x "$BIN_DIR/ruflo-enable"
chmod +x "$BIN_DIR/ruflo-disable"

# Create symlinks in ~/.local/bin
ln -sf "$BIN_DIR/optimizer" "$LOCAL_BIN/optimizer" 2>/dev/null || true
ln -sf "$BIN_DIR/ruflo-enable" "$LOCAL_BIN/ruflo-enable" 2>/dev/null || true
ln -sf "$BIN_DIR/ruflo-disable" "$LOCAL_BIN/ruflo-disable" 2>/dev/null || true

echo -e "  ${GREEN}✓${NC} optimizer"
echo -e "  ${GREEN}✓${NC} ruflo-enable"
echo -e "  ${GREEN}✓${NC} ruflo-disable"

# =============================================================================
# Step 7: Add to PATH if needed
# =============================================================================
log "Checking PATH..."

if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    warn "Adding $BIN_DIR to PATH in ~/.zshrc"
    echo 'export PATH="$HOME/.factory/bin:$PATH"' >> "$HOME/.zshrc"
    export PATH="$BIN_DIR:$PATH"
fi

if [[ ":$PATH:" != *":$LOCAL_BIN:"* ]]; then
    warn "Adding $LOCAL_BIN to PATH in ~/.zshrc"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
    export PATH="$LOCAL_BIN:$PATH"
fi

# =============================================================================
# Step 8: Make Python scripts executable
# =============================================================================
chmod +x "$OPTIMIZER_DIR/paths.py"
chmod +x "$OPTIMIZER_DIR/ruflo_bridge.py"
chmod +x "$OPTIMIZER_DIR/optimizer_cli.py"
chmod +x "$OPTIMIZER_DIR/write_state.py"
chmod +x "$OPTIMIZER_DIR/sync.py"

# =============================================================================
# Done!
# =============================================================================
echo ""
echo "=============================================="
log "Setup complete!"
echo "=============================================="
echo ""
info "Installed to: $INSTALL_DIR"
info "Optimizer dir: $OPTIMIZER_DIR"
info "Commands: $BIN_DIR"
echo ""
echo "Commands available:"
echo "  optimizer status"
echo "  optimizer store <key> <value>"
echo "  optimizer recall <query>"
echo "  optimizer list"
echo "  optimizer doctor"
echo "  ruflo-enable"
echo "  ruflo-disable"
echo ""
echo "Run 'optimizer status' to verify!"
echo ""
