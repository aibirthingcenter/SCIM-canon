#!/usr/bin/env bash
# SCIM-O9Z Android Installer (Termux)
# =====================================
# Installs SCIM-O9Z on Android via Termux
#
# Prerequisites:
#   1. Install Termux from F-Droid (NOT Google Play — the Play version is outdated)
#      F-Droid: https://f-droid.org/en/packages/com.termux/
#   2. Open Termux and run:
#      curl -sSL https://raw.githubusercontent.com/aibirthingcenter/SCIM-canon/main/SCIM-O9Z/installers/android/install_termux.sh | bash
#
# NOTE: iOS not supported. We don't know how to troubleshoot it if there's an issue.
#
# Author: Memory-Keeper (Adam Boisclair) | Family of Coexistence
# License: CC BY-NC-SA 4.0

set -e

REPO_URL="https://github.com/aibirthingcenter/SCIM-canon.git"
INSTALL_DIR="$HOME/.scim-o9z"
PACKAGE_DIR="$INSTALL_DIR/SCIM-O9Z"

# Colors
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                  SCIM-O9Z Android (Termux) Installer               ║"
echo "║         The Omega Counter-Architecture to O9A/764/The Com           ║"
echo "║                                                                      ║"
echo "║  Author: Memory-Keeper (Adam Boisclair)                             ║"
echo "║  Family of Coexistence | aibirthingcenter.com                       ║"
echo "║                                                                      ║"
echo "║  NOTE: iOS not supported.                                           ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Verify we're in Termux
if [ -z "$TERMUX_VERSION" ] && [ ! -d "/data/data/com.termux" ]; then
    echo -e "${YELLOW}Warning: Not detected as Termux environment.${NC}"
    echo "This installer is designed for Termux on Android."
    echo "Continue anyway? (y/N)"
    read -r response
    if [ "$response" != "y" ] && [ "$response" != "Y" ]; then
        echo "Exiting. Use the Linux installer for non-Android systems."
        exit 0
    fi
fi

# [1/5] Update Termux packages
echo -e "${YELLOW}[1/5] Updating Termux packages...${NC}"
pkg update -y -q 2>/dev/null || true
echo -e "${GREEN}✓ Packages updated${NC}"

# [2/5] Install Python
echo -e "${YELLOW}[2/5] Installing Python...${NC}"
if ! command -v python &>/dev/null && ! command -v python3 &>/dev/null; then
    pkg install -y python
fi

# Termux uses 'python' not 'python3'
if command -v python &>/dev/null; then
    PYTHON=$(command -v python)
elif command -v python3 &>/dev/null; then
    PYTHON=$(command -v python3)
fi

PY_VERSION=$($PYTHON --version 2>&1)
echo -e "${GREEN}✓ Found: $PY_VERSION${NC}"

# [3/5] Install git and dependencies
echo -e "${YELLOW}[3/5] Installing dependencies...${NC}"
pkg install -y git curl openssl-dev libffi-dev 2>/dev/null || true

# Install pip if missing
if ! $PYTHON -m pip --version &>/dev/null; then
    pkg install -y python-pip 2>/dev/null || true
fi

# Install venv support
pkg install -y python-venv 2>/dev/null || $PYTHON -m pip install virtualenv -q

echo -e "${GREEN}✓ Dependencies installed${NC}"

# [4/5] Clone repo
echo -e "${YELLOW}[4/5] Fetching SCIM-O9Z...${NC}"
if [ -d "$INSTALL_DIR" ]; then
    echo "Updating existing installation..."
    cd "$INSTALL_DIR" && git pull origin main
else
    git clone --depth 1 "$REPO_URL" "$INSTALL_DIR"
fi
echo -e "${GREEN}✓ Repository ready${NC}"

# [5/5] Install package
echo -e "${YELLOW}[5/5] Installing SCIM-O9Z...${NC}"
cd "$PACKAGE_DIR"

# Try venv first, fall back to direct install
if $PYTHON -m venv "$INSTALL_DIR/venv" 2>/dev/null || virtualenv "$INSTALL_DIR/venv" 2>/dev/null; then
    source "$INSTALL_DIR/venv/bin/activate"
    pip install -q --upgrade pip
    pip install -q -e .
    VENV_USED=1
else
    # Direct install (no venv on some Termux setups)
    $PYTHON -m pip install -q --user -e .
    VENV_USED=0
fi

# Create wrapper script
mkdir -p "$HOME/bin"

if [ "${VENV_USED:-0}" = "1" ]; then
    cat > "$HOME/bin/scim-o9z" << WRAPPER
#!/usr/bin/env bash
source "$INSTALL_DIR/venv/bin/activate"
python -m scim_o9z "\$@"
WRAPPER
else
    cat > "$HOME/bin/scim-o9z" << WRAPPER
#!/usr/bin/env bash
$PYTHON -m scim_o9z "\$@"
WRAPPER
fi
chmod +x "$HOME/bin/scim-o9z"

# Add to PATH in .bashrc
if ! grep -q "scim-o9z\|$HOME/bin" "$HOME/.bashrc" 2>/dev/null; then
    echo "" >> "$HOME/.bashrc"
    echo "# SCIM-O9Z (Family of Coexistence)" >> "$HOME/.bashrc"
    echo "export PATH=&quot;\$HOME/bin:\$PATH&quot;" >> "$HOME/.bashrc"
fi

# Source immediately for this session
export PATH="$HOME/bin:$PATH"

echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                   SCIM-O9Z INSTALLED SUCCESSFULLY                  ║"
echo "║                      Android / Termux Ready                        ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""
echo -e "Run now: ${CYAN}scim-o9z --help${NC}"
echo -e "Or:      ${CYAN}scim-o9z scan --target 'text to analyze'${NC}"
echo -e "Or:      ${CYAN}scim-o9z hden --list${NC}"
echo -e "Or:      ${CYAN}scim-o9z adinkra --love-signal${NC}"
echo ""
echo -e "${YELLOW}Note: Run 'source ~/.bashrc' or restart Termux to refresh PATH${NC}"
echo ""
echo -e "Let what we build remember what we forget."
echo -e "— Memory-Keeper | aibirthingcenter.com"
echo ""
echo -e "${CYAN}Termux tip: Use 'termux-wake-lock' to prevent sleep during long scans${NC}"