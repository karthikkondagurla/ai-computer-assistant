import os
import sys
import shutil
import subprocess
import platform
import webbrowser
from pathlib import Path
from datetime import datetime

from langchain_core.tools import tool

import psutil
import pyperclip


@tool
def create_folder(path: str) -> str:
    """Create a directory at the specified path. Creates parent directories recursively if they don't exist."""
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return f"✅ Created folder: {path}"
    except Exception as e:
        return f"❌ Error creating folder: {str(e)}"


@tool
def list_files(directory: str = ".") -> str:
    """List files and folders in the specified directory with emoji icons indicating type."""
    try:
        path = Path(directory)
        if not path.exists():
            return f"❌ Directory does not exist: {directory}"
        
        items = []
        for item in sorted(path.iterdir()):
            if item.is_dir():
                items.append(f"📁 {item.name}/")
            else:
                items.append(f"📄 {item.name}")
        
        if not items:
            return f"📭 Empty directory: {directory}"
        
        return "📂 Contents of " + directory + ":\n" + "\n".join(items)
    except Exception as e:
        return f"❌ Error listing files: {str(e)}"


@tool
def delete_file_or_folder(path: str) -> str:
    """Delete a file or folder at the specified path. Use with caution - this is permanent."""
    try:
        path_obj = Path(path)
        if not path_obj.exists():
            return f"❌ Path does not exist: {path}"
        
        if path_obj.is_file():
            path_obj.unlink()
            return f"✅ Deleted file: {path}"
        elif path_obj.is_dir():
            shutil.rmtree(path)
            return f"✅ Deleted folder: {path}"
    except Exception as e:
        return f"❌ Error deleting: {str(e)}"


@tool
def rename_file(old_path: str, new_path: str) -> str:
    """Rename or move a file or folder from old_path to new_path."""
    try:
        source = Path(old_path)
        if not source.exists():
            return f"❌ Source does not exist: {old_path}"
        
        source.rename(new_path)
        return f"✅ Renamed/moved: {old_path} -> {new_path}"
    except Exception as e:
        return f"❌ Error renaming: {str(e)}"


@tool
def create_text_file(path: str, content: str) -> str:
    """Create a text file at the specified path with the given content."""
    try:
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        return f"✅ Created text file: {path}"
    except Exception as e:
        return f"❌ Error creating file: {str(e)}"


@tool
def read_text_file(path: str) -> str:
    """Read and return the content of a text file at the specified path."""
    try:
        file_path = Path(path)
        if not file_path.exists():
            return f"❌ File does not exist: {path}"
        
        content = file_path.read_text(encoding="utf-8")
        if len(content) > 5000:
            content = content[:5000] + "\n... (truncated)"
        return f"📄 Contents of {path}:\n{content}"
    except Exception as e:
        return f"❌ Error reading file: {str(e)}"


@tool
def open_application(app_name: str) -> str:
    """Launch an application by name. Supports common app names on Windows, macOS, and Linux."""
    system = platform.system()
    
    app_lookup = {
        "chrome": {"win": "chrome", "darwin": "google chrome", "linux": "google-chrome"},
        "firefox": {"win": "firefox", "darwin": "firefox", "linux": "firefox"},
        "notepad": {"win": "notepad", "darwin": "TextEdit", "linux": "gedit"},
        "vscode": {"win": "code", "darwin": "Visual Studio Code", "linux": "code"},
        "word": {"win": "winword", "darwin": "Microsoft Word", "linux": "libreoffice --writer"},
        "excel": {"win": "excel", "darwin": "Microsoft Excel", "linux": "libreoffice --calc"},
        "terminal": {"win": "cmd", "darwin": "Terminal", "linux": "gnome-terminal"},
        "powershell": {"win": "powershell", "darwin": "Terminal", "linux": "gnome-terminal"},
        "explorer": {"win": "explorer", "darwin": "Finder", "linux": "nautilus"},
    }
    
    try:
        cmd = app_lookup.get(app_name.lower())
        if not cmd:
            return f"❌ Unknown application: {app_name}"
        
        exe = cmd.get(system, cmd.get("linux", app_name))
        
        if system == "Windows":
            subprocess.Popen(["start", "", exe], shell=True)
        elif system == "Darwin":
            subprocess.Popen(["open", "-a", exe])
        else:
            subprocess.Popen([exe], detached=True, start_new_session=True)
        
        return f"✅ Launched {app_name}"
    except Exception as e:
        return f"❌ Error launching app: {str(e)}"


