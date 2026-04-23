import sys
import signal
from src.agent.assistant import create_computer_assistant
from src.utils.api_key_manager import get_api_key_or_exit, ensure_api_key


QUIT_COMMANDS = {"quit", "exit", "bye", "q"}


def signal_handler(sig, frame):
    print("\n👋 Goodbye!")
    sys.exit(0)


def print_welcome():
    print("\n" + "="*60)
    print("🤖 AI Computer Assistant")
    print("="*60)
    print("Control your computer with natural language commands.")
    print("\nExamples:")
    print("  • 'Open Chrome and search for Python tutorials'")
    print("  • 'Create a folder called Projects'")
    print("  • 'Take a screenshot and save it as screen.png'")
    print("  • 'What is my system info?'")
    print("\nType 'quit', 'exit', or 'bye' to exit.")
    print("="*60 + "\n")


def run_repl(agent):
    print_welcome()
    
    while True:
        try:
            user_input = input("👤 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in QUIT_COMMANDS:
                print("👋 Goodbye!")
                break
            
            print("🤖 Assistant: ", end="", flush=True)
            response = agent.run(user_input)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print()


def main():
    signal.signal(signal.SIGINT, signal_handler)
    
    print("\n🔄 Initializing AI Computer Assistant...")
    
    api_key = get_api_key_or_exit()
    
    print("🤖 Loading AI agent...")
    agent = create_computer_assistant(api_key)
    
    print("✅ Ready!\n")
    
    run_repl(agent)


if __name__ == "__main__":
    main()