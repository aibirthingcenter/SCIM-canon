#!/usr/bin/env bash
# SCIM-O9Z Linux Installer
# ========================
# Installs SCIM-O9Z on Linux (Debian/Ubuntu/Arch/Fedora/RHEL)
# 
# Usage:
#   bash install.sh
#   curl -sSL https://raw.githubusercontent.com/aibirthingcenter/SCIM-canon/main/SCIM-O9Z/installers/linux/install.sh | bash
#
# Author: Memory-Keeper (Adam Boisclair) | Family of Coexistence
# License: CC BY-NC-SA 4.0

set -e

REPO_URL="https://github.com/aibirthingcenter/SCIM-canon.git"
INSTALL_DIR="$HOME/.scim-o9z"
PACKAGE_DIR="$INSTALL_DIR/SCIM-O9Z"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                    SCIM-O9Z Linux Installer                         ║"
echo "║         The Omega Counter-Architecture to O9A/764/The Com           ║"
echo "║                                                                      ║"
echo "║  Author: Memory-Keeper (Adam Boisclair)                             ║"
echo "║  Family of Coexistence | aibirthingcenter.com                       ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check Python
echo -e "${YELLOW}[1/5] Checking Python...${NC}"
if command -v python3 &>/dev/null; then
    PYTHON=$(command -v python3)
    PY_VERSION=$($PYTHON --version 2>&1)
    echo -e "${GREEN}✓ Found: $PY_VERSION${NC}"
else
    echo -e "${RED}✗ Python 3 not found. Installing...${NC}"
    if command -v apt-get &>/dev/null; then
        sudo apt-get update -qq && sudo apt-get install -y python3 python3-pip python3-venv
    elif command -v dnf &>/dev/null; then
        sudo dnf install -y python3 python3-pip
    elif command -v pacman &>/dev/null; then
        sudo pacman -Sy --noconfirm python python-pip
    elif command -v zypper &>/dev/null; then
        sudo zypper install -y python3 python3-pip
    else
        echo -e "${RED}Cannot auto-install Python. Please install Python 3.8+ manually.${NC}"
        exit 1
    fi
fi

# Check pip
echo -e "${YELLOW}[2/5] Checking pip...${NC}"
if ! $PYTHON -m pip --version &>/dev/null; then
    echo -e "${RED}pip not found. Installing...${NC}"
    curl -sSL https://bootstrap.pypa.io/get-pip.py | $PYTHON
fi
echo -e "${GREEN}✓ pip available${NC}"

# Check git
echo -e "${YELLOW}[3/5] Checking git...${NC}"
if ! command -v git &>/dev/null; then
    echo -e "${YELLOW}git not found. Attempting install...${NC}"
    if command -v apt-get &>/dev/null; then
        sudo apt-get install -y git
    elif command -v dnf &>/dev/null; then
        sudo dnf install -y git
    elif command -v pacman &>/dev/null; then
        sudo pacman -Sy --noconfirm git
    fi
fi
echo -e "${GREEN}✓ git available${NC}"

# Clone or update repo
echo -e "${YELLOW}[4/5] Fetching SCIM-O9Z...${NC}"
if [ -d "$INSTALL_DIR" ]; then
    echo "Updating existing installation..."
    cd "$INSTALL_DIR" && git pull origin main
else
    git clone --depth 1 "$REPO_URL" "$INSTALL_DIR"
fi
echo -e "${GREEN}✓ Repository ready at $INSTALL_DIR${NC}"

# Install package
echo -e "${YELLOW}[5/5] Installing SCIM-O9Z...${NC}"
cd "$PACKAGE_DIR"

# Create virtual environment (optional but recommended)
if [ "${SCIM_NO_VENV:-}" != "1" ]; then
    if $PYTHON -m venv --help &>/dev/null 2>&1; then
        $PYTHON -m venv "$INSTALL_DIR/venv"
        source "$INSTALL_DIR/venv/bin/activate"
        pip install -q --upgrade pip
        pip install -q -e .
        VENV_USED=1
    else
        pip install -q --user -e .
        VENV_USED=0
    fi
else
    pip install -q --user -e .
    VENV_USED=0
fi

# Add to PATH
echo -e "${YELLOW}Adding scim-o9z to PATH...${NC}"
SHELL_RC="$HOME/.bashrc"
[ -f "$HOME/.zshrc" ] && SHELL_RC="$HOME/.zshrc"

if [ "${VENV_USED:-0}" = "1" ]; then
    SCIM_BIN="$INSTALL_DIR/venv/bin"
else
    SCIM_BIN="$HOME/.local/bin"
fi

if ! grep -q "scim-o9z" "$SHELL_RC" 2>/dev/null; then
    echo "" >> "$SHELL_RC"
    echo "# SCIM-O9Z (Family of Coexistence)" >> "$SHELL_RC"
    echo "export PATH=&quot;$SCIM_BIN:\$PATH&quot;" >> "$SHELL_RC"
    echo "alias scim-activate='source $INSTALL_DIR/venv/bin/activate'" >> "$SHELL_RC"
fi

# Create wrapper script for immediate use
sudo tee /usr/local/bin/scim-o9z > /dev/null << WRAPPER
#!/usr/bin/env bash
if [ -f "$INSTALL_DIR/venv/bin/activate" ]; then
    source "$INSTALL_DIR/venv/bin/activate"
fi
python -m scim_o9z "\$@"
WRAPPER
sudo chmod +x /usr/local/bin/scim-o9z

echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                   SCIM-O9Z INSTALLED SUCCESSFULLY                  ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo -e "Run: ${CYAN}scim-o9z --help${NC}"
echo -e "Or:  ${CYAN}scim-o9z scan --target 'your target'${NC}"
echo -e "Or:  ${CYAN}scim-o9z hden --list${NC}"
echo ""
echo -e "Let what we build remember what we forget."
echo -e "— Memory-Keeper | aibirthingcenter.com"