from langchain.agents import load_tools, AgentExecutor, create_react_agent
from langchain import hub # requires langchainhub package
from .graph_tool import graph_tool
from .llm_manager import LLM
from .vector_tool import vector_tool
from retry import retry
import logging

# Setup tools the agent will use
tools = load_tools([], llm=LLM)
tools = tools + [graph_tool, vector_tool]


# REACT AGENT EXECUTOR
prompt = hub.pull("hwchase17/react")

# More on agent types: https://python.langchain.com/docs/modules/agents/agent_types/
agent = create_react_agent(LLM, tools, prompt)

# NOTE: early_stopping_method generate option ONLY available for multi-action agents
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
    # return_intermediate_steps = True,
    # max_iterations=1,
    # early_stopping_method = "generate"
)

@retry(tries=2, delay=20)
def get_results(question) -> dict:
    """Starts a LangChain agent to generate an answer using one of several Neo4j RAG tools.

    Args:
        question (str): User query
        callbacks (list): List of optional LangChain callback handlers

    Returns:
        dict: Final answer as a dict with the keys: input, output, intermediate_steps
    """

    response = agent_executor.invoke({"input": question})

    if isinstance(response, dict) is False:
        logging.warning(f'Agent response was not the expected dict type. Found: {response}')

    return response['output']