
from .secrets_manager import OPENAI_API_KEY
from langchain_openai import ChatOpenAI, OpenAIEmbeddings #Get a module not found error despite package being loaded

import os

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

LLM = ChatOpenAI(temperature=0)
EMBEDDINGS = OpenAIEmbeddings()