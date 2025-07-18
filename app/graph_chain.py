from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
from langchain.schema.runnable import Runnable
import logging

from app.config import (
    LLM,
    NEO4J_URI,
    NEO4J_DATABASE,
    NEO4J_USERNAME,
    NEO4J_PASSWORD,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def graph_chain() -> Runnable:
    """Create and return a graph chain for querying Neo4j with natural language."""
    try:
        # Initialize the Neo4j graph connection
        graph = Neo4jGraph(
            url=NEO4J_URI,
            username=NEO4J_USERNAME,
            password=NEO4J_PASSWORD,
            database=NEO4J_DATABASE
        )
        
        chain = GraphCypherQAChain.from_llm(
            llm=LLM, 
            graph=graph, 
            verbose=True,
            allow_dangerous_requests=True
        )

        return chain
        
    except Exception as e:
        error_msg = f"Failed to initialize graph chain: {str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg) from e
