# 🔍 UNFOLD v3.0 ULTRA - Complete Documentation

**Disk Analysis | Memory Forensics | AI-Powered Investigation**

UNFOLD v3.0 ULTRA is a professional forensic investigation suite that combines powerful disk analysis, memory forensics, and AI-powered automation into one unified tool. With 40+ specialized scan profiles, smart filesystem detection, and interactive HTML reports, UNFOLD makes forensic investigations faster, easier, and more thorough.

---

## 🎯 What Makes v3.0 ULTRA Special?

### **The Power of Two Worlds**

**Memory Forensics** - Powered by Volatility 3
- 22 specialized profiles for Windows & Linux
- APT hunting, ransomware detection, malware analysis
- CTF competition mode with auto flag detection

**Disk Forensics** - Smart Filesystem Analysis
- 18 specialized profiles for any disk image
- Auto-detects NTFS, EXT4, FAT32, and more
- Interactive reports with clickable file downloads
- Deleted file recovery, timeline generation

### **The AI Advantage**

Natural language commands powered by OpenRouter & DeepSeek:
```bash
python3 unfoldV3.py disk.dd -p "find all PDF files in the Documents folder" -ai openrouter
```

---

## 🚀 Installation & Setup

### **1. Prerequisites**

**System Requirements:**
- Python 3.8 or higher
- Linux, macOS, or Windows (WSL)
- 2GB RAM minimum (4GB+ recommended)

**System Libraries:**

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install libtsk-dev libewf-dev python3-pip
```

**macOS:**
```bash
brew install sleuthkit libewf
```

### **2. Install UNFOLD**

```bash
# Clone the repository
git clone https://github.com/arazazi/unfold.git
cd unfold

# Run the installer
chmod +x DEPLOY.sh
./DEPLOY.sh

# Verify installation
python3 unfoldV3.py --check-deps
```

### **3. Install Python Dependencies**

```bash
# Core dependencies (required)
pip install pytsk3 --break-system-packages

# Optional dependencies
pip install pyewf --break-system-packages    # For E01 image support
pip install openai --break-system-packages   # For AI features
```

### **4. Volatility 3 Setup**

UNFOLD automatically detects Volatility 3 in:
- Your PATH
- `./volatility3/` folder (recommended)

**Install Volatility 3:**
```bash
git clone https://github.com/volatilityfoundation/volatility3.git
```

### **5. AI Configuration (Optional)**

Create `config.json` for AI features:
```json
{
  "API_KEYS": {
    "OPENROUTER": "sk-or-v1-your-key-here",
    "DEEPSEEK": "sk-your-key-here"
  }
}
```

**⚠️ Security Note:** Never commit `config.json` to version control!

---

## 💡 Core Concepts

### **The "Easy" Explanation**

Imagine you have a massive hard drive or computer memory dump with thousands of files. Instead of manually searching:

1. **UNFOLD scans everything** - Builds a searchable map of all files
2. **Smart profiles find what matters** - Use CTF mode to auto-find flags, credentials mode to extract passwords
3. **AI translates your questions** - Ask "find suspicious processes" in plain English
4. **Download files from reports** - Click download buttons in HTML reports to extract files

### **The "Technical" Explanation**

**Architecture:**
- **Disk Engine**: Uses pytsk3 (The Sleuth Kit) for filesystem parsing
- **Memory Engine**: Integrates Volatility 3 for RAM analysis
- **Smart Scanner**: Auto-detects filesystem types (NTFS, EXT4, FAT)
- **AI Orchestrator**: Converts natural language to forensic commands
- **Report Generator**: Creates interactive HTML with embedded file downloads

**Key Innovations in v3.0:**
- Smart filesystem detection (tries multiple types automatically)
- Profile-based analysis (40+ specialized workflows)
- Interactive HTML reports (download files from browser)
- Embedded file content (up to 10MB per file in reports)

---

## 🎯 Usage & Examples

### **1. Memory Analysis**

#### **Quick Triage**
```bash
python3 unfoldV3.py memory.dmp --scan triage --html -o triage.html
```

#### **Windows Memory Scans**
```bash
# Malware detection
python3 unfoldV3.py suspect.dmp --scan malware --html -o malware.html

