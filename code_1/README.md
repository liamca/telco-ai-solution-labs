# RAG Pipeline - Document Processing and Vector Search

This folder contains scripts to build a complete Retrieval-Augmented Generation (RAG) pipeline for processing PDF documents.

## Overview

The pipeline consists of 5 steps:

1. **Extract Text** - Extract text from PDF documents
2. **Chunk Text** - Split content into semantically meaningful chunks
3. **Generate Embeddings** - Convert text chunks into vector representations
4. **Store in Vector DB** - Upload embeddings to a vector database
5. **Query** - Retrieve relevant chunks based on user questions

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys (optional - can use local embeddings)
```

### 3. Run the Pipeline

**Option A: Run complete pipeline**
```bash
python run_pipeline.py
```

**Option B: Run individual steps**
```bash
python 01_extract_text.py
python 02_chunk_text.py
python 03_generate_embeddings.py
python 04_store_in_vectordb.py
python 05_query_vectorstore.py
```

## Scripts

### `01_extract_text.py`
Extracts text from the PDF file using two methods:
- **pdfplumber** - Better for complex layouts, tables
- **PyPDF2** - Faster for simple documents

Output: `output/extracted_text.json`

### `02_chunk_text.py`
Splits text into smaller chunks using:
- **RecursiveCharacterTextSplitter** - Best for semantic meaning
- **TokenTextSplitter** - Best for token-limited models
- **Semantic Sections** - For well-structured documents

Output: `output/chunks.json`

### `03_generate_embeddings.py`
Generates vector embeddings using:
- **OpenAI** - `text-embedding-3-small` (requires API key)
- **Azure OpenAI** - Custom deployment (requires API key)
- **Sentence Transformers** - `all-MiniLM-L6-v2` (local, free)

Output: `output/embeddings.npy`, `output/metadata.json`

### `04_store_in_vectordb.py`
Stores embeddings in vector databases:
- **ChromaDB** - Persistent, easy to use, recommended
- **FAISS** - Fast, memory-efficient, by Facebook AI

Output: `output/chroma_db/`, `output/faiss_index/`

### `05_query_vectorstore.py`
Interactive query interface to search the vector store:
- Supports both ChromaDB and FAISS
- Returns top-k most relevant chunks
- Displays metadata (page number, source)

## Configuration

Edit `.env` to configure:

```env
# Embedding Provider (choose one)
OPENAI_API_KEY=your-key            # For OpenAI embeddings
AZURE_OPENAI_API_KEY=your-key      # For Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://...

# Chunking Settings
CHUNK_SIZE=1000                    # Characters per chunk
CHUNK_OVERLAP=200                  # Overlap between chunks

# Vector Store
COLLECTION_NAME=pdf_documents
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

## Output Structure

```
output/
├── extracted_text.json      # Raw text by page
├── chunks.json              # Text chunks with metadata
├── chunks_with_embeddings.json  # Full data (large file)
├── embeddings.npy           # Numpy array of embeddings
├── metadata.json            # Chunk metadata
├── chroma_db/               # ChromaDB persistent storage
│   └── ...
└── faiss_index/             # FAISS index files
    ├── index.faiss
    └── metadata.json
```

## Embedding Models

| Provider | Model | Dimensions | Cost |
|----------|-------|------------|------|
| OpenAI | text-embedding-3-small | 1536 | ~$0.02/1M tokens |
| OpenAI | text-embedding-3-large | 3072 | ~$0.13/1M tokens |
| Azure OpenAI | text-embedding-ada-002 | 1536 | Varies |
| Local | all-MiniLM-L6-v2 | 384 | Free |

## Usage Examples

### Query the vector store

```python
from chromadb import PersistentClient

client = PersistentClient(path="output/chroma_db")
collection = client.get_collection("pdf_documents")

results = collection.query(
    query_texts=["What is the main topic?"],
    n_results=5
)

for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
    print(f"Page {meta['page_number']}: {doc[:200]}...")
```

### Use with LangChain

```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

vectorstore = Chroma(
    persist_directory="output/chroma_db",
    embedding_function=OpenAIEmbeddings()
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
docs = retriever.get_relevant_documents("Your question here")
```

## Troubleshooting

**No API keys configured**
- The pipeline will automatically use local Sentence Transformers
- Quality may be lower than OpenAI embeddings

**PDF extraction issues**
- Try switching between pdfplumber and PyPDF2 in `01_extract_text.py`
- Some PDFs with images or special formatting may not extract well

**Memory issues with large PDFs**
- Reduce batch size in embedding generation
- Use FAISS with IVF index for large collections

## License

MIT License
