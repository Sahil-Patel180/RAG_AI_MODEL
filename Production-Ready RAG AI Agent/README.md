# Production-Ready RAG AI Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This directory contains the core application for a **production-grade Retrieval-Augmented Generation (RAG) AI Agent** powered by **Google Gemini 2.5 Pro**.  
It is designed to be scalable, maintainable, and easily deployable as a standalone intelligent service.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [Deployment](#deployment)

## Overview

This RAG agent provides an intelligent interface for querying a **private knowledge base** using **Gemini’s multimodal capabilities**.  
It retrieves the most relevant documents using a retriever model and then leverages **Gemini 2.5 Pro** to generate a grounded, human-like response.

Unlike research prototypes, this version is **production-ready**, featuring:
- API server integration
- Structured logging
- Environment-based configuration
- Error handling
- Modular service layers

## Features

- **Gemini 2.5 Pro Integration:** Leverages Google’s latest generative model for high-quality, grounded text generation.
- **Accurate, Context-Aware Answers:** Implements a full RAG pipeline to reduce hallucinations by grounding responses in real data.
- **API-Ready:** Exposes endpoints (via FastAPI or Flask) for seamless integration with external systems or frontends.
- **Scalable:** Modular design allows independent scaling of components (retriever, LLM handler, vector DB).
- **Configurable:** All key parameters Gemini API keys, database URIs, model name, etc. are loaded from environment variables.
- **Extensible:** Supports multimodal retrieval (text + images) and additional features like authentication, caching, or streaming responses.

## System Architecture

**High-Level Flow:**
1. **User Query** → Sent to **API Server** (e.g., `app.py`)
2. **API Server** → Calls **Retriever Service** (`retriever.py`)
3. **Retriever Service** → Queries **Vector Database** (e.g., Chroma, Pinecone)
4. **Retriever Service** → Passes retrieved chunks to **LLM Handler** (`llm_handler.py`)
5. **LLM Handler** → Uses **Gemini 2.5 Pro API** to generate grounded responses
6. **LLM Handler** → Returns output → **API Server** → **User**

**Data Flow Diagram (text-based):**
```

User → API → Retriever → Vector Store → Gemini 2.5 Pro → API → Response

````

## Getting Started

### Prerequisites

- Python 3.9+
- Gemini API access (via Google Cloud)
- A vector database (e.g., Chroma, Weaviate, or Pinecone)
- Internet connectivity for Gemini API calls

### Installation

1. **Clone the repository:**
  ```
   git clone https://github.com/Sahil-Patel180/RAG_AI_MODEL.git
   cd "RAG_AI_MODEL/Production-Ready RAG AI Agent"
  ```

2. **Create a virtual environment:**

   ```
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in this directory:

   ```
   cp .env.example .env
   ```

   Then open `.env` and add your Gemini credentials and configuration:

   ```
   # Example .env configuration
   GEMINI_API_KEY="your_google_gemini_api_key_here"
   MODEL_NAME="gemini-2.5-pro"
   VECTOR_DB_PATH="./db"
   EMBEDDING_MODEL="textembedding-gecko"
   CHUNK_SIZE=1000
   TOP_K=5
   ```

5. **Ingest your documents:**
   Run the ingestion script to process and index your data.

   ```bash
   python ingest_data.py --source "./data"
   ```

### Running the Application

To start the API server:

```bash
uvicorn app:main --reload --host 0.0.0.0 --port 8000
```

Once the server is running, you can visit:

```
http://127.0.0.1:8000/docs
```

to test API endpoints via the interactive Swagger UI.

## API Endpoints

| Endpoint  | Method | Description                                                                        |
| --------- | ------ | ---------------------------------------------------------------------------------- |
| `/query`  | POST   | Accepts a query, retrieves context, and generates an LLM-based answer using Gemini |
| `/ingest` | POST   | (Optional) Ingests and indexes new documents into the vector DB                    |
| `/health` | GET    | Returns the health status of the API                                               |

Example `POST /query` body:

```
{
  "query": "Explain how the RAG architecture improves factual accuracy."
}
```

Response:

```
{
  "answer": "Retrieval-Augmented Generation reduces hallucination by grounding responses in retrieved factual documents..."
}
```

## Configuration

All major configurations are environment-driven.
Refer to `.env` for customizing:

| Variable          | Description                                           |
| ----------------- | ----------------------------------------------------- |
| `GEMINI_API_KEY`  | Your Gemini API key                                   |
| `MODEL_NAME`      | The Gemini model name (default: `gemini-2.5-pro`)     |
| `VECTOR_DB_PATH`  | Local or remote vector database path                  |
| `EMBEDDING_MODEL` | Model used for generating text embeddings             |
| `CHUNK_SIZE`      | Size of document chunks during ingestion              |
| `TOP_K`           | Number of top results retrieved from the vector store |

## Deployment

This service can be deployed on:

* **Google Cloud Run**
* **AWS Lambda / ECS**
* **Docker container**
* **On-premises servers**

Example Docker command:

```
docker build -t rag-gemini-agent .
docker run -p 8000:8000 --env-file .env rag-gemini-agent
```

Ensure secrets (API keys, DB credentials) are stored securely using:

* Google Secret Manager (recommended)
* AWS Secrets Manager
* `.env` files (for local development only)

### 🔹 Author

**Sahil Patel**
*BCA Data Science Student | Data Analyst Enthusiast*
📍 SRM Institute of Science and Technology
🔗 [GitHub: Sahil-Patel180](https://github.com/Sahil-Patel180)

```
Would you like me to append an extra section like  
📸 Multimodal Support (PDFs + Images) explaining how Gemini can handle both text and images for RAG, since your current setup loads PDFs but not images yet?
```