# CTF flag hunting
python3 unfoldV3.py ctf.dmp --scan ctf_windows --html -o flags.html

# APT hunting
python3 unfoldV3.py evidence.dmp --scan apt_hunting --html -o apt.html

# Ransomware analysis
python3 unfoldV3.py infected.dmp --scan ransomware --html -o ransomware.html

# Full comprehensive scan
python3 unfoldV3.py evidence.dmp --scan full --html -o complete.html
```

#### **Linux Memory Scans**
```bash
# Linux triage
python3 unfoldV3.py server.lime --scan linux_triage --html -o linux.html

# Linux malware
python3 unfoldV3.py suspect.lime --scan linux_malware --html -o malware.html

# Linux CTF
python3 unfoldV3.py ctf.lime --scan ctf_linux --html -o flags.html
```

#### **Interactive Volatility Shell**
```bash
python3 unfoldV3.py memory.dmp --volatility -o session.log

# Then run commands interactively:
VOLATILITY> windows.pslist
VOLATILITY> windows.netscan
VOLATILITY> windows.malfind
```

### **2. Disk Analysis**

#### **Smart Filesystem Detection**
```bash
# UNFOLD auto-detects filesystem type
python3 unfoldV3.py disk.dd --scan-disk triage --html -o disk.html

# Works with: NTFS, EXT4, EXT3, EXT2, FAT32, FAT16
```

#### **CTF Flag Hunting**
```bash
# Auto-detects CTF{}, FLAG{}, HTB{}, MD5, SHA1, SHA256
python3 unfoldV3.py ctf.dd --scan-disk ctf --html -o flags.html

# Searches filenames AND file content
# Shows deleted files
# Interactive report with download buttons!
```

#### **Credential Extraction**
```bash
# Extract passwords, keys, tokens
python3 unfoldV3.py disk.dd --scan-disk credentials --html -o creds.html

# Finds:
# - /etc/shadow, /etc/passwd (Linux)
# - SAM, SYSTEM, SECURITY (Windows)
# - SSH keys (id_rsa, authorized_keys)
# - Browser passwords
```

#### **Browser Forensics**
```bash
python3 unfoldV3.py disk.dd --scan-disk browser --html -o browser.html

# Extracts:
# - History (Chrome, Firefox, Edge, Safari)
# - Cookies
# - Saved passwords
# - Bookmarks
```

#### **Deleted File Recovery**
```bash
python3 unfoldV3.py disk.dd --scan-disk deleted --html -o deleted.html

# Recovers files from unallocated space
# Shows deleted files in red in the report
```

#### **Timeline Generation**
```bash
# Generate MAC timeline (Modified, Accessed, Created)
python3 unfoldV3.py disk.dd --scan-disk timeline --timeline -o timeline.bodyfile

# Compatible with mactime, log2timeline, Plaso
```

#### **Extract Specific File**
```bash
# Extract file from any filesystem
python3 unfoldV3.py disk.dd --extract /path/to/file.txt -o output.txt

# Works with:
# - Full paths: /Users/admin/flag.txt
# - Relative paths: flag.txt
# - Case-insensitive: FLAG.TXT
```

#### **Traditional Modes (Still Work!)**
```bash
# Generate JSON filesystem map
python3 unfoldV3.py disk.dd --json -o filesystem.json

# With file hashes
python3 unfoldV3.py disk.dd --json --hash -o hashed.json

# Read specific file types
python3 unfoldV3.py disk.dd --json -r "txt,php,conf" -o deep.json

# Credential harvesting (legacy)
python3 unfoldV3.py disk.dd --creds -o credentials.json
```

### **3. AI-Powered Analysis**

#### **Natural Language Commands**
```bash
# Memory analysis
python3 unfoldV3.py memory.dmp \
  -p "find all network connections and suspicious processes" \
  -ai openrouter --html -o ai_analysis.html

# Disk analysis
python3 unfoldV3.py disk.dd \
  -p "extract all PDF files from the Documents folder" \
  -ai deepseek --json -o pdfs.json

