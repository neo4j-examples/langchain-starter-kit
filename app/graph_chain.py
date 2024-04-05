from langchain.chains import GraphCypherQAChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain_community.graphs import Neo4jGraph
from langchain.prompts.prompt import PromptTemplate
from langchain.schema.runnable import Runnable
from langchain_openai import ChatOpenAI
# from app.llms import LLM
# import logging
import os

def graph_chain() -> Runnable:

    NEO4J_URI = os.getenv("NEO4J_URI")
    NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")
    NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    LLM = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)

    CYPHER_GENERATION_TEMPLATE = """Task:Generate Cypher statement to query a graph database.
    Instructions:
    Use only the provided relationship types and properties in the schema.
    Do not use any other relationship types or properties that are not provided.
    Schema:
    {schema}
    Note: Do not include any explanations or apologies in your responses.
    Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
    Do not include any text except the generated Cypher statement.
    Examples: Here are a few examples of generated Cypher statements for particular questions:

    # How many Managers own Companies?
    MATCH (m:Manager)-[:OWNS_STOCK_IN]->(c:Company)
    RETURN count(DISTINCT m)

    # How many companies in the filings?
    MATCH (c:Company) 
    RETURN count(DISTINCT c)

    # Which companies are vulnerable to lithium shortage?
    MATCH (co:Company)-[fi]-(f:Form)-[po]-(c:Chunk)
    WHERE toLower(c.text) CONTAINS "lithium"
    RETURN DISTINCT count(c) as chunks, co.name ORDER BY chunks desc

    # Which companies are in the poultry business?
    MATCH (co:Company)-[fi]-(f:Form)-[po]-(c:Chunk)
    WHERE toLower(c.text) CONTAINS "chicken"
    RETURN DISTINCT count(c) as chunks, co.name ORDER BY chunks desc

    The question is:
    {question}"""

    CYPHER_GENERATION_PROMPT = PromptTemplate(
        input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
    )

    MEMORY = ConversationBufferMemory(
        memory_key="chat_history", 
        input_key='question', 
        output_key='answer', 
        return_messages=True)

    graph = Neo4jGraph(
        url=NEO4J_URI,
        username=NEO4J_USERNAME,
        password=NEO4J_PASSWORD,
        database=NEO4J_DATABASE,
        sanitize = True
    )

    graph.refresh_schema()

    # Official API doc for GraphCypherQAChain at: https://api.python.langchain.com/en/latest/chains/langchain.chains.graph_qa.base.GraphQAChain.html#
    graph_chain = GraphCypherQAChain.from_llm(
        cypher_llm = LLM,
        qa_llm = LLM,
        validate_cypher= True,
        graph=graph,
        verbose=True, 
        return_intermediate_steps = True,
        return_direct = True,
        memory = MEMORY
    )

    return graph_chain

# NEO4J_URI = os.getenv("NEO4J_URI")
# NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")
# NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
# NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# CYPHER_GENERATION_TEMPLATE = """Task:Generate Cypher statement to query a graph database.
# Instructions:
# Use only the provided relationship types and properties in the schema.
# Do not use any other relationship types or properties that are not provided.
# Schema:
# {schema}
# Note: Do not include any explanations or apologies in your responses.
# Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
# Do not include any text except the generated Cypher statement.
# Examples: Here are a few examples of generated Cypher statements for particular questions:

# # How many Managers own Companies?
# MATCH (m:Manager)-[:OWNS_STOCK_IN]->(c:Company)
# RETURN count(DISTINCT m)

# # How many companies in the filings?
# MATCH (c:Company) 
# RETURN count(DISTINCT c)

# # Which companies are vulnerable to lithium shortage?
# MATCH (co:Company)-[fi]-(f:Form)-[po]-(c:Chunk)
# WHERE toLower(c.text) CONTAINS "lithium"
# RETURN DISTINCT count(c) as chunks, co.name ORDER BY chunks desc

# # Which companies are in the poultry business?
# MATCH (co:Company)-[fi]-(f:Form)-[po]-(c:Chunk)
# WHERE toLower(c.text) CONTAINS "chicken"
# RETURN DISTINCT count(c) as chunks, co.name ORDER BY chunks desc

# The question is:
# {question}"""

# CYPHER_GENERATION_PROMPT = PromptTemplate(
#     input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
# )

# MEMORY = ConversationBufferMemory(
#     memory_key="chat_history", 
#     input_key='question', 
#     output_key='answer', 
#     return_messages=True)

# graph = Neo4jGraph(
#     url=NEO4J_URI,
#     username=NEO4J_USERNAME,
#     password=NEO4J_PASSWORD,
#     database=NEO4J_DATABASE,
#     sanitize = True
# )

# # Official API doc for GraphCypherQAChain at: https://api.python.langchain.com/en/latest/chains/langchain.chains.graph_qa.base.GraphQAChain.html#
# graph_chain = GraphCypherQAChain.from_llm(
#     cypher_llm = LLM,
#     qa_llm = LLM,
#     validate_cypher= True,
#     graph=graph,
#     verbose=True, 
#     return_intermediate_steps = True,
#     return_direct = True,
#     memory = MEMORY
# )

# def get_results(question) -> str:
#     """Generate a response from a GraphCypherQAChain targeted at generating answered related to relationships. 

#     Args:
#         question (str): User query

#     Returns:
#         str: Answer from chain
#     """

#     logging.info(f'Using Neo4j database at url: {NEO4J_URI}')

#     graph.refresh_schema()

#     chain_result = None

#     try:
#         chain_result = graph_chain.invoke({
#             "query": question},
#             prompt=CYPHER_GENERATION_PROMPT,
#             # return_only_outputs = True,
#         )
#     except Exception as e:
#         # Occurs when the chain can not generate a cypher statement
#         # for the question with the given database schema
#         logging.warning(f'Handled exception running graphCypher chain: {e}')

#     logging.debug(f'chain_result: {chain_result}')

#     if chain_result is None:
#         return "Sorry, I couldn't find an answer to your question"
    
#     result = chain_result.get("result", None)

#     return result