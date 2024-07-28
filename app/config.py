import os

# Neo4j Credentials
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# ==================
# Change models here
# ==================
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
EMBEDDINGS = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
# ==================
