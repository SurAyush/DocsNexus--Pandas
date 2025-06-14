from fastapi import FastAPI
from api import search, assistant
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get("/")
async def read_root():
    return {"message": "Hello, Developers! Welcome to DocsNexus: The easiest way to recall Pandas Reference API."}

app.include_router(search.router, prefix="/search", tags=["search"])
app.include_router(assistant.router, prefix="/assistant", tags=["assistant"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3001, reload=False)
