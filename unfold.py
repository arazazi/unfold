#!/usr/bin/env python3
import sys
import json
import argparse
import os
import glob
import hashlib
import re
import logging
import subprocess
from datetime import datetime

# --- BANNER ---
BANNER = """
 █    ██  ███▄    █   █████▒▒█████   ██▓    ▓█████▄ 
 ██  ▓██▒ ██ ▀█   █ ▓██   ▒▒██▒  ██▒▓██▒    ▒██▀ ██▌
▓██  ▒██░▓██  ▀█ ██▒▒████ ░▒██░  ██▒▒██░    ░██   █▌
▓▓█  ░██░▓██▒  ▐▌██▒░▓█▒  ░▒██   ██░▒██░    ░▓█▄   ▌
▒▒█████▓ ▒██░   ▓██░░▒█░   ░ ████▓▒░░██████▒░▒████▓ 
░▒▓▒ ▒ ▒ ░ ▒░   ▒ ▒  ▒ ░   ░ ▒░▒░▒░ ░ ▒░▓  ░ ▒▒▓  ▒ 
░░▒░ ░ ░ ░ ░░   ░ ▒░ ░       ░ ▒ ▒░ ░ ░ ▒  ░ ░ ▒  ▒ 
 ░░░ ░ ░    ░   ░ ░  ░ ░   ░ ░ ░ ▒    ░ ░    ░ ░  ░ 
   ░              ░            ░ ░      ░  ░   ░    
                                             ░       
                                        | Azazi
"""

# --- API & TSK Imports ---
try:
    from openai import OpenAI
    AI_AVAILABLE = True
except ImportError:
    print("WARNING: OpenAI library not found. Install with: pip install openai")
    AI_AVAILABLE = False

try:
    import pytsk3
except ImportError:
    print("[-] Error: 'pytsk3' library is missing.")
    sys.exit(1)
    
try:
    from pyewf import file_entry
    E01_AVAILABLE = True
except ImportError:
    E01_AVAILABLE = False

# --- CONFIGURATION (Load external API keys) ---
API_KEYS = {}
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
        API_KEYS = config.get("API_KEYS", {})
except FileNotFoundError:
    pass
except json.JSONDecodeError:
    print("ERROR: config.json is invalid JSON.")
    
# --- GLOBAL SETTINGS ---
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
TOOL_TITLE = "" 
TOOL_URL = ""
GLOBAL_VOLATILITY_PLUGINS = "" 

# --- FILTERING ---
NOISE_FILTERS = [
    "proc", "sys", "dev", "run", "tmp", "snap",
    "usr/lib", "usr/share", "usr/src", "usr/include",
    "var/lib", "var/cache", "var/backups", "lib", "lib64", "boot"
]
VITAL_DIRS = [
    "home", "root", "etc", "var/log", "var/www", "opt", "srv", 
    "Users", "Documents and Settings", "ProgramData", "Inetpub", "Program Files"
]

# --- UTILITIES ---
class CaseLogger:
    def __init__(self, filename):
        logging.basicConfig(filename=filename, level=logging.INFO, format='%(asctime)s - %(message)s')
        self.log = logging.getLogger()
        self.log.setLevel(logging.ERROR) 
        
    def info(self, msg):
        print(msg)
        self.log.info(msg)
        
    def error(self, msg):
        print(f"[!] ERROR: {msg}")
        self.log.error(msg)

class SessionManager:
    def __init__(self, session_file):
        self.file = session_file
        self.completed_paths = set()
        self.load()

    def load(self):
        if os.path.exists(self.file):
            try:
                with open(self.file, 'r') as f:
                    self.completed_paths = set(json.load(f))
                print(f"[*] Session loaded. Skipping {len(self.completed_paths)} previously scanned directories.")
            except:
                print("[!] Session file corrupt, starting fresh.")
                self.completed_paths = set()

    def mark_done(self, path):
        self.completed_paths.add(path)
        with open(self.file, 'w') as f:
            json.dump(list(self.completed_paths), f)

    def is_done(self, path):
        return path in self.completed_paths


