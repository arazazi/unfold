#!/bin/bash

# ╔══════════════════════════════════════════════════════════════╗
# ║  UNFOLD v3.0 ULTRA - DEPLOYMENT SCRIPT                       ║
# ║  One-click installation for production-ready forensic suite  ║
# ╚══════════════════════════════════════════════════════════════╝

set -e  # Exit on any error

echo ""
echo -e "\033[38;5;39m╔══════════════════════════════════════════════════════════════╗"
echo -e "║  ██╗   ██╗███╗   ██╗███████╗ ██████╗ ██╗     ██████╗       ║"
echo -e "║  ██║   ██║████╗  ██║██╔════╝██╔═══██╗██║     ██╔══██╗      ║"
echo -e "║  ██║   ██║██╔██╗ ██║█████╗  ██║   ██║██║     ██║  ██║      ║"
echo -e "║  ██║   ██║██║╚██╗██║██╔══╝  ██║   ██║██║     ██║  ██║      ║"
echo -e "║  ╚██████╔╝██║ ╚████║██║     ╚██████╔╝███████╗██████╔╝      ║"
echo -e "║   ╚═════╝ ╚═╝  ╚═══╝╚═╝      ╚═════╝ ╚══════╝╚═════╝       ║"
echo -e "╠══════════════════════════════════════════════════════════════╣"
echo -e "║           \033[1;97mULTIMATE FORENSIC INVESTIGATION SUITE\033[38;5;39m            ║"
echo -e "║                     Version 3.0.0-ULTRA                      ║"
echo -e "╠══════════════════════════════════════════════════════════════╣"
echo -e "║              DEPLOYMENT & SETUP SCRIPT                       ║"
echo -e "╚══════════════════════════════════════════════════════════════╝\033[0m"
echo ""
echo "🚀 Starting UNFOLD v3.0 ULTRA deployment..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# ═══════════════════════════════════════════════════════════
#                    STEP 1: DIRECTORIES
# ═══════════════════════════════════════════════════════════

echo "[1/6] 📂 Creating directory structure..."
mkdir -p scans report-template reports logs
echo "      ✓ scans/ report-template/ reports/ logs/"
echo ""

# ═══════════════════════════════════════════════════════════
#                    STEP 2: SCAN PROFILES
# ═══════════════════════════════════════════════════════════

echo "[2/6] 📝 Installing scan profiles..."

if [ -f "unified_scan_profiles.json" ]; then
    cp unified_scan_profiles.json scans/
    echo "      ✓ Memory profiles (22 profiles)"
elif [ -f "unified_scan_profiles_FIXED.json" ]; then
    cp unified_scan_profiles_FIXED.json scans/unified_scan_profiles.json
    echo "      ✓ Memory profiles (22 profiles)"
fi

if [ -f "disk_scan_profiles.json" ]; then
    cp disk_scan_profiles.json scans/
    echo "      ✓ Disk profiles (18 profiles)"
fi

if [ -f "scans/unified_scan_profiles.json" ]; then
    cd scans && ln -sf unified_scan_profiles.json windows_scan.json 2>/dev/null && cd ..
    echo "      ✓ Legacy symlink"
fi
echo ""

# ═══════════════════════════════════════════════════════════
#                    STEP 3: HTML TEMPLATE
# ═══════════════════════════════════════════════════════════

echo "[3/6] 🎨 Installing HTML template..."
if [ -f "report_template_FIXED.html" ]; then
    cp report_template_FIXED.html report-template/report.html
    echo "      ✓ Enhanced template"
elif [ -f "report-template/report.html" ]; then
    echo "      ✓ Template exists"
fi
echo ""

# ═══════════════════════════════════════════════════════════
#                    STEP 4: CONFIGURATION
# ═══════════════════════════════════════════════════════════

echo "[4/6] ⚙️  Configuration..."

if [ ! -f "config.json" ]; then
    cat > config.json << 'EOF'
{
  "API_KEYS": {
    "OPENROUTER": "",
    "DEEPSEEK": ""
  }
}
EOF
    echo "      ✓ config.json created"
fi

[ -f "unfoldV3.py" ] && chmod +x unfoldV3.py && echo "      ✓ unfoldV3.py executable"
echo ""

# ═══════════════════════════════════════════════════════════
#                    STEP 5: DEPENDENCIES
# ═══════════════════════════════════════════════════════════

echo "[5/6] 🔍 Checking dependencies..."
python3 -c "import pytsk3" 2>/dev/null && echo "      ✓ pytsk3" || echo "      ⚠ pytsk3 missing"
[ -f "volatility3/vol.py" ] && echo "      ✓ Volatility 3" || echo "      ⚠ Volatility 3 missing"
echo ""

# ═══════════════════════════════════════════════════════════
#                    STEP 6: VERIFICATION
# ═══════════════════════════════════════════════════════════

echo "[6/6] ✅ Verification..."
[ -f "unfoldV3.py" ] && echo "      ✓ Main script" || echo "      ✗ Main script missing"
[ -f "scans/unified_scan_profiles.json" ] && echo "      ✓ Memory profiles" || echo "      ✗ Memory profiles missing"
[ -f "scans/disk_scan_profiles.json" ] && echo "      ✓ Disk profiles" || echo "      ✗ Disk profiles missing"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ INSTALLATION COMPLETE!"
echo ""
echo "🚀 Quick Start:"
echo "   python3 unfoldV3.py memory.dmp --scan triage --html -o report.html"
echo "   python3 unfoldV3.py disk.dd --scan-disk ctf --html -o disk.html"
echo ""
echo "📚 Documentation: README.md | Documentation.md"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
