# Product Requirements Document (PRD)
## AI Computer Task Assistant — LangChain + Groq API

**Version:** 1.1  
**Date:** April 23, 2026  
**Status:** Draft  
**Author:** Karthik Kondagurla  
**Changelog:** v1.1 — Added Section 13 (Desktop Distribution & Packaging) covering PyInstaller executable, Windows/macOS/Linux installer formats, and distribution requirements.

---

## 1. Overview

### 1.1 Product Summary

The AI Computer Task Assistant is a Python-based desktop automation agent that allows users to control their laptop/PC using plain English commands. The system combines **Groq's ultra-fast LPU inference** (via the `llama-3.3-70b-versatile` model) with **LangChain's tool-calling agent framework** to understand user intent and execute real computer actions — file management, app launching, web browsing, keyboard simulation, system monitoring, and terminal commands.

The application is packaged as a **standalone desktop executable** (`.exe` for Windows, `.app` for macOS, binary for Linux) so end users can download and run it without installing Python or any dependencies.

### 1.2 Problem Statement

Performing repetitive computer tasks (opening apps, organizing files, searching the web, typing content) requires navigating multiple interfaces and remembering OS-specific commands. Non-technical users and power users alike spend unnecessary time on low-level operations that could be delegated to an intelligent agent.

Additionally, distributing Python-based tools to non-developers is traditionally difficult — requiring Python installation, `pip`, virtual environments, and manual environment variable setup. This project solves both problems.

### 1.3 Solution

A conversational AI agent that:
- Accepts natural language instructions (typed, extensible to voice)
- Selects and executes the correct tool from a library of 16 system actions
- Chains multiple steps autonomously for complex tasks
- Maintains short-term conversation memory for contextual follow-up
- Ships as a **downloadable, one-click installer** for Windows, macOS, and Linux laptops

---

## 2. Goals & Success Metrics

### 2.1 Goals

| Goal | Description |
|------|-------------|
| Accuracy | Agent correctly interprets and executes user commands without ambiguity |
| Speed | Groq LPU inference responds within 1–2 seconds per command |
| Safety | No destructive or unauthorized system actions are executed without explicit user instruction |
| Extensibility | New tools can be added as standalone Python functions with a `@tool` decorator |
| Cross-platform | Core functionality works on Windows, macOS, and Linux laptops |
| Distributable | End users can install and run the app without Python knowledge |

### 2.2 Success Metrics

| Metric | Target |
|--------|--------|
| Task completion rate | ≥ 90% of valid user commands complete successfully |
| Average response latency | < 2 seconds (LLM inference via Groq) |
| False positive tool execution | < 5% (agent executes wrong tool) |
| Tool chaining success | ≥ 80% for multi-step tasks (e.g., "open Chrome and search X") |
| Conversation context retention | Last 10 turns (20 messages) preserved correctly |
| Installer size | ≤ 80 MB for Windows `.exe`, ≤ 100 MB for macOS `.app` |
| Installer success rate | ≥ 95% clean installs on target OS versions |

---

## 3. Target Users

| User Type | Description | Primary Use Case |
|-----------|-------------|-----------------|
| Students | Non-technical users wanting to automate study tasks | Organizing files, searching topics, writing notes |
| Developers | Power users wanting fast CLI + GUI automation | Running commands, creating project structures |
| Office workers | Professionals doing repetitive desktop tasks | File management, app switching, copy-paste workflows |
| Accessibility users | Users with limited mobility | Keyboard-free computer interaction via text commands |

---

## 4. Scope

### 4.1 In Scope (v1.1)

- **16 built-in tools** covering: app launching, website/search, file CRUD, keyboard/mouse simulation, clipboard, screenshot, system info, terminal commands, datetime
- **LangChain `create_tool_calling_agent`** with `AgentExecutor` and multi-step chaining (up to 5 iterations)
- **Conversation memory** — rolling window of last 10 turns
- **Cross-platform support** — Windows, macOS, Linux with OS-specific app launchers
- **CLI interface** — interactive REPL loop with `input()`
- **Safety guardrails** — 15-second timeout on shell commands, no automatic root/admin escalation
- **Desktop packaging** — PyInstaller-based single-file executables for all three platforms
- **Windows installer** — Inno Setup `.exe` installer with setup wizard
- **macOS DMG** — drag-to-Applications `.dmg` disk image
- **Linux DEB/AppImage** — Debian package and portable AppImage
- **First-run API key prompt** — GUI dialog to enter `GROQ_API_KEY` on first launch (stored in OS keychain)

### 4.2 Out of Scope (v1.1)

- Voice input/output (speech-to-text, text-to-speech)
- Graphical user interface (beyond first-run API key dialog)
- Screen vision / screenshot analysis (visual grounding)
- Scheduled / cron-based task automation
- Multi-user or remote execution
- Plugin marketplace or community tool registry
- Long-term persistent memory (beyond session)
- Auto-update mechanism