class AIOrchestrator:
    def __init__(self, logger, ai_provider, memory_mode=False):
        self.logger = logger
        self.provider = ai_provider
        self.memory_mode = memory_mode
        
        self.model = self._get_model()
        self.client = self._initialize_client()
        
        self.system_instruction = self._get_system_instruction()

    def _initialize_client(self):
        if self.provider == 'openrouter':
            key_name = "OPENROUTER"
            base_url = OPENROUTER_BASE_URL
        elif self.provider == 'deepseek':
            key_name = "DEEPSEEK"
            base_url = "https://api.deepseek.com/v1"
        else:
            return None

        key = API_KEYS.get(key_name)
        
        if not key:
            self.logger.error(f"{key_name}_API_KEY not found in config.json. Cannot initialize AI.")
            return None
        
        try:
            headers = {}
            if self.provider == 'openrouter':
                 if TOOL_URL: headers["HTTP-Referer"] = TOOL_URL
                 if TOOL_TITLE: headers["X-Title"] = TOOL_TITLE

            return OpenAI(
                api_key=key,
                base_url=base_url,
            )
        except Exception as e:
            self.logger.error(f"Error initializing OpenAI client: {e}")
            return None

    def _get_model(self):
        if self.provider == 'openrouter': return "tngtech/deepseek-r1t2-chimera:free" 
        if self.provider == 'deepseek': return "deepseek-chat" 
        return None

    def _get_system_instruction(self):
        global GLOBAL_VOLATILITY_PLUGINS
        
        if self.memory_mode:
            plugin_context = ""
            if GLOBAL_VOLATILITY_PLUGINS:
                 plugin_context = f"The ONLY VALID plugins are: {GLOBAL_VOLATILITY_PLUGINS}. Use these strictly. "
            
            return (f"You are an expert in Volatility 3. {plugin_context} Your response MUST start with 'volatility' followed by the required arguments (e.g., windows.pslist). Output ONLY the raw command, NO explanations, NO markdown fences, and NO preamble.")
        else:
            return "You are an expert disk forensic tool, 'unfold.py'. Your response MUST start with 'unfold.py' followed by the required arguments (e.g., --extract /path/to/file -o output.txt). Output ONLY the raw command, NO explanations, NO markdown fences, and NO preamble."

    def query(self, user_query, image_path):
        if not self.client: return {"error": "AI client not initialized."}

        full_query = f"Image file: {image_path}. User request: {user_query}"
        
        extra_headers = {}
        if self.provider == 'openrouter':
            if TOOL_URL: extra_headers["HTTP-Referer"] = TOOL_URL
            if TOOL_TITLE: extra_headers["X-Title"] = TOOL_TITLE

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_instruction},
                    {"role": "user", "content": full_query}
                ],
                extra_headers=extra_headers
            )
            
            command_text = response.choices[0].message.content.strip()

            if command_text.startswith('```'):
                command_text = command_text.strip('`').split('\n')[-1].strip()

            parts = command_text.split(maxsplit=1)
            
            if len(parts) < 2:
                return {"error": "AI output lacked arguments.", "text": command_text}

            tool_name_raw = parts[0].lower().strip().replace('.py', '') 
            arguments = parts[1].strip()
            
            tool_name = "unfold" if "unfold" in tool_name_raw else "volatility" if "volatility" in tool_name_raw else tool_name_raw

            if tool_name not in ['unfold', 'volatility']:
                 self.logger.error(f"AI failed to name the tool: {command_text}")
                 return {"error": "AI failed to name the tool (unfold or volatility).", "text": command_text}

            return {"tool_name": tool_name, "arguments": arguments}

        except Exception as e:
            self.logger.error(f"API or general failure: {e}")
            return {"error": f"API or general failure: {e}"}

class Volatility:
    def __init__(self, logger):
        self.logger = logger
        self.vol_path = None
        
        try:
            subprocess.run(['volatility', '-h'], capture_output=True, check=True)
            self.vol_path = 'volatility'
            self._load_plugins()
            return
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        local_path = os.path.join(script_dir, 'volatility3', 'vol.py')
        
        if os.path.exists(local_path):
             self.vol_path = f"python3 {local_path}"
             self.logger.info(f"[*] Found local Volatility 3 executable.")
             self._load_plugins()
        else:
             self.logger.error("Volatility 3 executable not found globally or in ./volatility3/vol.py.")

    def _load_plugins(self):
        global GLOBAL_VOLATILITY_PLUGINS
        try:
            result = subprocess.run(f"{self.vol_path} -h", shell=True, check=True, capture_output=True, text=True)
            output = result.stdout
            
            match = re.search(r'\(choose from (.*?)\)\n', output, re.DOTALL)
            if match:
                plugin_names = match.group(1).replace('\n', '').strip()
                GLOBAL_VOLATILITY_PLUGINS = plugin_names
                self.logger.info(f"[*] Injected {len(plugin_names.split(','))} Volatility plugins into AI context.")
                return
            self.logger.info("Could not auto-parse Volatility plugin list. AI may hallucinate plugin names.")

        except Exception as e:
            self.logger.error(f"Failed to load Volatility plugin list: {e}")

    def run_command(self, command):
        if not self.vol_path: return
        
        final_command = f"{self.vol_path} {command}"
        self.logger.info(f"Executing Volatility: {final_command}")
        
        try:
            result = subprocess.run(final_command, shell=True, check=True, capture_output=True, text=True)
            print("\n--- Volatility Output ---")
            print(result.stdout)
            print("-------------------------\n")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Volatility execution failed. Return code: {e.returncode}")
            print(f"\n--- Volatility Error ---\n{e.stderr}")