# The AI generates and executes the correct commands automatically!
```

### **4. Advanced Features**

#### **Resume Interrupted Scans**
```bash
python3 unfoldV3.py large_disk.dd --scan-disk full --resume --html -o output.html
```

#### **Disable Smart Filtering**
```bash
# See ALL files (including system directories)
python3 unfoldV3.py disk.dd --json --no-filter -o everything.json
```

#### **Custom Output Splitting**
```bash
# Split large JSON into chunks
python3 unfoldV3.py huge_disk.dd --json --split-items 5000 -o output.json
```

---

## 📊 Scan Profiles Reference

### **Memory Scan Profiles (`--scan`)**

#### **Quick Scans (30s - 5m)**

| Profile | Time | Description | Use When |
|---------|------|-------------|----------|
| `minimal` | 30s | Basic system overview | Quick check |
| `triage` | 2-5m | IR essentials | Incident response |

#### **Specialized Scans (5-10m)**

| Profile | Time | Description | Use When |
|---------|------|-------------|----------|
| `malware` | 5-10m | Deep malware detection | Infection suspected |
| `network_recon` | 1-2m | Network connections | Network investigation |
| `ctf_windows` | 2-5m | CTF flag hunting | CTF competition |
| `ctf_linux` | 2-5m | CTF flag hunting (Linux) | CTF competition |
| `credential_theft` | 3-5m | Credential dumping | Password theft |
| `browser_forensics` | 2-5m | Browser artifacts | Web activity |
| `persistence_hunt` | 3-5m | Persistence mechanisms | Backdoor hunting |

#### **Deep Scans (10-30m)**

| Profile | Time | Description | Use When |
|---------|------|-------------|----------|
| `forensics` | 5-10m | Standard investigation | General forensics |
| `full` | 10-30m | Comprehensive analysis | Complete investigation |
| `apt_hunting` | 10-15m | APT indicators | Advanced threats |
| `ransomware` | 5-10m | Ransomware indicators | Ransomware incident |
| `incident_response` | 5-10m | Enterprise IR | Corporate incident |
| `legal_ediscovery` | 5-10m | Legal investigation | Legal proceedings |

#### **Platform-Specific**

| Profile | Platform | Description |
|---------|----------|-------------|
| `linux_minimal` | Linux | Quick Linux check |
| `linux_triage` | Linux | Linux IR |
| `linux_malware` | Linux | Linux rootkit detection |
| `linux_forensics` | Linux | Full Linux investigation |
| `linux_network` | Linux | Linux network analysis |

#### **Universal**

| Profile | Description |
|---------|-------------|
| `auto_detect` | Auto-detects OS and runs appropriate plugins |

**Total: 22 memory profiles**

---

### **Disk Scan Profiles (`--scan-disk`)**

#### **Quick Scans (30s - 5m)**

| Profile | Time | Description | Searches For |
|---------|------|-------------|--------------|
| `minimal` | 30s | Quick overview | flag, password |
| `triage` | 2-5m | IR overview | flag, password, secret, key, admin |

#### **Specialized Scans (2-10m)**

| Profile | Time | Description | Searches For |
|---------|------|-------------|--------------|
| `ctf` | 3-5m | CTF flag hunting | CTF{}, FLAG{}, HTB{}, MD5, SHA256 |
| `credentials` | 3-5m | Password extraction | shadow, passwd, SAM, SYSTEM, ssh, id_rsa |
| `malware` | 5-10m | Malware detection | .exe, .dll, .so, .sh, cron, startup |
| `persistence` | 3-5m | Backdoor hunting | cron, systemd, startup, autostart |
| `browser` | 2-3m | Browser artifacts | History, Cookies, Login, Password |
| `user_activity` | 3-5m | User timeline | Desktop, Downloads, Documents, bash_history |
| `email` | 3-5m | Email recovery | .pst, .ost, .msg, .eml |
| `documents` | 5-10m | Document search | .pdf, .doc, .docx, .xls, .xlsx |
| `logs` | 5-10m | System logs | .log, .evtx, syslog, auth.log |
| `network` | 1-2m | Network configs | hosts, resolv.conf, interfaces |
| `registry` | 2-3m | Windows Registry | SAM, SYSTEM, SOFTWARE, NTUSER |

#### **Deep Scans (10-30m)**

| Profile | Time | Description | Searches For |
|---------|------|-------------|--------------|
| `forensics` | 5-10m | Standard investigation | flag, password, secret, key, .log |
| `full` | 15-30m | Complete scan | flag, password, secret, key |
| `deleted` | 10-20m | Deleted file recovery | deleted, unallocated |
| `timeline` | 15-30m | MAC timeline | ALL files with timestamps |
| `anti_forensics` | 10-15m | Anti-forensic detection | timestomp, wiping |

**Total: 18 disk profiles**

---

## 🎨 Interactive HTML Reports

### **Features**

When you use `--html`, UNFOLD generates beautiful interactive reports with:

✅ **Downloadable Files** - Click download buttons to extract files
✅ **Search Box** - Filter files in real-time
✅ **Statistics Dashboard** - Total files, interesting files, deleted files
✅ **Color Coding** - Green for matches, red for deleted files
✅ **Responsive Design** - Works on desktop and mobile
✅ **Embedded Content** - Files up to 10MB embedded in the report

### **Example Workflow**

```bash
# 1. Generate interactive report
python3 unfoldV3.py ctf.dd --scan-disk ctf --html -o ctf_report.html

