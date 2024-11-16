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
