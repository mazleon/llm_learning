import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain.schema import HumanMessage, AIMessage
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Chat with LLM",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply custom CSS
st.markdown("""
    <style>
    /* Main container styling */
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
        background-color: #f8f9fa;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #ffffff;
        padding: 2rem 1rem;
    }
    
    /* Title styling */
    .main-title {
        text-align: center;
        color: #1f1f1f;
        padding: 1rem 0;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Chat container styling */
    .chat-container {
        background-color: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 0 auto;
        max-width: 800px;
    }
    
    /* Message styling */
    .chat-message {
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left: 5px solid #2196f3;
        margin-left: 2rem;
        margin-right: 0;
    }
    
    .assistant-message {
        background-color: #f5f5f5;
        border-left: 5px solid #9e9e9e;
        margin-right: 2rem;
        margin-left: 0;
    }
    
    /* Message header styling */
    .message-header {
        font-weight: bold;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #424242;
    }
    
    /* Message content styling */
    .message-content {
        line-height: 1.5;
        color: #212121;
    }
    
    /* Input box styling */
    .stTextInput > div > div > input {
        border-radius: 25px;
        padding: 0.75rem 1.5rem;
        border: 2px solid #e0e0e0;
        font-size: 1rem;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 25px;
        padding: 0.5rem 2rem;
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
    }
    
    /* Error message styling */
    .stAlert {
        border-radius: 10px;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "gemini_chat" not in st.session_state:
    st.session_state.gemini_chat = None

def get_openai_chat():
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    if not openai_api_key:
        st.error("Please provide your OpenAI API key!")
        return None
    return ChatOpenAI(openai_api_key=openai_api_key)

def initialize_gemini():
    google_api_key = st.sidebar.text_input("Google API Key", type="password", value=os.getenv("GOOGLE_API_KEY", ""))
    if not google_api_key:
        st.error("Please provide your Google API key!")
        return None
    
    try:
        genai.configure(api_key=google_api_key)
        model = genai.GenerativeModel(
            model_name="gemini-pro",
            generation_config={
                "temperature": 0.7,
                "top_p": 0.8,
                "top_k": 40,
            }
        )
        if st.session_state.gemini_chat is None:
            st.session_state.gemini_chat = model.start_chat(history=[])
        return model
    except Exception as e:
        st.error(f"Error initializing Gemini model: {str(e)}")
        return None

def get_ollama_chat():
    ollama_base_url = st.sidebar.text_input("Ollama Base URL", value="http://localhost:11434")
    model_name = "llama2:latest"  # Default model
    
    # Add model selection for Ollama
    ollama_model = st.sidebar.selectbox(
        "Choose Ollama Model",
        ["llama3.2:latest", "llama3.1:latest"],
        index=0
    )
    
    try:
        # Try to create chat model with selected configuration
        chat_model = ChatOllama(
            base_url=ollama_base_url,
            model=ollama_model
        )
        
        # Test if model is available by sending a simple message
        try:
            chat_model.invoke([HumanMessage(content="test")])
            return chat_model
        except Exception as e:
            if "404" in str(e):
                st.sidebar.error(f"Model {ollama_model} not found. Please run:\n```\nollama pull {ollama_model}\n```")
            else:
                st.sidebar.error(f"Error testing Ollama model: {str(e)}")
            return None
            
    except Exception as e:
        st.sidebar.error(f"Error initializing Ollama: {str(e)}")
        return None

# Title
st.markdown('<h1 class="main-title">💬 Chat with LLM</h1>', unsafe_allow_html=True)

# Model selection
model_option = st.sidebar.selectbox(
    "Choose your LLM model",
    ["OpenAI", "Gemini", "Ollama"]
)

# Get the appropriate chat model
chat_model = None
if model_option == "OpenAI":
    chat_model = get_openai_chat()
elif model_option == "Gemini":
    chat_model = initialize_gemini()
else:
    chat_model = get_ollama_chat()

# Create a container for the chat interface
chat_container = st.container()

with chat_container:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.container():
            st.markdown(f"""
                <div class="chat-message {'user-message' if message['role'] == 'user' else 'assistant-message'}">
                    <div class="message-header">
                        {"👤 User" if message['role'] == 'user' else "🤖 Assistant"}
                    </div>
                    <div class="message-content">
                        {message['content']}
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # Chat input
    if prompt := st.chat_input("What's on your mind?"):
        if not chat_model:
            st.error("Please configure the model properly!")
        else:
            # Add user message to state and display
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.container():
                st.markdown(f"""
                    <div class="chat-message user-message">
                        <div class="message-header">👤 User</div>
                        <div class="message-content">{prompt}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Get AI response
            with st.spinner("Thinking..."):
                try:
                    if model_option == "Gemini":
                        response = st.session_state.gemini_chat.send_message(prompt)
                        response_text = response.text
                    else:
                        if model_option == "OpenAI":
                            messages = [HumanMessage(content=msg["content"]) for msg in st.session_state.messages if msg["role"] == "user"]
                        else:  # Ollama
                            messages = [HumanMessage(content=prompt)]
                        response = chat_model.invoke(messages)
                        response_text = response.content
                    
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                    
                    # Display AI response
                    with st.container():
                        st.markdown(f"""
                            <div class="chat-message assistant-message">
                                <div class="message-header">🤖 Assistant</div>
                                <div class="message-content">{response_text}</div>
                            </div>
                        """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Add a clear chat button
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.gemini_chat = None
    st.rerun()