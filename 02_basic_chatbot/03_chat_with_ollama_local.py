from typing import List, Dict
import requests
import json
import sys

OLLAMA_MODEL_NAME="llama3.2"

class OllamaChat:
    def __init__(self, model_name: str = "llama2", host: str = "http://localhost:11434"):
        """Initialize Ollama chat with specified model and host"""
        self.model_name = model_name
        self.host = host
        self.history: List[Dict[str, str]] = []

    def verify_connection(self) -> bool:
        """Verify connection to Ollama server"""
        try:
            response = requests.get(f"{self.host}/api/tags")
            return response.status_code == 200
        except requests.RequestException:
            return False

    def list_models(self) -> List[str]:
        """Get list of available models"""
        try:
            response = requests.get(f"{self.host}/api/tags")
            models = response.json()
            return [model['name'] for model in models['models']]
        except Exception:
            return []

    def send_message(self, message: str) -> str:
        """Send a message to Ollama and get the response"""
        try:
            # Prepare the request with context from history
            data = {
                "model": self.model_name,
                "messages": self.history + [{"role": "user", "content": message}],
                "stream": False
            }

            # Send request to Ollama
            response = requests.post(f"{self.host}/api/chat", json=data)
            response_data = response.json()

            # Update history with the exchange
            self.history.append({"role": "user", "content": message})
            self.history.append({"role": "assistant", "content": response_data['message']['content']})

            return response_data['message']['content']

        except requests.RequestException as e:
            return f"Error communicating with Ollama: {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"

def main():
    """Main function to run the Ollama chat application"""
    print("\n=== Welcome to Ollama Chat! ===")
    
    # Initialize chat with default model
    chat = OllamaChat()
    
    # Verify Ollama connection
    if not chat.verify_connection():
        print("Error: Cannot connect to Ollama. Please ensure Ollama is running on localhost:11434")
        sys.exit(1)
    
    # Get available models
    models = chat.list_models()
    if models:
        print("\nAvailable models:", ", ".join(models))
        model_choice = input("\nChoose a model (press Enter for default 'llama2'): ").strip()
        if model_choice:
            chat.model_name = model_choice
    
    print(f"\nUsing model: {chat.model_name}")
    print("\nCommands:")
    print("- Type 'exit' to quit")
    print("- Type 'clear' to clear history")
    print("- Type 'model <name>' to switch models")
    print("- Press Ctrl+C to exit\n")

    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Handle commands
            if not user_input:
                continue
            elif user_input.lower() == "exit":
                print("\nGoodbye!")
                break
            elif user_input.lower() == "clear":
                chat.history = []
                print("\nConversation history cleared.")
                continue
            elif user_input.lower().startswith("model "):
                new_model = user_input[6:].strip()
                chat.model_name = new_model
                chat.history = []  # Clear history when switching models
                print(f"\nSwitched to model: {new_model}")
                continue
            
            # Get and print response
            print("\nAI: ", end="", flush=True)
            response = chat.send_message(user_input)
            print(response)

        except KeyboardInterrupt:
            print("\n\nExiting gracefully...")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try again.")

if __name__ == "__main__":
    main()