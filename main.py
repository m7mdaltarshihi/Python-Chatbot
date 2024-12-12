import sys
import os
import uvicorn
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DTOs.message import Message
from DTOs.query import QueryRequest
from services.llama3 import LLAMA38b
from services.vectorized_documents import vectordb
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llama = LLAMA38b()


@app.post("/api/query")
async def query_documents(chat_history: QueryRequest):
    try:
        query = chat_history.messages[-1].content
        results = vectordb.similarity_search(query, k=3)
        document = ""
        src = ""
        
        for result in results:
            document += result.page_content + " "
            src += result.metadata['source'] + " "

        llm_completion = llama.llama_model(chat_history.messages, document)
        assistant_message = Message(role="assistant", content=llm_completion, source=src)
        
        return assistant_message
    except Exception as e:
        return {"error": f"Internal Server Error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app)