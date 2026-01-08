"""
Step 3: Generate Embeddings
This script converts text chunks into vector embeddings using an embedding model.
"""

import os
import json
import numpy as np
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()


def load_chunks(input_path: str) -> list[dict]:
    """Load chunks from JSON file."""
    with open(input_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_embeddings_openai(
    chunks: list[dict],
    model: str = "text-embedding-3-small",
    batch_size: int = 100
) -> list[dict]:
    """
    Generate embeddings using OpenAI's embedding model.
    
    Args:
        chunks: List of chunk dictionaries
        model: OpenAI embedding model name
        batch_size: Number of texts to embed in one API call
        
    Returns:
        List of chunk dictionaries with embeddings added
    """
    from openai import OpenAI
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    texts = [chunk["text"] for chunk in chunks]
    all_embeddings = []
    
    print(f"Generating embeddings with OpenAI {model}...")
    
    for i in tqdm(range(0, len(texts), batch_size)):
        batch = texts[i:i + batch_size]
        response = client.embeddings.create(
            model=model,
            input=batch
        )
        batch_embeddings = [item.embedding for item in response.data]
        all_embeddings.extend(batch_embeddings)
    
    # Add embeddings to chunks
    for chunk, embedding in zip(chunks, all_embeddings):
        chunk["embedding"] = embedding
        chunk["embedding_model"] = model
        chunk["embedding_dim"] = len(embedding)
    
    return chunks


def generate_embeddings_azure_openai(
    chunks: list[dict],
    batch_size: int = 100
) -> list[dict]:
    """
    Generate embeddings using Azure OpenAI's embedding model.
    
    Args:
        chunks: List of chunk dictionaries
        batch_size: Number of texts to embed in one API call
        
    Returns:
        List of chunk dictionaries with embeddings added
    """
    from openai import AzureOpenAI
    
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-02-01",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )
    
    deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002")
    texts = [chunk["text"] for chunk in chunks]
    all_embeddings = []
    
    print(f"Generating embeddings with Azure OpenAI {deployment}...")
    
    for i in tqdm(range(0, len(texts), batch_size)):
        batch = texts[i:i + batch_size]
        response = client.embeddings.create(
            model=deployment,
            input=batch
        )
        batch_embeddings = [item.embedding for item in response.data]
        all_embeddings.extend(batch_embeddings)
    
    # Add embeddings to chunks
    for chunk, embedding in zip(chunks, all_embeddings):
        chunk["embedding"] = embedding
        chunk["embedding_model"] = f"azure:{deployment}"
        chunk["embedding_dim"] = len(embedding)
    
    return chunks


def generate_embeddings_sentence_transformers(
    chunks: list[dict],
    model_name: str = "all-MiniLM-L6-v2",
    batch_size: int = 32
) -> list[dict]:
    """
    Generate embeddings using Sentence Transformers (local, free).
    
    Args:
        chunks: List of chunk dictionaries
        model_name: Sentence Transformers model name
        batch_size: Batch size for encoding
        
    Returns:
        List of chunk dictionaries with embeddings added
    """
    from sentence_transformers import SentenceTransformer
    
    print(f"Loading Sentence Transformers model: {model_name}")
    model = SentenceTransformer(model_name)
    
    texts = [chunk["text"] for chunk in chunks]
    
    print(f"Generating embeddings for {len(texts)} chunks...")
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        convert_to_numpy=True
    )
    
    # Add embeddings to chunks
    for chunk, embedding in zip(chunks, embeddings):
        chunk["embedding"] = embedding.tolist()
        chunk["embedding_model"] = model_name
        chunk["embedding_dim"] = len(embedding)
    
    return chunks


def save_embeddings(chunks: list[dict], output_path: str):
    """Save chunks with embeddings to JSON file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)
    print(f"Saved embeddings to: {output_path}")


def save_embeddings_numpy(chunks: list[dict], output_dir: str):
    """Save embeddings as numpy arrays for efficient loading."""
    embeddings = np.array([chunk["embedding"] for chunk in chunks])
    
    # Save embeddings
    np.save(os.path.join(output_dir, "embeddings.npy"), embeddings)
    
    # Save metadata (without embeddings)
    metadata = []
    for chunk in chunks:
        meta = {k: v for k, v in chunk.items() if k != "embedding"}
        metadata.append(meta)
    
    with open(os.path.join(output_dir, "metadata.json"), 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"Saved embeddings to: {output_dir}/embeddings.npy")
    print(f"Saved metadata to: {output_dir}/metadata.json")


def main():
    # Configuration
    input_path = os.path.join(os.path.dirname(__file__), "output", "chunks.json")
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    
    # Load chunks
    if not os.path.exists(input_path):
        print(f"Error: Chunks not found at {input_path}")
        print("Run 02_chunk_text.py first.")
        return
    
    print(f"Loading chunks from: {input_path}\n")
    chunks = load_chunks(input_path)
    
    # Use Sentence Transformers for local, free embeddings
    print("Using local Sentence Transformers embeddings...")
    chunks_with_embeddings = generate_embeddings_sentence_transformers(chunks)
    
    # Save embeddings (both JSON and numpy formats)
    save_embeddings(chunks_with_embeddings, os.path.join(output_dir, "chunks_with_embeddings.json"))
    save_embeddings_numpy(chunks_with_embeddings, output_dir)
    
    # Print summary
    print(f"\n=== Embedding Summary ===")
    print(f"Chunks processed: {len(chunks_with_embeddings)}")
    print(f"Embedding model: {chunks_with_embeddings[0]['embedding_model']}")
    print(f"Embedding dimension: {chunks_with_embeddings[0]['embedding_dim']}")


if __name__ == "__main__":
    main()
