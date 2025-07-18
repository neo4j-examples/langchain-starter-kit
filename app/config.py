import os
from dotenv import load_dotenv

load_dotenv()

# Neo4j Credentials
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# ==================
# Change models here
# ==================
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_TEMPERATURE = os.getenv("OPENAI_TEMPERATURE", 0)
LLM = ChatOpenAI(model=OPENAI_MODEL, temperature=OPENAI_TEMPERATURE, openai_api_key=OPENAI_API_KEY)
EMBEDDINGS = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
# ==================
