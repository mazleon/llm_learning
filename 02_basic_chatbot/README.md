# 02_basic_chatbot

This directory contains three Python scripts demonstrating basic chatbot interactions using different language models: OpenAI, Google Gemini, and Ollama.  Each script provides a simple command-line interface for chatting with the respective model.

## 01_chat_with_openai.py

This script uses the Langchain library to interact with the OpenAI API. It allows users to have a conversation with a GPT-3.5-turbo model.  Key features include:

*   **Environment Setup:** Loads OpenAI API key from a `.env` file.  Ensure you have set the `OPENAI_API_KEY` environment variable.
*   **Model Initialization:** Initializes a `ChatOpenAI` model with specified parameters (model name, temperature).
*   **Conversation Handling:** Manages conversation history and handles user input, including commands like 'exit' and 'clear'.
*   **Error Handling:** Includes robust error handling for API requests and model initialization.

## 02_chat_with_gemini.py

This script utilizes the Google Generative AI library to interact with the Gemini Pro model.  It offers similar functionality to the OpenAI script but with Google's Gemini API:

*   **Environment Setup:** Loads Google API key from a `.env` file.  Ensure you have set the `GOOGLE_API_KEY` environment variable.
*   **Model Initialization:** Initializes a Gemini model with generation configuration parameters (temperature, top_p, top_k).
*   **Conversation Handling:** Manages conversation history and handles user input, including commands like 'exit', 'clear', and 'history' to view the chat history.
*   **Error Handling:** Includes error handling for API requests and model initialization.

## 03_chat_with_ollama_local.py

This script interacts with a locally running Ollama instance. It provides a flexible chat interface that allows users to switch between different models available on the Ollama server.

*   **Connection Verification:** Verifies the connection to the Ollama server before starting the chat.
*   **Model Listing:** Lists available models on the Ollama server.
*   **Model Selection:** Allows users to choose a model from the list or use the default model.
*   **Conversation Handling:** Manages conversation history and handles user input, including commands like 'exit', 'clear', and 'model' to switch models.
*   **Error Handling:** Includes error handling for API requests and other potential issues.


**To run these scripts:**

1.  **Install dependencies:**  Make sure you have the required libraries installed.  You can install them using `pip install -r requirements.txt`.
2.  **Set API keys:** Create a `.env` file in the same directory and add your OpenAI API key (`OPENAI_API_KEY`) and Google API key (`GOOGLE_API_KEY`).  For Ollama, ensure your Ollama server is running on `localhost:11434`.
3.  **Run the script:** Execute the desired script using `python <script_name>.py`.




## Chat with LLM

## Introduction

In this blog post, we'll explore how to build a modern, interactive chat application that integrates multiple Large Language Models (LLMs) using Streamlit. Our application supports OpenAI's GPT models, Google's Gemini, and Ollama's local models, giving users the flexibility to choose their preferred AI model.

## Key Features

### 1. Multi-Model Support

-   **OpenAI Integration**: Access GPT models with API key authentication
-   **Google Gemini**: Utilize Google's latest AI model with API key
-   **Ollama Local Models**: Run models locally with options:
    -   llama3.2:latest
    -   llama3.1:latest

### 2. Modern UI/UX Design

```
st.set_page_config(
    page_title="Chat with LLM",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

-   Clean, responsive interface with gradient backgrounds
-   Message bubbles with visual distinction between user and AI
-   Smooth animations and transitions
-   Sidebar for model selection and configuration

### 3. Secure API Key Management

```
def get_openai_chat():
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key", 
        type="password",
        value=os.getenv("OPENAI_API_KEY", "")
    )
 ```

-   Environment variable support (.env file)
-   Secure password input for API keys
-   Fallback to manual key entry if not in environment

### 4. Smart Error Handling

```
try:
    chat_model.invoke([HumanMessage(content="test")])
    return chat_model
except Exception as e:
    if "404" in str(e):
        st.sidebar.error(f"Model {ollama_model} not found...")
```

-   Graceful error handling for model unavailability
-   Clear error messages with resolution steps
-   Automatic model availability testing

### 5. Session Management

```
if "messages" not in st.session_state:
    st.session_state.messages = []
if "gemini_chat" not in st.session_state:
    st.session_state.gemini_chat = None
```

-   Persistent chat history within session
-   Separate chat instances for different models
-   Clear chat functionality

## Technical Implementation

### CSS Styling

The application uses custom CSS for a polished look:

```
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
}
```

### Model Integration

Each model is implemented with its own configuration:

1.  **OpenAI**:
    
    -   Uses  `ChatOpenAI`  from langchain_openai
    -   Supports API key configuration
    -   Maintains conversation context
2.  **Gemini**:
    
    -   Uses Google's generative AI SDK
    -   Custom chat session management
    -   Temperature and generation config support
3.  **Ollama**:
    
    -   Local model integration
    -   Model selection dropdown
    -   Automatic availability checking

### Message Handling

```
st.session_state.messages.append({
    "role": "user",
    "content": prompt
})
```

-   Consistent message format across models
-   Real-time message display
-   Markdown support for formatted responses

## Usage Instructions

1.  **Setup**:
    
    
    ```
    `pip install streamlit langchain-openai google-generativeai python-dotenv
    ```
    
2.  **Configuration**:
    
    -   Create a  `.env`  file with your API keys:
        
        ```
        OPENAI_API_KEY=your_key_here
		GOOGLE_API_KEY=your_key_here	```
        
3.  **Running the App**:
    
    `streamlit run app.py`
    
4.  **Using Different Models**:
    
    -   Select model from sidebar
    -   Enter API keys if required
    -   For Ollama, ensure models are pulled:
      
        `ollama pull llama3.2:latest`
        

## Conclusion

This Streamlit application demonstrates how to create a professional-grade chat interface that supports multiple LLM providers. The modular design makes it easy to add new models or customize existing ones, while the modern UI provides an excellent user experience.

## Future Enhancements

-   Add support for more LLM providers
-   Implement file upload for context
-   Add conversation export functionality
-   Integrate model-specific parameters adjustment
-   Add conversation branching

The complete source code is available in the app.py file, and you can customize it further based on your specific needs.
