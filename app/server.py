from __future__ import annotations
from typing import Union
from app.graph_chain import graph_chain, CYPHER_GENERATION_PROMPT
from app.vector_chain import vector_chain, VECTOR_PROMPT
from app.simple_agent import simple_agent_chain
from fastapi import FastAPI, HTTPException
from typing import Union, Optional
from pydantic import BaseModel, Field


class ApiChatPostRequest(BaseModel):
    message: str = Field(..., description="The chat message to send")
    mode: str = Field(
        "agent",
        description='The mode of the chat message. Current options are: "vector", "graph", "agent". Default is "agent"',
    )


class ApiChatPostResponse(BaseModel):
    response: str


app = FastAPI()


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
    try:
        v_response = vector_chain().invoke(
            {"question": question}, prompt=VECTOR_PROMPT, return_only_outputs=True
        )
    except Exception as e:
        msg = f"Problem running Neo4j vector chain. Check credentials and that the target Neo4j instance supports vector indexes (v5.11+) Exception: {e}"
        raise HTTPException(status_code=500, detail=msg)

    try:
        g_response = graph_chain().invoke(
            {"query": question},
            prompt=CYPHER_GENERATION_PROMPT,
            return_only_outputs=True,
        )
    except Exception as e:
        msg = f"Problem running Neo4j graph chain. Check credentials and that the target Neo4j instance is running. Exception: {e}"
        raise HTTPException(status_code=500, detail=msg)

    if body.mode == "vector":
        # Return only the Vector answer
        response = v_response
    elif body.mode == "graph":
        # Return only the Graph (text2Cypher) answer
        response = g_response
    else:
        print(f"vector response:{v_response}")
        # Return an answer from a chain that composites both the Vector and Graph responses
        response = simple_agent_chain().invoke(
            {
                "question": question,
                "vector_result": v_response,
                "graph_result": g_response,
            }
        )["text"]

    return ApiChatPostResponse(response == response)
