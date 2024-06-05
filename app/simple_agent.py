from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import Runnable
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain_core.prompts import PromptTemplate
import os


def simple_agent_chain() -> Runnable:

    final_prompt = """You are a helpful question-answering agent. Your task is to analyze 
    and synthesize information from two sources: the top result from a similarity search 
    (unstructured information) and relevant data from a graph database (structured information). 
    Given the user's query: {question}, provide a meaningful and efficient answer based 
    on the insights derived from the following data:

    Unstructured information: {vector_result}. 
    Structured information: {graph_result}.
    """

    prompt = PromptTemplate(
        input_variables=["question", "vector_result", "graph_result"],
        template=final_prompt,
    )

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    LLM = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
    output_parser = StrOutputParser()

    simple_agent_chain = prompt | LLM | output_parser

    return simple_agent_chain