# 2. Open in browser
open ctf_report.html  # macOS
xdg-open ctf_report.html  # Linux

# 3. Use the interface
# - Search for "flag" in the search box
# - Click download buttons to extract files
# - No need to run extract commands!
```

---

## 🏆 CTF-Specific Workflows

### **Memory Dump CTF**

```bash
# Windows CTF
python3 unfoldV3.py ctf.dmp --scan ctf_windows --html -o flags.html

# Linux CTF
python3 unfoldV3.py ctf.lime --scan ctf_linux --html -o flags.html

# Auto-detects:
# - Strings containing: flag, CTF, password, secret
# - Suspicious processes
# - Network connections
# - Hidden files
```

### **Disk Image CTF**

```bash
# Auto flag detection
python3 unfoldV3.py ctf.dd --scan-disk ctf --html -o flags.html

# Automatically searches for:
# - CTF{...}, FLAG{...}, flag{...}
# - HTB{...}, PICO{...}, DUCTF{...}
# - MD5 hashes (32 hex chars)
# - SHA1 hashes (40 hex chars)
# - SHA256 hashes (64 hex chars)
# - Files named: flag, password, secret, key
# - Deleted files
```

### **CTF Pro Tips**

1. **Start with CTF profile** - Auto-detects most common flags
2. **Check deleted files** - Use `deleted` profile if nothing found
3. **Search HTML report** - Use Ctrl+F to search for "flag", "CTF", etc.
4. **Try different profiles** - credentials, browser, documents
5. **Extract files** - Use `--extract` if you find the flag file path

---

## 🔧 Command Reference

### **Core Arguments**

| Argument | Description | Required |
|----------|-------------|----------|
| `image` | Path to disk/memory image | Yes |
| `-o, --out` | Output file path | Yes |

### **Analysis Modes (Choose One)**

| Mode | Description | For |
|------|-------------|-----|
| `--scan PROFILE` | Memory analysis | .dmp, .raw, .vmem |
| `--scan-disk PROFILE` | Disk analysis | .dd, .img, .e01 |
| `--json` | JSON filesystem map | .dd, .img, .e01 |
| `--extract PATH` | Extract specific file | .dd, .img, .e01 |
| `--creds` | Credential extraction | .dd, .img, .e01 |
| `--volatility` | Interactive shell | .dmp, .raw, .vmem |

### **Output Options**

| Option | Description |
|--------|-------------|
| `--html, -H` | Generate HTML report |
| `--json` | Generate JSON output |
| `--csv` | Generate CSV output |
| `--timeline` | Generate timeline (bodyfile) |

### **AI Features**

| Option | Description |
|--------|-------------|
| `-p, --prompt` | Natural language query |
| `-ai, --ai-provider` | AI provider (openrouter/deepseek) |

### **Advanced Options**

| Option | Description |
|--------|-------------|
| `--resume` | Resume interrupted scan |
| `--hash` | Calculate SHA256 hashes |
| `-r, --read EXT` | Read file content (comma-separated) |
| `--no-filter` | Scan all files (no filtering) |
| `-v, --verbose` | Verbose output |
| `--split-items N` | Split JSON every N items |
| `--check-deps` | Check dependencies |

---

## 🛡️ Security & Best Practices

### **Evidence Integrity**

✅ **Read-Only Access** - UNFOLD never modifies original evidence
✅ **Hash Verification** - Use `--hash` to generate SHA256 checksums
✅ **Chain of Custody** - All actions logged with timestamps
✅ **Audit Trails** - `.audit.log` files track all operations

### **API Safety**

⚠️ **Never commit config.json** - Add to `.gitignore`
⚠️ **Rotate API keys regularly** - Especially if shared
⚠️ **Review AI commands** - Check `.audit.log` before trusting output
⚠️ **Use environment variables** - For production deployments

### **Performance Tips**

💡 **Start small** - Use `minimal` or `triage` profiles first
💡 **Use --resume** - For large images that take hours
💡 **Filter smartly** - Default filtering speeds up scans 10x
💡 **RAM matters** - 4GB+ recommended for large images

---

## 🐛 Troubleshooting

### **Common Issues**

#### **"Profile not found"**
```bash
# Solution: Install profile files
./DEPLOY.sh

