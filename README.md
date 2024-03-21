# Neo4j LangChain Starter Kit
This kit provides a simple [FastAPI](https://fastapi.tiangolo.com/) backend service connected to [OpenAI](https://platform.openai.com/docs/overview) and [Neo4j](https://neo4j.com/developer/) for powering GenAI projects. The Neo4j interface leverages both [Vector Indexes](https://python.langchain.com/docs/integrations/vectorstores/neo4jvector) and [Text2Cypher](https://python.langchain.com/docs/use_cases/graph/integrations/graph_cypher_qa) chains to provide more accurate results. 

![alt text](https://res.cloudinary.com/dk0tizgdn/image/upload/v1711042573/langchain_starter_kit_sample_jgvnfb.gif "Testing Neo4j LangChain Starter Kit")


## Requirements
- [Pipenv](https://pypi.org/project/pipenv/) for dependency and virtual enviroment management
- [LangChain](https://python.langchain.com/docs/get_started/introduction)
- An [OpenAI API Key](https://openai.com/blog/openai-api)
- A running [local](https://neo4j.com/download/) or [cloud](https://neo4j.com/cloud/platform/aura-graph-database/) Neo4j database


## Configure
1. Copy the `env.sample` file as `.env` 
2. Update the new `.env` file with your Neo4j and OpenAI credentials

The `env.sample` file contains read-only access credentials to a publicly hosted Neo4j instance with public EDGAR SEC data. 

If you would like to load your own instance with a subset of this information. Copy, paste, and run the [edgar_import.cypher](edgar_import.cypher) in a [Neo4j browser](https://neo4j.com/docs/browser-manual/current/) connected to your instance.

## Usage
```
pipenv shell
pipenv install
pipenv run uvicorn langchain_starter_kit.main:app --reload
```

A FastAPI server should now be running on your local port 8000/api/chat.

## Docs
FastAPI will make endpoint information and the ability to test from a browser at http://localhost:8000/docs

## Testing
Alternatively, after the server is running, a curl command can be triggered to test the endpoint:
```
curl --location 'http://127.0.0.1:8000/api/chat' \
--header 'Content-Type: application/json' \
--data '{
    "message":"How many forms are there?"}'
```


## Learn More
If you'd like to learn more about using Neo4j with LLMs, we recommend checking out our [GraphAcademy Courses](https://graphacademy.neo4j.com).
