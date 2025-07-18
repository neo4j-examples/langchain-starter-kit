"""Module for creating and managing vector search functionality with Neo4j."""
import logging

from langchain.prompts import PromptTemplate
from langchain_community.vectorstores.neo4j_vector import Neo4jVector
from langchain.chains import RetrievalQA
from app.config import (
    LLM,
    EMBEDDINGS,
    NEO4J_URI,
    NEO4J_DATABASE,
    NEO4J_USERNAME,
    NEO4J_PASSWORD,
)

# Module-level constants
DEFAULT_INDEX_NAME = "form_10k_chunks"
DEFAULT_NODE_LABEL = "Chunk"
DEFAULT_NODE_PROPERTY_SOURCE = "text"
DEFAULT_EMBEDDING_PROPERTY = "textopenaiembedding"
DEFAULT_MAX_TOKENS = 2000


def vector_chain(
    index_name: str = DEFAULT_INDEX_NAME,
    node_label: str = DEFAULT_NODE_LABEL,
    node_property_source: str = DEFAULT_NODE_PROPERTY_SOURCE,
    node_property_name: str = DEFAULT_EMBEDDING_PROPERTY,
) -> RetrievalQA:
    """Creates a question-answering chain using Neo4j's vector search capabilities.
    
    This function initializes a retrieval-augmented QA system that:
    - Searches for relevant context using vector similarity in Neo4j
    - Uses the retrieved context to generate answers with an LLM
    - Handles input/output formatting for seamless integration with the server

    Args:
        index_name: Name of the vector index in Neo4j (default: "vector")
        node_label: Label of nodes containing the text and vector data (default: "Movie")
        node_property_source: Node property containing the source text to search (default: "plot")
        node_property_name: Property name where vector embeddings are stored (default: "embedding")

    Returns:
        A LangChain Runnable that takes a question and returns an answer string.
        The runnable expects input in the format: {"question": "your question here"}

    Raises:
        RuntimeError: If the vector store cannot be initialized or connected to
    """
    try:
        # Try to connect to existing vector store
        vector_store = Neo4jVector.from_existing_index(
            embedding=EMBEDDINGS,
            url=NEO4J_URI,
            username=NEO4J_USERNAME,
            password=NEO4J_PASSWORD,
            database=NEO4J_DATABASE,
            index_name=index_name,
            embedding_node_property=node_property_name,
            text_node_property=node_property_source,
        )
        logging.info(f"Connected to existing Neo4j vector index: {index_name}")
    except Exception as e:
        logging.warning(f"Could not connect to existing index: {str(e)}. Attempting to create new index...")
        try:
            vector_store = Neo4jVector.from_existing_graph(
                embedding=EMBEDDINGS,
                url=NEO4J_URI,
                username=NEO4J_USERNAME,
                password=NEO4J_PASSWORD,
                database=NEO4J_DATABASE,
                index_name=index_name,
                node_label=node_label,
                embedding_node_property=node_property_name,
                text_node_properties=[node_property_source],
            )
            logging.info(f"Created new Neo4j vector index: {index_name}")
        except Exception as e:
            error_msg = f"Failed to initialize Neo4jVector: {str(e)}"
            logging.error(error_msg)
            raise RuntimeError(error_msg) from e

    # Create a retriever
    retriever = vector_store.as_retriever()

    # Create the base QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=LLM,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=False,
        # chain_type_kwargs={"prompt": QA_PROMPT_TEMPLATE}
    )

    # NOTE: Technically this will return answers contained in the filing chunks,
    # which may or may not mention that actual source Company it's attached to.

    return qa_chain
