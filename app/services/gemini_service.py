import google.generativeai as genai
import shelve
from dotenv import load_dotenv
import os
import logging
from .rag_service import get_rag_instance

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=generation_config,
)

# Initialize RAG
rag = get_rag_instance()


def check_if_chat_exists(wa_id):
    """Check if a chat session exists for this WhatsApp ID"""
    with shelve.open("chats_db") as chats_shelf:
        return chats_shelf.get(wa_id, None)


def store_chat(wa_id, chat_history):
    """Store chat history for a WhatsApp ID"""
    with shelve.open("chats_db", writeback=True) as chats_shelf:
        chats_shelf[wa_id] = chat_history


def generate_response(message_body, wa_id, name):
    """
    Generate a response using Gemini AI with RAG.
    Maintains conversation history per user using their wa_id.
    """
    # Get relevant context from knowledge base
    context = rag.get_context_for_query(message_body, n_results=3)
    
    # Check if there is already a chat history for the wa_id
    chat_history = check_if_chat_exists(wa_id)

    # If a chat doesn't exist, create one with system instructions
    if chat_history is None:
        logging.info(f"Creating new chat for {name} with wa_id {wa_id}")
        chat_history = []
        
        # Start a new chat session
        chat = model.start_chat(history=chat_history)
        
        # Add system-like instruction as first message with knowledge base context
        system_message = (
            f"You are a helpful WhatsApp assistant for an Airbnb in Paris. "
            f"You are currently chatting with {name}. "
            f"Use the following knowledge base to answer questions accurately. "
            f"If you don't know the answer based on the knowledge base, say you cannot help with that question "
            f"and advise them to contact the host directly. "
            f"Be friendly, concise, and helpful. Keep answers brief for WhatsApp.\n\n"
            f"KNOWLEDGE BASE:\n{context if context else 'No specific context available.'}"
        )
        
        # Send system message (but don't include in stored history)
        chat.send_message(system_message)
    else:
        logging.info(f"Retrieving existing chat for {name} with wa_id {wa_id}")
        # Restore the chat session with existing history
        chat = model.start_chat(history=chat_history)

    # Prepare the user's message with context if available
    if context:
        enhanced_query = f"Based on the knowledge base, please answer: {message_body}\n\nRelevant information:\n{context}"
        logging.info(f"Enhanced query with RAG context")
    else:
        enhanced_query = message_body
    
    # Send the user's message and get response
    logging.info(f"User message: {message_body}")
    response = chat.send_message(enhanced_query)
    
    # Get the response text
    response_text = response.text
    logging.info(f"Generated response: {response_text}")
    
    # Update chat history (Gemini automatically maintains it in chat.history)
    store_chat(wa_id, chat.history)
    
    return response_text
