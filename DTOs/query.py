
from pydantic import BaseModel
from DTOs.message import Message

class QueryRequest(BaseModel):
    messages: list[Message]