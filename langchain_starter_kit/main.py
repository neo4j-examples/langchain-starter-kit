from __future__ import annotations
from typing import Union
from langchain_starter_kit.langchain.graph_chain import get_results as get_graph_results
from langchain_starter_kit.langchain.vector_chain import get_results as get_vector_results
from langchain_starter_kit.langchain.simple_agent import get_results as get_simple_agent_results
from fastapi import FastAPI 
from typing import Union
from .models import ApiChatPostRequest, ApiChatPostResponse

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

    if body.mode == 'vector':
        response = get_vector_results(body.message)
    elif body.mode == 'graph':
        response = get_graph_results(body.message)
    else:
        response = get_simple_agent_results(body.message)

    return f"{response}", 200