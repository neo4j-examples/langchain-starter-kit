"""FastAPI server for the LangChain Neo4j starter kit."""
from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException, Depends, status, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.graph_chain import graph_chain
from app.vector_chain import vector_chain
from app.simple_agent import simple_agent_chain


# Initialize FastAPI app
app = FastAPI(
    title="LangChain Neo4j Starter Kit API",
    description="API for querying Neo4j using LangChain with vector and graph capabilities",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class ChatRequest(BaseModel):
    """Request model for chat endpoints."""
    message: str = Field(..., description="The chat message to send")


class ChatResponse(BaseModel):
    """Response model for chat endpoints."""
    message: str = Field(..., description="The chat message response")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional metadata about the response"
    )


# Dependency to get the current active chain
def get_vector_chain():
    """Dependency to get the vector chain."""
    return vector_chain()


def get_graph_chain():
    """Dependency to get the graph chain."""
    return graph_chain()


def get_agent_chain():
    """Dependency to get the agent chain."""
    return simple_agent_chain()


@app.post(
    "/api/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    tags=["chat"],
    summary="Composite Chat Endpoint",
    description="""
    Endpoint that combines both vector search and graph database queries
    to provide naive composite responses. It allows for asking similarity or graph based
    questions from a single endpoint, but not questions requiring a chain of thought
    or multi-step process (ie similarity search followed by a graph query or vice versa)
    to answer.
    """,
    responses={
        status.HTTP_200_OK: {"model": ChatResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def chat_endpoint(
    request: ChatRequest = Body(
        ...,
        example={
            "message": "How many forms are there?"
        }
    ),
    agent_chain: Any = Depends(get_agent_chain),
    vector_chain: Any = Depends(get_vector_chain),
    graph_chain: Any = Depends(get_graph_chain),
) -> ChatResponse:
    """Handle chat requests with both vector and graph context."""
    try:
        # Get responses from both chains in parallel
        v_response = vector_chain.run(request.message)
        
        g_response = graph_chain.run(request.message)

        # Get composite response from agent
        response = await agent_chain.ainvoke(
            {
                "question": request.message,
                "vector_result": v_response,
                "graph_result": g_response,
            },
            config={"callbacks": None},
        )

        return ChatResponse(
            message=response,
            metadata={
                "sources": {
                    "vector": v_response,
                    "graph": g_response,
                }
            },
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat request: {str(e)}",
        ) from e


@app.post(
    "/api/chat/vector",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    tags=["chat"],
    summary="Vector Search Endpoint",
    description="Endpoint for utilizing only the vector index for semantic search.",
    responses={
        status.HTTP_200_OK: {"model": ChatResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def vector_chat_endpoint(
    request: ChatRequest = Body(
        ...,
        example={
            "message": "Which companies are related to manufacturing?"
        }
    ),
    chain: Any = Depends(get_vector_chain),
) -> ChatResponse:
    """Handle chat requests using only vector search."""
    try:
        response = chain.invoke({"query": request.message})

        if isinstance(response, dict):
            response = response.get("result", str(response))
        else:
            response = str(response)

        return ChatResponse(message=response)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing vector search: {str(e)}",
        ) from e


@app.post(
    "/api/chat/graph",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    tags=["chat"],
    summary="Graph Query Endpoint",
    description="Endpoint for querying the graph database using natural language to Cypher conversion.",

    responses={
        status.HTTP_200_OK: {"model": ChatResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def graph_chat_endpoint(
    request: ChatRequest = Body(
        ...,
        example={
            "message": "Which Manager manages the most Companies?"
        }
    ),
    chain: Any = Depends(get_graph_chain),
) -> ChatResponse:
    """Handle chat requests using only graph database queries."""
    try:
        print(f'request message: {request.message}')
        response = chain.invoke({"query": request.message})

        if isinstance(response, dict):
            response = response.get("result", str(response))
        else:
            response = str(response)
        
        return ChatResponse(message=response)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing graph query: {str(e)}",
        ) from e


# Health check endpoint
@app.get(
    "/health",
    status_code=status.HTTP_200_OK,
    tags=["system"],
    summary="Health Check",
    description="Check if the API is up and running.",
)
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}
