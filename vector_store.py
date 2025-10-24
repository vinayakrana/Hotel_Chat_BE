"""
ChromaDB Vector Store for RAG (Retrieval-Augmented Generation)
Manages FAQ embeddings and semantic search
"""
import chromadb
from chromadb.config import Settings
from typing import List
import os

# Initialize ChromaDB client with local persistence
client = chromadb.Client(Settings(
    persist_directory="./data/chroma",
    anonymized_telemetry=False
))

# Get or create collection
collection = client.get_or_create_collection(
    name="hotel_faqs",
    metadata={"description": "Hotel FAQ documents for semantic search"}
)


def load_faqs_to_vector_store():
    """
    Load FAQs from file into vector store
    Creates embeddings for semantic search
    """
    faq_path = "data/faqs.txt"
    
    if not os.path.exists(faq_path):
        print(f"Warning: FAQ file not found at {faq_path}")
        return
    
    with open(faq_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Split by newlines (each line is a FAQ entry)
    faqs = [line.strip() for line in content.split("\n") if line.strip()]
    
    # Add to collection with IDs
    collection.add(
        documents=faqs,
        ids=[f"faq_{i}" for i in range(len(faqs))]
    )
    
    print(f" Loaded {len(faqs)} FAQ entries into vector store")


def get_faq_context(question: str, k: int = 3) -> List[str]:
    """
    Retrieve relevant FAQ context using semantic search
    
    Args:
        question: User's question
        k: Number of relevant documents to retrieve
        
    Returns:
        List of relevant FAQ documents
    """
    try:
        results = collection.query(
            query_texts=[question],
            n_results=k
        )
        
        # ChromaDB returns nested lists
        if results and 'documents' in results and results['documents']:
            return results['documents'][0]
        
        return []
    
    except Exception as e:
        print(f"Error querying vector store: {e}")
        return []


def get_collection_count() -> int:
    """Get number of documents in collection"""
    return collection.count()


# Initialize vector store on import
if collection.count() == 0:
    print("Initializing vector store with FAQs...")
    load_faqs_to_vector_store()
else:
    print(f"Vector store ready with {collection.count()} FAQ entries")
