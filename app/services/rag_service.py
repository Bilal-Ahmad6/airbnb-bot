"""
RAG (Retrieval-Augmented Generation) system for Gemini
Loads PDF documents, creates embeddings, and retrieves relevant context
"""
import os
import logging
from pathlib import Path
import PyPDF2
import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.config import Settings

class GeminiRAG:
    def __init__(self, data_folder="data", collection_name="airbnb_docs"):
        """Initialize the RAG system with ChromaDB and sentence transformer"""
        self.data_folder = Path(data_folder)
        self.collection_name = collection_name
        
        # Initialize embedding model (smaller, faster model)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize ChromaDB client with persistent storage
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        
        # Get or create collection
        self.collection = self.chroma_client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        # Check if collection is empty and load documents if needed
        if self.collection.count() == 0:
            logging.info("Collection is empty. Loading documents...")
            self.load_documents()
        else:
            logging.info(f"Collection loaded with {self.collection.count()} documents")
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF file"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            logging.info(f"Extracted {len(text)} characters from {pdf_path}")
            return text
        except Exception as e:
            logging.error(f"Error reading PDF {pdf_path}: {e}")
            return ""
    
    def chunk_text(self, text, chunk_size=500, overlap=50):
        """Split text into overlapping chunks"""
        chunks = []
        words = text.split()
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk:
                chunks.append(chunk)
        
        logging.info(f"Created {len(chunks)} chunks from text")
        return chunks
    
    def load_documents(self):
        """Load all PDF documents from data folder"""
        pdf_files = list(self.data_folder.glob("*.pdf"))
        
        if not pdf_files:
            logging.warning(f"No PDF files found in {self.data_folder}")
            return
        
        all_chunks = []
        all_metadata = []
        all_ids = []
        
        for pdf_file in pdf_files:
            logging.info(f"Processing {pdf_file.name}...")
            text = self.extract_text_from_pdf(pdf_file)
            
            if text:
                chunks = self.chunk_text(text)
                
                for i, chunk in enumerate(chunks):
                    all_chunks.append(chunk)
                    all_metadata.append({
                        "source": pdf_file.name,
                        "chunk_id": i
                    })
                    all_ids.append(f"{pdf_file.stem}_chunk_{i}")
        
        if all_chunks:
            # Generate embeddings
            logging.info("Generating embeddings...")
            embeddings = self.embedding_model.encode(all_chunks).tolist()
            
            # Add to ChromaDB
            self.collection.add(
                embeddings=embeddings,
                documents=all_chunks,
                metadatas=all_metadata,
                ids=all_ids
            )
            logging.info(f"✅ Loaded {len(all_chunks)} document chunks into vector database")
        else:
            logging.warning("No content extracted from PDFs")
    
    def retrieve_context(self, query, n_results=3):
        """Retrieve relevant context for a query"""
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query]).tolist()
        
        # Search in ChromaDB
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        
        if results['documents'] and results['documents'][0]:
            contexts = results['documents'][0]
            logging.info(f"Retrieved {len(contexts)} relevant contexts")
            return contexts
        else:
            logging.info("No relevant contexts found")
            return []
    
    def get_context_for_query(self, query, n_results=3):
        """Get formatted context string for a query"""
        contexts = self.retrieve_context(query, n_results)
        
        if contexts:
            context_str = "\n\n---\n\n".join(contexts)
            return context_str
        else:
            return ""


# Singleton instance
_rag_instance = None

def get_rag_instance():
    """Get or create RAG instance (singleton pattern)"""
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = GeminiRAG()
    return _rag_instance
