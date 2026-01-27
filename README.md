# 🕵️ UNFOLD: UNIFIED FORENSIC COMMAND CENTER

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13%2B-blue?style=for-the-badge&logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20macOS-lightgrey?style=for-the-badge" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/AI-Powered-purple?style=for-the-badge&logo=openai" alt="AI Powered">
</p>

```text
 █    ██  ███▄    █   █████▒▒█████   ██▓    ▓█████▄ 
 ██  ▓██▒ ██ ▀█   █ ▓██   ▒▒██▒  ██▒▓██▒    ▒██▀ ██▌
▓██  ▒██░▓██  ▀█ ██▒▒████ ░▒██░  ██▒▒██░    ░██   █▌
▓▓█  ░██░▓██▒  ▐▌██▒░▓█▒  ░▒██   ██░▒██░    ░▓█▄   ▌
▒▒█████▓ ▒██░   ▓██░░▒█░   ░ ████▓▒░░██████▒░▒████▓ 
                                        | By Azazi

```

**Unfold** is a professional-grade forensic orchestration engine. It bridges the gap between raw disk images and memory dumps, utilizing Large Language Models (DeepSeek/OpenRouter) to translate natural language into complex, multi-step forensic actions.

---

## 🚀 Core Capabilities

| Feature | Technical Implementation |
| --- | --- |
| **Resilient Disk Mapping** | Direct block-level access via `pytsk3` with manual FAT/NTFS mounting overrides. |
| **AI Orchestration** | Translates natural language queries into precise `unfold` or `volatility` CLI syntax. |
| **Contextual Awareness** | Dynamically scrapes local Volatility 3 plugins to prevent AI hallucinations. |
| **Session Persistence** | Tracks progress via `.session` files for reliable analysis of multi-TB images. |
| **Smart Noise Filtering** | Automatically excludes OS "noise" (`/proc`, `/dev`, `/sys`) to focus on human artifacts. |

---

## 🛠️ Installation & Setup

### 1. System Prerequisites

Ensure your host system has the development headers for SleuthKit and LibEWF.

```bash
# Ubuntu / Kali / Debian
sudo apt update && sudo apt install -y libtsk-dev libewf-dev python3-pip python3-dev

```

### 2. Deployment

Unfold acts as a wrapper. For memory analysis, **Volatility 3** must be present in the root directory.

```bash
git clone [https://github.com/arazazi/unfold.git](https://github.com/arazazi/unfold.git)
cd unfold

# Clone Volatility 3 dependency
git clone [https://github.com/volatilityfoundation/volatility3.git](https://github.com/volatilityfoundation/volatility3.git)

# Install Python requirements
pip3 install pytsk3 openai pyewf

```

### 3. API Configuration

Create a `config.json` in the root directory:

```json
{
    "API_KEYS": {
        "OPENROUTER": "your_key",
        "DEEPSEEK": "your_key"
    }
}

```

---

## 📋 Flag Reference

| Flag | Argument | Description |
| --- | --- | --- |
| `--json` | - | Generates a full recursive JSON map of the filesystem. |
| `--extract` | `PATH` | Extracts a specific file from the image (requires `-o`). |
| `--creds` | - | Automated harvesting of shadow hashes or SAM/SYSTEM hives. |
| `-vol` | - | Activates Volatility 3 interactive or AI-guided mode. |
| `-p` | `QUERY` | **Natural Language Prompt** for AI-guided hunting. |
| `--hash` | - | Generates SHA256 for all files (Forensic Integrity). |
| `--resume` | - | Resumes a scan from the last saved `.session`. |

---

## 💡 Practical Examples & Scenarios

### 📂 Disk Forensics (Storage Analysis)

**Scenario 1: High-Speed Fast Mapping (Metadata Only)** Map a 2TB drive quickly by ignoring system noise and skipping file contents to generate a structural report.

```bash
python3 unfold.py image.dd --json -o structure_report.json

```

**Scenario 2: Deep Web Server Investigation** Scan a Linux server image, calculate SHA256 for integrity, and ingest the contents of configuration and environment files to find hidden backdoors.

```bash
python3 unfold.py server_disk.img --json --hash -r "conf,env,htaccess,php,sh" -o breach_analysis.json

```