class UnfoldForensics:
    def __init__(self, image_path, args, logger):
        self.image_path = image_path
        self.args = args
        self.logger = logger
        
        self.scanned_count = 0
        self.stop_scan = False
        self.current_chunk_data = {}
        self.current_chunk_size = 0
        self.chunk_index = 1
        
        self.session = SessionManager(args.out + ".session") if args.out and args.resume else None
        self.read_extensions = [ext.lower().strip() for ext in self.args.read.split(',')] if args.read else []

        self.img_info = self._get_handle()

    # --- CORE HELPERS (Missing in previous paste) ---
    def _is_noise(self, path):
        if self.args.no_filter: return False
        clean = path.lstrip("/").replace("\\", "/")
        for v in VITAL_DIRS:
            if clean.startswith(v): return False
        for n in NOISE_FILTERS:
            if clean == n or clean.startswith(n + "/"): return True
        return False

    def _get_hash(self, entry):
        s = hashlib.sha256()
        try:
            if entry.info.meta.size > 100 * 1024 * 1024: return "Skipped (Too Large)"
            offset = 0
            while offset < entry.info.meta.size:
                data = entry.read_random(offset, 1024*1024)
                if not data: break
                s.update(data)
                offset += 1024*1024
            return s.hexdigest()
        except: return "hash_error"
    # -----------------------------------------------

    def _get_handle(self):
        base, ext = os.path.splitext(self.image_path)
        ext = ext.lower()

        if ext == ".001":
            files = sorted(glob.glob(base + ".[0-9][0-9][0-9]"))
            return pytsk3.Img_Info(filenames=files)
        
        if ext == ".e01" and E01_AVAILABLE:
            self.logger.info("[*] Mounting E01 image using pyewf/pytsk3...")
            ewf_handle = file_entry()
            ewf_handle.open(self.image_path)
            return pytsk3.Img_Info(ewf_handle)
            
        return pytsk3.Img_Info(self.image_path)

    def _get_fs_iterator(self):
        """Yields (pytsk3.FS_Info, label) after attempting to detect FS type."""
        
        def safe_fs_mount(img_info, offset, fs_type):
            try:
                # 1. Try modern keyword (type=)
                return pytsk3.FS_Info(img_info, offset=offset, type=fs_type)
            except TypeError:
                # 2. Fallback to old keyword (ftype=) for older pytsk3 versions
                return pytsk3.FS_Info(img_info, offset=offset, ftype=fs_type)

        try:
            # 1. Try MBR/GPT Volume scan
            vol = pytsk3.Volume_Info(self.img_info)
            for part in vol:
                if part.flags & pytsk3.TSK_VS_PART_FLAG_ALLOC:
                    desc = part.desc.decode('utf-8').replace(" ", "_")
                    label = f"Partition_{part.addr}_{desc}"
                    offset = part.start * 512
                    
                    try:
                        fs_type = pytsk3.FS_Info.detect_filesystem(self.img_info, offset)
                        self.logger.info(f"    [Detect] Partition {part.addr} detected as {fs_type}")
                        yield safe_fs_mount(self.img_info, offset, fs_type), label
                    except Exception as e:
                        self.logger.error(f"Automatic detection failed on {label}. Trying manual overrides.")

        except IOError:
            # 2. Fallback to Raw image
            offset = 0
            try:
                fs_type = pytsk3.FS_Info.detect_filesystem(self.img_info, 0)
                self.logger.info(f"    [Detect] Raw image detected as {fs_type}")
                yield safe_fs_mount(self.img_info, offset, fs_type), "Raw_Filesystem"
            except Exception as e:
                # --- MANUAL OVERRIDE CHECK (Targeted FAT fix) ---
                try:
                    self.logger.info(f"    [Override] Forcing mount as FAT32...")
                    yield safe_fs_mount(self.img_info, offset, pytsk3.TSK_FS_TYPE_FAT32), "Raw_Filesystem_FAT32_Forced"
                except Exception as e_fat:
                    self.logger.error(f"Manual FAT override failed. No known filesystem could be mounted: {e_fat}")


    def _recurse_json(self, directory, current_path):
        """Recursively builds the JSON tree, applying filters and collecting hashes/content."""
        tree = {}
        
        for entry in directory:
            if self.stop_scan: break # Check stop flag
            if entry.info.name.name in [b".", b".."]: continue
            if not entry.info.meta: continue

            try:
                name = entry.info.name.name.decode('utf-8')
            except:
                name = entry.info.name.name.decode('utf-8', errors='replace')
            
            node_path = os.path.join(current_path, name).replace("\\", "/")

            # --- FILTERING ---
            if self._is_noise(node_path): 
                if entry.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
                    tree[name] = "ignored_os_noise"
                continue

            # --- PROGRESS ---
            self.scanned_count += 1
            if self.scanned_count % 1000 == 0 and not self.args.verbose:
                sys.stdout.write(f"\r       [*] Scanned {self.scanned_count} items...")
                sys.stdout.flush()
            if self.args.verbose: print(f"      [Scanning] {node_path}")


            # --- DIRECTORY ---
            if entry.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
                try:
                    sub = entry.as_directory()
                    res = self._recurse_json(sub, node_path)
                    if res: tree[name] = res
                except:
                    tree[name] = {"access": "denied"}
            
            # --- FILE ---
            elif entry.info.meta.type == pytsk3.TSK_FS_META_TYPE_REG:
                size = entry.info.meta.size
                file_obj = {
                    "size": size, 
                    "modified": str(entry.info.meta.mtime)
                }

                if self.args.hash: file_obj['sha256'] = self._get_hash(entry)

                ext = node_path.split(".")[-1].lower() if "." in node_path else ""
                if ext in self.read_extensions and size < 100000:
                    try:
                        content = entry.read_random(0, size).decode('utf-8', errors='replace')
                        file_obj["content"] = content.replace('\x00', '')
                    except:
                        file_obj["content_error"] = "read_failed"
                    
                if 'content' in file_obj or self.args.hash or size > 0:
                     tree[name] = file_obj
                elif size == 0:
                     tree[name] = "File (Empty)"


        return tree

    def process_json_map(self): 
        results = {}
        for fs, label in self._get_fs_iterator():
            try:
                root = fs.open_dir(path="/")
                self.logger.info(f"JSON Map Mode Running on {label}...")
                results[label] = self._recurse_json(root, "")
            except Exception as e:
                self.logger.error(f"Error processing root directory for {label}: {e}")
        return results
        
    def harvest_credentials(self): return {}
    def process_extract(self): pass


