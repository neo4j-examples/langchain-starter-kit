from __future__ import annotations
from typing import Union
from app.graph_chain import graph_chain
from app.vector_chain import vector_chain
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

    if body.mode == 'vector':
        response = vector_chain().invoke(question)
    elif body.mode == 'graph':
        response = graph_chain().invoke(question)
    else:
        v_response = vector_chain().invoke(question)
        g_response = graph_chain().invoke(question)
        response = simple_agent_chain().invoke({
            "question":question,
            "vector_result":v_response,
            "graph_result":g_response
        })["text"]

    return f"{response}", 200