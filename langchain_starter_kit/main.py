from __future__ import annotations
from typing import Union
from fastapi import FastAPI
from .models import ApiChatPostRequest, ApiChatPostResponse

app = FastAPI(
    title='Chat API',
    description='API for sending and receiving chat messages',
    version='0.1.0',
    servers=[{'url': 'http://localhost:3000'}],
)

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

    # Echo placeholder

    # TODO: Replace to call with underlying LLM using target framework
    return ApiChatPostResponse(message=body.message)
