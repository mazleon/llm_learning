import os
import json
import requests
from dotenv import load_dotenv
import sys

load_dotenv()

# Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# Available DeepSeek models on OpenRouter
DEEPSEEK_MODELS = {
    "deepseek-chat": "deepseek/deepseek-chat",
    "deepseek-r1": "deepseek/deepseek-r1"
}
DEFAULT_MODEL = "deepseek-r1"

def setup_environment():
    """Setup environment variables and validate API key"""
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenRouter API key like this:")
        print("OPENROUTER_API_KEY=your-api-key-here")
        print("You can get your API key from: https://openrouter.ai/keys")
        sys.exit(1)
    
    # List available models
    print("\nAvailable DeepSeek models on OpenRouter:")
    for i, (key, value) in enumerate(DEEPSEEK_MODELS.items(), 1):
        print(f"{i}. {key} ({value})")
    
    return api_key

def get_chat_completion(messages, api_key, model=DEFAULT_MODEL, temperature=0.7):
    """Get chat completion from OpenRouter API"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(data)
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None
        
def chat_with_deepseek():
    """Main chat loop function"""
    # Setup environment
    api_key = setup_environment()
    
    # Let user select a model
    print("\nSelect a model to use (or press Enter for default):")
    for i, (key, value) in enumerate(DEEPSEEK_MODELS.items(), 1):
        print(f"{i}. {key} ({value})")
    
    model_choice = input(f"\nEnter model number [1-{len(DEEPSEEK_MODELS)}] (default: 1): ").strip()
    try:
        if model_choice:
            model_idx = int(model_choice) - 1
            model_name = list(DEEPSEEK_MODELS.values())[model_idx]
        else:
            model_name = DEEPSEEK_MODELS[DEFAULT_MODEL]
    except (ValueError, IndexError):
        print(f"Invalid selection. Using default model: {DEFAULT_MODEL}")
        model_name = DEEPSEEK_MODELS[DEFAULT_MODEL]
    
    print(f"\nUsing model: {model_name}")
    
    # Initialize conversation history
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."}
    ]
    
    print("\n=== Welcome to the DeepSeek AI Chatbot (via OpenRouter)! ===")
    print("Type 'exit' to quit, 'clear' to clear history, or 'model' to change models.\n")

    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Handle special commands
            if user_input.lower() == "exit":
                print("\nGoodbye! Thank you for chatting.")
                break
            elif user_input.lower() == "clear":
                messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
                print("\nConversation history cleared.")
                continue
            elif user_input.lower() == "model":
                print("\nAvailable models:")
                for i, (key, value) in enumerate(DEEPSEEK_MODELS.items(), 1):
                    print(f"{i}. {key} ({value})")
                model_choice = input(f"\nSelect model [1-{len(DEEPSEEK_MODELS)}] (or press Enter to keep current): ").strip()
                if model_choice:
                    try:
                        model_idx = int(model_choice) - 1
                        model_name = list(DEEPSEEK_MODELS.values())[model_idx]
                        print(f"\nSwitched to model: {model_name}")
                    except (ValueError, IndexError):
                        print("Invalid selection. Keeping current model.")
                continue
            elif not user_input:
                continue

            # Add user message to history
            messages.append({"role": "user", "content": user_input})

            # Get AI response
            response = get_chat_completion(messages, api_key, model=model_name)
            
            if response is not None:
                # Add AI response to history and print it
                messages.append({"role": "assistant", "content": response})
                print(f"\nAI: {response}")
            else:
                print("\nSorry, I encountered an error. Please try again.")

        except KeyboardInterrupt:
            print("\n\nExiting gracefully...")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try again.")

def main():
    """Main function to run the chat application"""
    try:
        chat_with_deepseek()
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
