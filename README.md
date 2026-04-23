# AI Computer Assistant

A Python-based desktop automation agent that allows you to control your computer using natural language commands. Built with LangChain and Groq's ultra-fast LPU inference.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Features

- **16 Built-in Tools** - Control files, apps, web, keyboard/mouse, and system
- **Natural Language** - Plain English commands the AI understands
- **Fast Inference** - Groq's LPU for sub-2-second responses
- **Cross-Platform** - Works on Windows, macOS, and Linux
- **Secure** - API key stored in OS keychain

## Supported Commands

### File Management
- Create folders, files
- Read, rename, delete files
- List directory contents

### Applications & Web
- Launch apps (Chrome, Firefox, VSCode, etc.)
- Open websites
- Search Google

### Keyboard & Mouse
- Type text automatically
- Press key combinations (Ctrl+C, Alt+F4, etc.)
- Take screenshots
- Copy to clipboard

### System
- Get system info (CPU, RAM, disk)
- Run terminal commands
- Get current date/time

## Installation

### Prerequisites
- Python 3.10+
- Groq API Key ([Get free key](https://console.groq.com))

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/karthikkondagurla/ai-computer-assistant.git
cd ai-computer-assistant
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set your Groq API key**
```bash
# Option 1: Environment variable
export GROQ_API_KEY="your_api_key_here"

# Option 2: Create .env file
echo "GROQ_API_KEY=your_api_key_here" > .env
```

## Usage

### Run from source
```bash
python ai_computer_assistant.py
```

### Run from executable
```bash
./dist/AI-Assistant
```

### Example Commands

```
You: What is my system info?
Assistant: Your system is running Linux with 52% CPU usage, 76% RAM...

You: Create a folder called Projects
Assistant: ✅ Created folder: Projects

You: Open Chrome and search for Python tutorials
Assistant: I've opened Google search for Python tutorials in your browser.

You: Take a screenshot
Assistant: ✅ Screenshot saved: screenshot.png
```

Type `quit`, `exit`, or `bye` to exit.

## Building Executables

### Windows
```bash
scripts\build_windows.bat
```

### macOS
```bash
bash scripts/build_mac.sh
```

### Linux
```bash
bash scripts/build_linux.sh
```

## Project Structure

```
.
├── ai_computer_assistant.py   # Main entry point
├── src/
│   ├── agent/assistant.py     # LangChain agent
│   ├── tools/computer_tools.py # 16 tools
│   ├── ui/cli.py              # CLI interface
│   └── utils/api_key_manager.py
├── scripts/                   # Build scripts
└── requirements.txt
```

## Configuration

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Your Groq API key (required) |

## Tech Stack

- **Language**: Python 3.10+
- **LLM**: Groq llama-3.3-70b-versatile
- **Framework**: LangChain >= 0.3.0
- **Packaging**: PyInstaller

## License

MIT License - See LICENSE file for details.

## Author

Karthik Kondagurla

---

Made with LangChain + Groq 🚀