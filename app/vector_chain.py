from langchain.prompts.prompt import PromptTemplate
from langchain.vectorstores.neo4j_vector import Neo4jVector
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.schema.runnable import Runnable
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import logging
import os

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
    input_variables=["input","context"], template=VECTOR_PROMPT_TEMPLATE
)

def vector_chain() -> Runnable:

    NEO4J_URI = os.getenv("NEO4J_URI")
    NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")
    NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    LLM = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
    EMBEDDINGS = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    index_name = "vector"
    node_property_name = "embeddings"

    vector_store = None

    # Neo4jVector API: https://api.python.langchain.com/en/latest/vectorstores/langchain_community.vectorstores.neo4j_vector.Neo4jVector.html#langchain_community.vectorstores.neo4j_vector.Neo4jVector

    try:
        logging.debug(f'Attempting to retrieve existing vector index: {index_name}...')
        vector_store = Neo4jVector.from_existing_index(
            embedding=EMBEDDINGS,
            url=NEO4J_URI,
            username=NEO4J_USERNAME,
            password=NEO4J_PASSWORD,
            database=NEO4J_DATABASE,
            index_name=index_name,
            embedding_node_property=node_property_name,
        )
        logging.debug(f'Using existing index: {index_name}')
    except:
        logging.debug(f'No existing index found. Attempting to create a new vector index named {index_name}...')
        try:
            vector_store = Neo4jVector.from_existing_graph(
                embedding=EMBEDDINGS,
                url=NEO4J_URI,
                username=NEO4J_USERNAME,
                password=NEO4J_PASSWORD,
                database=NEO4J_DATABASE,
                index_name=index_name,
                node_label="Chunk",
                text_node_properties=["text"],
                embedding_node_property=node_property_name,
            )
            logging.debug(f'Created new index: {index_name}')
        except Exception as e:
            logging.error(f'Failed to retrieve existing or to create a Neo4jVector: {e}')

    if vector_store is None:
        logging.error(f'Failed to retrieve or create a Neo4jVector. Exiting.')
        exit()

    vector_retriever = vector_store.as_retriever()

    vector_chain = RetrievalQAWithSourcesChain.from_chain_type(
        LLM,
        chain_type="stuff", 
        retriever=vector_retriever,
        reduce_k_below_max_tokens = True,
        max_tokens_limit=2000
    )
    return vector_chain