from fastapi import FastAPI
from api import search, assistant
import uvicorn

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, Developers! Welcome to DocsNexus: The easiest way to recall Pandas Reference API."}

app.include_router(search.router, prefix="/search", tags=["search"])
app.include_router(assistant.router, prefix="/assistant", tags=["assistant"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3001, reload=False)
