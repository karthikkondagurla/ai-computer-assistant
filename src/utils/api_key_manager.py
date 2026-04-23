import os
import sys
import keyring
from groq import Groq

SERVICE_NAME = "ai-computer-assistant"
KEY_NAME = "groq_api_key"


def get_api_key() -> str | None:
    """Get API key from environment variable or OS keychain."""
    api_key = os.environ.get("GROQ_API_KEY")
    if api_key:
        return api_key
    
    api_key = keyring.get_password(SERVICE_NAME, KEY_NAME)
    if api_key:
        return api_key
    
    return None


def set_api_key(api_key: str) -> bool:
    """Store API key in OS keychain."""
    try:
        keyring.set_password(SERVICE_NAME, KEY_NAME, api_key)
        os.environ["GROQ_API_KEY"] = api_key
        return True
    except Exception as e:
        print(f"Error storing API key: {e}")
        return False


def delete_api_key() -> bool:
    """Remove API key from OS keychain."""
    try:
        keyring.delete_password(SERVICE_NAME, KEY_NAME)
        if "GROQ_API_KEY" in os.environ:
            del os.environ["GROQ_API_KEY"]
        return True
    except Exception:
        return False


def validate_api_key(api_key: str) -> bool:
    """Validate API key by making a test request to Groq."""
    try:
        client = Groq(api_key=api_key)
        client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        return True
    except Exception as e:
        print(f"API key validation failed: {e}")
        return False


def prompt_for_api_key() -> str | None:
    """Prompt user to enter their Groq API key."""
    print("\n" + "="*50)
    print("🔑 Groq API Key Required")
    print("="*50)
    print("Please enter your Groq API key.")
    print("Get a free key at: https://console.groq.com")
    print("="*50)
    
    api_key = input("Enter API key: ").strip()
    
    if not api_key:
        print("❌ No API key entered.")
        return None
    
    if validate_api_key(api_key):
        if set_api_key(api_key):
            print("✅ API key validated and saved securely!")
            return api_key
    else:
        print("❌ Invalid API key. Please check and try again.")
    
    return None


def ensure_api_key() -> str | None:
    """Ensure API key is available, prompt if not found."""
    api_key = get_api_key()
    
    if api_key:
        return api_key
    
    return prompt_for_api_key()


def get_api_key_or_exit() -> str:
    """Get API key or exit the application."""
    api_key = ensure_api_key()
    
    if not api_key:
        print("❌ Cannot proceed without a valid API key.")
        print("You can set GROQ_API_KEY environment variable or enter it when prompted.")
        sys.exit(1)
    
    return api_key