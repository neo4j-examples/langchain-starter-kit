# Neo4j LangChain Starter Kit

## Usage
```
poetry install

NEO4J_URI=<uri> \
NEO4J_DATABASE=<database_name> \
NEO4J_USERNAME=<username> \
NEO4J_PASSWORD=<password> \
OPENAI_API_KEY=<open_ai_key> \
poetry run uvicorn langchain_starter_kit.main:app --reload

```

Default local address will be: http://127.0.0.1:8000

To change port, append above with `--port=<port>`

## Docs
FastAPI will automatically generate a swagger doc interface at a `/docs#` path from above