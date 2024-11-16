from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import os
from dotenv import load_dotenv
import sys

def setup_environment():
    """Setup environment variables and validate API key"""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenAI API key like this:")
        print("OPENAI_API_KEY=your-api-key-here")
        sys.exit(1)
    return api_key

def initialize_chat_model(api_key):
    """Initialize the ChatOpenAI model with specified parameters"""
    try:
        return ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            openai_api_key=api_key
        )
    except Exception as e:
        print(f"Error initializing chat model: {str(e)}")
        sys.exit(1)

def chat_with_openai():
    """Main chat loop function"""
    # Setup environment and initialize model
    api_key = setup_environment()
    llm = initialize_chat_model(api_key)
    
    # Initialize conversation history
    conversation_history = [
        SystemMessage(content="You are a helpful AI assistant.")
    ]
    
    print("\n=== Welcome to the OpenAI Chatbot! ===")
    print("Type 'exit' to quit or 'clear' to clear history.\n")

    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Handle special commands
            if user_input.lower() == "exit":
                print("\nGoodbye! Thank you for chatting.")
                break
            elif user_input.lower() == "clear":
                conversation_history = [SystemMessage(content="You are a helpful AI assistant.")]
                print("\nConversation history cleared.")
                continue
            elif not user_input:
                continue

            # Add user message to history
            conversation_history.append(HumanMessage(content=user_input))

            # Get AI response
            response = llm.invoke(conversation_history)
            
            # Add AI response to history and print it
            conversation_history.append(AIMessage(content=response.content))
            print(f"\nAI: {response.content}")

        except KeyboardInterrupt:
            print("\n\nExiting gracefully...")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try again.")

if __name__ == "__main__":
    chat_with_openai()