---

## 5. Functional Requirements

### 5.1 Core Agent Behavior

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-01 | The agent MUST accept free-form natural language text as input | P0 |
| FR-02 | The agent MUST select the correct tool(s) based on user intent | P0 |
| FR-03 | The agent MUST confirm the action taken after each tool execution | P0 |
| FR-04 | The agent MUST chain multiple tools for multi-step requests | P0 |
| FR-05 | The agent MUST maintain conversation history for the last 10 turns | P1 |
| FR-06 | The agent MUST handle tool errors gracefully and return a human-readable message | P1 |
| FR-07 | The agent MUST ask for clarification when a request is genuinely ambiguous | P1 |
| FR-08 | The agent MUST exit cleanly on `quit`, `exit`, `bye`, or `Ctrl+C` | P0 |

### 5.2 Tool Requirements

#### File & Folder Management
| ID | Tool | Requirement |
|----|------|-------------|
| FR-10 | `create_folder` | Creates directories recursively using `Path.mkdir(parents=True)` |
| FR-11 | `list_files` | Lists files/folders with emoji icons for type distinction |
| FR-12 | `delete_file_or_folder` | Permanently deletes using `unlink()` or `shutil.rmtree()` |
| FR-13 | `rename_file` | Renames or moves using `Path.rename()` |
| FR-14 | `create_text_file` | Writes UTF-8 content to a specified path |
| FR-15 | `read_text_file` | Returns UTF-8 text content of a file |

#### Application & Web
| ID | Tool | Requirement |
|----|------|-------------|
| FR-20 | `open_application` | Launches OS-specific apps via app name lookup table + fallback |
| FR-21 | `open_website` | Opens any URL in the default browser; auto-prepends `https://` |
| FR-22 | `search_web_query` | Opens a Google search in the browser for the given query |

#### Keyboard, Mouse & System
| ID | Tool | Requirement |
|----|------|-------------|
| FR-30 | `type_text` | Simulates keyboard input at current cursor position (1s focus delay) |
| FR-31 | `press_key` | Presses single keys or combos (e.g., `ctrl+s`, `alt+f4`) |
| FR-32 | `take_screenshot` | Captures full screen and saves as PNG to specified path |
| FR-33 | `copy_to_clipboard` | Copies text to system clipboard via `pyperclip` |
| FR-34 | `get_system_info` | Returns OS, CPU %, RAM %, disk usage, and last boot time |
| FR-35 | `run_terminal_command` | Executes shell command with 15-second timeout; returns stdout/stderr |
| FR-36 | `get_current_datetime` | Returns current date and time in human-readable format |

### 5.3 LLM & API Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-40 | The system MUST use `ChatGroq` with model `llama-3.3-70b-versatile` | P0 |
| FR-41 | The system MUST read the API key from `GROQ_API_KEY` environment variable OR OS keychain | P0 |
| FR-42 | The system MUST display a clear error if `GROQ_API_KEY` is not set | P0 |
| FR-43 | `temperature` MUST be set to `0` for deterministic, repeatable tool calls | P1 |
| FR-44 | `max_iterations` MUST be capped at `5` to prevent runaway agent loops | P1 |

### 5.4 Distribution & Packaging Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-50 | The app MUST be packaged with **PyInstaller** into a standalone executable | P0 |
| FR-51 | A **Windows `.exe` installer** MUST be buildable using Inno Setup | P0 |
| FR-52 | A **macOS `.dmg`** disk image MUST be buildable using `create-dmg` or `hdiutil` | P1 |
| FR-53 | A **Linux AppImage** MUST be buildable for portability across distros | P1 |
| FR-54 | The packaged executable MUST run without Python or pip installed on the user's machine | P0 |
| FR-55 | On first launch, if no API key is found, the app MUST prompt the user to enter their Groq API key | P0 |
| FR-56 | The API key MUST be stored securely using the OS keychain (`keyring` library) | P1 |
| FR-57 | The Windows installer MUST create a Desktop shortcut and Start Menu entry | P1 |
| FR-58 | The installer MUST include an uninstaller (`unins000.exe` on Windows) | P1 |
| FR-59 | Build scripts MUST be provided for all three platforms (`build_windows.bat`, `build_mac.sh`, `build_linux.sh`) | P0 |

---

## 6. Non-Functional Requirements

