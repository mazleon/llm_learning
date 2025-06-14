# Basic Chatbot Collection

This directory contains Python scripts demonstrating chatbot implementations using various language models. Each script provides a command-line interface for interacting with different AI models.

## Available Chatbots

### 01_chat_with_openai.py
A simple chat interface for OpenAI's GPT models.

This script uses the Langchain library to interact with the OpenAI API. It allows users to have a conversation with a GPT-3.5-turbo model.  Key features include:

*   **Environment Setup:** Loads OpenAI API key from a `.env` file.  Ensure you have set the `OPENAI_API_KEY` environment variable.
*   **Model Initialization:** Initializes a `ChatOpenAI` model with specified parameters (model name, temperature).
*   **Conversation Handling:** Manages conversation history and handles user input, including commands like 'exit' and 'clear'.
*   **Error Handling:** Includes robust error handling for API requests and model initialization.

### 02_chat_with_gemini.py
A chat interface for Google's Gemini model with the following features:
- **Environment Setup:** Loads Google API key from `.env` file
- **Model Configuration:** Customizable temperature, top_p, and top_k parameters
- **Conversation Features:**
  - Maintains chat history
  - Commands: 'exit', 'clear', 'history'
  - Error handling for API requests

### 03_chat_with_ollama_local.py
A local chat interface for Ollama models with these features:
- **Local Model Support:** Works with any Ollama model
- **Model Management:**
  - Lists available models
  - Allows switching models during chat
  - Verifies model availability
- **Commands:** 'exit', 'clear', 'model'

### 04_chat_with_grok.py
A chat interface for Grok AI with the following features:
- **Environment Setup:** Requires Grok API key in `.env`
- **Conversation Features:**
  - Maintains chat history
  - Supports standard chat commands
  - Error handling for API requests

### 05_chat_with_deepseek.py
A chat interface for DeepSeek models via OpenRouter with these features:
- **Multiple Models:** Supports various DeepSeek models
- **Model Selection:** Choose from available models at runtime
- **Commands:** 'exit', 'clear', 'model' to switch models
- **Error Handling:** Robust API error handling

### app.py
A Streamlit web application that combines all chat interfaces into a single, interactive web app with:
- **Unified Interface:** Access all models from one place
- **Modern UI:** Clean, responsive design
- **Model Configuration:** Set API keys and parameters via UI
- **Session Management:** Maintains separate chat histories

## Getting Started

### Prerequisites
- Python 3.8+
- Required Python packages (install with `pip install -r requirements.txt`):
  ```
  python-dotenv
  openai
  google-generativeai
  ollama
  langchain-openai
  langchain-google-genai
  requests
  streamlit
  ```

### Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd llm_learning/02_basic_chatbot
   ```

2. Create a `.env` file in the project root with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   GOOGLE_API_KEY=your_google_api_key
   OPENROUTER_API_KEY=your_openrouter_api_key
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. For Ollama users, pull the desired models:
   ```bash
   ollama pull llama3.2:latest
   ```

### Running the Scripts

#### Command Line Interface
Run any of the individual chat scripts:
```bash
python 01_chat_with_openai.py
python 02_chat_with_gemini.py
python 03_chat_with_ollama_local.py
python 04_chat_with_grok.py
python 05_chat_with_deepseek.py
```

#### Web Interface
Run the Streamlit app for a unified interface:
```bash
streamlit run app.py
```

## Features Comparison

| Feature | OpenAI | Gemini | Ollama | DeepSeek | Grok |
|---------|--------|--------|--------|----------|------|
| Cloud-based | ✓ | ✓ | ✗ | ✓ | ✓ |
| Local Execution | ✗ | ✗� | ✓ | ✗ | ✗ |
| Model Selection | Limited | Limited | Full | Multiple | Limited |
| API Key Required | ✓ | ✓ | ✗ | ✓ | ✓ |
| Conversation History | ✓ | ✓ | ✓ | ✓ | ✓ |
| Custom Parameters | ✓ | ✓ | ✓ | ✓ | ✓ |

## Troubleshooting

- **API Connection Issues:** Ensure your API keys are correctly set in the `.env` file
- **Model Not Found (Ollama):** Make sure to pull the model first using `ollama pull <model-name>`
- **Module Not Found:** Install missing dependencies with `pip install -r requirements.txt`
- **Rate Limiting:** If you encounter rate limits, try reducing the frequency of your requests or upgrade your API plan

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.




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
