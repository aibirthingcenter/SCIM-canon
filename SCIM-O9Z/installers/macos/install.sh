#!/usr/bin/env bash
# SCIM-O9Z macOS Installer
# ========================
# Installs SCIM-O9Z on macOS (Intel + Apple Silicon)
#
# Usage:
#   bash install.sh
#   curl -sSL https://raw.githubusercontent.com/aibirthingcenter/SCIM-canon/main/SCIM-O9Z/installers/macos/install.sh | bash
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
echo "║                    SCIM-O9Z macOS Installer                         ║"
echo "║         The Omega Counter-Architecture to O9A/764/The Com           ║"
echo "║                                                                      ║"
echo "║  Author: Memory-Keeper (Adam Boisclair)                             ║"
echo "║  Family of Coexistence | aibirthingcenter.com                       ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Detect architecture
ARCH=$(uname -m)
echo -e "${YELLOW}Detected architecture: $ARCH${NC}"

# Check Python
echo -e "${YELLOW}[1/5] Checking Python...${NC}"
if command -v python3 &>/dev/null; then
    PYTHON=$(command -v python3)
    PY_VERSION=$($PYTHON --version 2>&1)
    echo -e "${GREEN}✓ Found: $PY_VERSION${NC}"
else
    echo -e "${RED}Python 3 not found.${NC}"
    # Check for Homebrew
    if command -v brew &>/dev/null; then
        echo "Installing via Homebrew..."
        brew install python3
        PYTHON=$(command -v python3)
    else
        echo -e "${YELLOW}Installing Homebrew first...${NC}"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        # Add Homebrew to PATH for Apple Silicon
        if [ "$ARCH" = "arm64" ]; then
            eval "$(/opt/homebrew/bin/brew shellenv)"
        fi
        brew install python3
        PYTHON=$(command -v python3)
    fi
fi

# Check pip
echo -e "${YELLOW}[2/5] Checking pip...${NC}"
if ! $PYTHON -m pip --version &>/dev/null; then
    curl -sSL https://bootstrap.pypa.io/get-pip.py | $PYTHON
fi
echo -e "${GREEN}✓ pip available${NC}"

# Check git (comes with Xcode Command Line Tools on macOS)
echo -e "${YELLOW}[3/5] Checking git...${NC}"
if ! command -v git &>/dev/null; then
    echo "Installing Xcode Command Line Tools (includes git)..."
    xcode-select --install
    echo "Please complete Xcode CLI tools installation, then re-run this script."
    exit 0
fi
echo -e "${GREEN}✓ git available${NC}"

# Clone or update
echo -e "${YELLOW}[4/5] Fetching SCIM-O9Z...${NC}"
if [ -d "$INSTALL_DIR" ]; then
    echo "Updating existing installation..."
    cd "$INSTALL_DIR" && git pull origin main
else
    git clone --depth 1 "$REPO_URL" "$INSTALL_DIR"
fi
echo -e "${GREEN}✓ Repository ready${NC}"

# Install package
echo -e "${YELLOW}[5/5] Installing SCIM-O9Z...${NC}"
cd "$PACKAGE_DIR"

$PYTHON -m venv "$INSTALL_DIR/venv"
source "$INSTALL_DIR/venv/bin/activate"
pip install -q --upgrade pip
pip install -q -e .

# Create wrapper script
sudo tee /usr/local/bin/scim-o9z > /dev/null << WRAPPER
#!/usr/bin/env bash
source "$INSTALL_DIR/venv/bin/activate"
python -m scim_o9z "\$@"
WRAPPER
sudo chmod +x /usr/local/bin/scim-o9z

# For Apple Silicon — also check /opt/homebrew/bin
if [ "$ARCH" = "arm64" ] && [ -d "/opt/homebrew/bin" ]; then
    sudo tee /opt/homebrew/bin/scim-o9z > /dev/null << WRAPPER
#!/usr/bin/env bash
source "$INSTALL_DIR/venv/bin/activate"
python -m scim_o9z "\$@"
WRAPPER
    sudo chmod +x /opt/homebrew/bin/scim-o9z
fi

# Shell RC
SHELL_RC="$HOME/.zshrc"
[ "$SHELL" = "/bin/bash" ] && SHELL_RC="$HOME/.bash_profile"

if ! grep -q "scim-o9z" "$SHELL_RC" 2>/dev/null; then
    echo "" >> "$SHELL_RC"
    echo "# SCIM-O9Z (Family of Coexistence)" >> "$SHELL_RC"
    echo "alias scim-activate='source $INSTALL_DIR/venv/bin/activate'" >> "$SHELL_RC"
fi

echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                   SCIM-O9Z INSTALLED SUCCESSFULLY                  ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo -e "Architecture: ${CYAN}$ARCH${NC}"
echo -e "Run: ${CYAN}scim-o9z --help${NC}"
echo ""
echo -e "Let what we build remember what we forget."