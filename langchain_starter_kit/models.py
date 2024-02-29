from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field


class ApiChatPostRequest(BaseModel):
    message: str = Field(..., description='The chat message to send')


class ApiChatPostResponse(BaseModel):
    message: Optional[str] = Field(None, description='The chat message response')
