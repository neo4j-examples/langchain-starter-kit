from __future__ import annotations
from typing import Union
from app.graph_chain import graph_chain, CYPHER_GENERATION_PROMPT
from app.vector_chain import vector_chain, VECTOR_PROMPT
from app.simple_agent import simple_agent_chain
from fastapi import FastAPI 
from typing import Union, Optional
from pydantic import BaseModel, Field


class ApiChatPostRequest(BaseModel):
    message: str = Field(..., description='The chat message to send')
    mode: str = Field('agent', description='The mode of the chat message. Current options are: "vector", "graph", "agent". Default is "agent"')


class ApiChatPostResponse(BaseModel):
    message: Optional[str] = Field(None, description='The chat message response')


app = FastAPI() 

@app.post(
    '/api/chat',
    response_model=None,
    responses={'201': {'model': ApiChatPostResponse}},
    tags=['chat'],
)
def send_chat_message(body: ApiChatPostRequest) -> Union[None, ApiChatPostResponse]:
    """
    Send a chat message
    """

    question = body.message

    v_response = vector_chain().invoke(
        {"question":question},
        prompt = VECTOR_PROMPT,
        return_only_outputs = True
    )
    g_response = graph_chain().invoke(
        {"query":question},
        prompt = CYPHER_GENERATION_PROMPT,
        return_only_outputs = True
    )
    
    if body.mode == 'vector':
        # Return only the Vector answer
        response = v_response
    elif body.mode == 'graph':
        # Return only the Graph (text2Cypher) answer
        response = g_response
    else:
        # Return an answer from a chain that composites both the Vector and Graph responses
        response = simple_agent_chain().invoke({
            "question":question,
            "vector_result":v_response,
            "graph_result":g_response
        })["text"]

    return f"{response}", 200