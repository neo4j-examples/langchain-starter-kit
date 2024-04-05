from langchain.chains import LLMChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import Runnable
from app.llms import LLM


def simple_agent_chain() -> Runnable:

    MEMORY = ConversationBufferMemory(memory_key="chat_history", input_key='question', output_key='text', return_messages=True)

    final_prompt = """You are a helpful question-answering agent. Your task is to analyze 
    and synthesize information from two sources: the top result from a similarity search 
    (unstructured information) and relevant data from a graph database (structured information). 
    Given the user's query: {question}, provide a meaningful and efficient answer based 
    on the insights derived from the following data:

    Unstructured information: {vector_result}. 
    Structured information: {graph_result}.
    """

    prompt = PromptTemplate.from_template(final_prompt)

    simple_agent_chain = LLMChain(
        prompt=prompt, 
        llm=LLM,
        memory = MEMORY)
    
    return simple_agent_chain

# def get_results(question: str) -> str:
#     """Generate response by analyzing and synthesizing information from vector and graph chains.
    
#     Args:
#         question (str): User query

#     Returns:
#         str: Final answer
#     """

#     graph_result = get_graph_results(question)

#     vector_result = get_vector_results(question)

#     final_prompt = """You are a helpful question-answering agent. Your task is to analyze 
#     and synthesize information from two sources: the top result from a similarity search 
#     (unstructured information) and relevant data from a graph database (structured information). 
#     Given the user's query: {question}, provide a meaningful and efficient answer based 
#     on the insights derived from the following data:

#     Unstructured information: {vector_result}. 
#     Structured information: {graph_result}.
#     """

#     if isinstance(graph_result, dict):
#         print("hello")

#     print(f'Final prompt: {final_prompt}')

#     prompt = PromptTemplate.from_template(final_prompt)

#     llm_chain = LLMChain(
#         prompt=prompt, 
#         llm=LLM,
#         memory = MEMORY)

#     result = llm_chain.invoke({"question":question, 
#                              "vector_result": vector_result, 
#                              "graph_result": graph_result})
    
#     return result["text"]
