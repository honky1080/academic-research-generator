from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
from services.pipeline_manager import orchestrate_research
from config import settings

# 1. Initialize FastAPI
app = FastAPI(
    title="Research Generator API",
    description="A simplified FastAPI server that runs an automated multi-agent research pipeline."
)

# 2. Add CORS Middleware (allowing frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Request Body Schemas
class StatusCheck(BaseModel):
    status: str

class GenerateSSERequest(BaseModel):
    topic: str
    agents: List[str]
    reference_structure: Optional[str] = ""
    live: bool = False

# 4. Status Check Endpoint
@app.get("/")
def read_root():
    return {
        "status": "online",
        "provider": settings.DEFAULT_LLM_PROVIDER,
        "instructions": "Send a POST request to /api/generate-sse to stream research papers."
    }

# 5. Core SSE Streaming Endpoint
@app.post("/api/generate-sse")
async def generate_sse(req: GenerateSSERequest):
    """
    Spawns the research pipeline and streams logs, metrics, and draft content 
    using Server-Sent Events (SSE) representation.
    """
    generator = orchestrate_research(
        topic=req.topic,
        selected_agents=req.agents,
        reference_structure=req.reference_structure,
        use_live_api=req.live
    )
    return StreamingResponse(generator, media_type="text/event-stream")