| ID | Category | Requirement |
|----|----------|-------------|
| NFR-01 | Performance | LLM response latency ≤ 2 seconds under normal Groq load |
| NFR-02 | Safety | Shell commands timeout after 15 seconds; no sudo/admin escalation |
| NFR-03 | Reliability | Agent handles `Exception` from any tool and continues session |
| NFR-04 | Portability | Works on Windows 10+, macOS 12+, Ubuntu 20.04+ |
| NFR-05 | Privacy | No user data is logged or sent beyond the Groq API call |
| NFR-06 | Memory | Chat history capped at 20 messages (10 turns) to stay within token limits |
| NFR-07 | Extensibility | New tools require only a `@tool`-decorated function — no agent refactoring |
| NFR-08 | Usability | Error messages are human-readable with ✅/❌ status indicators |
| NFR-09 | Package Size | Windows `.exe` ≤ 80 MB; macOS `.app` ≤ 100 MB; Linux AppImage ≤ 90 MB |
| NFR-10 | Startup Time | Executable launches and is ready for input within ≤ 5 seconds |
| NFR-11 | Security | API key stored in OS keychain (Windows Credential Manager / macOS Keychain / Linux Secret Service) |

---

## 7. System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│              Packaged Executable (PyInstaller)               │
│   ai-assistant.exe / ai-assistant.app / ai-assistant.bin    │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              User Interface (CLI REPL)                 │  │
│  │            input() loop — plain English                │  │
│  └───────────────────────┬────────────────────────────────┘  │
│                          │                                   │
│                          ▼                                   │
│  ┌────────────────────────────────────────────────────────┐  │
│  │       LangChain Agent (create_tool_calling_agent)      │  │
│  │  System Prompt | Chat History | Input | Scratchpad     │  │
│  └───────────────────────┬────────────────────────────────┘  │
│                          │                                   │
│                          ▼                                   │
│  ┌────────────────────────────────────────────────────────┐  │
│  │       ChatGroq (llama-3.3-70b-versatile)               │  │
│  │       temperature=0 | Groq LPU Inference               │  │
│  └───────────────────────┬────────────────────────────────┘  │
│                          │                                   │
│                          ▼                                   │
│  ┌────────────────────────────────────────────────────────┐  │
│  │          Tool Dispatcher (AgentExecutor)               │  │
│  │          max_iterations=5                              │  │
│  └───────┬───────────────┬──────────────────┬────────────┘  │
│          ▼               ▼                  ▼               │
│  ┌─────────────┐ ┌─────────────┐   ┌─────────────┐         │
│  │  pyautogui  │ │  os/pathlib │   │   psutil    │         │
│  │  subprocess │ │  webbrowser │   │  pyperclip  │         │
│  └─────────────┘ └─────────────┘   └─────────────┘         │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │   API Key Manager (keyring — OS Keychain)              │  │
│  │   First-run prompt → stores key → loads on startup     │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

---

## 8. Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Language | Python | 3.10+ |
| LLM Provider | Groq API | Latest |
| LLM Model | llama-3.3-70b-versatile | Latest |
| Agent Framework | LangChain | ≥ 0.3.0 |
| Groq Integration | langchain-groq | ≥ 0.2.0 |
| Keyboard/Mouse | pyautogui | ≥ 0.9.54 |
| System Info | psutil | ≥ 5.9.0 |
| Screenshots | Pillow (ImageGrab) | ≥ 10.0.0 |
| Clipboard | pyperclip | ≥ 1.8.2 |
| **Packaging** | **PyInstaller** | **≥ 6.0** |
| **API Key Storage** | **keyring** | **≥ 24.0** |
| **Windows Installer** | **Inno Setup** | **≥ 6.0** |
| **macOS DMG** | **create-dmg** | **Latest** |
| **Linux Portable** | **AppImageTool** | **Latest** |

---

## 9. Installation & Configuration

### 9.1 For Developers (Source)
1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variable: `export GROQ_API_KEY="your_key"`
3. Run: `python ai_computer_assistant.py`

### 9.2 For End Users (Packaged Executable)
1. Download the installer for your OS from the releases page
2. Run the installer (`setup.exe` on Windows, mount `.dmg` on macOS, run `.AppImage` on Linux)
3. Launch **AI Computer Assistant** from Desktop/Applications
4. On first launch, enter your free Groq API key when prompted — it is saved securely

### 9.3 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | ✅ Yes (dev) | Authentication key for Groq API (auto-prompted in packaged app) |

---

## 10. Desktop Packaging Details

### 10.1 PyInstaller Build

PyInstaller bundles the Python interpreter, all dependencies, and the script into a single executable. The `--onefile` flag produces a single distributable binary.

```bash
# Windows
pyinstaller --onefile --console --name "AI-Assistant" \
  --hidden-import langchain_groq \
  --hidden-import pyautogui \
  --hidden-import psutil \
  --hidden-import keyring \
  ai_computer_assistant.py

# macOS
pyinstaller --onefile --console --name "AI-Assistant" \
  --target-arch universal2 \
  ai_computer_assistant.py

# Linux
pyinstaller --onefile --console --name "ai-assistant" \
  ai_computer_assistant.py
```

