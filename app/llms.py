from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

LLM = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
EMBEDDINGS = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)