"""
Step 2: Split Content into Semantically Meaningful Chunks
This script takes extracted text and splits it into smaller chunks for embedding.
"""

import os
import json
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    TokenTextSplitter
)

load_dotenv()


def load_extracted_text(input_path: str) -> list[dict]:
    """Load extracted text from JSON file."""
    with open(input_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def chunk_with_recursive_splitter(
    pages_data: list[dict],
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> list[dict]:
    """
    Split text using RecursiveCharacterTextSplitter.
    This splitter tries to split on paragraphs, then sentences, then words.
    Best for maintaining semantic meaning.
    
    Args:
        pages_data: List of page dictionaries with text
        chunk_size: Maximum size of each chunk
        chunk_overlap: Overlap between chunks for context continuity
        
    Returns:
        List of chunk dictionaries with metadata
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    chunks = []
    chunk_id = 0
    
    for page in pages_data:
        if not page["text"]:
            continue
            
        page_chunks = splitter.split_text(page["text"])
        
        for i, chunk_text in enumerate(page_chunks):
            chunks.append({
                "chunk_id": chunk_id,
                "text": chunk_text,
                "char_count": len(chunk_text),
                "page_number": page["page_number"],
                "chunk_index_in_page": i,
                "source": page["source"],
                "metadata": {
                    "page": page["page_number"],
                    "source": page["source"],
                    "chunk_method": "recursive"
                }
            })
            chunk_id += 1
    
    return chunks


def chunk_with_token_splitter(
    pages_data: list[dict],
    chunk_size: int = 500,
    chunk_overlap: int = 50
) -> list[dict]:
    """
    Split text using TokenTextSplitter (based on token count).
    Better for ensuring chunks fit within model token limits.
    
    Args:
        pages_data: List of page dictionaries with text
        chunk_size: Maximum tokens per chunk
        chunk_overlap: Token overlap between chunks
        
    Returns:
        List of chunk dictionaries with metadata
    """
    splitter = TokenTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    chunks = []
    chunk_id = 0
    
    for page in pages_data:
        if not page["text"]:
            continue
            
        page_chunks = splitter.split_text(page["text"])
        
        for i, chunk_text in enumerate(page_chunks):
            chunks.append({
                "chunk_id": chunk_id,
                "text": chunk_text,
                "char_count": len(chunk_text),
                "page_number": page["page_number"],
                "chunk_index_in_page": i,
                "source": page["source"],
                "metadata": {
                    "page": page["page_number"],
                    "source": page["source"],
                    "chunk_method": "token"
                }
            })
            chunk_id += 1
    
    return chunks


def chunk_by_semantic_sections(
    pages_data: list[dict],
    section_markers: Optional[list[str]] = None
) -> list[dict]:
    """
    Split text by semantic sections (headers, bullet points, etc.).
    Useful when document has clear structure.
    
    Args:
        pages_data: List of page dictionaries with text
        section_markers: Optional list of section header patterns
        
    Returns:
        List of chunk dictionaries with metadata
    """
    if section_markers is None:
        section_markers = ["\n# ", "\n## ", "\n### ", "\n\n"]
    
    # Combine all text first
    full_text = "\n\n".join(p["text"] for p in pages_data if p["text"])
    
    # Simple section-based splitting
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=100,
        separators=section_markers + ["\n", " ", ""]
    )
    
    raw_chunks = splitter.split_text(full_text)
    
    chunks = []
    for i, chunk_text in enumerate(raw_chunks):
        # Find which page this chunk likely belongs to
        page_num = 1
        char_count = 0
        for page in pages_data:
            char_count += len(page["text"])
            if char_count > i * 1000:  # Rough estimation
                page_num = page["page_number"]
                break
        
        chunks.append({
            "chunk_id": i,
            "text": chunk_text,
            "char_count": len(chunk_text),
            "page_number": page_num,
            "chunk_index_in_page": 0,
            "source": pages_data[0]["source"] if pages_data else "unknown",
            "metadata": {
                "page": page_num,
                "source": pages_data[0]["source"] if pages_data else "unknown",
                "chunk_method": "semantic"
            }
        })
    
    return chunks


def save_chunks(chunks: list[dict], output_path: str):
    """Save chunks to JSON file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(chunks)} chunks to: {output_path}")


def main():
    # Configuration
    chunk_size = int(os.getenv("CHUNK_SIZE", 1000))
    chunk_overlap = int(os.getenv("CHUNK_OVERLAP", 200))
    
    input_path = os.path.join(os.path.dirname(__file__), "output", "extracted_text.json")
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    
    # Load extracted text
    if not os.path.exists(input_path):
        print(f"Error: Extracted text not found at {input_path}")
        print("Run 01_extract_text.py first.")
        return
    
    print(f"Loading extracted text from: {input_path}\n")
    pages_data = load_extracted_text(input_path)
    
    # Chunk using recursive splitter (recommended for most cases)
    print(f"Chunking with size={chunk_size}, overlap={chunk_overlap}")
    chunks = chunk_with_recursive_splitter(
        pages_data,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    # Save chunks
    output_path = os.path.join(output_dir, "chunks.json")
    save_chunks(chunks, output_path)
    
    # Print summary
    print(f"\n=== Chunking Summary ===")
    print(f"Input pages: {len(pages_data)}")
    print(f"Output chunks: {len(chunks)}")
    print(f"Chunk size: {chunk_size} chars")
    print(f"Chunk overlap: {chunk_overlap} chars")
    
    # Show sample chunks
    print(f"\n=== Sample Chunks ===")
    for chunk in chunks[:3]:
        print(f"\nChunk {chunk['chunk_id']} (Page {chunk['page_number']}):")
        print(f"  Length: {chunk['char_count']} chars")
        print(f"  Preview: {chunk['text'][:100]}...")


if __name__ == "__main__":
    main()