### 10.2 Platform-Specific Output

| Platform | Output Format | Installer Tool | Final Deliverable |
|----------|--------------|----------------|-------------------|
| Windows 10/11 | `.exe` (PyInstaller) | Inno Setup | `AI-Assistant-Setup.exe` |
| macOS 12+ | `.app` bundle | `create-dmg` | `AI-Assistant.dmg` |
| Ubuntu 20.04+ | binary | AppImageTool | `AI-Assistant.AppImage` |
| Debian/Ubuntu | binary | `dpkg-deb` | `ai-assistant.deb` |

### 10.3 Windows Installer (Inno Setup)

The Inno Setup script (`installer.iss`) will:
- Install the executable to `C:\Program Files\AI Computer Assistant\`
- Create a **Desktop shortcut**
- Add a **Start Menu** entry under "AI Computer Assistant"
- Register an **uninstaller** (`unins000.exe`) in Add/Remove Programs
- Prompt for Groq API key during installation (optional — can be skipped and set on first run)

### 10.4 First-Run API Key Flow

```
User launches app for first time
          │
          ▼
  Is GROQ_API_KEY in keychain?
     No ──► Show prompt: "Enter your Groq API Key"
             (get free key at console.groq.com)
          │
          ▼
     Validate key by making a test API call
          │
     Valid ──► Store in OS keychain via `keyring`
          │
          ▼
     App starts normally
```

### 10.5 Build Scripts

| Script | Platform | Command |
|--------|----------|---------|
| `build_windows.bat` | Windows | `build_windows.bat` |
| `build_mac.sh` | macOS | `bash build_mac.sh` |
| `build_linux.sh` | Linux | `bash build_linux.sh` |

Each script installs PyInstaller, runs the build, and produces the final installer in a `dist/` folder.

---

## 11. Future Enhancements (v2.0 Roadmap)

| Feature | Description | Priority |
|---------|-------------|----------|
| Voice Input | Integrate `speech_recognition` for microphone-based commands | P1 |
| Screen Vision | Send screenshots to a vision model (e.g., LLaVA) for GUI grounding | P1 |
| Graphical UI | Replace CLI REPL with a native Tkinter or Electron chat window | P1 |
| Auto-Updater | Check GitHub Releases for new versions and update in-place | P2 |
| Persistent Memory | Store conversation history across sessions using a local SQLite DB | P2 |
| Scheduled Tasks | Allow users to schedule recurring tasks via `schedule` library | P2 |
| Custom Tool Registry | Let users define and register personal tools via a YAML/JSON config | P3 |
| Plugin System | Downloadable community tool packs (e.g., "Gmail tools", "VS Code tools") | P3 |
| Sandboxed Execution | Run terminal commands in isolated Docker container for safety | P3 |

---

## 12. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Groq API key exposed in logs | Medium | High | Key stored in OS keychain; never printed to console |
| `delete_file_or_folder` deletes wrong path | Medium | High | Agent requires explicit full path; no wildcards |
| `run_terminal_command` runs malicious command | Low | High | 15-second timeout; agent warned in system prompt |
| `type_text` types into wrong window | Medium | Medium | 1-second delay built in; user must pre-focus window |
| Groq API rate limit hit | Low | Medium | Handle `RateLimitError` with user-friendly message |
| LLM hallucinates a non-existent tool | Low | Low | `handle_parsing_errors=True` in AgentExecutor |
| Antivirus flags PyInstaller executable | Medium | Medium | Code-sign executable on Windows/macOS; provide SHA256 hash |
| Large binary size slows downloads | Low | Low | Use `--onefile` + UPX compression in PyInstaller |
| macOS Gatekeeper blocks unsigned app | High | High | Sign with Apple Developer certificate or provide notarization guide |

---

## 13. Glossary

| Term | Definition |
|------|------------|
| **LPU** | Language Processing Unit — Groq's custom inference chip |
| **Tool Calling** | LLM capability to select and invoke structured functions based on user intent |
| **AgentExecutor** | LangChain class that orchestrates the agent's reasoning and tool execution loop |
| **REPL** | Read-Eval-Print Loop — the interactive command-line session |
| **PyInstaller** | Tool that bundles Python apps and all dependencies into a single standalone executable |
| **Inno Setup** | Free Windows installer builder that creates `.exe` setup wizards |
| **AppImage** | Portable Linux application format that runs on any distro without installation |
| **DMG** | Apple Disk Image — the standard macOS distribution format for apps |
| **keyring** | Python library for secure OS-level credential storage (Windows Vault, macOS Keychain, etc.) |
| **pyautogui** | Python library for programmatic keyboard and mouse control |
| **psutil** | Python library for retrieving system and process information |
