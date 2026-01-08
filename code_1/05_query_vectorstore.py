"""
Step 5: Query the Vector Store
This script retrieves relevant chunks based on user questions.
"""

import os
import json
import numpy as np
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class ChromaDBRetriever:
    """Retriever for ChromaDB vector store."""
    
    def __init__(self, persist_directory: str, collection_name: str = "pdf_documents"):
        import chromadb
        from chromadb.config import Settings
        
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_collection(collection_name)
        print(f"Connected to ChromaDB collection: {collection_name}")
        print(f"Total documents: {self.collection.count()}")
    
    def query(
        self,
        query_text: str,
        n_results: int = 5,
        embedding_function: Optional[callable] = None
    ) -> list[dict]:
        """
        Query the vector store with a text query.
        
        Args:
            query_text: The user's question
            n_results: Number of results to return
            embedding_function: Optional function to generate query embedding
            
        Returns:
            List of relevant chunks with metadata and scores
        """
        # If embedding function provided, use it; otherwise let ChromaDB handle it
        if embedding_function:
            query_embedding = embedding_function(query_text)
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )
        else:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )
        
        # Format results
        formatted_results = []
        for i in range(len(results["ids"][0])):
            formatted_results.append({
                "chunk_id": results["ids"][0][i],
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
                "relevance_score": 1 - results["distances"][0][i]  # Convert distance to similarity
            })
        
        return formatted_results


class FAISSRetriever:
    """Retriever for FAISS vector store."""
    
    def __init__(self, index_path: str):
        import faiss
        
        self.index = faiss.read_index(os.path.join(index_path, "index.faiss"))
        
        with open(os.path.join(index_path, "metadata.json"), 'r') as f:
            self.metadata = json.load(f)
        
        print(f"Loaded FAISS index with {self.index.ntotal} vectors")
    
    def query(
        self,
        query_embedding: np.ndarray,
        n_results: int = 5
    ) -> list[dict]:
        """
        Query the FAISS index with an embedding.
        
        Args:
            query_embedding: Query vector
            n_results: Number of results to return
            
        Returns:
            List of relevant chunks with metadata and scores
        """
        import faiss
        
        # Normalize query embedding
        query_embedding = query_embedding.astype('float32').reshape(1, -1)
        faiss.normalize_L2(query_embedding)
        
        # Search
        scores, indices = self.index.search(query_embedding, n_results)
        
        # Format results
        formatted_results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:  # No result
                continue
            meta = self.metadata[idx]
            formatted_results.append({
                "chunk_id": meta["chunk_id"],
                "text": meta["text"],
                "metadata": {
                    "page_number": meta["page_number"],
                    "source": meta["source"]
                },
                "relevance_score": float(score)
            })
        
        return formatted_results


def get_embedding_function():
    """Get embedding function using Sentence Transformers (local, free)."""
    from sentence_transformers import SentenceTransformer
    
    print("Loading Sentence Transformers model: all-MiniLM-L6-v2")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    def embed(text: str) -> list[float]:
        return model.encode(text).tolist()
    
    return embed


def format_results(results: list[dict]) -> str:
    """Format results for display."""
    output = []
    for i, result in enumerate(results, 1):
        output.append(f"\n{'='*60}")
        output.append(f"Result {i} (Score: {result['relevance_score']:.4f})")
        output.append(f"Page: {result['metadata'].get('page_number', 'N/A')}")
        output.append(f"Source: {result['metadata'].get('source', 'N/A')}")
        output.append(f"{'='*60}")
        output.append(result['text'])
    return "\n".join(output)


def interactive_query_session(retriever, embedding_function=None):
    """Run an interactive query session."""
    print("\n" + "="*60)
    print("Interactive Query Session")
    print("Type 'quit' or 'exit' to end the session")
    print("="*60)
    
    while True:
        query = input("\nEnter your question: ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not query:
            continue
        
        print(f"\nSearching for: '{query}'...")
        
        if isinstance(retriever, FAISSRetriever):
            query_embedding = np.array(embedding_function(query))
            results = retriever.query(query_embedding, n_results=5)
        else:
            results = retriever.query(query, n_results=5, embedding_function=embedding_function)
        
        print(format_results(results))


def main():
    # Configuration
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    collection_name = os.getenv("COLLECTION_NAME", "pdf_documents")
    chroma_persist_dir = os.path.join(output_dir, os.getenv("CHROMA_PERSIST_DIRECTORY", "chroma_db"))
    faiss_index_path = os.path.join(output_dir, "faiss_index")
    
    # Choose retriever (ChromaDB by default)
    use_faiss = False  # Set to True to use FAISS instead
    
    print("Initializing retriever...\n")
    
    if use_faiss:
        retriever = FAISSRetriever(faiss_index_path)
        embedding_function = get_embedding_function()
    else:
        retriever = ChromaDBRetriever(chroma_persist_dir, collection_name)
        embedding_function = get_embedding_function()
    
    # Example queries
    example_queries = [
        "What is the main topic of this document?",
        "Can you summarize the key points?",
        "What are the important findings?"
    ]
    
    print("\n=== Example Queries ===")
    for query in example_queries[:1]:  # Just one example
        print(f"\nQuery: '{query}'")
        
        if use_faiss:
            query_embedding = np.array(embedding_function(query))
            results = retriever.query(query_embedding, n_results=3)
        else:
            results = retriever.query(query, n_results=3, embedding_function=embedding_function)
        
        print(format_results(results))
    
    # Start interactive session
    interactive_query_session(retriever, embedding_function)


if __name__ == "__main__":
    main()
