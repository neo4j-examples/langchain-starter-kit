from __future__ import annotations
from typing import Union
# from .chains import get_graph_response
# from .rag_agent import get_results
from langchain_starter_kit.simple_agent import get_results
# from langchain_starter_kit.chains.graph_chain import get_results
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

    response = get_results(body.message)

    return f"{response}", 200