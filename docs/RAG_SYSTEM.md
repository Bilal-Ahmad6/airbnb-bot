# RAG (Retrieval-Augmented Generation) System

## Overview

This WhatsApp bot now uses **Gemini AI with RAG** to answer questions based on your knowledge base (PDF documents in the `data/` folder).

## How It Works

### 1. **Document Processing**
- Reads PDF files from the `data/` folder
- Extracts text and splits into chunks (500 words with 50-word overlap)
- Generates embeddings using `sentence-transformers` (all-MiniLM-L6-v2 model)

### 2. **Vector Database**
- Stores document chunks and embeddings in ChromaDB
- Persistent storage in `./chroma_db/` folder
- Only processes documents once (on first run)

### 3. **Query Processing**
When a user sends a message:
1. **Retrieve**: Search vector database for relevant content (top 3 chunks)
2. **Augment**: Add retrieved context to the user's question
3. **Generate**: Gemini AI generates answer based on context + question
4. **Respond**: Send answer back via WhatsApp

### 4. **Conversation Memory**
- Maintains separate chat history for each WhatsApp user (wa_id)
- Stores conversation in `chats_db` (local shelve database)
- Preserves context across multiple messages

## Architecture

```
User WhatsApp Message
       ↓
Flask Webhook Endpoint
       ↓
RAG Service (retrieve relevant PDF chunks)
       ↓
Gemini Service (generate response with context)
       ↓
WhatsApp API (send reply)
```

## Files Structure

```
app/
├── services/
│   ├── gemini_service.py    # Gemini AI integration + RAG
│   ├── rag_service.py        # Vector DB & retrieval logic
│   └── openai_service.py     # Original OpenAI implementation
├── utils/
│   └── whatsapp_utils.py     # WhatsApp message handling
data/
└── airbnb-faq.pdf            # Knowledge base document(s)
chroma_db/                     # Vector database (auto-created)
chats_db/                      # Chat history (auto-created)
```

## Adding More Documents

Simply add PDF files to the `data/` folder:

```
data/
├── airbnb-faq.pdf
├── house-rules.pdf
├── local-recommendations.pdf
└── emergency-contacts.pdf
```

Then delete the `chroma_db/` folder and restart Flask - it will reindex all documents.

## System Prompt

The bot is configured as:
> "You are a helpful WhatsApp assistant for an Airbnb in Paris. Use the knowledge base to answer questions accurately. If you don't know the answer, advise to contact the host directly. Be friendly and concise."

Modify this in `gemini_service.py` → `generate_response()` function.

## Technical Details

### Dependencies
- `google-generativeai`: Gemini AI API
- `PyPDF2`: PDF text extraction
- `chromadb`: Vector database
- `sentence-transformers`: Text embeddings

### Models Used
- **Gemini**: `gemini-2.5-flash` (fast, efficient)
- **Embeddings**: `all-MiniLM-L6-v2` (384-dimensional vectors)

### Configuration
- **Chunk size**: 500 words
- **Overlap**: 50 words
- **Retrieved chunks**: 3 per query
- **Similarity**: Cosine distance

## Testing

Run tests with:
```bash
python test_rag_simple.py   # Test RAG retrieval only
python test_rag.py           # Test full RAG + Gemini integration
```

## Comparison: OpenAI vs Gemini RAG

| Feature | OpenAI Assistants | Gemini + Custom RAG |
|---------|-------------------|---------------------|
| **Setup** | Simple (built-in) | Custom implementation |
| **Cost** | Higher | Lower (free Gemini tier) |
| **Control** | Limited | Full control over retrieval |
| **File Support** | Native | Manual PDF processing |
| **Customization** | Limited | Highly customizable |
| **Speed** | Good | Very fast (gemini-2.5-flash) |

## Troubleshooting

### "No contexts found"
- Check if PDFs exist in `data/` folder
- Delete `chroma_db/` and restart to reindex

### "Module not found" errors
- Run: `pip install -r requirements.txt`

### Slow first run
- First run downloads ~80MB embedding model
- Subsequent runs are fast (model is cached)

## Future Enhancements

- [ ] Support for more file types (DOCX, TXT, etc.)
- [ ] Hybrid search (keyword + semantic)
- [ ] Re-ranking for better accuracy
- [ ] Metadata filtering (by document, date, etc.)
- [ ] Admin commands to reindex documents
