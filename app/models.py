from pydantic import BaseModel

class MessageRequest(BaseModel):
    session_id: str
    message: str

class EndSessionRequest(BaseModel):
    session_id: str