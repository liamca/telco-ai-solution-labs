"""
Complete RAG Pipeline Runner
This script runs all steps of the RAG pipeline in sequence.
"""

import os
import sys
import subprocess
from pathlib import Path


def run_step(script_name: str, description: str) -> bool:
    """Run a pipeline step and return success status."""
    print(f"\n{'='*60}")
    print(f"STEP: {description}")
    print(f"Running: {script_name}")
    print('='*60 + "\n")
    
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    
    result = subprocess.run(
        [sys.executable, script_path],
        cwd=os.path.dirname(__file__)
    )
    
    if result.returncode != 0:
        print(f"\n❌ Error in {script_name}")
        return False
    
    print(f"\n✅ Completed: {description}")
    return True


def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║           RAG Pipeline - Document Processing                 ║
║                                                              ║
║  This pipeline will:                                         ║
║  1. Extract text from PDF                                    ║
║  2. Split text into semantic chunks                          ║
║  3. Generate vector embeddings                               ║
║  4. Store in vector database                                 ║
║  5. Enable semantic search queries                           ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Check for .env file
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if not os.path.exists(env_path):
        print("⚠️  Warning: No .env file found.")
        print("   Copy .env.example to .env and configure your API keys.")
        print("   Without API keys, the pipeline will use local embeddings.\n")
    
    steps = [
        ("01_extract_text.py", "Extract Text from PDF"),
        ("02_chunk_text.py", "Split Content into Chunks"),
        ("03_generate_embeddings.py", "Generate Embeddings"),
        ("04_store_in_vectordb.py", "Store in Vector Database"),
    ]
    
    for script_name, description in steps:
        success = run_step(script_name, description)
        if not success:
            print(f"\n❌ Pipeline failed at: {description}")
            sys.exit(1)
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                    Pipeline Complete! ✅                     ║
╚══════════════════════════════════════════════════════════════╝

Your documents are now indexed and ready for querying!

To query the vector store, run:
  python 05_query_vectorstore.py

Output files are in the 'output' directory:
  - extracted_text.json    : Raw text from PDF
  - chunks.json            : Text chunks with metadata
  - embeddings.npy         : Vector embeddings
  - metadata.json          : Chunk metadata
  - chroma_db/             : ChromaDB vector store
  - faiss_index/           : FAISS vector store
    """)


if __name__ == "__main__":
    main()
