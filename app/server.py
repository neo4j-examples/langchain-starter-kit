from __future__ import annotations
from typing import Union
from app.graph_chain import graph_chain, CYPHER_GENERATION_PROMPT
from app.vector_chain import vector_chain, VECTOR_PROMPT
from app.simple_agent import simple_agent_chain
from fastapi import FastAPI
from typing import Union, Optional
from pydantic import BaseModel, Field


class ApiChatPostRequest(BaseModel):
    message: str = Field(..., description="The chat message to send")


class ApiChatPostResponse(BaseModel):
    message: Optional[str] = Field(None, description="The chat message response")


app = FastAPI()


@app.post(
    "/api/chat",
    response_model=None,
    responses={"201": {"model": ApiChatPostResponse}},
    tags=["chat"],
    description="Endpoint utilizing a simple agent to composite responses from the Vector and Graph chains interfacing with a Neo4j instance.",
)
def send_chat_message(body: ApiChatPostRequest) -> Union[None, ApiChatPostResponse]:
    """
    Send a chat message
    """

    question = body.message

    v_response = vector_chain().invoke(
        {"question": question}, prompt=VECTOR_PROMPT, return_only_outputs=True
    )
    g_response = graph_chain().invoke(
        {"query": question}, prompt=CYPHER_GENERATION_PROMPT, return_only_outputs=True
    )

    # Return an answer from a chain that composites both the Vector and Graph responses
    response = simple_agent_chain().invoke(
        {
            "question": question,
            "vector_result": v_response,
            "graph_result": g_response,
        }
    )["text"]

    return f"{response}", 200


@app.post(
    "/api/chat/vector",
    response_model=None,
    responses={"201": {"model": ApiChatPostResponse}},
    tags=["chat"],
    description="Endpoint for utilizing only vector index for querying Neo4j instance.",
)
def send_chat_vector_message(
    body: ApiChatPostRequest,
) -> Union[None, ApiChatPostResponse]:
    """
    Send a chat message
    """

    question = body.message

    response = vector_chain().invoke(
        {"question": question}, prompt=VECTOR_PROMPT, return_only_outputs=True
    )

    return f"{response}", 200


@app.post(
    "/api/chat/graph",
    response_model=None,
    responses={"201": {"model": ApiChatPostResponse}},
    tags=["chat"],
    description="Endpoint using only Text2Cypher for querying with Neo4j instance.",
)
def send_chat_graph_message(
    body: ApiChatPostRequest,
) -> Union[None, ApiChatPostResponse]:
    """
    Send a chat message
    """

    question = body.message

    response = graph_chain().invoke(
        {"query": question}, prompt=CYPHER_GENERATION_PROMPT, return_only_outputs=True
    )

    return f"{response}", 200