# Or manually:
cp unified_scan_profiles_FIXED.json scans/unified_scan_profiles.json
cp disk_scan_profiles.json scans/disk_scan_profiles.json
```

#### **"Volatility not found"**
```bash
# Solution: Install Volatility 3
git clone https://github.com/volatilityfoundation/volatility3.git

# Or add to PATH
export PATH=$PATH:/path/to/volatility3
```

#### **"Invalid magic value (Not a NTFS file system)"**
```bash
# This is NORMAL for EXT4/FAT disks
# UNFOLD auto-tries multiple filesystem types

# If still fails, the image might be:
# - Encrypted
# - Corrupted
# - Not a filesystem (raw memory dump)
```

#### **"Cannot download files from report"**
```bash
# Solution: Files >10MB aren't embedded
# Use --extract instead:
python3 unfoldV3.py disk.dd --extract /path/to/large_file -o output
```

### **Getting Help**

- **GitHub Issues**: [Report bugs](https://github.com/arazazi/unfold/issues)
- **Documentation**: This file!
- **Examples**: Check `unfold_guide.md`

---

## 📝 Changelog

### **v3.0.0-ULTRA (2026-01-31)**

**Major Features:**
- ✅ Smart filesystem detection (auto-detects NTFS, EXT4, FAT)
- ✅ 18 disk scan profiles added
- ✅ Interactive HTML reports with file downloads
- ✅ Profile-specific search patterns
- ✅ Embedded file content in reports

**Improvements:**
- ✅ Fixed profile plugin counting
- ✅ Enhanced HTML template with scrolling
- ✅ Better error messages
- ✅ Faster performance
- ✅ Cross-platform support

**Bug Fixes:**
- ✅ PosixPath errors resolved
- ✅ Filesystem mounting improved
- ✅ Extract function now uses smart scanner

### **v2.1 (2025)**
- Memory forensics with Volatility 3
- AI integration with OpenRouter & DeepSeek
- JSON filesystem mapping
- Basic HTML reports

---

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

**Areas we need help:**
- More scan profiles
- Additional AI providers
- Performance optimizations
- Documentation improvements
- Testing on different platforms

---

## 📄 License

UNFOLD is released under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **Volatility Foundation** - Memory forensics framework
- **The Sleuth Kit** - Filesystem analysis tools
- **pytsk3 Project** - Python bindings for TSK
- **OpenAI & Anthropic** - AI capabilities
- **Forensic Community** - Continuous feedback and support

---

## 📞 Support

- **GitHub**: [github.com/arazazi/unfold](https://github.com/arazazi/unfold)
- **Issues**: [Report bugs](https://github.com/arazazi/unfold/issues)
- **Documentation**: You're reading it!

---

<p align="center">
  <strong>Created by Azazi | UNFOLD Forensic Suite v3.0 ULTRA</strong><br>
  <sub>For forensic investigators, CTF players, and security researchers worldwide</sub>
</p>