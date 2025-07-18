"""Module for creating a simple agent chain that combines vector and graph search results."""
import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from app.config import (
    LLM
)


def simple_agent_chain(
    model_name: str = None,
    temperature: float = None,
) -> Runnable:
    """Create a simple agent chain that combines vector and graph search results.
    
    This chain takes a question and two sources of information (vector search results
    and graph database results) and synthesizes them into a coherent response.
    
    Args:
        model_name (deprecated): Name of the OpenAI model to use (e.g., 'gpt-4', 'gpt-3.5-turbo'). Configure via env variable now
        temperature (deprecated): Controls randomness in the model's output (0.0 = deterministic). Configure via env variable now
        
    Returns:
        A Runnable chain that takes a dictionary with 'question', 'vector_result', and 
        'graph_result' keys and returns a string response.
        
    Example:
        chain = simple_agent_chain()
        response = chain.invoke({
            "question": "What is the capital of France?",
            "vector_result": "Paris is the capital of France.",
            "graph_result": "France is a country in Europe with Paris as its capital."
        })
    """
    # Define the system and human messages
    system_message = """You are a helpful question-answering agent. Your task is to analyze 
    and synthesize information from two sources: the top result from a similarity search 
    (unstructured information) and relevant data from a graph database (structured information)."""
    
    human_message = """Given the user's query: {question}, provide a meaningful and efficient answer based 
    on the insights derived from the following data:

    Unstructured information: {vector_result} 
    Structured information: {graph_result}
    
    Your response should be clear, concise, and directly address the user's question.
    If the information from both sources conflicts, note the discrepancy.
    """

    # Create the prompt template
    prompt = PromptTemplate(
        template=(
            "System: {system_message}\n\n"
            "Human: {human_message}"
        ),
        input_variables=["system_message", "human_message"],
    )
    
    # Get the OpenAI API key from environment variables
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable is not set. "
            "Please set it with your OpenAI API key."
        )

    # Initialize the LLM with the provided parameters
    # llm = ChatOpenAI(
    #     model=model_name,
    #     temperature=temperature,
    #     openai_api_key=openai_api_key,
    # )
    
    # Create the output parser
    output_parser = StrOutputParser()
    
    # Create the chain using LCEL (LangChain Expression Language)
    chain = {
        "system_message": lambda x: system_message,
        "human_message": lambda x: human_message.format(
            question=x["question"],
            vector_result=x["vector_result"],
            graph_result=x["graph_result"]
        )
    } | prompt | LLM | output_parser
    
    return chain
