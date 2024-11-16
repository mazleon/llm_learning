import os
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Set up OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please set it in your .env file.")

# Initialize the OpenAI model
llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_api_key)

# Create a conversation chain
conversation = ConversationChain(llm=llm)

def chat():
    print("Welcome to the LangChain Chatbot! Type 'exit' to end the chat.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Chat ended.")
            break
        response = conversation.predict(input=user_input)
        print(f"Bot: {response}")

if __name__ == "__main__":
    chat()