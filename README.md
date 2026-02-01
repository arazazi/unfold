<img width="1633" height="714" alt="image" src="https://github.com/user-attachments/assets/43f8edad-c670-409b-9a76-785768c86399" />

# 🔍 UNFOLD v3.0 ULTRA

> **The Ultimate Forensic Investigation Suite**  
> Professional disk & memory forensics tool with AI-powered analysis, beautiful HTML reports, and CTF-optimized workflows.

<p align="center">
  <img src="https://img.shields.io/badge/version-3.0.0--ULTRA-blue?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8+-green?style=for-the-badge" alt="Python">
  <img src="https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey?style=for-the-badge" alt="Platform">
  <img src="https://img.shields.io/badge/license-MIT-orange?style=for-the-badge" alt="License">
</p>

---

## ✨ Features

### 🧠 **Memory Forensics**
- **22 specialized profiles** for Windows & Linux memory analysis
- Powered by **Volatility 3** with smart auto-detection
- CTF competition mode with auto flag detection
- APT hunting, ransomware detection, malware analysis

### 💾 **Disk Forensics** 
- **18 specialized profiles** for filesystem analysis
- **Smart filesystem detection** - auto-detects NTFS, EXT4, FAT32, etc.
- **Interactive HTML reports** with file download buttons
- Credential extraction, deleted file recovery, timeline generation

### 🤖 **AI Integration**
- Natural language forensic commands
- OpenRouter & DeepSeek API support
- AI-powered evidence analysis

### 📊 **Professional Reports**
- Beautiful interactive HTML reports
- Download files directly from browser
- Search & filter capabilities
- Export to JSON, CSV, timeline formats

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/arazazi/unfold.git
cd unfold

# Run setup (creates directories, installs profiles)
chmod +x DEPLOY.sh
./DEPLOY.sh

# Check dependencies
python3 unfoldV3.py --check-deps
```

### Basic Usage

```bash
# Memory Analysis (Windows)
python3 unfoldV3.py memory.dmp --scan triage --html -o report.html

# Disk Analysis (any filesystem)
python3 unfoldV3.py disk.dd --scan-disk ctf --html -o disk_report.html

# Extract file from disk
python3 unfoldV3.py disk.dd --extract /path/to/file.txt -o output.txt

# Traditional modes
python3 unfoldV3.py disk.dd --json -o filesystem.json
python3 unfoldV3.py disk.dd --creds -o credentials.json
```

---

## 🎯 Scan Profiles

### Memory Scans (`--scan`)

| Profile | Speed | Description |
|---------|-------|-------------|
| `minimal` | 30s | Quick system overview |
| `triage` | 2-5m | Incident response essentials |
| `malware` | 5-10m | Deep malware detection |
| `ctf_windows` | 2-5m | CTF flag hunting (Windows) |
| `ctf_linux` | 2-5m | CTF flag hunting (Linux) |
| `apt_hunting` | 10-15m | Advanced persistent threats |
| `ransomware` | 5-10m | Ransomware indicators |
| `full` | 10-30m | Comprehensive analysis |

**22 total profiles available** - [View all →](Documentation.md)

### Disk Scans (`--scan-disk`)

| Profile | Speed | Description |
|---------|-------|-------------|
| `triage` | 2-5m | Quick filesystem overview |
| `ctf` | 3-5m | CTF flag hunting with auto-detection |
| `credentials` | 3-5m | Password & key extraction |
| `malware` | 5-10m | Suspicious file detection |
| `browser` | 2-3m | Browser artifacts & history |
| `deleted` | 10-20m | Deleted file recovery |
| `timeline` | 15-30m | Complete MAC timeline |

**18 total profiles available** - [View all →](Documentation.md)

---

## 💡 Use Cases

### 🏆 CTF Competitions
```bash
# Auto-detect flags in memory
python3 unfoldV3.py ctf.dmp --scan ctf_windows --html -o flags.html

# Auto-detect flags in disk
python3 unfoldV3.py ctf.dd --scan-disk ctf --html -o disk_flags.html

# Automatically searches for: CTF{}, FLAG{}, HTB{}, MD5, SHA1, SHA256
```

### 🔐 Incident Response
```bash
# Quick triage
python3 unfoldV3.py suspect.dmp --scan triage --html -o triage.html

# Hunt for persistence
python3 unfoldV3.py disk.dd --scan-disk persistence --html -o backdoors.html

# Extract credentials
python3 unfoldV3.py disk.dd --scan-disk credentials --html -o creds.html
```

### 🕵️ Digital Forensics
```bash
# Generate complete timeline
python3 unfoldV3.py evidence.dd --scan-disk timeline --timeline -o timeline.bodyfile

# Browser forensics
python3 unfoldV3.py disk.dd --scan-disk browser --html -o browser.html

# Document recovery
python3 unfoldV3.py disk.dd --scan-disk documents --html -o docs.html
```

---

## 🛠️ Advanced Features

### Interactive Reports with File Download

Disk scan reports include **clickable download buttons** for files:

```bash
python3 unfoldV3.py disk.dd --scan-disk ctf --html -o report.html
# Open report.html in browser
# Click any "Download" button to extract files instantly!
```

### AI-Powered Analysis (Optional)

```bash
# Natural language commands
python3 unfoldV3.py memory.dmp \
  -p "find all suspicious processes and their network connections" \
  -ai openrouter --html -o ai_analysis.html
```

---

## 📋 Requirements

- **Python** 3.8+
- **pytsk3** - Disk analysis
- **Volatility 3** - Memory analysis (included)
- **pyewf** - E01 image support (optional)
- **openai** - AI features (optional)

### Installation
```bash
pip install pytsk3 --break-system-packages
pip install pyewf openai --break-system-packages  # Optional
```

---

## 🎨 Project Structure

```
unfold/
├── unfold.py                 # Main script
├── DEPLOY.sh                   # One-click installer
├── config.example.json         # Example config (no real keys)
├── scans/                      # Scan profile definitions
│   ├── unified_scan_profiles.json
│   └── disk_scan_profiles.json
├── report-template/            # HTML templates
│   └── report.html
├── Documentation.md            # Complete user guide
└── README.md                   # This file
```

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📄 License

MIT License - see LICENSE file for details.

---

## 🙏 Acknowledgments

- **Volatility Foundation** - Memory forensics framework
- **The Sleuth Kit** - Filesystem analysis tools
- **OpenAI & Anthropic** - AI integration

---

<p align="center">
  <sub>Built with ❤️ for forensic investigators, CTF players, and security researchers</sub>
</p>
