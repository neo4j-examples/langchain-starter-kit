# Neo4j LangChain Starter Kit


## Requirements
- [Poetry]() for running locally

## Usage
```
poetry install

NEO4J_URI=<database_uri> \
NEO4J_DATABASE=<database_name> \
NEO4J_USERNAME=<username> \
NEO4J_PASSWORD=<password> \
OPENAI_API_KEY=<api_key> \
poetry run uvicorn langchain_starter_kit.main:app --reload --port=8003 --log-config=log_conf.yaml
```