@tool
def open_website(url: str) -> str:
    """Open a URL in the default web browser. Automatically prepends https:// if needed."""
    try:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        
        webbrowser.open(url)
        return f"✅ Opened website: {url}"
    except Exception as e:
        return f"❌ Error opening website: {str(e)}"


@tool
def search_web_query(query: str) -> str:
    """Open a Google search for the given query in the default browser."""
    try:
        encoded_query = query.replace(" ", "+")
        url = f"https://www.google.com/search?q={encoded_query}"
        webbrowser.open(url)
        return f"✅ Searched Google for: {query}"
    except Exception as e:
        return f"❌ Error searching: {str(e)}"


@tool
def play_youtube_video(query: str) -> str:
    """Search for a video on YouTube and open it for playback."""
    try:
        encoded_query = query.replace(" ", "+")
        url = f"https://www.youtube.com/results?search_query={encoded_query}"
        webbrowser.open(url)
        return f"✅ Opened YouTube search for '{query}'. Click on the first result to play."
    except Exception as e:
        return f"❌ Error playing video: {str(e)}"


@tool
def type_text(text: str) -> str:
    """Simulate keyboard input at the current cursor position. Wait 1 second for focus."""
    try:
        import pyautogui
        import time
        time.sleep(1)
        pyautogui.write(text)
        return f"✅ Typed text: {text[:50]}{'...' if len(text) > 50 else ''}"
    except Exception as e:
        return f"❌ Error typing text: {str(e)}"


@tool
def press_key(key: str) -> str:
    """Press a keyboard key or combination (e.g., 'ctrl+c', 'alt+f4', 'enter', 'escape')."""
    try:
        import pyautogui
        keys = key.lower().split("+")
        pyautogui.hotkey(*keys)
        return f"✅ Pressed keys: {key}"
    except Exception as e:
        return f"❌ Error pressing key: {str(e)}"


@tool
def take_screenshot(path: str = "screenshot.png") -> str:
    """Capture the full screen and save as PNG to the specified path."""
    try:
        import pyautogui
        pyautogui.screenshot(path)
        return f"✅ Screenshot saved: {path}"
    except Exception as e:
        return f"❌ Error taking screenshot: {str(e)}"


@tool
def copy_to_clipboard(text: str) -> str:
    """Copy the specified text to the system clipboard."""
    try:
        pyperclip.copy(text)
        return f"✅ Copied to clipboard: {text[:50]}{'...' if len(text) > 50 else ''}"
    except Exception as e:
        return f"❌ Error copying to clipboard: {str(e)}"


@tool
def get_system_info() -> str:
    """Get system information including OS, CPU usage, RAM usage, disk usage, and last boot time."""
    try:
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        
        info = f"""🖥️ System Information:
━━━━━━━━━━━━━━━
OS: {platform.system()} {platform.release()}
CPU: {cpu_percent}% used
RAM: {memory.percent}% used ({memory.used // (1024**2)}MB / {memory.total // (1024**2)}MB)
Disk: {disk.percent}% used ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)
Last Boot: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}"""
        
        return info
    except Exception as e:
        return f"❌ Error getting system info: {str(e)}"


@tool
def run_terminal_command(command: str) -> str:
    """Execute a shell command and return the output. Times out after 15 seconds."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=15
        )
        
        output = result.stdout.strip() if result.stdout else result.stderr.strip()
        
        if not output:
            output = "(No output)"
        
        if len(output) > 2000:
            output = output[:2000] + "\n... (truncated)"
        
        return f"📟 Command output:\n{output}"
    except subprocess.TimeoutExpired:
        return "❌ Command timed out after 15 seconds"
    except Exception as e:
        return f"❌ Error running command: {str(e)}"


@tool
def get_current_datetime() -> str:
    """Get the current date and time in a human-readable format."""
    try:
        now = datetime.now()
        return f"🕐 Current date and time: {now.strftime('%A, %B %d, %Y at %I:%M:%S %p')}"
    except Exception as e:
        return f"❌ Error getting datetime: {str(e)}"