**Scenario 3: Targeted Artifact Extraction** You have the path from a previous scan; now pull the specific Windows Registry hive for offline analysis.

```bash
python3 unfold.py win_c_drive.e01 --extract "/Windows/System32/config/SAM" -o SAM_hive.bak

```

**Scenario 4: Automated Credential Harvesting** Quickly pull Linux password hashes (`/etc/shadow`) or Windows Registry hives (SAM/SYSTEM) for offline cracking.

```bash
python3 unfold.py forensic_image.dd --creds -o dumped_secrets.txt

```

### 🧠 Memory Forensics (Volatility 3 Wrapper)

**Scenario 5: Interactive Memory Exploration** Drop into a persistent shell where you can run multiple Volatility plugins against a RAM dump without re-loading the image every time.

```bash
python3 unfold.py physical_memory.raw -vol --extract DUMMY -o volatility_session.log
# Inside the shell:
# VOLATILITY> windows.pslist
# VOLATILITY> windows.netscan

```

**Scenario 6: Automated Network Forensics (Volatility)** Use the Volatility engine to list all active network connections and save them directly to a text file.

```bash
# AI will suggest the netscan command
python3 unfold.py ram_dump.mem -vol --extract DUMMY -ai openrouter -p "List all active network connections" -o connections.txt

```

### 🤖 AI-Powered "Smart" Investigation

**Scenario 7: Investigating User Persistence (The "Hidden" Search)** You suspect a hacker added a startup script. Ask the AI to find it for you across the entire filesystem.

```bash
# The AI generates the necessary --extract command
python3 unfold.py disk.img --extract DUMMY -ai deepseek -p "Search for any unusual scripts in startup folders or cron jobs" -o persistence_finds.json

```

**Scenario 8: Identifying Injected Code in RAM** Ask the AI to choose and execute the correct Volatility plugins to find "Process Hollowing" or memory injections.

```bash
# The AI generates the required windows.malfind or similar command
python3 unfold.py ram.vmem -vol -ai openrouter -p "Check for memory regions marked as RWX that don't have a file backing" -o memory_alerts.txt

```

**Scenario 9: Evidence of Lateral Movement** Locate logs related to Remote Desktop (RDP) or SSH logins using natural language.

```bash
python3 unfold.py server.e01 --extract DUMMY -ai deepseek -p "Find and extract all RDP login event logs and SSH authorized_keys" -o access_logs.zip

```

### 🛡️ Resilience & Large-Scale Ops

**Scenario 10: The "Resume" Logic for 10TB+ Drives** If a scan of a massive NAS drive is interrupted, use the session tracker to pick up exactly where it left off.

```bash
python3 unfold.py massive_nas.dd --json --resume -o massive_report.json

```

**Scenario 11: Investigating Ransomware (Deep Content Search)** Scan for specific file extensions created by ransomware (e.g., `.locky`, `.crypted`) and read the "Ransom Note" content automatically.

```bash
python3 unfold.py encrypted_drive.img --json -r "txt,html,crypted" --no-filter -o ransomware_discovery.json

```

**Scenario 12: Browser Artifact Recovery via AI** Instead of manually hunting through AppData, let the AI find the database and extract it for you.

```bash
python3 unfold.py workstation.dd --extract DUMMY -ai openrouter -p "Extract the Chrome Login Data and Cookies database for the user 'john_doe'" -o john_secrets.db

```

---

## 📈 Analysis Workflow

1. **Map:** Use `--json` to get a bird's eye view of the disk.
2. **Filter:** Focus on Vital Dirs (Users, etc, var) automatically.
3. **Query:** Use `-p` (AI) to ask complex questions about the artifacts.
4. **Extract:** Use `--extract` to pull the evidence for your final report.
5. **Verify:** Always run with `--hash` for court-ready logs.

---

## 🤝 Connect & Support

**Developer:** [Abdulrahman Alazazi](https://github.com/arazazi)

**Professional Network:** [LinkedIn Profile](https://www.linkedin.com/in/arazazi)

**License:** MIT | Built for the DFIR Community | 🛡️ Stay Ethical
