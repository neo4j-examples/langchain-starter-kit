
from .secrets_manager import OPENAI_API_KEY
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

LLM = ChatOpenAI(temperature=0)
EMBEDDINGS = OpenAIEmbeddings()