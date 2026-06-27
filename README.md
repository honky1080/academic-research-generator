# Autonomous Multi-Agent Academic Research Generator

An automated AI research pipeline that coordinates cooperative agent nodes (Planning, Retrieval, Analysis, Writing, and Review) to generate long-form academic manuscripts. The system features real-time Server-Sent Events (SSE) streaming, arXiv retrieval-augmented generation (RAG), and a modern metrics dashboard console.

---

## Key Features

- **Multi-Agent Pipeline**: Coordinates five specialized agents:
  1. **Planning Agent**: Formulates outline structure based on optional reference structures.
  2. **Retrieval Agent**: Queries arXiv REST API and maps reference documents to citations.
  3. **Analysis Agent**: Synthesizes literature trends and identifies research gaps.
  4. **Writing Agent**: Drafts section blocks using RAG contexts.
  5. **Review Agent**: Refines academic tone and compiles references.
- **Long-Form Generation**: Iterative writing blocks supporting detailed, structured papers (up to 18,000–22,000 words).
- **Server-Sent Events (SSE)**: Real-time backend streaming of logs, metrics, and text drafts directly to the user interface.

## Project Structure

- **`backend/`** (Python Server Code)
  - `main.py`: The FastAPI server entrypoint exposing endpoints for connection and SSE streaming.
  - `config.py` & `.env`: Handles environment parameters and optional API keys.
  - `requirements.txt`: Python package requirements.
  - `services/arxiv_retriever.py`: Fetches and parses relevant XML metadata feeds from arXiv.
  - `services/pipeline_manager.py`: Coordinates the multi-agent execution pipeline.
  - `services/llm_service.py`: Helper class for LLM API calls and offline mock fallbacks.