def execute_ai_command(command_dict, image_path, logger):
    tool_name = command_dict.get('tool_name')
    arguments = command_dict.get('arguments')
    
    if not tool_name or not arguments:
        logger.error("AI response lacked necessary 'tool_name' or 'arguments'.")
        return

    # --- ARGUMENT CLEANUP (CRITICAL FIX) ---
    cleaned_args = arguments
    escaped_image_path = re.escape(image_path)
    
    # 1. Remove redundant image path and flag variations
    redundant_path_pattern = r'(\s|^)(--image\s+|--file\s+|-f\s+)?' + escaped_image_path
    cleaned_args = re.sub(redundant_path_pattern, ' ', arguments, flags=re.IGNORECASE).strip()
    
    # 2. Collapse multiple spaces, and remove leading tool name
    cleaned_args = re.sub(r'\s+', ' ', cleaned_args).strip()
    if cleaned_args.lower().startswith(tool_name):
        cleaned_args = cleaned_args[len(tool_name):].strip()

    logger.info(f"AI Execution: {tool_name} {cleaned_args}")

    # --- AUTOMATIC EXECUTION ---
    script_path = os.path.abspath(sys.argv[0])
    
    if tool_name == 'unfold':
        # Rebuild the command for nested execution: python3 [script] [image] [new_args]
        final_cmd = f"python3 {script_path} {image_path} {cleaned_args}"
        
        logger.info(f"[!] AUTO EXECUTING DISK COMMAND: {final_cmd}")
        
        try:
            result = subprocess.run(final_cmd, shell=True, check=True, capture_output=True, text=True)
            print("\n--- AUTO-EXECUTION OUTPUT ---")
            print(result.stdout)
            print("-----------------------------")
        except subprocess.CalledProcessError as e:
            logger.error(f"Nested disk execution failed. Command: {e.cmd}. Error: {e.stderr}")
        
    elif tool_name == 'volatility':
        vol_tool = Volatility(logger)
        vol_tool.run_command(cleaned_args)
        
    else:
        logger.error(f"Unknown tool name '{tool_name}' returned by AI.")


