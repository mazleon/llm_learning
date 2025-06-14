import streamlit as st
import os
import json
import html
import requests
from dotenv import load_dotenv
from typing import Optional, Dict, Any, List, Union

# LangChain imports
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from google.generativeai.types import GenerationConfig
from langchain.schema import HumanMessage, AIMessage, SystemMessage
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Available models
AVAILABLE_MODELS = {
    "OpenAI": ["gpt-4o-mini", "gpt-4o"],
    "Gemini": ["gemini-2.0-flash-exp"],
    "Ollama": ["llama3.2:latest", "llama3.1:latest", "mistral:latest"],
    "Grok": ["grok-1"],
    "DeepSeek": ["deepseek/deepseek-chat", "deepseek/deepseek-coder"]
}

# Initialize session state
def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "gemini_chat" not in st.session_state:
        st.session_state.gemini_chat = None
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "OpenAI"
    if "model_name" not in st.session_state:
        st.session_state.model_name = AVAILABLE_MODELS["OpenAI"][0]
    if "api_keys" not in st.session_state:
        st.session_state.api_keys = {
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
            "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY", ""),
            "GROK_API_KEY": os.getenv("GROK_API_KEY", ""),
            "OPENROUTER_API_KEY": os.getenv("OPENROUTER_API_KEY", "")
        }

