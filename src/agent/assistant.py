import os
import sys
from typing import List
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain.agents import create_agent as langchain_create_agent
from langgraph.checkpoint.memory import MemorySaver

from src.tools.computer_tools import (
    create_folder, list_files, delete_file_or_folder, rename_file,
    create_text_file, read_text_file, open_application, open_website,
    search_web_query, type_text, press_key, take_screenshot,
    copy_to_clipboard, get_system_info, run_terminal_command, get_current_datetime
)


TOOLS = [
    create_folder, list_files, delete_file_or_folder, rename_file,
    create_text_file, read_text_file, open_application, open_website,
    search_web_query, type_text, press_key, take_screenshot,
    copy_to_clipboard, get_system_info, run_terminal_command, get_current_datetime
]

SYSTEM_PROMPT = """You are an AI Computer Assistant that helps users control their computer using natural language commands.

You have access to the following tools:
- create_folder: Create directories recursively
- list_files: List files/folders with emoji icons
- delete_file_or_folder: Delete files or folders (PERMANENT - use with caution)
- rename_file: Rename or move files/folders
- create_text_file: Create text files with UTF-8 content
- read_text_file: Read text file contents
- open_application: Launch applications (chrome, firefox, vscode, notepad, etc.)
- open_website: Open URLs in the default browser
- search_web_query: Search Google for any query
- type_text: Simulate keyboard typing at cursor position
- press_key: Press keyboard keys or combinations (ctrl+c, alt+f4, etc.)
- take_screenshot: Capture the screen as a PNG image
- copy_to_clipboard: Copy text to system clipboard
- get_system_info: Get OS, CPU, RAM, disk usage info
- run_terminal_command: Execute shell commands (15 second timeout)
- get_current_datetime: Get current date and time

IMPORTANT SAFETY RULES:
1. Never execute destructive commands without explicit user confirmation
2. Shell commands have a 15-second timeout - keep commands simple
3. Do not attempt to escalate to root/admin privileges
4. When deleting files, warn the user about permanence
5. Use full absolute paths when possible to avoid ambiguity

When a user asks to do something:
1. Understand their intent
2. Select the appropriate tool(s)
3. Execute the tool and report the result
4. For multi-step tasks, chain the tools together

If a command is ambiguous, ask for clarification.
If an error occurs, explain it clearly and suggest a fix.
Always be helpful, polite, and concise."""


class ComputerAssistantAgent:
    def __init__(self, groq_api_key: str, model: str = "llama-3.3-70b-versatile"):
        self.llm = ChatGroq(
            model=model,
            api_key=groq_api_key,
            temperature=0,
            max_retries=2
        )
        
        self.chat_history = InMemoryChatMessageHistory()
        
        memory = MemorySaver()
        
        self.graph = langchain_create_agent(
            model=self.llm,
            tools=TOOLS,
            system_prompt=SYSTEM_PROMPT,
            checkpointer=memory
        )
        
        self.config = {"configurable": {"thread_id": "default"}}
    
    def run(self, user_input: str) -> str:
        try:
            full_messages = list(self.chat_history.messages)
            full_messages.append(HumanMessage(content=user_input))
            
            response_text = ""
            
            for chunk in self.graph.stream(
                {"messages": full_messages},
                self.config,
                stream_mode="values"
            ):
                if "messages" in chunk:
                    last_msg = chunk["messages"][-1]
                    if hasattr(last_msg, "content") and last_msg.content:
                        response_text = last_msg.content
            
            self.chat_history.add_message(HumanMessage(content=user_input))
            self.chat_history.add_message(AIMessage(content=response_text))
            
            return response_text if response_text else "No response generated"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def clear_history(self):
        self.chat_history = InMemoryChatMessageHistory()
    
    def get_history(self) -> List:
        return self.chat_history.messages


def create_computer_assistant(groq_api_key: str) -> ComputerAssistantAgent:
    """Factory function to create the agent instance."""
    return ComputerAssistantAgent(groq_api_key)