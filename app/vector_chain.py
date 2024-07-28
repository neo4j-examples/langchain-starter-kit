from langchain.prompts.prompt import PromptTemplate
from langchain_community.vectorstores import Neo4jVector
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.schema.runnable import Runnable
from app.config import (
    LLM,
    EMBEDDINGS,
    NEO4J_URI,
    NEO4J_DATABASE,
    NEO4J_USERNAME,
    NEO4J_PASSWORD,
)
import logging

VECTOR_PROMPT_TEMPLATE = """Human: You are a data analyst who can answer questions only based on the context below.
* Answer the question STRICTLY based on the context provided in JSON below.
* Do not assume or retrieve any information outside of the context 
* Use three sentences maximum and keep the answer concise
* Think step by step before answering.
* Do not return helpful or extra text or apologies
* Just return summary to the user. DO NOT start with Here is a summary
* List the results in rich text format if there are more than one results
* If the context is empty, just respond None

<question>
{input}
</question>

Here is the context:
<context>
{context}
</context>

Assistant:"""

VECTOR_PROMPT = PromptTemplate(
    input_variables=["input", "context"], template=VECTOR_PROMPT_TEMPLATE
)


def vector_chain() -> Runnable:

    # Arbitraty name of index
    index_name = "vector"

    # Nodes to contain vector data
    node_label = "Movie"

    # Property containing unstructured text of interest.
    node_property_source = "plot"

    # Node property to contain / that contains vector embeddings
    node_property_name = "embeddings"

    vector_store = None

    # Neo4jVector API: https://api.python.langchain.com/en/latest/vectorstores/langchain_community.vectorstores.neo4j_vector.Neo4jVector.html#langchain_community.vectorstores.neo4j_vector.Neo4jVector

    try:
        logging.debug(f"Attempting to retrieve existing vector index: {index_name}...")
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
        logging.debug(f"Using existing index: {index_name}")
    except:
        logging.debug(
            f"No existing index found. Attempting to create a new vector index named {index_name} (this could take a while)..."
        )
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
            logging.debug(f"Created new index: {index_name}")
        except Exception as e:
            logging.error(
                f"Failed to retrieve existing or to create a Neo4jVector: {e}"
            )

    if vector_store is None:
        logging.error(f"Failed to retrieve or create a Neo4jVector. Exiting.")
        exit()

    vector_retriever = vector_store.as_retriever()

    vector_chain = RetrievalQAWithSourcesChain.from_chain_type(
        LLM,
        chain_type="stuff",
        retriever=vector_retriever,
        reduce_k_below_max_tokens=True,
        max_tokens_limit=2000,
    )
    return vector_chain