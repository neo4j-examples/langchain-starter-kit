from __future__ import annotations
from app.graph_chain import graph_chain, CYPHER_GENERATION_PROMPT
from app.vector_chain import vector_chain, VECTOR_PROMPT
from app.simple_agent import simple_agent_chain
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel, Field
from neo4j import exceptions


class ApiChatPostRequest(BaseModel):
    message: str = Field(..., description="The chat message to send")
    mode: str = Field(
        "agent",
        description='The mode of the chat message. Current options are: "vector", "graph", "agent". Default is "agent"',
    )


class ApiChatPostResponse(BaseModel):
    response: str


class Neo4jExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except exceptions.AuthError as e:
            msg = f"Neo4j Authentication Error: {e}"
            return Response(content=msg, status_code=400)
        except exceptions.ServiceUnavailable as e:
            msg = f"Neo4j Database Unavailable Error: {e}"
            return Response(content=msg, status_code=400)
        except Exception as e:
            return Response(content=str(e), status_code=400)


# Allowed CORS origins
origins = [
    "http://127.0.0.1",  # Alternative localhost address
    "http://localhost",
]

app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Add Neo4j exception handling middleware
app.add_middleware(Neo4jExceptionMiddleware)


@app.post(
    "/api/chat",
    response_model=None,
    responses={"201": {"model": ApiChatPostResponse}},
    tags=["chat"],
)
def send_chat_message(body: ApiChatPostRequest):
    """
    Send a chat message
    """

    question = body.message

    # Simple exception check. See https://neo4j.com/docs/api/python-driver/current/api.html#errors for full set of driver exceptions

    if body.mode == "vector":
        # Return only the Vector answer
        v_response = vector_chain().invoke(
            {"query": question}, prompt=VECTOR_PROMPT, return_only_outputs=True
        )
        response = v_response
    elif body.mode == "graph":
        # Return only the Graph (text2Cypher) answer
        g_response = graph_chain().invoke(
            {"query": question},
            prompt=CYPHER_GENERATION_PROMPT,
            return_only_outputs=True,
        )
        response = g_response["result"]
    else:
        # Return both vector + graph answers
        v_response = vector_chain().invoke(
            {"query": question}, prompt=VECTOR_PROMPT, return_only_outputs=True
        )
        g_response = graph_chain().invoke(
            {"query": question},
            prompt=CYPHER_GENERATION_PROMPT,
            return_only_outputs=True,
        )["result"]

        # Synthesize a composite of both the Vector and Graph responses
        response = simple_agent_chain().invoke(
            {
                "question": question,
                "vector_result": v_response,
                "graph_result": g_response,
            }
        )

    return response, 200
