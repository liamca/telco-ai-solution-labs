"""
Step 4: Store Embeddings in a Vector Store
This script uploads embeddings and metadata to a vector database (ChromaDB or FAISS).
"""

import os
import json
import numpy as np
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


def load_embeddings_and_metadata(output_dir: str) -> tuple[np.ndarray, list[dict]]:
    """Load embeddings and metadata from files."""
    embeddings = np.load(os.path.join(output_dir, "embeddings.npy"))
    
    with open(os.path.join(output_dir, "metadata.json"), 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    return embeddings, metadata


def store_in_chromadb(
    embeddings: np.ndarray,
    metadata: list[dict],
    collection_name: str = "pdf_documents",
    persist_directory: str = "./chroma_db"
) -> None:
    """
    Store embeddings in ChromaDB (persistent vector database).
    
    Args:
        embeddings: Numpy array of embeddings
        metadata: List of metadata dictionaries
        collection_name: Name of the ChromaDB collection
        persist_directory: Directory to persist the database
    """
    import chromadb
    from chromadb.config import Settings
    
    print(f"Initializing ChromaDB at: {persist_directory}")
    
    # Create persistent client
    client = chromadb.PersistentClient(
        path=persist_directory,
        settings=Settings(anonymized_telemetry=False)
    )
    
    # Delete collection if it exists (for fresh start)
    try:
        client.delete_collection(collection_name)
        print(f"Deleted existing collection: {collection_name}")
    except Exception:
        pass  # Collection doesn't exist, that's fine
    
    # Create collection
    collection = client.create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}  # Use cosine similarity
    )
    
    # Prepare data for insertion
    ids = [str(meta["chunk_id"]) for meta in metadata]
    documents = [meta["text"] for meta in metadata]
    metadatas = [
        {
            "page_number": meta["page_number"],
            "source": meta["source"],
            "chunk_index": meta.get("chunk_index_in_page", 0),
            "char_count": meta["char_count"]
        }
        for meta in metadata
    ]
    
    # Add to collection in batches
    batch_size = 100
    for i in range(0, len(ids), batch_size):
        end_idx = min(i + batch_size, len(ids))
        collection.add(
            ids=ids[i:end_idx],
            embeddings=embeddings[i:end_idx].tolist(),
            documents=documents[i:end_idx],
            metadatas=metadatas[i:end_idx]
        )
        print(f"Added chunks {i+1}-{end_idx} to ChromaDB")
    
    print(f"\nSuccessfully stored {len(ids)} chunks in ChromaDB")
    print(f"Collection: {collection_name}")
    print(f"Persist directory: {persist_directory}")


def store_in_faiss(
    embeddings: np.ndarray,
    metadata: list[dict],
    index_path: str = "./faiss_index"
) -> None:
    """
    Store embeddings in FAISS (Facebook AI Similarity Search).
    
    Args:
        embeddings: Numpy array of embeddings
        metadata: List of metadata dictionaries
        index_path: Directory to save FAISS index
    """
    import faiss
    
    print("Creating FAISS index...")
    
    # Ensure output directory exists
    Path(index_path).mkdir(parents=True, exist_ok=True)
    
    # Normalize embeddings for cosine similarity
    embeddings_normalized = embeddings.astype('float32')
    faiss.normalize_L2(embeddings_normalized)
    
    # Create FAISS index
    dimension = embeddings.shape[1]
    
    # Use IndexFlatIP for inner product (cosine similarity with normalized vectors)
    index = faiss.IndexFlatIP(dimension)
    
    # For larger datasets, use IVF index for faster search
    # nlist = min(100, len(embeddings) // 10)  # Number of clusters
    # quantizer = faiss.IndexFlatIP(dimension)
    # index = faiss.IndexIVFFlat(quantizer, dimension, nlist, faiss.METRIC_INNER_PRODUCT)
    # index.train(embeddings_normalized)
    
    # Add vectors to index
    index.add(embeddings_normalized)
    
    # Save index
    index_file = os.path.join(index_path, "index.faiss")
    faiss.write_index(index, index_file)
    
    # Save metadata separately
    metadata_file = os.path.join(index_path, "metadata.json")
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"\nSuccessfully stored {len(embeddings)} vectors in FAISS")
    print(f"Index file: {index_file}")
    print(f"Metadata file: {metadata_file}")


def main():
    # Configuration
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    collection_name = os.getenv("COLLECTION_NAME", "pdf_documents")
    chroma_persist_dir = os.path.join(output_dir, os.getenv("CHROMA_PERSIST_DIRECTORY", "chroma_db"))
    faiss_index_path = os.path.join(output_dir, "faiss_index")
    
    # Load embeddings and metadata
    embeddings_file = os.path.join(output_dir, "embeddings.npy")
    metadata_file = os.path.join(output_dir, "metadata.json")
    
    if not os.path.exists(embeddings_file) or not os.path.exists(metadata_file):
        print(f"Error: Embeddings not found.")
        print("Run 03_generate_embeddings.py first.")
        return
    
    print(f"Loading embeddings and metadata...\n")
    embeddings, metadata = load_embeddings_and_metadata(output_dir)
    
    print(f"Loaded {len(embeddings)} embeddings (dimension: {embeddings.shape[1]})")
    print(f"Loaded {len(metadata)} metadata entries\n")
    
    # Store in ChromaDB (recommended for most use cases)
    print("=== Storing in ChromaDB ===")
    store_in_chromadb(
        embeddings,
        metadata,
        collection_name=collection_name,
        persist_directory=chroma_persist_dir
    )
    
    # Also store in FAISS (alternative option)
    print("\n=== Storing in FAISS ===")
    store_in_faiss(
        embeddings,
        metadata,
        index_path=faiss_index_path
    )
    
    print("\n=== Storage Complete ===")
    print(f"ChromaDB: {chroma_persist_dir}")
    print(f"FAISS: {faiss_index_path}")


if __name__ == "__main__":
    main()
