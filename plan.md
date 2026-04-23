# AI Computer Task Assistant - Project Plan

## Project Overview

Build an AI-powered desktop automation agent that allows users to control their computer using natural language commands. The system uses LangChain's tool-calling agent framework combined with Groq's fast LPU inference (LLaMA 3.3 70B) to understand user intent and execute real computer actions.

---

## Phase 1: Project Setup & Core Infrastructure

### 1.1 Initialize Project Structure
- [ ] Create project directory structure
- [ ] Set up virtual environment (Python 3.10+)
- [ ] Create requirements.txt with all dependencies
- [ ] Initialize git repository

### 1.2 Install Dependencies
```
langchain>=0.3.0
langchain-groq>=0.2.0
pyautogui>=0.9.54
psutil>=5.9.0
pillow>=10.0.0
pyperclip>=1.8.2
keyring>=24.0
pyinstaller>=6.0
```

### 1.3 Environment Configuration
- [ ] Create .env.example file
- [ ] Set up GROQ_API_KEY environment variable handling
- [ ] Create first-run API key prompt logic
- [ ] Implement OS keychain storage (keyring)

---

## Phase 2: Tool Implementation (16 Tools)

### 2.1 File & Folder Management Tools
- [ ] `create_folder` - Create directories recursively
- [ ] `list_files` - List files/folders with emoji icons
- [ ] `delete_file_or_folder` - Delete files/folders
- [ ] `rename_file` - Rename or move files
- [ ] `create_text_file` - Write UTF-8 content
- [ ] `read_text_file` - Read file content

### 2.2 Application & Web Tools
- [ ] `open_application` - Launch OS-specific apps
- [ ] `open_website` - Open URL in default browser
- [ ] `search_web_query` - Open Google search

### 2.3 Keyboard, Mouse & System Tools
- [ ] `type_text` - Simulate keyboard input
- [ ] `press_key` - Press single keys or combos
- [ ] `take_screenshot` - Capture full screen as PNG
- [ ] `copy_to_clipboard` - Copy text to clipboard
- [ ] `get_system_info` - Return OS, CPU, RAM, disk info
- [ ] `run_terminal_command` - Execute shell command (15s timeout)
- [ ] `get_current_datetime` - Return current date/time

---

## Phase 3: LangChain Agent Implementation

### 3.1 Agent Setup
- [ ] Configure ChatGroq with llama-3.3-70b-versatile
- [ ] Set temperature=0 for deterministic responses
- [ ] Set max_iterations=5 to prevent runaway loops

### 3.2 Tool Binding
- [ ] Create @tool-decorated functions for all 16 tools
- [ ] Bind tools to agent using create_tool_calling_agent
- [ ] Set up AgentExecutor

### 3.3 Conversation Memory
- [ ] Implement rolling window memory (last 10 turns/20 messages)
- [ ] Configure token limit management

### 3.4 Safety Guardrails
- [ ] Implement 15-second timeout for shell commands
- [ ] Add warning messages in system prompt
- [ ] Handle exceptions gracefully

---

## Phase 4: User Interface

### 4.1 CLI REPL Interface
- [ ] Implement interactive input() loop
- [ ] Add quit/exit handling (quit, exit, bye, Ctrl+C)
- [ ] Add status indicators (✅/❌)
- [ ] Display human-readable error messages

### 4.2 First-Run Experience
- [ ] Check for GROQ_API_KEY on startup
- [ ] Show API key prompt if not found
- [ ] Validate key with test API call
- [ ] Store in OS keychain via keyring

---

## Phase 5: Desktop Packaging

### 5.1 PyInstaller Configuration
- [ ] Create build scripts for all platforms:
  - `build_windows.bat`
  - `build_mac.sh`
  - `build_linux.sh`
- [ ] Configure PyInstaller with hidden imports
- [ ] Test single-file executable generation

### 5.2 Platform-Specific Packaging
- [ ] Windows: Create Inno Setup script (installer.iss)
- [ ] macOS: Create DMG using create-dmg or hdiutil
- [ ] Linux: Create AppImage and DEB package

---

## Phase 6: Testing & Quality Assurance

### 6.1 Unit Testing
- [ ] Test all 16 tools individually
- [ ] Test error handling for each tool
- [ ] Test agent tool selection logic

### 6.2 Integration Testing
- [ ] Test multi-step command chaining
- [ ] Test conversation memory
- [ ] Test API key storage/retrieval

### 6.3 Platform Testing
- [ ] Test on Windows 10/11
- [ ] Test on macOS 12+
- [ ] Test on Ubuntu 20.04+

### 6.4 Performance Testing
- [ ] Measure response latency (target: <2 seconds)
- [ ] Test task completion rate (target: ≥90%)
- [ ] Verify false positive rate (<5%)

---

## Phase 7: Distribution & Release

### 7.1 Build Final Installers
- [ ] Build Windows .exe installer (target: ≤80 MB)
- [ ] Build macOS .dmg (target: ≤100 MB)
- [ ] Build Linux AppImage (target: ≤90 MB)

### 7.2 Documentation
- [ ] Create README.md
- [ ] Create user guide
- [ ] Document API key setup process

### 7.3 Release
- [ ] Create GitHub releases
- [ ] Generate checksums (SHA256)
- [ ] Code-sign executables (if available)

---

## Future Enhancements (v2.0 Roadmap)
- Voice input (speech-to-text)
- Screen vision (screenshot analysis)
- Graphical UI (Tkinter/Electron)
- Auto-updater
- Persistent memory (SQLite)
- Scheduled tasks
- Custom tool registry
- Plugin system
- Sandboxed execution

---

## Technical Stack Summary

| Component | Technology |
|-----------|------------|
| Language | Python 3.10+ |
| LLM | Groq llama-3.3-70b-versatile |
| Framework | LangChain >= 0.3.0 |
| Packaging | PyInstaller >= 6.0 |
| Key Storage | keyring >= 24.0 |

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Task completion rate | ≥ 90% |
| Response latency | < 2 seconds |
| False positive tool execution | < 5% |
| Multi-step task success | ≥ 80% |
| Windows installer size | ≤ 80 MB |
| macOS installer size | ≤ 100 MB |
| Installer success rate | ≥ 95% |

---

## Project Timeline (Suggested)

- **Week 1**: Project setup, environment configuration, first-run flow
- **Week 2**: Implement all 16 tools
- **Week 3**: LangChain agent implementation, memory, safety
- **Week 4**: CLI interface, testing, debugging
- **Week 5**: PyInstaller packaging, build scripts
- **Week 6**: Platform-specific installers, final testing
- **Week 7**: Documentation, release preparation

---

*Plan generated from PRD_AI_Computer_Assistant.md*