def main():
    print(BANNER)
    parser = argparse.ArgumentParser(
        description="Unfold: Unified Forensic Suite (Disk, Memory, AI Guidance)",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument("image", help="Path to forensic image (.dd, .e01, .img, or memory dump).")
    
    # --- MODES ---
    mode_group = parser.add_argument_group('ANALYSIS MODES', 'Select one primary action.')
    mode_group_select = mode_group.add_mutually_exclusive_group(required=True)
    mode_group_select.add_argument("--json", action="store_true", help="Generate JSON filesystem map (Disk Analysis).")
    mode_group_select.add_argument("--extract", metavar="PATH", help="Extract single file from disk image. Requires -o.")
    mode_group_select.add_argument("--creds", action="store_true", help="Harvest users/hashes from disk image.")
    mode_group_select.add_argument("--volatility", '-vol', action="store_true", help="Enter Volatility 3 mode for memory analysis.")

    # --- AI ASSISTANCE ---
    ai_group = parser.add_argument_group('AI ASSISTANCE (Requires config.json)', 'Use AI to generate commands for advanced analysis.')
    ai_group.add_argument("-p", "--prompt", metavar="QUERY", help="Natural language query to execute (e.g., 'extract the flag.txt from the desktop').")
    ai_group.add_argument("-ai", "--ai-provider", choices=['openrouter', 'deepseek'], help="AI model provider (openrouter or deepseek).")
    
    # --- OPTIONS ---
    parser.add_argument("-o", "--out", required=True, help="REQUIRED: Output path for report, extracted file, or base name for splits.")
    parser.add_argument("--resume", action="store_true", help="Resume JSON map from session file.")
    parser.add_argument("--hash", action="store_true", help="Calculate SHA256 hashes.")
    parser.add_argument("-r", "--read", default="", help="Extensions to read content (e.g., 'txt,conf').")
    parser.add_argument("--no-filter", action="store_true", help="Disable Smart Filtering (Scan ALL files).")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show live folder paths.")
    parser.add_argument("--split-items", metavar="N", type=int, default=10000, help="Split JSON output every N items (default: 10000).")

    args = parser.parse_args()

    if not os.path.exists(args.image):
        print(f"[!] Error: File '{args.image}' not found.")
        sys.exit(1)

    log_file = args.out + ".audit.log"
    logger = CaseLogger(log_file)
    logger.info(f"Analysis started on {args.image}: {datetime.now()}")

    # --- AI QUERY DISPATCH ---
    if args.prompt:
        if not args.ai_provider:
            logger.error("Must specify an AI provider (-ai openrouter/deepseek) with -p/--prompt.")
            sys.exit(1)
        if not AI_AVAILABLE:
            logger.error("AI modules are not installed. Cannot process query.")
            sys.exit(1)
            
        memory_mode = args.volatility
        
        if memory_mode:
            vol_tool = Volatility(logger)
            if not vol_tool.vol_path:
                logger.error("Cannot proceed with AI query: Volatility executable is missing.")
                sys.exit(1)
        
        orchestrator = AIOrchestrator(logger, args.ai_provider, memory_mode)
        
        print(f"[*] Querying AI ({orchestrator.model})...")
        result = orchestrator.query(args.prompt, args.image)
        
        if 'error' in result:
            logger.error(f"AI Query Failed: {result['error']}")
        else:
            execute_ai_command(result, args.image, logger)
        sys.exit(0)


    # --- VOLATILITY INTERACTIVE MODE ---
    if args.volatility:
        vol_tool = Volatility(logger)
        if not vol_tool.vol_path:
            sys.exit(1)
            
        print(f"\n[!] Entering Volatility 3 Interactive Shell. File: {args.image}")
        while True:
            cmd = input(f"\nVOLATILITY> ")
            if cmd.lower().strip() in ['exit', 'quit']: break
            if not cmd.strip(): continue
            full_command = f"{vol_tool.vol_path} -f {args.image} {cmd}"
            vol_tool.run_command(cmd)
        sys.exit(0)
    
    # --- DISK ANALYSIS MODES ---
    tool = UnfoldForensics(args.image, args, logger)
    
    try:
        if args.json:
            data = tool.process_json_map()
            
            json_output = json.dumps(data, indent=2)
            with open(args.out, 'w') as f:
                f.write(json_output)
            print(f"[+] JSON Map saved to {args.out}")

        elif args.creds:
            tool.harvest_credentials()
        elif args.extract:
            tool.process_extract()
            logger.info(f"File '{args.extract}' not found.")
            
    except KeyboardInterrupt:
        logger.info("User aborted process.")
        print("\n[!] Aborted.")
             
    logger.info(f"Analysis finished: {datetime.now()}")

if __name__ == "__main__":
    main()
