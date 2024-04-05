from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from app.graph_chain import graph_chain
from app.vector_chain import vector_chain
from app.simple_agent import simple_agent_chain

app = FastAPI()

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

add_routes(app, vector_chain(), path="/vector")
add_routes(app, graph_chain(), path="/graph")
add_routes(app, simple_agent_chain(), path="/simple_agent")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)