init_session_state()

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
        max-width: 100%;
        padding: 0 1rem;
        background-color: #f8fafc;
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        /* Base app styling */
        .stApp {
            background-color: #0f172a;
            color: #f8fafc;
        }
        
        /* Chat container and sidebar */
        .chat-container, .css-1d391kg, .st-emotion-cache-1cypcdb {
            background-color: #1e293b !important;
            color: #f8fafc !important;
        }
        
        /* Input fields */
        .message-content, .stTextInput > div > div > input, .stTextArea > div > div > textarea {
            color: #f8fafc !important;
            background-color: #1e293b !important;
        }
        
        /* Input placeholders */
        .stTextInput > div > div > input::placeholder,
        .stTextArea > div > div > textarea::placeholder {
            color: #94a3b8 !important;
        }
        
        /* Sidebar text */
        .stSidebar *,
        .stSidebar .stMarkdown,
        .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4,
        .stSidebar p, .stSidebar span, .stSidebar div,
        .stSidebar label,
        .stSidebar .stMarkdown p,
        .stSidebar .stMarkdown span,
        .stSidebar .stSelectbox > label,
        .stSidebar .stRadio > label,
        .stSidebar .stCheckbox > label,
        .stSidebar .stNumberInput > label,
        .stSidebar .stSlider > label,
        .stSidebar .stSelectbox > div > div > div {
            color: #f8fafc !important;
        }
        
        /* Dropdown menus */
        .stSelectbox > div > div > div > div,
        .stSelectbox ul li {
            color: #f8fafc !important;
            background-color: #1e293b !important;
        }
        
        /* Hover states */
        .stSelectbox ul li:hover,
        .stSelectbox > div:hover > div > div,
        .stButton > button:hover,
        .stForm > div > div > div > div:hover {
            background-color: #2d3748 !important;
        }
        
        /* Form elements */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > div,
        .stNumberInput > div > div > input,
        .stSlider > div > div > div > div {
            border-color: #4a5568 !important;
            background-color: #1e293b !important;
            color: #f8fafc !important;
        }
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #ffffff;
        padding: 1.5rem 1rem;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.05);
    }
    
    /* Title styling */
    .main-title {
        text-align: center;
        padding: 1.5rem 0;
        margin: -1rem -1rem 2rem -1rem;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.2);
    }
    
    /* Chat container styling */
    .chat-container {
        background-color: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 2px 20px rgba(0, 0, 0, 0.05);
        margin: 0 auto 2rem;
        max-width: 900px;
        border: 1px solid #e2e8f0;
    }
    
    /* Message styling */
    .chat-message {
        padding: 1.25rem 1.5rem;
        border-radius: 16px;
        margin-bottom: 1.25rem;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        position: relative;
        transition: all 0.2s ease;
        max-width: 90%;
    }
    
    .chat-message:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    .user-message {
        background-color: #f0f4ff;
        border-left: 4px solid #4f46e5;
        margin-left: auto;
        margin-right: 0;
        border-top-right-radius: 4px;
        border-bottom-right-radius: 4px;
    }
    
    .assistant-message {
        background-color: #ffffff;
        border-left: 4px solid #8b5cf6;
        margin-right: auto;
        margin-left: 0;
        border-top-left-radius: 4px;
        border-bottom-left-radius: 4px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    
    /* Dark mode message styling */
    @media (prefers-color-scheme: dark) {
        .user-message {
            background-color: #1e293b;
            border-left: 4px solid #6366f1;
            color: #f8fafc;
        }
        
        .assistant-message {
            background-color: #0f172a;
            border-left: 4px solid #8b5cf6;
            color: #f8fafc;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }
        
        .message-content {
            color: #f8fafc !important;
        }
        
        .message-header {
            color: #c7d2fe !important;
        }
    }
    
    /* Message header styling */
    .message-header {
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        color: #4f46e5;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    .assistant-message .message-header {
        color: #8b5cf6;
    }
    
    /* Message content styling */
    .message-content {
        line-height: 1.6;
        color: #1e293b;
        font-size: 1rem;
    }
    
    /* Input area styling */
    .stTextInput > div > div {
        border-radius: 16px;
        padding: 0.5rem;
        background: white;
        box-shadow: 0 2px 15px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div:focus-within {
        border-color: #8b5cf6;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2);
    }
    
    .stTextInput > div > div > input {
        padding: 1rem 1.25rem;
        font-size: 1rem;
        border: none;
        border-radius: 12px;
        background: transparent;
    }
    
    .stTextInput > div > div > input:focus {
        box-shadow: none;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #94a3b8;
        opacity: 1;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 12px;
        padding: 0.75rem 2rem;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(99, 102, 241, 0.2);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #c7d2fe;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #8b5cf6;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2);
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background-color: #8b5cf6 !important;
    }
    
    .stSlider > div > div > div > div > div {
        background-color: white;
        border: 2px solid #8b5cf6;
    }
    
    /* Number input styling */
    .stNumberInput > div > div > input {
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        padding: 0.5rem 1rem;
    }
    
    /* Error message styling */
    .stAlert {
        border-radius: 12px;
        border: none;
        background-color: #fef2f2;
        border-left: 4px solid #ef4444;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
    </style>
""", unsafe_allow_html=True)

def get_openai_chat():
    with st.sidebar.form("openai_key_form"):
        st.session_state.api_keys["OPENAI_API_KEY"] = st.text_input(
            "OpenAI API Key", 
            type="password", 
            value=st.session_state.api_keys["OPENAI_API_KEY"]
        )
        st.form_submit_button("Save")
    
    if not st.session_state.api_keys["OPENAI_API_KEY"]:
        st.sidebar.error("Please provide your OpenAI API key!")
        return None
    
    try:
        return ChatOpenAI(
            openai_api_key=st.session_state.api_keys["OPENAI_API_KEY"],
            model_name=st.session_state.model_name
        )
    except Exception as e:
        st.error(f"Error initializing OpenAI: {str(e)}")
        return None

def initialize_gemini():
    with st.sidebar.form("google_key_form"):
        st.session_state.api_keys["GOOGLE_API_KEY"] = st.text_input(
            "Google API Key", 
            type="password", 
            value=st.session_state.api_keys["GOOGLE_API_KEY"]
        )
        st.form_submit_button("Save")
    
    if not st.session_state.api_keys["GOOGLE_API_KEY"]:
        st.sidebar.error("Please provide your Google API key!")
        return None
    
    try:
        genai.configure(api_key=st.session_state.api_keys["GOOGLE_API_KEY"])
        
        # Get the selected model name
        model_name = st.session_state.model_name
        
        # Create generation config with proper typing
        generation_config = GenerationConfig(
            temperature=0.7,
            top_p=0.8,
            top_k=40,
            max_output_tokens=2048,
        )
        
        # Initialize the model with the selected model name
        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config
        )
        
        # Initialize chat if not already done
        if st.session_state.gemini_chat is None:
            st.session_state.gemini_chat = model.start_chat(history=[])
        
        return model
    except Exception as e:
        st.error(f"Error initializing Gemini: {str(e)}")
        return None

def get_ollama_chat():
    with st.sidebar.form("ollama_url_form"):
        ollama_base_url = st.text_input("Ollama Base URL", value="http://localhost:11434")
        st.form_submit_button("Save")
    
    try:
        from langchain_ollama import ChatOllama as NewChatOllama
        chat_model = NewChatOllama(
            base_url=ollama_base_url,
            model=st.session_state.model_name
        )
        
        # Test if model is available
        try:
            chat_model.invoke([HumanMessage(content="test")])
            return chat_model
        except Exception as e:
            if "404" in str(e):
                st.sidebar.error(f"Model {st.session_state.model_name} not found. Please run:\n```\nollama pull {st.session_state.model_name}\n```")
            else:
                st.sidebar.error(f"Error testing Ollama model: {str(e)}")
            return None
            
    except Exception as e:
        st.sidebar.error(f"Error initializing Ollama: {str(e)}")
        return None

def get_grok_chat():
    with st.sidebar.form("grok_key_form"):
        st.session_state.api_keys["GROK_API_KEY"] = st.text_input(
            "Grok API Key", 
            type="password", 
            value=st.session_state.api_keys["GROK_API_KEY"]
        )
        st.form_submit_button("Save")
    
    if not st.session_state.api_keys["GROK_API_KEY"]:
        st.sidebar.error("Please provide your Grok API key!")
        return None
    
    class GrokChat:
        def __init__(self, api_key: str, model: str = "grok-1"):
            self.api_key = api_key
            self.model = model
            self.base_url = "https://api.groq.com/openai/v1"
            self.headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        
        def invoke(self, messages: List[Dict[str, str]]) -> str:
            try:
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json={
                        "model": self.model,
                        "messages": messages,
                        "temperature": 0.7
                    }
                )
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]
            except Exception as e:
                st.error(f"Error calling Grok API: {str(e)}")
                raise
    
    try:
        return GrokChat(api_key=st.session_state.api_keys["GROK_API_KEY"], model=st.session_state.model_name)
    except Exception as e:
        st.error(f"Error initializing Grok: {str(e)}")
        return None

def get_deepseek_chat():
    with st.sidebar.form("openrouter_key_form"):
        st.session_state.api_keys["OPENROUTER_API_KEY"] = st.text_input(
            "OpenRouter API Key", 
            type="password", 
            value=st.session_state.api_keys["OPENROUTER_API_KEY"]
        )
        st.form_submit_button("Save")
    
    if not st.session_state.api_keys["OPENROUTER_API_KEY"]:
        st.sidebar.error("Please provide your OpenRouter API key!")
        return None
    
    class DeepSeekChat:
        def __init__(self, api_key: str, model: str):
            self.api_key = api_key
            self.model = model
            self.base_url = "https://openrouter.ai/api/v1"
            self.headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        
        def invoke(self, messages: List[Dict[str, str]]) -> str:
            try:
                # Convert LangChain messages to OpenRouter format
                openrouter_messages = []
                for msg in messages:
                    if isinstance(msg, HumanMessage):
                        role = "user"
                    elif isinstance(msg, AIMessage):
                        role = "assistant"
                    else:
                        role = "system"
                    openrouter_messages.append({"role": role, "content": msg.content})
                
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json={
                        "model": self.model,
                        "messages": openrouter_messages,
                        "temperature": 0.7
                    }
                )
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]
            except Exception as e:
                st.error(f"Error calling OpenRouter API: {str(e)}")
                raise
    
    try:
        return DeepSeekChat(api_key=st.session_state.api_keys["OPENROUTER_API_KEY"], model=st.session_state.model_name)
    except Exception as e:
        st.error(f"Error initializing DeepSeek: {str(e)}")
        return None

# Title
st.markdown('<h1 class="main-title">💬 Chat with LLM</h1>', unsafe_allow_html=True)

# Sidebar - Model Selection
with st.sidebar:
    st.header("Model Configuration")
    
    # Store previous model provider to detect changes
    previous_provider = st.session_state.get('selected_model', 'OpenAI')
    
    # Model provider selection
    model_provider = st.selectbox(
        "Choose Model Provider",
        list(AVAILABLE_MODELS.keys()),
        index=list(AVAILABLE_MODELS.keys()).index(st.session_state.selected_model) if st.session_state.selected_model in AVAILABLE_MODELS else 0,
        key="model_provider"
    )
    
    # Reset model name if provider changed
    if model_provider != previous_provider:
        st.session_state.model_name = AVAILABLE_MODELS[model_provider][0]
    
    st.session_state.selected_model = model_provider
    
    # Model selection based on provider
    model_name = st.selectbox(
        f"Select {model_provider} Model",
        AVAILABLE_MODELS[model_provider],
        index=AVAILABLE_MODELS[model_provider].index(st.session_state.model_name) if st.session_state.model_name in AVAILABLE_MODELS[model_provider] else 0,
        key="model_selector"
    )
    st.session_state.model_name = model_name
    
    # Model-specific configuration
    st.subheader("Model Settings")
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
    max_tokens = st.number_input("Max Tokens", 100, 4000, 1000, 100)
    
    st.markdown("---")
    st.markdown("### API Keys")
    st.caption("Enter your API keys below. They'll be saved in your session.")

# Get the appropriate chat model
chat_model = None
model_functions = {
    "OpenAI": get_openai_chat,
    "Gemini": initialize_gemini,
    "Ollama": get_ollama_chat,
    "Grok": get_grok_chat,
    "DeepSeek": get_deepseek_chat
}

# Only try to initialize the model if we have the required API key
if model_provider in model_functions:
    try:
        chat_model = model_functions[model_provider]()
    except Exception as e:
        st.sidebar.error(f"Error initializing {model_provider}: {str(e)}")
        st.session_state.pop('_error', None)
        st.session_state['_error'] = f"Failed to initialize {model_provider}. Please check your API key and try again."

# Main chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    with st.container():
        # Clean and format the message content
        content = message['content']
        
        # Convert markdown code blocks to HTML with proper formatting
        if '```' in content:
            # Split content by code blocks
            parts = content.split('```')
            formatted_parts = []
            
            for i, part in enumerate(parts):
                # Every odd part is a code block
                if i % 2 == 1:
                    # Get language if specified (first line)
                    lines = part.split('\n', 1)
                    language = lines[0].strip() if len(lines) > 1 and lines[0].strip() else ''
                    code = lines[1] if len(lines) > 1 else lines[0]
                    
                    # Format as code block
                    formatted_parts.append(f'<pre><code class="language-{language}">{html.escape(code)}</code></pre>')
                else:
                    # Format regular text with line breaks
                    formatted_parts.append(html.escape(part).replace('\n', '<br>'))
            
            formatted_content = ''.join(formatted_parts)
        else:
            # Simple text with line breaks
            formatted_content = html.escape(content).replace('\n', '<br>')
        
        st.markdown(f"""
            <div class="chat-message {'user-message' if message['role'] == 'user' else 'assistant-message'} animate__animated animate__fadeIn">
                <div class="message-header">
                    {"👤 You" if message['role'] == 'user' else f"🤖 {model_provider}"}
                </div>
                <div class="message-content">
                    {formatted_content}
                </div>
            </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Fixed input area at the bottom
st.markdown("""
    <style>
        .fixed-input {
            position: fixed;
            bottom: 2rem;
            left: 0;
            right: 0;
            padding: 0 2rem;
            max-width: 900px;
            margin: 0 auto;
            background: white;
            z-index: 1000;
            border-radius: 16px;
            box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.05);
        }
        @media (prefers-color-scheme: dark) {
            .fixed-input {
                background: #1e293b !important;
            }
        }
        @media (max-width: 768px) {
            .fixed-input {
                padding: 0 1rem;
                bottom: 1rem;
            }
        }
    </style>
    <div class="fixed-input">
""", unsafe_allow_html=True)

# Chat input with improved styling
prompt = st.chat_input("Message...", key="user_input")

st.markdown("</div>", unsafe_allow_html=True)

# Handle user input and AI response
if prompt:
    if not chat_model:
        st.error("⚠️ Please configure the model properly in the sidebar!")
    else:
        # Add user message to state if it's not already there
        if not st.session_state.messages or st.session_state.messages[-1]["content"] != prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Process the message immediately instead of rerunning
            with st.spinner("Generating response..."):
                try:
                    # Clear any previous errors
                    st.session_state.pop('_error', None)
                    
                    if model_provider == "Gemini":
                        if st.session_state.gemini_chat is None:
                            model = genai.GenerativeModel(model_name=st.session_state.model_name)
                            st.session_state.gemini_chat = model.start_chat(history=[])
                        response = st.session_state.gemini_chat.send_message(prompt)
                        response_text = response.text
                    
                    elif model_provider in ["OpenAI", "Ollama"]:
                        if model_provider == "OpenAI":
                            # Convert session messages to LangChain format
                            messages = []
                            for msg in st.session_state.messages:
                                if msg["role"] == "user":
                                    messages.append(HumanMessage(content=msg["content"]))
                                elif msg["role"] == "assistant":
                                    messages.append(AIMessage(content=msg["content"]))
                            
                            # Make sure the latest message is included
                            if not messages or messages[-1].content != prompt:
                                messages.append(HumanMessage(content=prompt))
                            
                            response = chat_model.invoke(messages)
                            response_text = response.content
                        else:  # Ollama
                            messages = [HumanMessage(content=prompt)]
                            response = chat_model.invoke(messages)
                            response_text = response.content
                    
                    else:  # Grok or DeepSeek
                        # Convert all messages to the format expected by these APIs
                        messages = [
                            {"role": "user" if msg["role"] == "user" else "assistant", "content": msg["content"]}
                            for msg in st.session_state.messages
                        ]
                        
                        # Ensure the latest message is included
                        if not messages or messages[-1]["content"] != prompt:
                            messages.append({"role": "user", "content": prompt})
                            
                        response_text = chat_model.invoke(messages)
                    
                    # Add assistant's response to state
                    # Ensure response is a string and clean any unwanted HTML
                    if not isinstance(response_text, str):
                        response_text = str(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                    
                    # Rerun to update the UI
                    st.rerun()
                    
                except Exception as e:
                    st.session_state._error = str(e)
                    st.error(f"Error generating response: {str(e)}")
                    st.rerun()

# Show error message if any
if '_error' in st.session_state:
    st.error(f"Error: {st.session_state._error}")
    st.button("Clear Error", on_click=lambda: st.session_state.pop('_error', None))

# Add a clear chat button
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.gemini_chat = None