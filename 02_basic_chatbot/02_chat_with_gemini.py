from dotenv import load_dotenv
import google.generativeai as genai
import os
import sys
from typing import List, Dict

def setup_environment() -> str:
    """Setup environment variables and validate Gemini API key"""
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in environment variables.")
        print("Please create a .env file with your Gemini API key like this:")
        print("GOOGLE_API_KEY=your-api-key-here")
        sys.exit(1)
    return api_key

def initialize_model(api_key: str) -> genai.GenerativeModel:
    """Initialize the Gemini model with specified parameters"""
    try:
        genai.configure(api_key=api_key)
        
        # Configure model settings
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config={
                "temperature": 0.7,
                "top_p": 0.8,
                "top_k": 40,
            }
        )
        return model
    except Exception as e:
        print(f"Error initializing Gemini model: {str(e)}")
        sys.exit(1)

def format_chat_history(history: List[Dict]) -> str:
    """Format chat history for display"""
    formatted = ""
    for message in history:
        role = "You" if message["role"] == "user" else "AI"
        formatted += f"{role}: {message['content']}\n"
    return formatted

def chat_with_gemini():
    """Main chat loop function"""
    # Setup environment and initialize model
    api_key = setup_environment()
    model = initialize_model(api_key)
    
    # Initialize chat
    chat = model.start_chat(history=[])
    
    print("\n=== Welcome to the Gemini AI Chatbot! ===")
    print("Type 'exit' to quit, 'clear' to clear history, or 'history' to view chat history.\n")

    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Handle special commands
            if user_input.lower() == "exit":
                print("\nGoodbye! Thank you for chatting.")
                break
            elif user_input.lower() == "clear":
                chat = model.start_chat(history=[])
                print("\nConversation history cleared.")
                continue
            elif user_input.lower() == "history":
                print("\n=== Chat History ===")
                print(format_chat_history(chat.history))
                continue
            elif not user_input:
                continue

            # Get AI response
            response = chat.send_message(user_input)
            
            # Print the response
            print(f"\nAI: {response.text}")

        except KeyboardInterrupt:
            print("\n\nExiting gracefully...")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try again.")

def main():
    """Main function to run the chat application"""
    try:
        chat_with_gemini()
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()