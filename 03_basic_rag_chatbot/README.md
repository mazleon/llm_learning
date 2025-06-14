# RAG-based Chatbot with Gemini and LangChain

A Retrieval-Augmented Generation (RAG) chatbot that leverages Google's Gemini model, LangChain framework, and a vector database to provide accurate and context-aware responses.

## Features

- **Document Ingestion**: Load and process various document formats (PDF, TXT, DOCX, etc.)
- **Vector Embeddings**: Convert documents into vector representations using state-of-the-art embedding models
- **Semantic Search**: Retrieve relevant document chunks based on user queries
- **Context-Aware Responses**: Generate accurate responses using Gemini model with retrieved context
- **Conversation Memory**: Maintain chat history for coherent multi-turn conversations
- **Web Interface**: User-friendly Streamlit-based web interface

## Prerequisites

- Python 3.8+
- Google API Key (for Gemini)
- [Optional] Vector Database (Chroma, FAISS, or Pinecone)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd 03_basic_rag_chatbot
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the project root and add your API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   # Optional: Add other API keys if using additional services
   ```

## Project Structure

```
03_basic_rag_chatbot/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables
├── data/                 # Directory for document storage
├── vector_store/         # Directory for vector database
└── README.md             # This file
```

## Usage

1. Place your documents in the `data/` directory
2. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
3. Open your browser and navigate to the provided local URL
4. Upload documents and start chatting!

## How It Works

1. **Document Processing**:
   - Documents are split into smaller chunks
   - Each chunk is converted to vector embeddings
   - Vectors are stored in a vector database

2. **Query Processing**:
   - User query is converted to a vector
   - Most relevant document chunks are retrieved
   - Context is passed to the Gemini model
   - Response is generated based on the retrieved context

## Customization

- **Embedding Model**: Modify `get_embedding_model()` in `app.py`
- **Vector Store**: Change the vector store in `setup_vector_store()`
- **Chat Model**: Adjust parameters in `get_chat_model()`
- **UI**: Customize the Streamlit interface in `app.py`

## Dependencies

- `streamlit` - Web application framework
- `langchain` - Framework for developing LLM applications
- `google-generativeai` - Google's Gemini model integration
- `python-dotenv` - Environment variable management
- `chromadb` - Vector database (or other supported vector stores)
- `pypdf` - PDF processing
- `python-docx` - DOCX document processing

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [LangChain Documentation](https://python.langchain.com/)
- [Google AI Gemini](https://ai.google.dev/)
- [Streamlit](https://streamlit.io/)

## Support

For support, please open an issue in the repository or contact the maintainers.
