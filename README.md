# CodePilot AI — Local AI Software Engineering Assistant

CodePilot AI is a local AI-powered software engineering assistant designed to help developers understand and explore source code repositories using natural-language questions.

Built with Python, FastAPI, Ollama, Tree-sitter, and ChromaDB, it combines code structure analysis with Retrieval-Augmented Generation (RAG) to provide context-aware answers based on a selected project.

The goal is to build a developer-focused assistant that can eventually support code analysis, debugging, refactoring, and other software engineering workflows while keeping LLM inference local.

## Features

- **Repository-aware chat:** Ask natural-language questions about a codebase.
- **Multi-language code parsing:** Use Tree-sitter to extract code structures from supported programming languages.
- **Structure-aware chunking:** Divide parsed source code into chunks for retrieval.
- **Local embeddings:** Generate vector embeddings using `nomic-embed-text` through Ollama.
- **Semantic code search:** Retrieve relevant code chunks using ChromaDB.
- **Context-aware responses:** Supply retrieved code to a local Qwen2.5-Coder model.
- **Project-specific indexing:** Generate separate ChromaDB collections for different project paths.
- **REST API:** Expose chat and repository functionality through FastAPI.

## Architecture

```text
                  User Question
                       |
                       v
                FastAPI /chat
                       |
                       v
              Project Indexer
                       |
              +--------+--------+
              |                 |
              v                 v
         Tree-sitter       Code Chunker
              |                 |
              +--------+--------+
                       |
                       v
               Ollama Embeddings
                nomic-embed-text
                       |
                       v
                   ChromaDB
                       |
                       v
                Code Retriever
                       |
                       v
                 Context Builder
                       |
                       v
                Ollama / Qwen
                       |
                       v
                  AI Response
```

The indexing pipeline parses source files, creates code chunks, generates embeddings, and stores them with their associated metadata.

When a project-specific question is submitted, CodePilot retrieves relevant chunks and includes them in the prompt sent to the local language model.

## Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| Backend API | FastAPI |
| Local LLM runtime | Ollama |
| Code generation and reasoning | Qwen2.5-Coder 3B |
| Embedding model | nomic-embed-text |
| Vector database | ChromaDB |
| Code parsing | Tree-sitter |
| HTTP communication | Requests |
| Data validation | Pydantic |

## Project Structure

```text
CodePilot-ai/
├── backend/
│   └── app/
│       ├── main.py
│       ├── routes/
│       │   ├── chat.py
│       │   ├── repository.py
│       │   └── search.py
│       ├── schemas/
│       │   └── chat.py
│       └── services/
│           ├── ollama_service.py
│           ├── repository_service.py
│           └── search_service.py
├── parser/
│   ├── languages.py
│   ├── parser.py
│   └── structure.py
├── rag/
│   ├── chunker.py
│   ├── embeddings.py
│   ├── indexer.py
│   ├── retriever.py
│   ├── context_builder.py
│   └── vector_store.py
├── tests/
├── requirements.txt
├── README.md
└── .gitignore
```

## Prerequisites

Before running CodePilot AI, install:

- Python 3.12 or a compatible Python version.
- [Ollama](https://ollama.com/)
- Git
- A supported source-code project to analyze.

The local language model and embedding model must be available through Ollama.

## Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd CodePilot-ai
```

Replace the placeholder with your repository URL.

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Download the required Ollama models

```bash
ollama pull qwen2.5-coder:3b
ollama pull nomic-embed-text
```

Make sure the Ollama service is running and accessible at `http://localhost:11434`.

### 5. Start the API server

```bash
uvicorn backend.app.main:app --reload
```

The API will be available at:

- **API:** http://127.0.0.1:8000
- **Interactive API documentation:** http://127.0.0.1:8000/docs

## Usage

### Ask a question about a project

Send a request to the chat endpoint using `curl`:

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explain the architecture of this project.",
    "project_path": "/absolute/path/to/your/project"
  }'
```

Replace the example path with the absolute path of a project accessible to the running backend.

The API returns a JSON response containing the generated answer.

### Ask a general question

The chat endpoint also accepts a request without a project path:

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explain the difference between lists and tuples in Python."
  }'
```

Without a project path, the current implementation sends the question directly to the local language model.

### Index a project manually

The project indexer can also be used independently:

```bash
python -c "from rag.indexer import index_project; print(index_project('/absolute/path/to/your/project'))"
```

The indexer discovers supported source files, parses them, creates chunks, generates embeddings, and stores the resulting records in ChromaDB.

## ChromaDB and Vector Search

CodePilot AI uses ChromaDB to store the vector representations of source-code chunks.

Each indexed record includes:

- A unique chunk identifier.
- The source-code content.
- The numerical embedding vector.
- Metadata such as file path, language, symbol name, and line numbers.

The embedding model converts code into numerical vectors. ChromaDB uses vector similarity search to retrieve relevant code for a user's question.

The default persistent storage directory is `data/chroma`, relative to the working directory used to initialize the vector store.

Project-specific collection names are derived from resolved project paths.

